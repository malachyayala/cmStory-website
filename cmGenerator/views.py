# cmGenerator/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
import os
from .models import Story
from .utils.story_generator import generate_all

def index(request):
    return render(request, 'cmGenerator/index.html')

  # Ensures only logged-in users can generate stories
def generate_story(request):
    """Generates a new story but does NOT save it."""
    if request.method == "POST":
        data = generate_all()  # Generate new story data

        return JsonResponse({
            "success": True,
            "club": data['club'],
            "formation": data['formation'],
            "challenge": data['challenge'],
            "background": data['background']
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def save_story(request):
    """Saves a story when the user explicitly clicks 'Save Story'."""
    if request.method == "POST":
        club = request.POST.get("club")
        formation = request.POST.get("formation")
        challenge = request.POST.get("challenge")
        background = request.POST.get("background")

        if club and formation and challenge and background:
            Story.objects.create(
                user=request.user,
                club=club,
                formation=formation,
                challenge=challenge,
                background=background
            )
            return JsonResponse({"success": True, "message": "Story saved!"})

    return JsonResponse({"error": "Failed to save story"}, status=400)

def generate_story(request):
    data = generate_all()
    return JsonResponse(data)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserCreationForm()
    
    return render(request, 'cmGenerator/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Redirect to home after successful login
        messages.error(request, "Invalid username or password.")  # Display error message

    else:
        form = AuthenticationForm()

    return render(request, 'cmGenerator/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('/login/')

def my_stories(request):
    stories = Story.objects.filter(user=request.user).order_by('-created_at')  # Get only user's stories
    return render(request, 'cmGenerator/my_stories.html', {'stories': stories})