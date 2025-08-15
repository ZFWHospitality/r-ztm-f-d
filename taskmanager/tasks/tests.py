from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Task

class TaskAPITests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="secret123")
        self.bob = User.objects.create_user(username="bob", password="secret123")
        self.admin = User.objects.create_user(username="admin", password="secret123", is_staff=True)

        self.client = APIClient()

        # Alice login
        res = self.client.post(reverse("token_obtain_pair"), {"username":"alice","password":"secret123"}, format="json")
        self.alice_access = res.data["access"]

        # Bob login
        res_bob = self.client.post(reverse("token_obtain_pair"), {"username":"bob","password":"secret123"}, format="json")
        self.bob_access = res_bob.data["access"]

        # Alice task
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.alice_access}")
        r = self.client.post("/api/tasks/", {"title":"Alice Task","description":"desc"}, format="json")
        self.alice_task_id = r.data["id"]

    def test_list_only_own_tasks(self):
        # Alice sees her task
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.alice_access}")
        r = self.client.get("/api/tasks/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data["results"]), 1)
        self.assertEqual(r.data["results"][0]["title"], "Alice Task")

        # Bob sees none
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.bob_access}")
        r = self.client.get("/api/tasks/")
        self.assertEqual(len(r.data["results"]), 0)

    def test_owner_can_update(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.alice_access}")
        r = self.client.put(f"/api/tasks/{self.alice_task_id}/",
                            {"title":"Updated","description":"d","completed":True}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertTrue(r.data["completed"])

    def test_admin_can_modify_any(self):
        res = self.client.post(reverse("token_obtain_pair"), {"username":"admin","password":"secret123"}, format="json")
        admin_access = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_access}")
        r = self.client.patch(f"/api/tasks/{self.alice_task_id}/", {"completed": True}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertTrue(r.data["completed"])

    def test_filter_completed(self):
        Task.objects.filter(id=self.alice_task_id).update(completed=True)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.alice_access}")
        r = self.client.get("/api/tasks/?completed=true")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data["results"]), 1)

