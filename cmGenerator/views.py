from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
import os
from .models import Story, SeasonPlayerStats
from .utils.story_generator import generate_all
from django.core.exceptions import ObjectDoesNotExist

def index(request: HttpRequest) -> HttpResponse:
    """
    Renders the index page.
    
    Args:
        request (HttpRequest): The request object.
    
    Returns:
        HttpResponse: The rendered index page.
    """
    return render(request, 'cmGenerator/index.html')

@login_required
def generate_story(request: HttpRequest) -> JsonResponse:
    """
    Generates a new story but does NOT save it.
    
    Args:
        request (HttpRequest): The request object.
    
    Returns:
        JsonResponse: A JSON response with the generated story data or an error message.
    """
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
def save_story(request: HttpRequest) -> JsonResponse:
    """
    Saves a story when the user explicitly clicks 'Save Story'.
    
    Args:
        request (HttpRequest): The request object.
    
    Returns:
        JsonResponse: A JSON response indicating success or failure.
    """
    if request.method == "POST":
        club = request.POST.get("club")
        formation = request.POST.get("formation")
        challenge = request.POST.get("challenge")
        background = request.POST.get("background")

        if club and formation and challenge and background:
            story = Story.objects.create(
                user=request.user,
                club=club,
                formation=formation,
                challenge=challenge,
                background=background
            )
            return JsonResponse({"success": True, "message": "Story saved!", "story_id": story.id})

    return JsonResponse({"error": "Failed to save story"}, status=400)

@login_required
def save_season_stats(request: HttpRequest) -> JsonResponse:
    """
    Adds season stats to a story.
    
    Args:
        request (HttpRequest): The request object.
    
    Returns:
        JsonResponse: A JSON response indicating success or failure.
    """
    if request.method == "POST":
        story_id = request.POST.get("story_id")
        season = request.POST.get("season")
        appearances = request.POST.get("appearances")
        goals = request.POST.get("goals")
        assists = request.POST.get("assists")
        clean_sheets = request.POST.get("clean_sheets")
        season_avg = request.POST.get("season_avg")

        try:
            story = Story.objects.get(id=story_id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Story does not exist"}, status=400)

        SeasonPlayerStats.objects.create(
            story=story,
            player_name=request.POST.get("player_name"),
            season=season,
            appearances=appearances,
            goals=goals,
            assists=assists,
            clean_sheets=clean_sheets,
            season_avg=season_avg
        )
        return JsonResponse({"success": True, "message": "Season stats added!"})

    return JsonResponse({"error": "Failed to add season stats"}, status=400)

@login_required
def season_stats(request, story_id):
    """
    Displays and adds season stats for a specific story.
    
    Args:
        request (HttpRequest): The request object.
        story_id (int): The ID of the story.
    
    Returns:
        HttpResponse: The page displaying and adding season stats.
    """
    story = get_object_or_404(Story, id=story_id, user=request.user)
    if request.method == "POST":
        player_name = request.POST.get("player_name")
        season = request.POST.get("season")
        appearances = request.POST.get("appearances")
        goals = request.POST.get("goals")
        assists = request.POST.get("assists")
        clean_sheets = request.POST.get("clean_sheets")
        season_avg = request.POST.get("season_avg")

        SeasonPlayerStats.objects.create(
            story=story,
            player_name=player_name,
            season=season,
            appearances=appearances,
            goals=goals,
            assists=assists,
            clean_sheets=clean_sheets,
            season_avg=season_avg
        )
        return redirect('season_stats', story_id=story.id)

    season_stats = story.season_stats.all()
    return render(request, 'cmGenerator/season_stats.html', {'story': story, 'season_stats': season_stats})

def register(request: HttpRequest) -> HttpResponse:
    """
    Handles user registration.
    
    Args:
        request (HttpRequest): The request object.
    
    Returns:
        HttpResponse: The registration page or a redirect to the login page upon successful registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserCreationForm()
    
    return render(request, 'cmGenerator/register.html', {'form': form})

def custom_login(request: HttpRequest) -> HttpResponse:
    """
    Handles user login.
    
    Args:
        request (HttpRequest): The request object.
    
    Returns:
        HttpResponse: The login page or a redirect to the home page upon successful login.
    """
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

def custom_logout(request: HttpRequest) -> HttpResponse:
    """
    Logs out the user and redirects to the login page.
    
    Args:
        request (HttpRequest): The request object.
    
    Returns:
        HttpResponse: A redirect to the login page.
    """
    logout(request)
    return redirect('/login/')

@login_required
def my_stories(request: HttpRequest) -> HttpResponse:
    """
    Displays the stories created by the logged-in user.
    
    Args:
        request (HttpRequest): The request object.
    
    Returns:
        HttpResponse: The page displaying the user's stories.
    """
    stories = Story.objects.filter(user=request.user).order_by('-created_at')  # Get only user's stories
    return render(request, 'cmGenerator/my_stories.html', {'stories': stories})