import math
import random
import time
import player

import coin
import penny
import nickel
import dime
import dollar

class AIPlayer(player.Player):
    def __init__(self, is_ai=True, is_heads=False):
        player.Player.__init__(self, is_ai, is_heads)

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
        best_shooter = None
        best_target = None
        best_score = -math.inf

        scores = []
        for my_coin in my_coins:
            for their_coin in their_coins:
                simulation = game.get_simulation()
                simulation.simulation.shoot_coin(my_coin, target=their_coin)
                simulation.simulate()

                score = self.score(simulation)
                scores.append(score)

                if score > best_score:
                    best_score = score
                    best_shooter = my_coin
                    best_target = their_coin

        game.table.header = str(scores)
        return best_shooter, best_target

    def score(self, simulation):
        table = simulation.simulation.table
        coins = table.coins
        score = 0
        for cc in coins:
            if table.off_board(cc):
                continue
            coin_value = 0
            if cc.__class__ is coin.Coin:
                coin_value = 1
            elif cc.__class__ is nickel.Nickel:
                coin_value = 2
            elif cc.__class__ is dollar.Dollar:
                coin_value = 3
            elif cc.__class__ is dime.Dime:
                coin_value = 5

            if cc.is_heads is self.is_heads:
                score += coin_value
            else:
                score -= coin_value
        return score
