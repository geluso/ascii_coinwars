import pymunk
from pymunk import Vec2d
from pymunk import pygame_util
from coin import *

import math
import random
from collections import defaultdict

class Table:
    def __init__(self, rows=50, cols=50):
        self.header = ""
        self.needs_clearing = False
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 0.0)
        self.space.damping = .9
        self.space.idle_speed_threshold = .1
        self.space.sleep_time_threshold = 1

        self.cells = defaultdict(lambda: defaultdict(lambda: " "))
        self.rows = rows
        self.cols = cols

        self.path_x0 = 0
        self.path_y0 = 0
        self.path_x1 = 0
        self.path_y1 = 0

        t1 = Coin(x=10, y=10, is_heads=True)
        t2 = Coin(x=20, y=10, is_heads=True)
        t3 = Coin(x=30, y=10, is_heads=True)
        t4 = Coin(x=40, y=10, is_heads=True)

        h1 = Coin(x=10, y=30, is_heads=False)
        h2 = Coin(x=20, y=30, is_heads=False)
        h3 = Coin(x=30, y=30, is_heads=False)
        h4 = Coin(x=40, y=30, is_heads=False)

        self.coins = [t1, t2, t3, t4, h1, h2, h3, h4]

        self.reformat_coin_hud()

        self.current_coin_index = 0
        self.set_highlight()

        self.selected_coin = None

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

    def set_coin_cells(self):
      for coin in self.coins:
          row = coin.roundY()
          col = coin.roundX()
          self.cells[row][col] = str(coin)

          if (coin is self.highlighted):
              self.cells[row][col - 1] = "("
              self.cells[row][col + 1] = ")"

          if (coin is self.selected_coin):
              self.cells[row][col - 1] = "["
              self.cells[row][col + 1] = "]"

    def draw_cursor(self):
        prev = self.cells[self.cursory][self.cursorx]
        if prev is " ":
          self.cells[self.cursory][self.cursorx] = "_"
        elif self.selected_coin and self.selected_coin.roundX() == self.cursorx and self.selected_coin.roundY() == self.cursory:
          self.cells[self.cursory][self.cursorx - 1] = "["
          self.cells[self.cursory][self.cursorx + 1] = "]"
        else:
          self.cells[self.cursory][self.cursorx - 1] = "("
          self.cells[self.cursory][self.cursorx + 1] = ")"

    def __str__(self):
        self.set_board_cells()
        self.draw_path()
        self.set_coin_cells()
        self.draw_cursor()

        result = ""
        for row in range(0, self.rows):
          for col in range(0, self.cols):
            result += self.cells[row][col]
          result += "\n"

        return result

    def set_highlight(self):
        self.highlighted = self.coins[self.current_coin_index]
        self.cursorx = self.highlighted.roundX()
        self.cursory = self.highlighted.roundY()

    def cancel_highlight(self):
        self.highlighted = None

    def select_next_coin(self):
        self.increment_current_count_index()
        if (self.get_current_count() is self.selected_coin):
            self.increment_current_count_index()
        self.set_highlight()

    def increment_current_count_index(self):
        self.current_coin_index = (self.current_coin_index + 1) % len(self.coins)

    def get_current_count(self):
        return self.coins[self.current_coin_index]

    def select_current_coin(self):
        if self.highlighted:
          self.selected_coin = self.coins[self.current_coin_index]
        else:
          for coin in self.coins:
            if coin.roundX() == self.cursorx and coin.roundY() == self.cursory:
              self.selected_coin = coin

    def reset_selections(self):
        self.selected_coin = None
        self.current_coin_index = 0
        self.set_highlight()

    def clear(self):
      self.selected_coin = None
      self.highlighted = None
      self.current_coin_index = -1
      self.clear_path()

    def clear_path(self):
      self.path_x0 = -1
      self.path_y0 = -1
      self.path_x1 = -1
      self.path_y1 = -1

    def draw_path(self):
        if not (self.selected_coin and self.cursorx > 0 and self.cursory > 0):
            return
        # is the line going left?
        x0, y0 = self.selected_coin.roundX(), self.selected_coin.roundY()
        x1, y1 = self.cursorx, self.cursory
        if x1 < x0:
          x0, y0 = self.cursorx, self.cursory
          x1, y1 = self.selected_coin.roundX(), self.selected_coin.roundY()

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

    def clone_coins(self):
        # reset all of the coins to prevent wonky physics
        clones = []
        for coin in self.coins:
            if not coin.is_dirty():
                continue
            clone = Coin(coin.is_heads, coin.kind, coin.body.position.x, coin.body.position.y)
            if self.highlighted is coin:
                self.highlighted = clone
            if self.selected_coin is coin:
                self.selected_coin = clone
            self.space.remove(coin.body)
            self.space.remove(coin.shape)
            self.space.add(clone.body, clone.shape)
            clones.append(clone)
        self.coins = clones



