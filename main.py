from game import *
import time
import curses
from curses import wrapper

def loop(screen):
    board = Board()
    last_dx, last_dy, last_force = None, None, None

    IS_ANIMATED = False
    JUST_FINISHED_ANIMATING = False
    SHOW_KEY_CHAR = False

    while True:
        screen.clear()
        IS_ANIMATED = board.tick()

        heads = board.get_heads()
        heads_str = "".join([str(coin) for coin in heads])
        tails = board.get_tails()
        tails_str = "".join([str(coin) for coin in tails])

        header = f"Heads: {heads_str}  Tails: {tails_str}"
        if board.selected_coin is not None:
            coin = board.selected_coin
            header += f" {coin.roundX()},{coin.roundY()}"
        if board.path_x1 and board.path_y1:
            coin = board.selected_coin
            header += f" {board.path_x1},{board.path_y1}"
        header += "\n"

        screen.addstr(header)
        screen.addstr(str(board))
        screen.addstr("Commands: (tab) next coin (p) set path (c) clear (qx) exit\n")
        screen.addstr("Commands: (s) shoot (.) repeat shot\n")
        screen.addstr(str([f"{coin.body.velocity.length}" for coin in board.coins]))
        screen.addstr("\n")
        screen.addstr(str([f"{coin.body.is_sleeping}" for coin in board.coins]))
        screen.addstr("\n")
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
        if char in "\r\n":
          coin = board.selected_coin
          board.select_current_coin()
          if coin:
              dx = board.cursorx - coin.x
              dy = board.cursory - coin.y
              magnitude = (dx * dx + dy * dy) ** .5
              magnitude = round(magnitude)

              last_coin = coin
              last_dx, last_dy, last_force = dx, dy, magnitude
              board.selected_coin.apply_force(dx, dy, magnitude)
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
            last_dx, last_dy, last_force = dx, dy, force
            last_coin = coin
            coin.apply_force(dx, dy, force)
        if char is '.':
          last_coin.apply_force(last_dx, last_dy, last_force)
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
        if char is ' ':
          coin = board.selected_coin
          if coin:
            coin.apply_force(270, 8)
          
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
