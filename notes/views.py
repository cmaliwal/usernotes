from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework import filters, permissions, viewsets
from rest_framework.serializers import BaseSerializer

from .models import Note
from .serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing notes owned by the authenticated user.

    Attributes:
        serializer_class (BaseSerializer): The serializer class that should be used
                                           for validating and deserializing input and
                                           for serializing output.
        permission_classes (list): A list of permission classes that will be used to
                                   check if the user has permission to perform the
                                   requested action.
    """

    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ("title", "content")

    def get_queryset(self) -> QuerySet:
        """
        Retrieve the queryset of notes for the currently authenticated user.

        Overrides the `get_queryset` method to filter notes, returning only those
        owned by the currently authenticated user.

        Returns:
            QuerySet: A Django QuerySet that contains `Note` instances owned by the
                      authenticated user.
        """
        user: User = self.request.user
        return Note.objects.filter(user=user)

    def perform_create(self, serializer: BaseSerializer) -> None:
        """
        Perform the note creation.

        Overrides the `perform_create` method to assign the currently authenticated user
        as the owner of the note.

        Args:
            serializer (BaseSerializer): The serializer instance that should be used
                                         to save the model instance.

        Returns:
            None
        """
        serializer.save(user=self.request.user)
