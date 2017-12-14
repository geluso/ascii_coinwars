from player import Player

class HumanPlayer(Player):
    def __init__(self, is_ai=False, is_heads=False):
        Player.__init__(self, is_ai, is_heads)

    def take_turn(self, display, game):
        char = display.screen.getkey()
        if char in "t\t":
            display.target_next_coin()
        if char in "e\r\n":
            result = display.select_or_shoot_coin()
            if result is "shot":
                game.end_turn()
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
