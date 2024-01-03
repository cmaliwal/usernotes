from typing import Any, Dict

from rest_framework import serializers

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Note model.
    
    This serializer provides serialization and deserialization for the Note model.
    It includes fields for 'id', 'title', 'content', and 'user'. The 'user' field is
    read-only as it is set to the current user making the request.
    """

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'user', 'created', 'updated']
        read_only_fields = ['user']

    def create(self, validated_data: Dict[str, Any]) -> Note:
        """
        Create and return a new `Note` instance, given the validated data.

        Args:
            validated_data (Dict[str, Any]): The data that has passed validation checks
                                             and is ready to be used to create a Note instance.

        Returns:
            Note: The newly created Note instance.
        """
        # Assign the user from the request context to the validated data.
        validated_data['user'] = self.context['request'].user
        # Create a new Note instance with the validated data.
        return super().create(validated_data)
