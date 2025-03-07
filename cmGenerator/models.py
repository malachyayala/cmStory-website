from django.db import models
from django.contrib.auth.models import User

class Club(models.Model):
    name = models.CharField(max_length=255)
    league = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    nationality = models.CharField(max_length=100)
    birth_year = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    formation = models.CharField(max_length=255)
    challenge = models.TextField()
    background = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.club.name} - {self.user.username}"

class Season(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='seasons')
    name = models.CharField(max_length=10)  # e.g. "2024-2025"
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['story', 'name']
        ordering = ['name']

    def __str__(self):
        return f"{self.story.club.name} - {self.name}"
    
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
        return f"Awards for {self.story.club.name} - Season {self.season}"

class Transfer(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='transfers')
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='seasons')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    from_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='transfers_out')
    to_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='transfers_in')
    fee = models.DecimalField(max_digits=12, decimal_places=2)
    fee_currency = models.CharField(max_length=3, default='EUR')
    transfer_date = models.DateField()
    
    class Meta:
        unique_together = ('season', 'player', 'from_club', 'to_club')

class PlayerStats(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='seasons')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='player_stats')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    overall_rating = models.IntegerField(default=0)
    appearances = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    clean_sheets = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    
    class Meta:
        unique_together = ['season', 'player']

    def __str__(self):
        return f"{self.season.name} - {self.player.name}"

class Competition(models.Model):
    name = models.CharField(max_length=100)  # e.g. "Premier League", "Champions League"
    competition_type = models.CharField(max_length=50)  # e.g. "League", "Cup"
    
    def __str__(self):
        return self.name

class CompetitionWinner(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='seasons')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='competition_winners')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    winner = models.ForeignKey(Club, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['season', 'competition']

class IndividualAward(models.Model):
    name = models.CharField(max_length=100)  # e.g. "Ballon d'Or"
    
    def __str__(self):
        return self.name

class AwardWinner(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='seasons')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='award_winners')
    award = models.ForeignKey(IndividualAward, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['season', 'award']

