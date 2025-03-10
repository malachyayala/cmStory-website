from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Competition


class CompetitionModelTest (TestCase):

    def testBPL (self):
        self.competition = Competition (
            name = "Premier League",
            competition_type = "LEAGUE",
            country = "England",
            logo_url = "http://example.com/logo.png",
            league_rep = 5,
            tier = 1,
            min_wage_budget = 1000000.00
        )

    def test_competition_creation(self):
        self.assertEqual(self.competition.name, "Premier League")
        self.assertEqual(self.competition.slug, "premier-league")
        self.assertEqual(self.competition.competition_type, "LEAGUE")
        self.assertEqual(self.competition.country, "England")
        self.assertEqual(self.competition.logo_url, "http://example.com/logo.png")
        self.assertEqual(self.competition.league_rep, 5)
        self.assertEqual(self.competition.tier, 1)
        self.assertEqual(self.competition.min_wage_budget, 1000000.00)

    def testLL (self):
        self.competition = Competition (
            name = "La Liga",
            competition_type = "LEAGUE",
            country = "Spain",
            logo_url = "http://example.com/logo.png",
            league_rep = 5,
            tier = 1,
            min_wage_budget = 1000000.00
        )
