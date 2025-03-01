from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.CharField(max_length=255)
    formation = models.CharField(max_length=255)
    challenge = models.TextField()
    background = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.club} - {self.user.username}"

class SeasonPlayerStats(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='season_stats')
    player_name = models.CharField(max_length=255)  # New field for player's name
    season = models.CharField(max_length=255)
    appearances = models.IntegerField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    clean_sheets = models.IntegerField()
    season_avg = models.IntegerField()

    def __str__(self):
        return f"Season {self.season} - {self.story.club} - {self.player_name}"