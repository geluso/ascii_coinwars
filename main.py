from game import Game

import time
import curses
from curses import wrapper

USE_MY_WRAPPER = False

def loop(screen):
    game = Game()

    IS_ANIMATED = False
    JUST_FINISHED_ANIMATING = False
    SHOW_KEY_CHAR = False

    while True:
        screen.clear()
        IS_ANIMATED = game.table.tick()

        screen.addstr("                    COIN WARS" + "\n")
        screen.addstr("* N=nickel D=dime Q=quarter $=dollar coin\n")
        screen.addstr("* Nickels immobilize a coin for a turn.\n")
        screen.addstr("* Dimes convert coins between heads and tails.\n")
        screen.addstr("* Dollars and dimes can't be converted.\n")
        screen.addstr("* Take turns. Knock all other coins off to win.\n")
        screen.addstr(f"\n")

        coin_hud = f"Heads: {game.table.heads_str}   Tails: {game.table.tails_str}"
        if len(game.table.heads) == 0 and len(game.table.tails) == 0:
            coin_hud += "    MUTUAL DESTRUCTION!!"
        elif len(game.table.heads) == 0:
            coin_hud += "    TAILS wins!!"
        elif len(game.table.tails) == 0:
            coin_hud += "    HEADS wins!!"
        screen.addstr(coin_hud + "\n")

        if len(game.table.header) > 0:
          screen.addstr("Header: " + game.table.header + "\n")

        screen.addstr(str(game.table))
        screen.refresh()

        if IS_ANIMATED:
            continue

        char = screen.getkey()
        if SHOW_KEY_CHAR:
            screen.addstr(char)
            screen.refresh()
        if char is "\t":
          game.table.select_next_coin()
          coin = game.table.selected_coin
          if coin:
              game.table.path_x0 = coin.roundX()
              game.table.path_y0 = coin.roundY()
              game.table.path_x1 = game.table.cursorx
              game.table.path_y1 = game.table.cursory
        if char in "e\r\n":
          coin = game.table.selected_coin
          game.table.select_current_coin()
          if coin:
              if coin.is_immobilized:
                  screen.addstr("IMMOBILIZED\n")
                  screen.refresh()
                  continue
              game.table.clone_coins()

              dx = game.table.cursorx - coin.roundX()
              dy = game.table.cursory - coin.roundY()
              magnitude = (dx * dx + dy * dy) ** .5
              magnitude = round(magnitude)

              game.table.selected_coin.apply_force(dx, dy, magnitude)

              # after a coin successfully fires manually reset
              # all coins that were immobilized
              game.table.reset_immobilized()

              game.table.clear()
        if char in 'qx':
            import sys
            sys.exit()
        if char is 'c':
          game.table.clear()
        if char is 's':
          coin = game.table.highlight
          if coin:
            dx, dy, force = [int(n) for n in input("input (dx dy force): ").split(" ")]
            coin.apply_force(dx, dy, force)
        if char in "hjklKEY_LEFTKEY_RIGHTKEY_UPKEY_DOWN":
            if char in "hKEY_LEFT":
                game.table.cursorx -= 1
            if char in "jKEY_DOWN":
                game.table.cursory += 1
            if char in "kKEY_UP":
                game.table.cursory -= 1
            if char in "lKEY_RIGHT":
                game.table.cursorx += 1

            game.table.cancel_highlight()
        if char is 'c':
            game.table.clone_coins()
        if char is ' ':
          coin = game.table.selected_coin
          if coin:
            coin.apply_force(270, 8)
          
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
