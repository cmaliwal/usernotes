from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase


class UserCreateAndLoginViewTestCase(APITestCase):
    """
    Test cases for UserCreate and LoginView.

    This class tests the functionality of creating new users and authenticating them
    using the UserCreate and LoginView API views.
    """

    def setUp(self) -> None:
        """
        Set up the test environment.

        This method is called before each test execution. It sets up a test client.
        """
        self.client: APIClient = APIClient()
        self.create_url: str = reverse("register")
        self.login_url: str = reverse("login")

    def test_create_user_success(self) -> None:
        """
        Test the successful creation of a new user.

        Ensures that a new user can be created and a correct response is received.
        """
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com",
        }
        response: Response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_create_user_invalid_data(self) -> None:
        """
        Test the creation of a new user with invalid data.

        Ensures that an appropriate error response is received when invalid data is provided.
        """
        data = {"username": "newuser", "password": ""}
        response: Response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self) -> None:
        """
        Test the successful login of a user.

        Ensures that a user can log in and receive an authentication token.
        """
        User.objects.create_user(username="testuser", password="12345")
        data = {"username": "testuser", "password": "12345"}
        response: Response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in response.data)

    def test_login_failure(self) -> None:
        """
        Test the login of a user with incorrect credentials.

        Ensures that an error response is received when invalid credentials are provided.
        """
        User.objects.create_user(username="testuser", password="12345")
        data = {"username": "testuser", "password": "wrongpassword"}
        response: Response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
