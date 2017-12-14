import pymunk
from pymunk import Vec2d
from pymunk import pygame_util
from coin import Coin
from dime import Dime
from nickel import Nickel
from dollar import Dollar

import copy
import math
import random
from collections import defaultdict

class Table:
    def __init__(self, rows=40, cols=50, game=None):
        self.ticks = 0
        self.header = ""
        self.needs_clearing = False
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 0.0)
        self.space.damping = .9
        self.space.idle_speed_threshold = .1
        self.space.sleep_time_threshold = 1
        self.show_turn_message = False

        def collide(arbiter, space, data):
            shape1, shape2 = arbiter.shapes
            coin1, coin2 = shape1.coin, shape2.coin
            coin1.collide(coin2)
            coin2.collide(coin1)

        collision_handler = self.space.add_collision_handler(1, 1)
        collision_handler.post_solve = collide

        self.cells = defaultdict(lambda: defaultdict(lambda: " "))
        self.rows = rows
        self.cols = cols

        self.coins = []

        self.coins.append(Coin(x=10, y=10, is_heads=True, game=game))
        self.coins.append(Coin(x=20, y=10, is_heads=True, game=game))
        self.coins.append(Coin(x=30, y=10, is_heads=True, game=game))
        self.coins.append(Coin(x=40, y=10, is_heads=True, game=game))
        self.coins.append(Dime(x=15, y=14, is_heads=True, game=game))
        self.coins.append(Dollar(x=25, y=14, is_heads=True, game=game))
        self.coins.append(Nickel(x=35, y=14, is_heads=True, game=game))

        self.coins.append(Coin(x=10, y=30, is_heads=False, game=game))
        self.coins.append(Coin(x=20, y=30, is_heads=False, game=game))
        self.coins.append(Coin(x=30, y=30, is_heads=False, game=game))
        self.coins.append(Coin(x=40, y=30, is_heads=False, game=game))
        self.coins.append(Dime(x=15, y=26, is_heads=False, game=game))
        self.coins.append(Dollar(x=25, y=26, is_heads=False, game=game))
        self.coins.append(Nickel(x=35, y=26, is_heads=False, game=game))

        self.reformat_coin_hud()

        for coin in self.coins:
            self.space.add(coin.body, coin.shape)

    def get_heads(self):
        return [coin for coin in self.coins if coin.is_heads]

    def get_tails(self):
        return [coin for coin in self.coins if not coin.is_heads]

    def set_board_cells(self):
        result = ""
        for col in range(self.cols):
          self.cells[0][col] = "="
          self.cells[self.rows - 1][col] = "="

        for row in range(self.rows):
            self.cells[row][0] = "|"
            self.cells[row][self.cols - 1] = "|"

        for row in range(1, self.rows - 1):
          for col in range(1, self.cols - 1):
            self.cells[row][col] = " "

    def set_coin_cells(self, selected, cx, cy):
        if self.show_turn_message:
            x = self.cols / 2
            x -= len(self.show_turn_message) / 2
            y = self.rows / 2

            x = round(x)
            y = round(y)
            self.label_xy(x, y, self.show_turn_message)

        for coin in self.coins:
            row = coin.roundY()
            col = coin.roundX()
            self.cells[row][col] = str(coin)

            if coin.roundX() == cx and coin.roundY() == cy:
              self.cells[row][col - 1] = "("
              self.cells[row][col + 1] = ")"
              # remind the player they can't select an immobilized coin
              if coin.is_immobilized:
                self.label(coin, "IMMOBILIZED!")
                if coin.remind_cant_select:
                    self.label(coin, "CANT SELECT", yoff=1)

            if (coin is selected):
              self.cells[row][col - 1] = "["
              self.cells[row][col + 1] = "]"

            if coin.is_recently_immobilized:
                self.label(coin, "IMMOBILIZED!", xoff=3)

            if coin.is_recently_converted:
                self.label(coin, "CONVERTED!", xoff=3)

            if coin.is_recently_resisted_conversion:
                self.label(coin, "CANT CONVERT!", xoff=3)

    def label(self, coin, msg, xoff=0, yoff=0):
        x = coin.roundX() + xoff
        y = coin.roundY() + yoff
        self.label_xy(x, y, msg)

    def label_xy(self, x, y, msg, xoff=0, yoff=0):
        # if the message would run into the right wall
        if (xoff + x + len(msg)) > self.cols:
            xoff = -2 - len(msg)

        for i in range(len(msg)):
            self.cells[y][x + xoff + i] = msg[i]

    def draw_cursor(self, selected, cx, cy):
        prev = self.cells[cy][cx]
        if prev is " ":
          self.cells[cy][cx] = "_"
        elif selected and selected.roundX() == cx and selected.roundY() == cy:
          self.cells[cy][cx - 1] = "["
          self.cells[cy][cx + 1] = "]"
        else:
          self.cells[cy][cx - 1] = "("
          self.cells[cy][cx + 1] = ")"

    def __str__(self):
        return self.draw()

    def draw(self, cx=0, cy=0, selected=None):
        self.set_board_cells()
        if selected:
            self.draw_path(selected, cx, cy)
        self.set_coin_cells(selected, cx, cy)
        # set coin cells and draw cursor are veery similar
        self.draw_cursor(selected, cx, cy)

        result = ""
        for row in range(0, self.rows):
          for col in range(0, self.cols):
            result += self.cells[row][col]
          result += "\n"
        return result

    def get_coin(self, x, y):
        for coin in self.coins:
            # exact match
            if coin.roundX() == x and coin.roundY() == y:
                return coin
        return None

    def draw_path(self, selected, cx, cy):
        if selected is None:
            return
        if cx < 0 or cy < 0:
            return

        # is the line going left?
        x0, y0 = selected.roundX(), selected.roundY()
        x1, y1 = cx, cy
        if x1 < x0:
          # swap the two points
          x0, y0, x1, y1 = x1, y1, x0, y0

        dy = y1 - y0
        dx = x1 - x0

        if dx is 0:
          self.draw_vertical_path(x0, y0, x1, y1)
        elif dy is 0:
          self.draw_horizontal_path(x0, y0, x1, y1)
        elif dy < 0 and dx > 0:
          self.draw_top_right_path(x0, y0, x1, y1)
        elif dy > 0 and dx > 0:
          self.draw_bottom_right_path(x0, y0, x1, y1)

    def draw_vertical_path(self, x0, y0, x1, y1):
      minn = min(y0, y1)
      maxx = max(y0, y1)

      minn = round(minn)
      maxx = round(maxx)
      for yy in range(minn, maxx):
        self.cells[yy][x0] = "."

    def draw_horizontal_path(self, x0, y0, x1, y1):
      left = min(x0, x1)
      right = max(x0, x1)

      left = round(left)
      right = round(right)
      for xx in range(left, right):
        self.cells[y0][xx] = "."

    def draw_top_right_path(self, x0, y0, x1, y1):
      miny = min(y0, y1)
      maxy = max(y0, y1)
      left = min(x0, x1)
      right = max(x0, x1)
      fslope = (maxy - miny) / (left - right)
      slope = (maxy - miny) // (left - right)

      current_y = maxy
      left = round(left)
      right = round(right)
      for xx in range(left, right + 1):

        xprogress = (xx - left) / (right - left)
        y_spread = maxy - miny
        yy_coord = maxy - xprogress * y_spread

        self.cells[current_y][xx] = "."
        while current_y > yy_coord:
            self.cells[current_y][xx] = "."
            current_y -= 1

    def draw_bottom_right_path(self, x0, y0, x1, y1):
      miny = min(y0, y1)
      maxy = max(y0, y1)
      left = min(x0, x1)
      right = max(x0, x1)
      fslope = (maxy - miny) / (left - right)
      slope = (maxy - miny) // (left - right)

      path = []
      current_y = miny
      left = round(left)
      right = round(right)
      for xx in range(left, right + 1):
        xprogress = (xx - left) / (right - left)
        y_spread = maxy - miny
        yy_coord = miny + xprogress * y_spread

        self.cells[current_y][xx] = "."
        while current_y < yy_coord:
            self.cells[current_y][xx] = "."
            current_y += 1

    def off_board(self, coin):
        if coin.roundX() < 0:
            return True
        if coin.roundY() < 0:
            return True
        if coin.roundX() > self.cols:
            return True
        if coin.roundY() > self.rows:
            return True
        return False

    def tick(self):
        self.ticks += 1

        dt = 1.0/60
        self.space.step(dt)
        is_animated = False
        still_on_board = []
        for coin in self.coins:
            if (not coin.body.is_sleeping):
                is_animated = True
            if not self.off_board(coin):
                still_on_board.append(coin)

        self.reformat_coin_hud()

        self.coins = still_on_board
        return is_animated

    def display_coin_coords(self):
        self.header = ""
        for coin in self.coins:
            self.header += f"{coin.x},{coin.y} "

    def reformat_coin_hud(self):
        self.heads = [coin for coin in self.coins if coin.is_heads]
        self.tails = [coin for coin in self.coins if not coin.is_heads]

        self.heads_str = "".join([str(coin) for coin in self.heads])
        self.tails_str = "".join([str(coin) for coin in self.tails])

    def reset_immobilized(self):
        for coin in self.coins:
            coin.is_immobilized = False

    def clone_coins(self):
        # reset all of the coins to prevent wonky physics
        clones = []
        for coin in self.coins:
            if not coin.is_dirty():
                continue
            clone = coin.clone()
            self.space.remove(coin.body)
            self.space.remove(coin.shape)
            self.space.add(clone.body, clone.shape)
            clones.append(clone)
        self.coins = clones

    def clone(self):
        return copy.deepcopy(self)
