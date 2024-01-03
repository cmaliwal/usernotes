from typing import List
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework.response import Response

from .models import Note


class NoteViewSetTestCase(APITestCase):
    """
    Test cases for NoteViewSet.

    This class contains various test cases for testing the NoteViewSet, ensuring
    the correct handling of note creation, retrieval, updating, deletion, and
    unauthorized access.
    """

    def setUp(self) -> None:
        """
        Set up the test environment.

        This method is called before each test execution. It sets up a test user,
        token for authentication, and a test client.
        """
        self.user: User = User.objects.create_user(
            username="testuser", password="12345"
        )
        self.token: Token = Token.objects.create(user=self.user)
        self.client: APIClient = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token.key)
        self.url: str = reverse("note-list")

    def create_notes(self, count: int = 3) -> List[Note]:
        """
        Helper method to create a specified number of notes.

        Args:
            count (int): Number of notes to create.

        Returns:
            List[Note]: A list of created Note instances.
        """
        return [
            Note.objects.create(
                user=self.user, title=f"Test Note{i}", content=f"This is test note {i}."
            )
            for i in range(1, count + 1)
        ]

    def test_get_notes_list(self) -> None:
        """
        Test to verify getting a list of notes.

        Ensures that the list of notes is correctly retrieved and that the
        response contains the expected number of notes.
        """
        self.create_notes(3)
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("results")), 3)

    def test_search_notes(self) -> None:
        """
        Test to verify the search functionality in the notes list.

        Ensures that the search query correctly filters the notes.
        """
        self.create_notes(3)
        search_url = f"{self.url}?search=Note1"
        response: Response = self.client.get(search_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("results")), 1)
        self.assertIn("Note1", response.json().get("results")[0].get("title"))

    def test_create_note(self) -> None:
        """
        Test to verify note creation.

        Ensures that a new note can be successfully created and stored in the database.
        """
        data = {"title": "New Note", "content": "Content of the new note."}
        response: Response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)

    def test_update_note(self) -> None:
        """
        Test to verify note updating.

        Ensures that an existing note can be successfully updated.
        """
        note: Note = Note.objects.create(
            user=self.user, title="Original Title", content="Original content."
        )
        url: str = reverse("note-detail", args=[note.id])
        data = {"title": "Updated Title", "content": "Updated content."}
        response: Response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note.refresh_from_db()
        self.assertEqual(note.title, "Updated Title")

    def test_delete_note(self) -> None:
        """
        Test to verify note deletion.

        Ensures that a note can be successfully deleted from the database.
        """
        note: Note = Note.objects.create(
            user=self.user, title="Note to be deleted", content="Content of the note."
        )
        url: str = reverse("note-detail", args=[note.id])
        response: Response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Note.objects.filter(id=note.id).exists())

    def test_unauthorized_access(self) -> None:
        """
        Test to verify unauthorized access handling.

        Ensures that unauthorized access to the notes API is correctly denied.
        """
        self.client.credentials()  # Remove authentication token
        response: Response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
