from game import *
import curses
from curses import wrapper

def loop(screen):
    last_dx, last_dy, last_force = None, None, None

    while True:
        screen.clear()
        screen.addstr(str(board))
        screen.addstr("Commands: (tab) next coin (p) set path (c) clear (qx) exit\n")
        screen.addstr("Commands: (s) shoot (.) repeat shot\n")
        char = screen.getkey()
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
        if char is 'p':
          x0, y0, x1, y1 = [int(n) for n in input("Enter coords: ").split()]
          board.set_path(x0, y0, x1, y1)
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
        if char in "hjkl":
            if char is "h":
                board.cursorx -= 1
            if char is "j":
                board.cursory += 1
            if char is "k":
                board.cursory -= 1
            if char is "l":
                board.cursorx += 1

            board.cancel_highlight()

            if board.selected_coin is not None:
              c1 = board.selected_coin
              board.set_path(c1.x, c1.y, board.cursorx, board.cursory)
        if char is ' ':
          coin = board.selected_coin
          if coin:
            coin.apply_force(270, 8)
          

board = Board()

def main(stdscr):
    # Clear screen
    stdscr.clear()

    stdscr.addstr("hello!")

    stdscr.refresh()
    key = stdscr.getkey()

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
