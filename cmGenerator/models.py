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
    player_name = models.CharField(max_length=100)
    season = models.CharField(max_length=10)
    appearances = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    clean_sheets = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    
    class Meta:
        unique_together = ['story', 'season', 'player_name']

    def __str__(self):
        return f"Season {self.season} - {self.story.club} - {self.player_name}"