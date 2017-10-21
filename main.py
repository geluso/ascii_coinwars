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
    while True:
        print(board)
        print("Commands: (tab) next coin  (x) exit")
        char = getchar()
        print(char)
        if char is 'x':
            import sys
            sys.exit()
        if char is '\t':
          print("next coin")
          board.select_next_coin()
        if char is '\n':
          print("select coin")
          board.select_current_coin()
        if char is '\r':
          print("select coin")
          board.select_current_coin()

board = Board()
print(board)

loop()
