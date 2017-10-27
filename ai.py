import random
import time
import player

class AIPlayer(player.Player):
    def __init__(self, is_ai=True, is_heads=False):
        player.Player.__init__(self, is_ai, is_heads)

    def take_turn(self, display, game):
        time.sleep(1)

        my_coins = game.table.tails
        their_coins = game.table.heads
        if self.is_heads:
            my_coins = game.table.heads
            their_coins = game.table.tails

        my_coin = random.sample(my_coins, 1)[0]
        target = random.sample(their_coins, 1)[0]

        display.selected_coin = my_coin
        display.cursorx = target.roundX()
        display.cursory = target.roundY()
        display.draw()

        time.sleep(3)

        game.shoot_coin(my_coin, target.roundX(), target.roundY())
        display.selected_coin = None