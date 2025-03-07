from django.test import TestCase
from django.contrib.auth.models import User
from cmGenerator.models import Club, Player, Story, Season, Transfer, PlayerStats, Competition, CompetitionWinner, IndividualAward, AwardWinner

class ClubModelTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(name="FC Barcelona", league="La Liga", country="Spain")

    def test_club_creation(self):
        self.assertEqual(self.club.name, "FC Barcelona")
        self.assertEqual(self.club.league, "La Liga")
        self.assertEqual(self.club.country, "Spain")
        self.assertEqual(str(self.club), "FC Barcelona")

class PlayerModelTest(TestCase):
    def setUp(self):
        self.player = Player.objects.create(name="Lionel Messi", position="Forward", nationality="Argentina", birth_year=1987)

    def test_player_creation(self):
        self.assertEqual(self.player.name, "Lionel Messi")
        self.assertEqual(self.player.position, "Forward")
        self.assertEqual(self.player.nationality, "Argentina")
        self.assertEqual(self.player.birth_year, 1987)
        self.assertEqual(str(self.player), "Lionel Messi")

class StoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.club = Club.objects.create(name="FC Barcelona", league="La Liga", country="Spain")
        self.story = Story.objects.create(user=self.user, club=self.club, formation="4-3-3", challenge="Win the league", background="Club history", created_at="2025-03-07")

    def test_story_creation(self):
        self.assertEqual(self.story.user.username, "testuser")
        self.assertEqual(self.story.club.name, "FC Barcelona")
        self.assertEqual(self.story.formation, "4-3-3")
        self.assertEqual(self.story.challenge, "Win the league")
        self.assertEqual(self.story.background, "Club history")
        self.assertEqual(str(self.story), "FC Barcelona - testuser")

class SeasonModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.club = Club.objects.create(name="FC Barcelona", league="La Liga", country="Spain")
        self.story = Story.objects.create(user=self.user, club=self.club, formation="4-3-3", challenge="Win the league", background="Club history", created_at="2025-03-07")
        self.season = Season.objects.create(story=self.story, name="2024-2025", is_current=True, created_at="2025-03-07")

    def test_season_creation(self):
        self.assertEqual(self.season.story, self.story)
        self.assertEqual(self.season.name, "2024-2025")
        self.assertTrue(self.season.is_current)
        self.assertEqual(str(self.season), "FC Barcelona - 2024-2025")

class TransferModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.club1 = Club.objects.create(name="FC Barcelona", league="La Liga", country="Spain")
        self.club2 = Club.objects.create(name="Paris Saint-Germain", league="Ligue 1", country="France")
        self.player = Player.objects.create(name="Lionel Messi", position="Forward", nationality="Argentina", birth_year=1987)
        self.story = Story.objects.create(user=self.user, club=self.club1, formation="4-3-3", challenge="Win the league", background="Club history", created_at="2025-03-07")
        self.season = Season.objects.create(story=self.story, name="2024-2025", is_current=True, created_at="2025-03-07")
        self.transfer = Transfer.objects.create(season=self.season, story=self.story, player=self.player, from_club=self.club1, to_club=self.club2, fee=100000000, fee_currency="EUR", transfer_date="2025-03-07")

    def test_transfer_creation(self):
        self.assertEqual(self.transfer.season, self.season)
        self.assertEqual(self.transfer.story, self.story)
        self.assertEqual(self.transfer.player, self.player)
        self.assertEqual(self.transfer.from_club, self.club1)
        self.assertEqual(self.transfer.to_club, self.club2)
        self.assertEqual(self.transfer.fee, 100000000)
        self.assertEqual(self.transfer.fee_currency, "EUR")
        self.assertEqual(self.transfer.transfer_date, "2025-03-07")
        self.assertEqual(str(self.transfer), "Lionel Messi from FC Barcelona to Paris Saint-Germain for 100000000 EUR")

# Add similar test cases for PlayerStats, Competition, CompetitionWinner, IndividualAward, and AwardWinner models
