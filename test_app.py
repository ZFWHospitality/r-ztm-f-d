import pytest
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from db_config import db
from models import User, Task
from jwt_utils import generate_jwt, decode_jwt


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'test_secret_key_for_testing_only'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


@pytest.fixture
def auth_token(client):
    # Create test user
    username = "testuser"
    password = "testpass123"
    
    response = client.post('/signup', json={
        'username': username,
        'password': password
    })
    
    # Login to get token
    response = client.post('/login', json={
        'username': username,
        'password': password
    })
    
    data = response.get_json()
    return data['token']


class TestUserAuthentication:
    
    def test_signup_success(self, client):
        """Test successful user registration."""
        response = client.post('/signup', json={
            'username': 'newuser',
            'password': 'password123'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'User registered successfully'
    
    def test_signup_duplicate_username(self, client):
        # First registration
        client.post('/signup', json={
            'username': 'duplicate',
            'password': 'password123'
        })
        
        # Try to register again with same username
        response = client.post('/signup', json={
            'username': 'duplicate',
            'password': 'password123'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'already exists' in data['error'].lower()
    
    def test_signup_missing_credentials(self, client):
        # Missing username
        response = client.post('/signup', json={
            'password': 'password123'
        })
        assert response.status_code == 400
        
        # Missing password
        response = client.post('/signup', json={
            'username': 'testuser'
        })
        assert response.status_code == 400
    
    def test_login_success(self, client):
        # First register
        client.post('/signup', json={
            'username': 'loginuser',
            'password': 'password123'
        })
        
        # Then login
        response = client.post('/login', json={
            'username': 'loginuser',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'token' in data
        assert data['message'] == 'Login successful'
    
    def test_login_invalid_credentials(self, client):
        # Register a user
        client.post('/signup', json={
            'username': 'validuser',
            'password': 'correctpass'
        })
        
        # Try to login with wrong password
        response = client.post('/login', json={
            'username': 'validuser',
            'password': 'wrongpass'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
    
    def test_login_nonexistent_user(self, client):
        response = client.post('/login', json={
            'username': 'nonexistent',
            'password': 'password123'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
    
    def test_profile_success(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post('/profile', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'user' in data
        assert data['user']['username'] == 'testuser'
        assert 'id' in data['user']
        assert 'created_at' in data['user']
    
    def test_profile_invalid_token(self, client):
        headers = {'Authorization': 'Bearer invalid_token'}
        response = client.post('/profile', headers=headers)
        
        assert response.status_code == 401
    
    def test_profile_missing_token(self, client):
        response = client.post('/profile')
        
        assert response.status_code == 401


class TestTaskCRUD:
    
    def test_create_task_success(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post('/tasks/create', json={
            'title': 'Test Task',
            'description': 'This is a test task'
        }, headers=headers)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'Test Task'
        assert data['description'] == 'This is a test task'
        assert data['completed'] == False
        assert 'id' in data
        assert 'created_at' in data
    
    def test_create_task_missing_fields(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Missing title
        response = client.post('/tasks/create', json={
            'description': 'Description only'
        }, headers=headers)
        assert response.status_code == 400
        
        # Missing description
        response = client.post('/tasks/create', json={
            'title': 'Title only'
        }, headers=headers)
        assert response.status_code == 400
    
    def test_create_task_unauthorized(self, client):
        response = client.post('/tasks/create', json={
            'title': 'Test Task',
            'description': 'This is a test task'
        })
        
        assert response.status_code == 401
    
    def test_get_all_tasks_success(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Create some tasks first
        for i in range(3):
            client.post('/tasks/create', json={
                'title': f'Task {i}',
                'description': f'Description {i}'
            }, headers=headers)
        
        # Get all tasks
        response = client.post('/tasks', json={'page': 1}, headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'tasks' in data
        assert 'page' in data
        assert 'total_tasks' in data
        assert 'total_pages' in data
        assert len(data['tasks']) == 3
    
    def test_get_all_tasks_pagination(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Create 7 tasks (more than per_page limit of 5)
        for i in range(7):
            client.post('/tasks/create', json={
                'title': f'Task {i}',
                'description': f'Description {i}'
            }, headers=headers)
        
        # Get first page
        response = client.post('/tasks', json={'page': 1}, headers=headers)
        data = response.get_json()
        assert len(data['tasks']) == 5  
        assert data['has_next'] == True
        assert data['has_prev'] == False
        
        # Get second page
        response = client.post('/tasks', json={'page': 2}, headers=headers)
        data = response.get_json()
        assert len(data['tasks']) == 2  
        assert data['has_next'] == False
        assert data['has_prev'] == True
    
    def test_get_single_task_success(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Create a task
        create_response = client.post('/tasks/create', json={
            'title': 'Single Task',
            'description': 'Single task description'
        }, headers=headers)
        task_id = create_response.get_json()['id']
        
        # Get the task
        response = client.post(f'/tasks/{task_id}', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Single Task'
        assert data['description'] == 'Single task description'
    
    def test_get_single_task_not_found(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post('/tasks/99999', headers=headers)
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
    
    def test_update_task_success(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Create a task
        create_response = client.post('/tasks/create', json={
            'title': 'Original Title',
            'description': 'Original description'
        }, headers=headers)
        task_id = create_response.get_json()['id']
        
        # Update the task
        response = client.post(f'/tasks/update/{task_id}', json={
            'title': 'Updated Title',
            'description': 'Updated description',
            'completed': True
        }, headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Updated Title'
        assert data['description'] == 'Updated description'
        assert data['completed'] == True
    
    def test_update_task_partial(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Create a task
        create_response = client.post('/tasks/create', json={
            'title': 'Original Title',
            'description': 'Original description'
        }, headers=headers)
        task_id = create_response.get_json()['id']
        
        # Update only title
        response = client.post(f'/tasks/update/{task_id}', json={
            'title': 'Only Title Updated'
        }, headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'Only Title Updated'
    
    def test_update_task_not_found(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post('/tasks/update/99999', json={
            'title': 'Updated Title'
        }, headers=headers)
        
        assert response.status_code == 404
    
    def test_update_task_no_data(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Create a task
        create_response = client.post('/tasks/create', json={
            'title': 'Original Title',
            'description': 'Original description'
        }, headers=headers)
        task_id = create_response.get_json()['id']
        
        # Try to update with empty data
        response = client.post(f'/tasks/update/{task_id}', json={}, headers=headers)
        
        assert response.status_code == 400
    
    def test_delete_task_success(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Create a task
        create_response = client.post('/tasks/create', json={
            'title': 'Task to Delete',
            'description': 'Will be deleted'
        }, headers=headers)
        task_id = create_response.get_json()['id']
        
        # Delete the task
        response = client.post(f'/tasks/delete/{task_id}', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Task deleted successfully'
        
        # Verify task is deleted (should not be retrievable)
        response = client.post(f'/tasks/{task_id}', headers=headers)
        assert response.status_code == 404
    
    def test_delete_task_not_found(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.post('/tasks/delete/99999', headers=headers)
        
        assert response.status_code == 404


class TestTaskFiltering:
    
    def test_filter_by_completed(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Create completed and incomplete tasks
        for i in range(3):
            create_response = client.post('/tasks/create', json={
                'title': f'Task {i}',
                'description': f'Task {i} description'
            }, headers=headers)
            task_id = create_response.get_json()['id']
            
            # Mark every other task as completed
            if i % 2 == 0:
                client.post(f'/tasks/update/{task_id}', json={
                    'completed': True
                }, headers=headers)
        
        # Filter by completed
        response = client.post('/tasks/filter', json={
            'completed': True
        }, headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2  # Should have 2 completed tasks
        assert all(task['completed'] == True for task in data)
    
    def test_filter_by_incomplete(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Create tasks
        for i in range(5):
            create_response = client.post('/tasks/create', json={
                'title': f'Task {i}',
                'description': f'Task {i} description'
            }, headers=headers)
            task_id = create_response.get_json()['id']
            
            # Mark some as completed
            if i < 2:
                client.post(f'/tasks/update/{task_id}', json={
                    'completed': True
                }, headers=headers)
        
        # Filter by incomplete
        response = client.post('/tasks/filter', json={
            'completed': False
        }, headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3  # Should have 3 incomplete tasks
        assert all(task['completed'] == False for task in data)
    
    def test_filter_by_date_range(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Create some tasks
        for i in range(3):
            client.post('/tasks/create', json={
                'title': f'Task {i}',
                'description': f'Task {i} description'
            }, headers=headers)
        
        # Filter by date
        response = client.post('/tasks/filter', json={
            'created_after': '2024-01-01',
            'created_before': '2024-12-31'
        }, headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 3
    
    def test_filter_invalid_date_format(self, client, auth_token):
        headers = {'Authorization': f'Bearer {auth_token}'}
        
        # Create a task
        client.post('/tasks/create', json={
            'title': 'Test Task',
            'description': 'Test description'
        }, headers=headers)
        
        # Filter with invalid date format
        response = client.post('/tasks/filter', json={
            'created_after': 'invalid-date'
        }, headers=headers)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data


class TestUserIsolation:
    
    def test_users_cannot_access_other_users_tasks(self, client):
        # Create first user
        client.post('/signup', json={
            'username': 'user1',
            'password': 'pass123'
        })
        
        login_response = client.post('/login', json={
            'username': 'user1',
            'password': 'pass123'
        })
        token1 = login_response.get_json()['token']
        
        headers1 = {'Authorization': f'Bearer {token1}'}
        
        # Create task for user1
        create_response = client.post('/tasks/create', json={
            'title': 'User1 Task',
            'description': 'User1 task description'
        }, headers=headers1)
        task_id = create_response.get_json()['id']
        
        # Create second user
        client.post('/signup', json={
            'username': 'user2',
            'password': 'pass456'
        })
        
        login_response = client.post('/login', json={
            'username': 'user2',
            'password': 'pass456'
        })
        token2 = login_response.get_json()['token']
        
        headers2 = {'Authorization': f'Bearer {token2}'}
        
        # User2 should not be able to access User1's task
        response = client.post(f'/tasks/{task_id}', headers=headers2)
        assert response.status_code == 404
        
        # User2 should not be able to update User1's task
        response = client.post(f'/tasks/update/{task_id}', json={
            'title': 'Hacked'
        }, headers=headers2)
        assert response.status_code == 404
        
        # User2 should not be able to delete User1's task
        response = client.post(f'/tasks/delete/{task_id}', headers=headers2)
        assert response.status_code == 404


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

