from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required


User = get_user_model()

def register(request):
    pass

def login_view(request):
    pass

def logout_view():
    pass