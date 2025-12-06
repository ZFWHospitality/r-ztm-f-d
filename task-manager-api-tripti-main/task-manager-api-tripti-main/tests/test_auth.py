def test_register_and_login(client):
    r = client.post('/auth/register', json={'username':'alice','password':'pass123'})
    assert r.status_code == 201

    r = client.post('/auth/login', json={'username':'alice','password':'pass123'})
    assert r.status_code == 200
    data = r.get_json()
    assert 'access_token' in data

    r = client.post('/auth/login', json={'username':'alice','password':'wrong'})
    assert r.status_code == 401
