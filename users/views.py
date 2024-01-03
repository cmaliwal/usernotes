from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, UserSerializer


class UserCreate(APIView):
    """
    API view to create a new user.

    This view handles POST requests to create new user accounts. It uses the
    UserSerializer to validate and create a new User object.
    """

    serializer_class = UserSerializer

    def post(self, request: HttpRequest, format: str = "json") -> Response:
        """
        Handle POST request to create a new user.

        Args:
            request (HttpRequest): The incoming request object.
            format (str): The format of the request content.

        Returns:
            Response: A DRF Response object containing the new user's data and
                      status code HTTP_201_CREATED on successful creation,
                      or error details and status code HTTP_400_BAD_REQUEST
                      on failure.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API view for user authentication.

    This view handles POST requests to authenticate users. It checks the provided
    credentials and returns an authentication token if they are valid.
    """

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
