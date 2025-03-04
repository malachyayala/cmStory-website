from django.contrib import admin
from django.urls import path, include  # Make sure to import include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('generate/', views.generate_story, name='generate'),
    path('my-stories/', views.my_stories, name='my_stories'),
    path('save-story/', views.save_story, name='save_story'),
    path('add-season-stats/', views.save_season_stats, name='add_season_stats'),
    path('season-stats/<int:story_id>/', views.season_stats, name='season_stats'),
    path('save-season-stats/<int:story_id>/', views.save_season_stats, name='save_season_stats'),
    path('story/<int:story_id>/stats/save/', views.save_season_stats, name='save_season_stats'),
    path('story/<int:story_id>/add-season/', views.add_season, name='add_season'),
    path('save-season-awards/<int:story_id>/', views.save_season_awards, name='save_season_awards'),
    path('story/<int:story_id>/save-transfer/', views.save_transfer, name='save_transfer'),
    path('story/<int:story_id>/delete-transfer/', views.delete_transfer, name='delete_transfer'),
    path('story/<int:story_id>/get-transfers/', views.get_transfers, name='get_transfers'),
    path('story/<int:story_id>/get-seasons/', views.get_seasons, name='get_seasons'),
]