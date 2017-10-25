from game import Game
from display import Display

import time
import curses
from curses import wrapper

USE_MY_WRAPPER = False

def loop(screen):
    game = Game()
    display = Display(screen, game)

    IS_ANIMATED = False
    SHOW_KEY_CHAR = False

    while True:
        IS_ANIMATED = game.table.tick()

        display.draw()

        if IS_ANIMATED:
            continue

        char = screen.getkey()
        if SHOW_KEY_CHAR:
            screen.addstr(char)
            screen.refresh()
        if char is "\t":
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
