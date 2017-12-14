import math
import random
import time
from player import Player

from coin import Coin
from penny import Penny
from nickel import Nickel
from dime import Dime
from dollar import Dollar

class AIPlayer(Player):
    # ai_difficulty represents an index in a list
    # the list is moves the AI has simulated and scored.
    # the list is sorted with the best-scored moves at the front, at index zero.
    # setting ai_difficulty to 0 means the AI always chooses the absolute best move.
    # ai_difficulty is clamped between 0 and the length of whatever choices are
    # available on each turn
    def __init__(self, is_ai=True, is_heads=False, ai_difficulty=8):
        Player.__init__(self, is_ai, is_heads)
        self.difficulty = ai_difficulty

    def take_turn(self, display, game):
        my_coins = game.table.tails
        their_coins = game.table.heads
        if self.is_heads:
            my_coins = game.table.heads
            their_coins = game.table.tails

        my_coin, target = self.explore(game, my_coins, their_coins)

        display.selected_coin = my_coin
        display.cursorx = target.roundX()
        display.cursory = target.roundY()
        display.draw()

        time.sleep(3)

        game.shoot_coin(my_coin, target=target)
        display.selected_coin = None
        game.end_turn()

    def random_coins(self, mine, theirs):
        my_coin = random.sample(mine, 1)[0]
        target = random.sample(theirs, 1)[0]
        return my_coin, target

    def explore(self, game, my_coins, their_coins):
        class ExploredScore:
            def __init__(self, shooter, target, score):
                self.shooter_i = shooter
                self.target_i = target
                self.score = score

        scores = []
        for my_i, _ in enumerate(my_coins):
            for their_i, _ in enumerate(their_coins):
                simulation = game.get_simulation()

                if self.is_heads:
                    my_coin = simulation.simulation.table.heads[my_i]
                    their_coin = simulation.simulation.table.tails[their_i]
                else:
                    my_coin = simulation.simulation.table.tails[my_i]
                    their_coin = simulation.simulation.table.heads[their_i]

                simulation.simulation.shoot_coin(my_coin, target=their_coin)
                simulation.simulate()

                score = self.score(simulation)
                score = ExploredScore(my_i, their_i, score)
                scores.append(score)

        scores = sorted(scores, key=lambda score: score.score, reverse=True)

        # 9 is the "hardest" AI someone can select
        # the scores are sorted so the best is at the front
        # 9 (hard-coded) minus difficulty means the AI always picks the best
        # difficulty 0 means the AI will choose randomly among the top 9 choices
        max_worst = self.difficulty * 3
        if max_worst is 0:
            max_worst = 1
        choice = random.choice(scores[:max_worst])

        shooter = my_coins[choice.shooter_i]
        target = their_coins[choice.target_i]

        return shooter, target

    def score(self, simulation):
        table = simulation.simulation.table
        coins = table.coins
        score = 0
        for cc in coins:
            if table.off_board(cc):
                continue
            coin_value = 0
            if cc.__class__ is Coin:
                coin_value = 1
            elif cc.__class__ is Nickel:
                coin_value = 2
            elif cc.__class__ is Dollar:
                coin_value = 3
            elif cc.__class__ is Dime:
                coin_value = 5

            if cc.is_heads is self.is_heads:
                score += coin_value
            else:
                score -= coin_value
        return score
