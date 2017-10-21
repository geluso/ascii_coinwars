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
        char = getchar()
        print(char)
        if char is 'x':
            import sys
            sys.exit()
        if char is '\t':
          print("next coin")
          board.select_next_coin()
        if char is '\r':
          print("select coin")
          if board.selected_coin is not None:
              c1 = board.selected_coin
              c2 = board.highlighted
              print("set path:", c1, c2)
              print(c1.x, c1.y, c2.x, c2.y)
              board.set_path(c1.x, c1.y, c2.x, c2.y)
          board.select_current_coin()
        if char is 'p':
          x0, y0, x1, y1 = [int(n) for n in input("Enter coords: ").split()]
          board.set_path(x0, y0, x1, y1)
        if char is 'c':
          board.clear()
        if char is 'f':
          coin = board.highlighted
          if coin:
              dx, dy, force = [int(n) for n in input("input (dx dy force): ").split(" ")]
              last_dx, last_dy, last_force = dx, dy, force
              coin.apply_force(dx, dy, force)
        if char is '.':
              coin.apply_force(last_dx, last_dy, last_force)
        if char is ' ':
          coin = board.selected_coin
          if coin:
            coin.apply_force(270, 8)
          

board = Board()
print(board)

loop()
