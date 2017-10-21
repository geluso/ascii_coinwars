from game import *

def getchar():
  #Returns a single character from standard input
  import tty, termios, sys
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ch

def loop():
    last_dx, last_dy, last_force = None, None, None

    while True:
        print(board)
        print("Commands: (tab) next coin (p) set path (c) clear (x) exit")
        print("Commands: (s) shoot (.) repeat shot")
        char = getchar()
        print(char)
        if char is 'x':
            import sys
            sys.exit()
        if char is '\t':
          board.select_next_coin()
        if char is '\r':
          board.select_current_coin()
          coin = board.selected_coin
          if coin:
              dx = board.cursorx - coin.x
              dy = board.cursory - coin.y
              magnitude = (dx * dx + dy * dy) ** .5
              magnitude = round(magnitude)

              last_coin = coin
              last_dx, last_dy, last_force = dx, dy, magnitude
              board.selected_coin.apply_force(dx, dy, magnitude)
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
print(board)

loop()
