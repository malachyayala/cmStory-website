# fifa_storyline/urls.py
from django.contrib import admin
from django.urls import path, include  # Make sure to import include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
    path('login/', views.custom_login, name='login'),  # Use the custom login view
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('generate/', views.generate_story, name='generate'),
    path('my-stories/', views.my_stories, name='my_stories'),
    path('save-story/', views.save_story, name='save_story'),
]