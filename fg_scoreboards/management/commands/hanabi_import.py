from django.core.management.base import BaseCommand, CommandError
from fg_scoreboards.models import ScoreBoard, Game, PlayerStats

import csv

def repack(data):
    repacked = {}

    for value in data:
        key = value['gameId']
        repeat = key.split("-")[-1]
        code = (value['seed'], value['agentPaired'], value['players'], repeat)
        code = "$".join([ str(x) for x in code ])

        if code not in repacked:
            repacked[code] = dict()

        repacked[code][ value['agentUnderTest'] ] = (value['score'], value['moves'])
    return repacked

class Command(BaseCommand):
    help = 'Import a CSV file game results'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        with open(options['filename']) as f:
            data = csv.DictReader(f)
            if not data:
                raise CommandError('could not read CSV data')
            data = repack(data)

        board = ScoreBoard()
        board.name = "Console Import"
        board.save()
        for (gameid, results) in data.items():
            game = Game()
            game.game_id = gameid
            game.board = board
            game.owner_id = 1
            game.save()
            self.stdout.write(self.style.SUCCESS('Created game "%s"' % game))

            for (player, (score, time)) in results.items():
                ps = PlayerStats()
                ps.player_id = 4
                ps.game = game
                ps.points = score
                ps.time_taken = time
                ps.result = 'W'
                ps.save()
                self.stdout.write(self.style.SUCCESS('added scores "%s"' % ps))
