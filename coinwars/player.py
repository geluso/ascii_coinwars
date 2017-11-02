import random

class Player:
    def __init__(self, is_ai=False, is_heads=False):
        self.is_ai = is_ai
        self.is_heads = is_heads

    def take_turn(self, game):
        pass

    def take_human_turn(self):
        char = screen.getkey()
        if char is "t\t":
            display.target_next_coin()
        if char in "e\r\n":
            display.select_or_shoot_coin()
        if char in 'qx':
            display.quit()
        if char is 'c':
            display.clear()
        if char in "hjklKEY_LEFTKEY_RIGHTKEY_UPKEY_DOWN":
            if char in "hKEY_LEFT":
                display.move_cursor_left()
            if char in "jKEY_DOWN":
                display.move_cursor_down()
            if char in "kKEY_UP":
                display.move_cursor_up()
            if char in "lKEY_RIGHT":
                display.move_cursor_right()

    def take_ai_turn(self):
        my_coins = game.table.tails
        their_coins = game.table.heads
        if self.is_heads:
            my_coins = game.table.heads
            their_coins = game.table.tails

        my_coin = random.sample(my_coins, 1)[0]
        target = random.sample(their_coins, 1)[0]

        game.shoot_coin(my_coin, target.roundX(), target.roundY())
