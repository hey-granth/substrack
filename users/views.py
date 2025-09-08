import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required


User = get_user_model()


@csrf_exempt
def register(request) -> JsonResponse:
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            email: str = data.get('email')
            password: str = data.get('password')
            username: str = data.get('username')

            # validating input data
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'})
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'})
            if not email:
                return JsonResponse({'error': 'Email is required'})
            if not password:
                return JsonResponse({'error': 'Password is required'})
            if not username:
                return JsonResponse({'error': 'Username is required'})

            # verifying password strength
            if len(password) < 8:
                return JsonResponse({'error': 'Password must be at least 8 characters long'})
            if not any(char.isdigit() for char in password):
                return JsonResponse({'error': 'Password must contain at least one digit'})
            if not any(char.isalpha() for char in password):
                return JsonResponse({'error': 'Password must contain at least one letter'})
            if not any(char in '!@#$%^&*()_+' for char in password):
                return JsonResponse({'error': 'Password must contain at least one special character'})

            user: User = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return JsonResponse({'message': 'Registration Successful'})

        return JsonResponse({'error': 'Invalid request method'})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'})


@csrf_exempt
def login_view(request) -> JsonResponse:
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            email: str = data.get('email')
            password: str = data.get('password')

            if not email or not password:
                return JsonResponse({'error': 'Email and password are required'})

            user: User = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login Successful'})
            else:
                return JsonResponse({'error': 'Invalid email or password'})

        return JsonResponse({'error': 'Invalid request method'})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'})


@login_required
@csrf_exempt
def logout_view(request) -> JsonResponse:
    try:
        logout(request)
        return JsonResponse({'message': 'Logout Successful'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'})