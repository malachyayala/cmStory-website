from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

class Club(models.Model):
    """
    Represents a football club.

    Attributes:
        name (str): The name of the club. This is a CharField with a maximum length of 255 characters.
        league (str): The league in which the club competes. This is a CharField with a maximum length of 100 characters.
        country (str): The country where the club is based. This is a CharField with a maximum length of 100 characters.
    """
    name = models.CharField(max_length=255)
    league = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Player(models.Model):
    # Primary identifiers
    player_id = models.IntegerField(unique=True)  # Keep this if it matches your CSV column    
    # Basic info
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)  # URL-friendly name
    
    # Position fields with choices for better validation
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('CB', 'Center Back'),
        ('LB', 'Left Back'),
        ('RB', 'Right Back'),
        ('CDM', 'Defensive Midfielder'),
        ('CM', 'Central Midfielder'),
        ('CAM', 'Attacking Midfielder'),
        ('LM', 'Left Midfielder'),
        ('RM', 'Right Midfielder'),
        ('LW', 'Left Winger'),
        ('RW', 'Right Winger'),
        ('ST', 'Striker'),
        ('CF', 'Center Forward'),
    ]
    
    primary_position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    secondary_position = models.CharField(max_length=50, choices=POSITION_CHOICES, blank=True, null=True)
    tertiary_position = models.CharField(max_length=50, choices=POSITION_CHOICES, blank=True, null=True)
    
    # Personal details
    nationality = models.CharField(max_length=100)
    birth_date = models.DateField()
    birth_year = models.IntegerField(null=True, blank=True)  # Derived field, can be calculated from birth_date
    age = models.IntegerField()  # Consider making this a property method instead of a field
    face_pic_url = models.URLField(null=True, blank=True)
    
    # Club information
    club = models.ForeignKey(Club, on_delete=models.CASCADE, db_index=True)  # Changed to ForeignKey
    
    # Contract details
    wage_eur = models.DecimalField(max_digits=10, decimal_places=2)
    wage_usd = models.DecimalField(max_digits=10, decimal_places=2)
    wage_gbp = models.DecimalField(max_digits=10, decimal_places=2)
    contract_start = models.DateField()
    contract_end = models.DateField()
    contract_loan = models.BooleanField(default=False)
    
    # Skills and ratings
    overall = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )
    potential = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )
    
    # Import tracking
    last_import_date = models.DateTimeField(auto_now=True)
    import_source = models.CharField(max_length=100, blank=True, null=True)  # e.g., "FIFA23_CSV_IMPORT"
    
    # Meta configuration
    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"
        ordering = ['-overall', 'name']
        indexes = [
            models.Index(fields=['name', 'overall']),
            models.Index(fields=['club', 'primary_position']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.overall}) - {self.club}"
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.player_id}")
        
        # Calculate birth_year from birth_date if not provided
        if not self.birth_year and self.birth_date:
            self.birth_year = self.birth_date.year
            
        super().save(*args, **kwargs)
        
    @property
    def current_age(self):
        """Calculate current age instead of using static field"""
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

class Story(models.Model):
    """
    Represents a user's career mode story.

    Attributes:
        user (User): The user who created the story. This is a ForeignKey to the User model with CASCADE delete.
        club (Club): The club associated with the story. This is a ForeignKey to the Club model with CASCADE delete.
        formation (str): The formation used in the story. This is a CharField with a maximum length of 255 characters.
        challenge (str): The challenge description of the story. This is a TextField.
        background (str): The background information of the story. This is a TextField.
        created_at (datetime): The date and time when the story was created. This is a DateTimeField with auto_now_add=True.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    formation = models.CharField(max_length=255)
    challenge = models.TextField()
    background = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.club.name} - {self.user.username}"

class Season(models.Model):
    """
    Represents a season within a story.

    Attributes:
        story (Story): The story to which the season belongs. This is a ForeignKey to the Story model with CASCADE delete and a related_name of 'seasons'.
        name (str): The name of the season (e.g., "2024-2025"). This is a CharField with a maximum length of 10 characters.
        is_current (bool): Indicates if this is the current season. This is a BooleanField with a default value of False.
        created_at (datetime): The date and time when the season was created. This is a DateTimeField with auto_now_add=True.
    
    Meta:
        unique_together (tuple): Ensures that the combination of story and name is unique.
        ordering (list): Orders the seasons by name.
    """
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='seasons')
    name = models.CharField(max_length=10)  # e.g. "2024-2025"
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['story', 'name']
        ordering = ['name']

    def __str__(self):
        return f"{self.story.club.name} - {self.name}"

class Transfer(models.Model):
    """
    Represents a player transfer between clubs.

    Attributes:
        season (Season): The season during which the transfer occurred. This is a ForeignKey to the Season model with CASCADE delete and a related_name of 'transfers'.
        story (Story): The story to which the transfer belongs. This is a ForeignKey to the Story model with CASCADE delete and a related_name of 'seasons'.
        player (Player): The player being transferred. This is a ForeignKey to the Player model with CASCADE delete.
        from_club (Club): The club from which the player is being transferred. This is a ForeignKey to the Club model with CASCADE delete and a related_name of 'transfers_out'.
        to_club (Club): The club to which the player is being transferred. This is a ForeignKey to the Club model with CASCADE delete and a related_name of 'transfers_in'.
        fee (decimal): The transfer fee. This is a DecimalField with a maximum of 12 digits and 2 decimal places.
        fee_currency (str): The currency of the transfer fee. This is a CharField with a maximum length of 3 characters and a default value of 'EUR'.
        transfer_date (date): The date of the transfer. This is a DateField.
    
    Meta:
        unique_together (tuple): Ensures that the combination of season, player, from_club, and to_club is unique.
    """
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='transfers')
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='transfers')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    from_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='transfers_out')
    to_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='transfers_in')
    fee = models.DecimalField(max_digits=12, decimal_places=2)
    fee_currency = models.CharField(max_length=3, default='EUR')
    transfer_date = models.DateField()
    
    class Meta:
        unique_together = ('season', 'player', 'from_club', 'to_club')

class PlayerStats(models.Model):
    """
    Represents the statistics of a player for a specific season.

    Attributes:
        story (Story): The story to which the player stats belong. This is a ForeignKey to the Story model with CASCADE delete and a related_name of 'seasons'.
        season (Season): The season during which the stats were recorded. This is a ForeignKey to the Season model with CASCADE delete and a related_name of 'player_stats'.
        player (Player): The player whose stats are being recorded. This is a ForeignKey to the Player model with CASCADE delete.
        overall_rating (int): The overall rating of the player. This is an IntegerField with a default value of 0.
        appearances (int): The number of appearances made by the player. This is an IntegerField with a default value of 0.
        goals (int): The number of goals scored by the player. This is an IntegerField with a default value of 0.
        assists (int): The number of assists made by the player. This is an IntegerField with a default value of 0.
        clean_sheets (int): The number of clean sheets kept by the player. This is an IntegerField with a default value of 0.
        red_cards (int): The number of red cards received by the player. This is an IntegerField with a default value of 0.
        yellow_cards (int): The number of yellow cards received by the player. This is an IntegerField with a default value of 0.
        average_rating (decimal): The average rating of the player. This is a DecimalField with a maximum of 4 digits, 2 decimal places, and a default value of 0.00.
    
    Meta:
        unique_together (tuple): Ensures that the combination of season and player is unique.
    """
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='player_stats')
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
    """
    Represents a football competition.

    Attributes:
        name (str): The name of the competition. This is a CharField with a maximum length of 100 characters.
        competition_type (str): The type of competition (e.g., "League", "Cup"). This is a CharField with a maximum length of 50 characters.
    """
    name = models.CharField(max_length=100)  # e.g. "Premier League", "Champions League"
    competition_type = models.CharField(max_length=50)  # e.g. "League", "Cup"
    
    def __str__(self):
        return self.name

class CompetitionWinner(models.Model):
    """
    Represents the winner of a competition for a specific season.

    Attributes:
        story (Story): The story to which the competition winner belongs. This is a ForeignKey to the Story model with CASCADE delete and a related_name of 'seasons'.
        season (Season): The season during which the competition was held. This is a ForeignKey to the Season model with CASCADE delete and a related_name of 'competition_winners'.
        competition (Competition): The competition that was won. This is a ForeignKey to the Competition model with CASCADE delete.
        winner (Club): The club that won the competition. This is a ForeignKey to the Club model with CASCADE delete.
    
    Meta:
        unique_together (tuple): Ensures that the combination of season and competition is unique.
    """
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='competition_winners')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='competition_winners')
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    winner = models.ForeignKey(Club, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['season', 'competition']

class IndividualAward(models.Model):
    """
    Represents an individual award.

    Attributes:
        name (str): The name of the award. This is a CharField with a maximum length of 100 characters.
    """
    name = models.CharField(max_length=100)  # e.g. "Ballon d'Or"
    
    def __str__(self):
        return self.name

class AwardWinner(models.Model):
    """
    Represents the winner of an individual award for a specific season.

    Attributes:
        story (Story): The story to which the award winner belongs. This is a ForeignKey to the Story model with CASCADE delete and a related_name of 'seasons'.
        season (Season): The season during which the award was given. This is a ForeignKey to the Season model with CASCADE delete and a related_name of 'award_winners'.
        award (IndividualAward): The award that was won. This is a ForeignKey to the IndividualAward model with CASCADE delete.
        player (Player): The player who won the award. This is a ForeignKey to the Player model with CASCADE delete.
    
    Meta:
        unique_together (tuple): Ensures that the combination of season and award is unique.
    """
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='award_winners')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='award_winners')
    award = models.ForeignKey(IndividualAward, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['season', 'award']

