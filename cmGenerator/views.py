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
from .models import Season, Story, SeasonPlayerStats, SeasonAwards
from .utils.story_generator import generate_all
from django.views.decorators.http import require_http_methods
from .models import Transfer
from django.core.exceptions import ValidationError
import re

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
            
            # Create initial season
            Season.objects.create(
                story=story,
                season="24/25"
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
            
            new_player_id = None  # Initialize variable to store new player ID
            
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
                    'overall_rating': int(stat.get('overall_rating', 0)),
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
                    # Create new stat
                    new_stat = SeasonPlayerStats.objects.create(
                        story=story,
                        **stat_data
                    )
                    new_player_id = new_stat.id

            # Include the new player ID in the response
            response_data = {'success': True}
            if new_player_id:
                response_data['new_player_id'] = new_player_id
                
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

@login_required
def season_stats(request, story_id):
    story = get_object_or_404(Story, id=story_id, user=request.user)
    season = request.GET.get('season')

    # Always get seasons from Season model
    seasons = Season.objects.filter(story=story).values('season').distinct()

    # If no season specified, get the most recent one
    if not season and seasons.exists():
        season = seasons.order_by('-season').first()['season']
    elif not season:  # If still no season (no seasons exist at all)
        season = None

    # Rest of the view remains the same...

    # Get player stats for the selected season
    season_stats = SeasonPlayerStats.objects.filter(story=story, season=season)
    
    # Get season awards
    try:
        season_awards = SeasonAwards.objects.get(story=story, season=season)
    except SeasonAwards.DoesNotExist:
        season_awards = None
    
    # Get transfers for the selected season
    transfers_in = Transfer.objects.filter(story=story, season=season, direction='in')
    transfers_out = Transfer.objects.filter(story=story, season=season, direction='out')
    
    return render(request, 'cmGenerator/season_stats.html', {
        'story': story,
        'seasons': seasons,
        'selected_season': season,
        'season_stats': season_stats,
        'season_awards': season_awards,
        'transfers_in': transfers_in,
        'transfers_out': transfers_out,
    })

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

@login_required
@login_required
def add_season(request, story_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            story = get_object_or_404(Story, id=story_id, user=request.user)
            season = data.get('season')

            # Check for duplicate season as the first step
            if Season.objects.filter(story=story, season=season).exists():
                return JsonResponse({'success': False, 'error': f'Season {season} already exists.'}, status=400)

            # Create and save the new season
            Season.objects.create(story=story, season=season)

            return JsonResponse({'success': True, 'season': season})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

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

@login_required
def create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST) # type: ignore
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            
            # Create initial season
            Season.objects.create(
                story=story,
                season="24/25"
            )
            
            return redirect('season_stats', story_id=story.id)
    else:
        form = StoryForm() # type: ignore
    return render(request, 'cmGenerator/create_story.html', {'form': form})

@login_required
def save_season_awards(request, story_id):
    if request.method == 'POST':
        try:
            story = get_object_or_404(Story, id=story_id, user=request.user)
            season = request.POST.get('season')
            
            # Create or update season awards
            SeasonAwards.objects.update_or_create(
                story=story,
                season=season,
                defaults={
                    # League Winners
                    'la_liga_winner': request.POST.get('la_liga_winner', ''),
                    'serie_a_winner': request.POST.get('serie_a_winner', ''),
                    'bundesliga_winner': request.POST.get('bundesliga_winner', ''),
                    'ligue_1_winner': request.POST.get('ligue_1_winner', ''),
                    'premier_league_winner': request.POST.get('premier_league_winner', ''),
                    # Cup Winners
                    'champions_league_winner': request.POST.get('champions_league_winner', ''),
                    'europa_league_winner': request.POST.get('europa_league_winner', ''),
                    'conference_league_winner': request.POST.get('conference_league_winner', ''),
                    'super_cup_winner': request.POST.get('super_cup_winner', ''),
                    # Individual Awards
                    'balon_dor_winner': request.POST.get('balon_dor_winner', ''),
                    'golden_boy_winner': request.POST.get('golden_boy_winner', ''),
                }
            )
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@require_http_methods(["POST"])
def save_transfer(request, story_id):
    try:
        data = json.loads(request.body)
        transfer_data = data.get('transfer')
        
        # Check if transfer exists
        transfer_id = transfer_data.get('id')
        if transfer_id and transfer_id > 0:
            # Update existing transfer
            transfer = Transfer.objects.get(id=transfer_id, story_id=story_id)
            for field, value in transfer_data.items():
                if field != 'id' and hasattr(transfer, field):
                    setattr(transfer, field, value)
            transfer.save()
        else:
            # Create new transfer
            transfer = Transfer.objects.create(
                story_id=story_id,
                player_name=transfer_data.get('player_name', 'New Player'),
                club=transfer_data.get('club', ''),
                fee=transfer_data.get('fee', '€0'),
                season=transfer_data.get('season'),
                direction=transfer_data.get('direction')
            )
        
        return JsonResponse({
            'success': True,
            'transfer_id': transfer.id
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@require_http_methods(["POST"])
def delete_transfer(request, story_id):
    try:
        data = json.loads(request.body)
        transfer_id = data.get('transfer_id')
        
        # Find and delete the transfer
        transfer = Transfer.objects.get(id=transfer_id, story_id=story_id)
        transfer.delete()
        
        return JsonResponse({
            'success': True
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@require_http_methods(["GET"])
def get_transfers(request, story_id):
    try:
        season = request.GET.get('season')
        
        # Get transfers for the season
        transfers_in = Transfer.objects.filter(
            story_id=story_id,
            season=season,
            direction='in'
        ).values('id', 'player_name', 'club', 'fee')
        
        transfers_out = Transfer.objects.filter(
            story_id=story_id,
            season=season,
            direction='out'
        ).values('id', 'player_name', 'club', 'fee')
        
        return JsonResponse({
            'success': True,
            'transfers_in': list(transfers_in),
            'transfers_out': list(transfers_out)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

def get_seasons(request, story_id):
    if request.method == 'GET':
        try:
            story = Story.objects.get(id=story_id)
            if story.user != request.user:
                return JsonResponse({'success': False, 'error': 'Permission denied'})
            
            # Get seasons from Season model
            seasons = Season.objects.filter(story=story)\
                          .values_list('season', flat=True)\
                          .distinct()
            
            return JsonResponse({'success': True, 'seasons': list(seasons)})
            
        except Story.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Story not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

