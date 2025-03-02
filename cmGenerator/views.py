import json
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
from .models import Season, Story, SeasonPlayerStats
from .utils.story_generator import generate_all
from django.core.exceptions import ObjectDoesNotExist
from openai import OpenAI
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import PyPDF2

def index(request: HttpRequest) -> HttpResponse:
    """
    Renders the index page.
    
    Args:
        request (HttpRequest): The request object.
    
    Returns:
        HttpResponse: The rendered index page.
    """
    return render(request, 'cmGenerator/index.html')

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
def save_season_stats(request, story_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            stats = data.get('stats', [])
            story = get_object_or_404(Story, id=story_id, user=request.user)
            
            for stat in stats:
                stat_id = stat.get('id')
                player_name = stat.get('player_name')
                season = stat.get('season')

                # Skip if player name is empty
                if not player_name:
                    continue

                # Prepare the stat data
                stat_data = {
                    'player_name': player_name,
                    'season': season,
                    'appearances': int(stat.get('appearances', 0)),
                    'goals': int(stat.get('goals', 0)),
                    'assists': int(stat.get('assists', 0)),
                    'clean_sheets': int(stat.get('clean_sheets', 0)),
                    'red_cards': int(stat.get('red_cards', 0)),
                    'yellow_cards': int(stat.get('yellow_cards', 0)),
                    'average_rating': float(stat.get('average_rating', 0))
                }

                if stat_id and int(stat_id) > 0:
                    # Update existing stat
                    SeasonPlayerStats.objects.filter(
                        id=stat_id, 
                        story=story
                    ).update(**stat_data)
                else:
                    # Create new stat using update_or_create to handle duplicates
                    SeasonPlayerStats.objects.update_or_create(
                        story=story,
                        season=season,
                        player_name=player_name,
                        defaults=stat_data
                    )

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

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

@csrf_exempt
@login_required
def extract_data_from_pdf(request):
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf = request.FILES['pdf']
        pdf_path = default_storage.save('uploads/' + pdf.name, ContentFile(pdf.read()))

        try:
            # Extract text from the PDF
            with open(pdf_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfFileReader(pdf_file)
                text = ""
                for page_num in range(reader.numPages):
                    text += reader.getPage(page_num).extract_text()

            # Initialize the OpenAI client with the new API format
            client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
            
            # Use the new API format to analyze the text
            response = client.chat.completions.create(
                model='your-model',
                messages=[
                    {"role": "user", "content": f"Extract player stats from this text and return ONLY a valid JSON object with these fields: player_name, season, appearances, goals, assists, clean_sheets, season_avg. Format as valid JSON.\n\n{text}"},
                ],
                max_tokens=300
            )
            
            # Get the raw text response
            data_text = response.choices[0].message.content
            
            # Try to parse the response as JSON, or create default values if it fails
            try:
                # Clean up the text - sometimes models return markdown-formatted JSON
                # Strip any markdown code block markers if present
                if "```json" in data_text:
                    data_text = data_text.split("```json")[1].split("```")[0].strip()
                elif "```" in data_text:
                    data_text = data_text.split("```")[1].split("```")[0].strip()
                
                extracted_data = json.loads(data_text)
                
                # Ensure all required fields exist
                required_fields = ['player_name', 'season', 'appearances', 'goals', 
                                   'assists', 'clean_sheets', 'season_avg']
                for field in required_fields:
                    if field not in extracted_data:
                        extracted_data[field] = ""
            
            except json.JSONDecodeError:
                # If we can't parse as JSON, create default values
                extracted_data = {
                    'player_name': "Could not extract name",
                    'season': "Unknown",
                    'appearances': "0",
                    'goals': "0",
                    'assists': "0",
                    'clean_sheets': "0",
                    'season_avg': "0.0"
                }
                
                # Log the response for debugging
                print(f"Failed to parse JSON response: {data_text}")

            # Clean up the temporary file
            default_storage.delete(pdf_path)

            return JsonResponse({
                'success': True,
                'newRowId': -1,  # Use a negative ID for new rows
                'player_name': extracted_data['player_name'],
                'season': extracted_data['season'],
                'appearances': extracted_data['appearances'],
                'goals': extracted_data['goals'],
                'assists': extracted_data['assists'],
                'clean_sheets': extracted_data['clean_sheets'],
                'season_avg': extracted_data['season_avg']
            })
            
        except Exception as e:
            # Handle any other exceptions
            print(f"Error in extract_data_from_pdf: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def add_season(request, story_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            story = get_object_or_404(Story, id=story_id, user=request.user)
            season = data.get('season')
            
            # You might want to add the season to a Seasons model if you have one
            # For now, we'll just return success since seasons are stored client-side
            
            return JsonResponse({
                'success': True,
                'season': season
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    }, status=405)

@login_required
def season_stats_view(request, story_id):
    story = get_object_or_404(Story, id=story_id, user=request.user)
    seasons = Season.objects.filter(story=story).order_by('season')
    season_stats = SeasonPlayerStats.objects.filter(story=story)
    
    return render(request, 'cmGenerator/season_stats.html', {
        'story': story,
        'season_stats': season_stats,
        'seasons': seasons  # Add this line
    })