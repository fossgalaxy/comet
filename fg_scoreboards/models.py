from django.db import models
from django.db.models import Avg

from django.conf import settings

# Create your models here.
ENTRANT_MODEL = "fg_competitions.submission"

WIN_LOSS_CHOICES = (
    ('L', "Loss"),
    ('D', "Draw"),
    ('W', "Win"),
    ('X', 'Disqualified')
)

SCORE_TYPES = (
    ('win', 'Total Wins'),
    ('avg', 'Mean Points'),
    ('sum', 'Total Points')
)

class ScoreBoard(models.Model):
    """A collection of games"""
    name = models.CharField(max_length=150)

    # choices
    scoring_system = models.CharField(max_length=3, choices=SCORE_TYPES, default='avg')
    points_name = models.CharField(max_length=15, blank=True, null=True)

    @property
    def ordering(self):
        if self.scoring_system == 'win':
            return self.wins
        elif self.scoring_system == 'sum':
            return self.total_points
        elif self.scoring_system == 'avg':
            return self.avg_points
        else:
            return []

    @property
    def wins(self):
        """Calcuate and return wins for each player over all games played.

        For easy development, this is presently calcuated in python. It should
        be refactored to a group by clause in the database before hitting
        production :)"""
        our_games = self.game_set.all()

        players = {}

        for game in our_games:
            for result in game.stats.all():
                pk = result.player.pk
                if not pk in players:
                    players[pk] = {
                        "player": result.player,
                        "points": 1 if result.outcome == 'W' else 0,
                        "games": 1
                    }
                else:
                    players[pk]['points'] += 1 if result.outcome == 'W' else 0
                    players[pk]['games'] += 1

        return self._annotate_ranks(players)

    @property
    def avg_points(self):
        """Calcuate and return averages for each player over all games played.

        For easy development, this is presently calcuated in python. It should
        be refactored to a group by clause in the database before hitting
        production :)"""
        our_games = self.game_set.all()

        players = {}

        for game in our_games:
            for result in game.stats.all():
                pk = result.player.pk
                if not pk in players:
                    players[pk] = {
                        "rank": 1,
                        "player": result.player,
                        "points": result.points,
                        "games": 1
                    }
                else:
                    players[pk]['points'] += result.points
                    players[pk]['games'] += 1

        for (player, row) in players.items():
            row['points'] = row['points'] / row['games']

        last_rank = 0
        next_rank = 1
        last_points = -99999

        for (player, row) in players.items():
            if row['points'] == last_points:
                row['rank'] = last_rank
                next_rank += 1
            else:
                row['rank'] = next_rank
                last_rank = next_rank
                next_rank += 1
                last_points = row['points']

        return self._annotate_ranks(players)

    @property
    def total_points(self):
        """Calcuate and return totals for each player over all games played.

        For easy development, this is presently calcuated in python. It should
        be refactored to a group by clause in the database before hitting
        production :)"""
        our_games = self.game_set.all()

        players = {}

        for game in our_games:
            for result in game.stats.all():
                pk = result.player.pk
                if not pk in players:
                    players[pk] = {
                        "player": result.player,
                        "points": result.points,
                        "games": 1
                    }
                else:
                    players[pk]['points'] += result.points
                    players[pk]['games'] += 1

        return self._annotate_ranks(players)

    def _annotate_ranks(self, players):
        """Annotate a dictionary of pk => entry into rank order"""
        players = sorted(players.values(), key=lambda x: x['points'], reverse=True)

        last_rank = 0
        next_rank = 1
        last_points = -99999

        for row in players:
            if row['points'] == last_points:
                row['rank'] = last_rank
                next_rank += 1
            else:
                row['rank'] = next_rank
                last_rank = next_rank
                next_rank += 1
                last_points = row['points']
        return players

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('scoreboard', kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

class Game(models.Model):
    """A thing that we're scoring"""
    board = models.ForeignKey(ScoreBoard, on_delete=models.CASCADE)
    game_id = models.CharField(max_length=60)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.board, self.game_id)

class PlayerStats(models.Model):
    """Something which played a game"""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="stats")
    player = models.ForeignKey(ENTRANT_MODEL, on_delete=models.CASCADE)

    # stats
    points = models.DecimalField(max_digits=19, decimal_places=8)
    time_taken = models.PositiveIntegerField(default=0)
    outcome = models.CharField(max_length=1, choices=WIN_LOSS_CHOICES)

    def __str__(self):
        return "{}".format(self.player)
