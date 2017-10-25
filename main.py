from table import *
from coin import *
from my_wrapper import *

import time
import curses
from curses import wrapper

USE_MY_WRAPPER = False

def loop(screen):
    board = Table()

    IS_ANIMATED = False
    JUST_FINISHED_ANIMATING = False
    SHOW_KEY_CHAR = False

    while True:
        screen.clear()
        IS_ANIMATED = board.tick()

        screen.addstr("                    COIN WARS" + "\n")
        screen.addstr("* N=nickel D=dime Q=quarter $=dollar coin\n")
        screen.addstr("* Nickels immobilize a coin for a turn.\n")
        screen.addstr("* Dimes convert coins between heads and tails.\n")
        screen.addstr("* Dollars and dimes can't be converted.\n")
        screen.addstr("* Take turns. Knock all other coins off to win.\n")
        screen.addstr(f"\n")

        coin_hud = f"Heads: {board.heads_str}   Tails: {board.tails_str}"
        if len(board.heads) == 0 and len(board.tails) == 0:
            coin_hud += "    MUTUAL DESTRUCTION!!"
        elif len(board.heads) == 0:
            coin_hud += "    TAILS wins!!"
        elif len(board.tails) == 0:
            coin_hud += "    HEADS wins!!"
        screen.addstr(coin_hud + "\n")

        if len(board.header) > 0:
          screen.addstr("Header: " + board.header + "\n")

        screen.addstr(str(board))
        screen.refresh()

        if IS_ANIMATED:
            continue

        char = screen.getkey()
        if SHOW_KEY_CHAR:
            screen.addstr(char)
            screen.refresh()
        if char is "\t":
          board.select_next_coin()
          coin = board.selected_coin
          if coin:
              board.path_x0 = coin.roundX()
              board.path_y0 = coin.roundY()
              board.path_x1 = board.cursorx
              board.path_y1 = board.cursory
        if char in "e\r\n":
          coin = board.selected_coin
          board.select_current_coin()
          if coin:
              if coin.is_immobilized:
                  screen.addstr("IMMOBILIZED\n")
                  screen.refresh()
                  continue
              board.clone_coins()

              dx = board.cursorx - coin.roundX()
              dy = board.cursory - coin.roundY()
              magnitude = (dx * dx + dy * dy) ** .5
              magnitude = round(magnitude)


              board.selected_coin.apply_force(dx, dy, magnitude)

              # after a coin successfully fires manually reset
              # all coins that were immobilized
              board.reset_immobilized()

              board.clear()
        if char in 'qx':
            import sys
            sys.exit()
        if char is 'c':
          board.clear()
        if char is 's':
          coin = board.highlight
          if coin:
            dx, dy, force = [int(n) for n in input("input (dx dy force): ").split(" ")]
            coin.apply_force(dx, dy, force)
        if char in "hjklKEY_LEFTKEY_RIGHTKEY_UPKEY_DOWN":
            if char in "hKEY_LEFT":
                board.cursorx -= 1
            if char in "jKEY_DOWN":
                board.cursory += 1
            if char in "kKEY_UP":
                board.cursory -= 1
            if char in "lKEY_RIGHT":
                board.cursorx += 1

            board.cancel_highlight()
        if char is 'c':
            board.clone_coins()
        if char is ' ':
          coin = board.selected_coin
          if coin:
            coin.apply_force(270, 8)
          
if USE_MY_WRAPPER:
    my_wrapper(loop)
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
