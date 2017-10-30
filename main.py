from game import Game
from display import Display

import time
import curses
from curses import wrapper

def loop(screen):
    game = Game()
    display = Display(screen, game)

    is_animated = False
    while True:
        is_animated = game.table.tick()

        msg = ",".join([str(coin.is_shooting) for coin in game.table.coins])
        game.table.header = msg
        display.draw()

        if is_animated:
            continue

        player = game.get_current_player()
        player.take_turn(display, game)
          
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
