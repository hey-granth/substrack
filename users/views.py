import json
from django.http import JsonResponse
from .utils import upi_validation
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model


User = get_user_model()


@api_view(["POST"])
def register_view(request):
    """
    Register view for user registration.
    """
    try:
        data = json.loads(request.body)
        email: str = data.get("email")
        password: str = data.get("password")
        username: str = data.get("username")
        upi_id: str = data.get("upi_id")

        # validating input data
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(upi_id=upi_id).exists():
            return Response(
                {"error": "UPI ID already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not upi_id:
            return Response(
                {"error": "UPI ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not email:
            return Response(
                {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not password:
            return Response(
                {"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not username:
            return Response(
                {"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # verifying password strength
        if len(password) < 8:
            return Response(
                {"error": "Password must be at least 8 characters long"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not any(char.isdigit() for char in password):
            return Response(
                {"error": "Password must contain at least one digit"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not any(char.isalpha() for char in password):
            return Response(
                {"error": "Password must contain at least one letter"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not any(char in "!@#$%^&*()_+" for char in password):
            return Response(
                {"error": "Password must contain at least one special character"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if upi_validation(upi_id):
            return Response(
                {"error": "Invalid UPI ID format"}, status=status.HTTP_400_BAD_REQUEST
            )

        user: User = User.objects.create_user(
            username=username, email=email, password=password, upi_id=upi_id
        )
        return Response(
            {"message": "Registration Successful"}, status=status.HTTP_201_CREATED
        )

    except json.JSONDecodeError:
        return Response(
            {"error": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST
        )


# when the user wants to login, they call the "/api/token/" endpoint provided by SimpleJWT to get their JWT token pair (access and refresh tokens)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request) -> JsonResponse:
    # in stateless JWT, logout is handled on the client side by deleting the token. Here, we just provide an endpoint for the client to call when they want to "logout"
    try:
        return JsonResponse({"message": "Logout Successful"})
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"})
