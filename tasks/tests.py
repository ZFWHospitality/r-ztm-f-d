# tasks/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework import status
from .models import Task

class JWTTestMixin:
    """
    Helpers to obtain JWT tokens and authenticated APIClient.
    Expects you have a named URL 'token_obtain_pair' for SimpleJWT.
    """
    def _get_tokens(self, username, password):
        url = reverse('token_obtain_pair')
        c = APIClient()
        resp = c.post(url, {'username': username, 'password': password}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK, msg=f"Token obtain failed: {resp.status_code} {resp.data}")
        return resp.data

    def auth_client(self, username, password):
        tokens = self._get_tokens(username, password)
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        return c

class TaskAPITestCase(APITestCase, JWTTestMixin):
    def setUp(self):

        self.user = User.objects.create_user(username='alice', password='alicepass')
        self.other = User.objects.create_user(username='bob', password='bobpass')
        self.staff = User.objects.create_user(username='admin', password='adminpass', is_staff=True)


        self.client_alice = self.auth_client('alice', 'alicepass')
        self.client_bob = self.auth_client('bob', 'bobpass')
        self.client_admin = self.auth_client('admin', 'adminpass')


        self.anon = APIClient()

    def create_task_api(self, client, title="T1", description="d", completed=False):
        url = reverse('task-list')
        payload = {'title': title, 'description': description, 'completed': completed}
        return client.post(url, payload, format='json')


    def test_token_endpoint(self):
        tokens = self._get_tokens('alice', 'alicepass')
        self.assertIn('access', tokens)
        self.assertIn('refresh', tokens)


    def test_create_task_authenticated(self):
        resp = self.create_task_api(self.client_alice, title="Alice Task")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.json()
        self.assertEqual(data['title'], "Alice Task")
        self.assertEqual(data['owner'], self.user.username)
        self.assertEqual(Task.objects.filter(owner=self.user).count(), 1)

    def test_create_task_unauth_fails(self):
        resp = self.create_task_api(self.anon, title="Anon Task")

        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))


    def test_list_returns_only_owner(self):
        Task.objects.create(owner=self.user, title="A1")
        Task.objects.create(owner=self.other, title="B1")
        resp = self.client_alice.get(reverse('task-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        results = data.get('results', data)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'A1')

    def test_filter_completed(self):
        Task.objects.create(owner=self.user, title="Done", completed=True)
        Task.objects.create(owner=self.user, title="NotDone", completed=False)
        resp = self.client_alice.get(reverse('task-list') + '?completed=True')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        results = data.get('results', data)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0]['completed'])


    def test_retrieve_own_task(self):
        t = Task.objects.create(owner=self.user, title="Detail")
        url = reverse('task-detail', kwargs={'pk': t.pk})
        resp = self.client_alice.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['title'], 'Detail')

    def test_retrieve_other_task_forbidden_or_404(self):
        t = Task.objects.create(owner=self.other, title="OtherDetail")
        url = reverse('task-detail', kwargs={'pk': t.pk})
        resp = self.client_alice.get(url)
        self.assertIn(resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND))

    def test_put_update_by_owner(self):
        t = Task.objects.create(owner=self.user, title="Before", description="old", completed=False)
        url = reverse('task-detail', kwargs={'pk': t.pk})
        payload = {'title': 'After', 'description': 'new', 'completed': True}
        resp = self.client_alice.put(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        j = resp.json()
        self.assertIn('message', j)
        self.assertIn('task', j)
        self.assertEqual(j['task']['title'], 'After')
        t.refresh_from_db()
        self.assertTrue(t.completed)

    def test_patch_partial_update_by_owner(self):
        t = Task.objects.create(owner=self.user, title="PatchMe", completed=False)
        url = reverse('task-detail', kwargs={'pk': t.pk})
        resp = self.client_alice.patch(url, {'completed': True}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        j = resp.json()
        self.assertEqual(j['message'], 'Task updated successfully!')
        t.refresh_from_db()
        self.assertTrue(t.completed)

    def test_update_by_non_owner_forbidden_or_404(self):
        t = Task.objects.create(owner=self.user, title="OwnerOnly")
        url = reverse('task-detail', kwargs={'pk': t.pk})
        resp = self.client_bob.put(url, {'title': 'Hack', 'description': '', 'completed': False}, format='json')
        self.assertIn(resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND))
        t.refresh_from_db()
        self.assertEqual(t.title, 'OwnerOnly')

    def test_delete_by_owner(self):
        t = Task.objects.create(owner=self.user, title="ToDelete")
        url = reverse('task-detail', kwargs={'pk': t.pk})
        resp = self.client_alice.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        j = resp.json()
        self.assertIn("has been deleted successfully", j.get('message', ''))
        self.assertFalse(Task.objects.filter(pk=t.pk).exists())

    def test_delete_by_non_owner_forbidden_or_404(self):
        t = Task.objects.create(owner=self.user, title="NotYourTask")
        url = reverse('task-detail', kwargs={'pk': t.pk})
        resp = self.client_bob.delete(url)
        self.assertIn(resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND))
        self.assertTrue(Task.objects.filter(pk=t.pk).exists())

    def test_admin_sees_all_tasks_and_can_delete(self):
        Task.objects.create(owner=self.user, title="U1")
        Task.objects.create(owner=self.other, title="O1")
        resp = self.client_admin.get(reverse('task-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        results = data.get('results', data)
        self.assertGreaterEqual(len(results), 2)

        t = Task.objects.create(owner=self.other, title="DeleteByAdmin")
        url = reverse('task-detail', kwargs={'pk': t.pk})
        resp2 = self.client_admin.delete(url)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.assertFalse(Task.objects.filter(pk=t.pk).exists())

    def test_pagination_exists(self):
        Task.objects.create(owner=self.user, title="P1")
        Task.objects.create(owner=self.user, title="P2")
        Task.objects.create(owner=self.user, title="P3")
        resp = self.client_alice.get(reverse('task-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertTrue(('results' in data) or isinstance(data, list))
