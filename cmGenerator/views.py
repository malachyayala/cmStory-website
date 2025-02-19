# cmGenerator/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os
from .utils.story_generator import generate_all

def index(request):
    return render(request, 'cmGenerator/index.html')

def generate_story(request):
    data = generate_all()
    return JsonResponse(data)