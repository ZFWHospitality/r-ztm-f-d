from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Task

# Create your tests here.

class TaskAPITests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.task1 = Task.objects.create(title='Test_task', owner=self.user1)

    def test_authenticated_user_can_create_task(self):
        self.client.force_authenticate(user=self.user1)
        data = {'title': 'New Task', 'owner': self.user1.id}
        response = self.client.post('/api/tasks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_unauthenticated_user_cannot_create_task(self):
        data = {'title': 'New Task', 'owner': self.user1.id}
        response = self.client.post('/api/tasks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_owner_can_update_task(self):
        self.client.force_authenticate(user=self.user1)
        data = {'title': 'Updated Task 1', 'completed': True}
        response = self.client.patch(f'/api/tasks/{self.task1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task 1')

    def test_non_owner_cannot_update_task(self):
        self.client.force_authenticate(user=self.user2)
        data = {'title': 'Illegal Update'}
        response = self.client.patch(f'/api/tasks/{self.task1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_owner_can_delete_task(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)