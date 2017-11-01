from game import Game
from display import Display
from config import Configuration
from welcome import WelcomeScreen

import time
import curses
from curses import wrapper

def loop(screen):
    while True:
        welcome = WelcomeScreen(screen)
        welcome.display_title_screen()

        config = Configuration()
        if not config.is_configured:
          config.prompt_configuration(screen)

        game = Game(config.players)
        display = Display(screen, game)

        is_animated = False
        back_to_menu = False
        while not back_to_menu:
            is_animated = game.table.tick()

            msg = ",".join([str(coin.is_shooting) for coin in game.table.coins])
            game.table.header = msg
            display.draw()

            if is_animated:
                continue

            if not game.is_game_over():
                player = game.get_current_player()
                player.take_turn(display, game)

                key = screen.getkey()
                if key is "n" or key is "m":
                    back_to_menu = True
                elif key is "x":
                    import sys
                    sys.exit()
          
USE_MY_WRAPPER = False
if USE_MY_WRAPPER:
    import my_wrapper
    my_wrapper.my_wrapper(loop)
else:
    try:
      stdscr = curses.initscr()
      curses.cbreak()
      curses.noecho()
      stdscr.keypad(1)

      wrapper(loop)
    except KeyboardInterrupt:
      pass
    finally:
      curses.nocbreak()
      stdscr.keypad(0)
      curses.echo()
      curses.endwin()
