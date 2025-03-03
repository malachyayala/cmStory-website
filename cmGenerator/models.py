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

class Season(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='seasons')
    season = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['story', 'season']
        ordering = ['season']

    def __str__(self):
        return f"{self.story.club} - {self.season}"

class SeasonPlayerStats(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='season_stats')
    player_name = models.CharField(max_length=100)
    season = models.CharField(max_length=10)
    overall_rating = models.IntegerField(default=0)  # New field for player's overall rating
    appearances = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    clean_sheets = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    
    class Meta:
        unique_together = ['story', 'season', 'player_name']

    def __str__(self):
        return f"Season {self.season} - {self.story.club} - {self.player_name}"
    
class SeasonAwards(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='season_awards')
    season = models.CharField(max_length=10)
    # League Winners
    la_liga_winner = models.CharField(max_length=100, blank=True)
    serie_a_winner = models.CharField(max_length=100, blank=True)
    bundesliga_winner = models.CharField(max_length=100, blank=True)
    ligue_1_winner = models.CharField(max_length=100, blank=True)
    premier_league_winner = models.CharField(max_length=100, blank=True)
    # Cup Winners
    champions_league_winner = models.CharField(max_length=100, blank=True)
    europa_league_winner = models.CharField(max_length=100, blank=True)
    conference_league_winner = models.CharField(max_length=100, blank=True)
    super_cup_winner = models.CharField(max_length=100, blank=True)
    # Individual Awards
    balon_dor_winner = models.CharField(max_length=100, blank=True)
    golden_boy_winner = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ['story', 'season']
        ordering = ['season']

    def __str__(self):
        return f"Awards for {self.story.club} - Season {self.season}"

class Transfer(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='transfers')
    season = models.CharField(max_length=10)
    player_name = models.CharField(max_length=100)
    club = models.CharField(max_length=100)
    fee = models.CharField(max_length=50)
    direction = models.CharField(max_length=5, choices=[('in', 'In'), ('out', 'Out')])
    
    class Meta:
        unique_together = ('story', 'season', 'player_name', 'direction')

