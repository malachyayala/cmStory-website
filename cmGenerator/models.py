from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link story to user
    club = models.CharField(max_length=255)
    formation = models.CharField(max_length=255)
    challenge = models.TextField()
    background = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Store when the story was created

    def __str__(self):
        return f"{self.club} - {self.user.username}"
