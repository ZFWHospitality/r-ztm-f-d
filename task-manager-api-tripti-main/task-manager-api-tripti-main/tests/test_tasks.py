def get_token(client, username='bob'):
    client.post('/auth/register', json={'username': username, 'password': 'p'})
    r = client.post('/auth/login', json={'username': username, 'password': 'p'})
    return r.get_json()['access_token']

def test_crud_tasks(client):
    token = get_token(client)
    headers = {'Authorization': f'Bearer {token}'}

    r = client.post('/tasks', json={'title':'t1'}, headers=headers)
    assert r.status_code == 201
    t = r.get_json()
    assert t['title'] == 't1'

    task_id = t['id']

    r = client.get(f'/tasks/{task_id}')
    assert r.status_code == 200

    r = client.put(f'/tasks/{task_id}', json={'completed': True}, headers=headers)
    assert r.status_code == 200
    assert r.get_json()['completed'] is True

    r = client.delete(f'/tasks/{task_id}', headers=headers)
    assert r.status_code == 200

    r = client.get(f'/tasks/{task_id}')
    assert r.status_code == 404

def test_pagination_and_filter(client):
    token = get_token(client, username='puser')
    headers = {'Authorization': f'Bearer {token}'}

    for i in range(15):
        client.post('/tasks', json={'title': f't{i}', 'completed': i % 2 == 0}, headers=headers)

    r = client.get('/tasks?page=1&per_page=5')
    assert r.status_code == 200
    data = r.get_json()
    assert data['per_page'] == 5
    assert data['total'] == 15

    r = client.get('/tasks?completed=true')
    assert r.status_code == 200
    data = r.get_json()
    assert all(t['completed'] for t in data['tasks'])
