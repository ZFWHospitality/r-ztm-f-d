from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Task

class TaskAPITests(APITestCase):
    #basic setup for creating users and obtaining tokens
    def setUp(self):
        self.satyam = User.objects.create_user(username="satyam", password="Oct@2025", is_staff=True)
        self.client = APIClient()

        # Alice login
        res = self.client.post(reverse("token_obtain_pair"), {"username":"satyam","password":"Oct@2025"}, format="json")
        self.alice_access = res.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.satyam_access}")
        r = self.client.post("/api/tasks/", {"id":"1","title":"task","description":"desc"}, format="json")
        self.satyam_task_id = r.data["id"]

    #To check if we can get all tasks, get task by id, update task, delete task and unauthenticated access
    def test_Get_All_Tasks(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.satyam_access}")
        r = self.client.get("/api/tasks/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data["results"]), 1)
        self.assertEqual(r.data["results"][0]["title"], "task")
        self.assertEqual(r.data["results"][0]["description"], "desc")

    def test_Get_Task_By_ID(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.satyam_access}")
        r = self.client.get(f"/api/tasks/{self.satyam_task_id}/")  
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["title"], "task")
        self.assertEqual(r.data["description"], "desc")
    
    def test_Update_Task(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.satyam_access}")
        r = self.client.put(f"/api/tasks/{self.satyam_task_id}/", {"title":"updated task","description":"updated desc"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["title"], "updated task")
        self.assertEqual(r.data["description"], "updated desc")
        self.assertEqual(r.data["owner"], "satyam")

    def test_Delete_Task(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.satyam_access}")
        r = self.client.delete(f"/api/tasks/{self.satyam_task_id}/")
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        r = self.client.get("/api/tasks/")
        self.assertEqual(len(r.data["results"]), 0)

    def test_Unauthenticated_Access(self):
        self.client.credentials()  # Remove any existing credentials
        r = self.client.get("/api/tasks/")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
        r = self.client.post("/api/tasks/", {"title":"task","description":"desc"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
        r = self.client.get(f"/api/tasks/{self.satyam_task_id}/")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
        r = self.client.put(f"/api/tasks/{self.satyam_task_id}/", {"title":"updated task","description":"updated desc"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
        r = self.client.delete(f"/api/tasks/{self.satyam_task_id}/")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)