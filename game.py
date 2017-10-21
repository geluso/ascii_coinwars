import math
import random
from collections import defaultdict

class Coin:
    def __init__(self, is_heads=False, kind="s", x=0, y=0):
        self.is_heads = is_heads
        self.kind = kind
        self.x = x
        self.y = y

    def __str__(self):
        result = self.kind
        if (self.is_heads):
            result = result.upper()
        return result

    def __repr__(self):
        return f"{str(self)} ({self.x},{self.y})"

class Board:
    def __init__(self, rows=50, cols=50):
        self.cells = defaultdict(lambda: defaultdict(lambda: " "))
        self.rows = rows
        self.cols = cols

        self.path_x0 = 0
        self.path_y0 = 0
        self.path_x1 = 0
        self.path_y1 = 0

        cc = Coin(x=25, y=20)

        t1 = Coin(x=10, y=10)
        t2 = Coin(x=20, y=10)
        t3 = Coin(x=30, y=10)
        t4 = Coin(x=40, y=10)

        h1 = Coin(x=10, y=30, is_heads=True)
        hh1 = Coin(x=19, y=29, is_heads=True)
        hhh1 = Coin(x=19, y=31, is_heads=True)
        h2 = Coin(x=20, y=30, is_heads=True)
        h3 = Coin(x=30, y=30, is_heads=True)
        h4 = Coin(x=40, y=30, is_heads=True)

        self.coins = [t1, t2, t3, t4, cc, h1, hh1, h2, hhh1, h3, h4]
        self.current_coin_index = 0
        self.highlighted = self.coins[0]

        self.selected_coin = None

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
          row = coin.y
          col = coin.x
          self.cells[row][col] = str(coin)

          if (coin is self.highlighted):
              self.cells[row][col - 1] = "("
              self.cells[row][col + 1] = ")"

          if (coin is self.selected_coin):
              self.cells[row][col - 1] = "["
              self.cells[row][col + 1] = "]"

    def __str__(self):
        self.set_board_cells()
        self.draw_path()
        self.set_coin_cells()

        result = ""
        for row in range(0, self.rows):
          for col in range(0, self.cols):
            result += self.cells[row][col]
          result += "\n"

        return result

    def select_next_coin(self):
        self.increment_current_count_index()
        if (self.get_current_count() is self.selected_coin):
            self.increment_current_count_index()
        self.highlighted = self.coins[self.current_coin_index]

    def increment_current_count_index(self):
        self.current_coin_index = (self.current_coin_index + 1) % len(self.coins)

    def get_current_count(self):
        return self.coins[self.current_coin_index]

    def select_current_coin(self):
        self.selected_coin = self.coins[self.current_coin_index]

    def reset_selections(self):
        self.selected_coin = None
        self.current_coin_index = 0
        self.highlighted = self.coins[self.current_coin_index]

    def set_path(self, x0, y0, x1, y1):
      self.path_x0 = x0
      self.path_y0 = y0
      self.path_x1 = x1
      self.path_y1 = y1
      if x1 < x0:
        self.path_x0 = x1
        self.path_y0 = y1
        self.path_x1 = x0
        self.path_y1 = y0

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
      dy = self.path_y1 - self.path_y0
      dx = self.path_x1 - self.path_x0

      if dx is 0:
        self.draw_vertical_path()
      elif dy is 0:
        self.draw_horizontal_path()
      elif dy < 0 and dx > 0:
        self.draw_top_right_path()
      elif dy > 0 and dx > 0:
        self.draw_bottom_right_path()

    def draw_vertical_path(self):
      print("vert")
      minn = min(self.path_y0, self.path_y1)
      maxx = max(self.path_y0, self.path_y1)
      for yy in range(minn, maxx):
        self.cells[yy][self.path_x0] = "."

    def draw_horizontal_path(self):
      print("horz")
      left = min(self.path_x0, self.path_x1)
      right = max(self.path_x0, self.path_x1)
      for xx in range(left, right):
        self.cells[self.path_y0][xx] = "."

    def draw_top_right_path(self):
      print("top right path")
      miny = min(self.path_y0, self.path_y1)
      maxy = max(self.path_y0, self.path_y1)
      left = min(self.path_x0, self.path_x1)
      right = max(self.path_x0, self.path_x1)
      fslope = (maxy - miny) / (left - right)
      slope = (maxy - miny) // (left - right)

      current_y = maxy
      for xx in range(left, right + 1):

        xprogress = (xx - left) / (right - left)
        y_spread = maxy - miny
        yy_coord = maxy - xprogress * y_spread

        while current_y > yy_coord:
            self.cells[current_y][xx] = "."
            current_y -= 1

    def draw_bottom_right_path(self):
      print("bot right path")

    def old_draw_path(self):
      row = self.path_y0
      col = self.path_x0

      dy = self.path_y1 - self.path_y0
      dx = self.path_x1 - self.path_x0

      if dx is 0:
        slope = math.inf
      else:
        slope = int(math.ceil(dy / dx))

      print("slope:", slope)

      offx = 1
      if self.path_x1 < self.path_x0:
        offx = -1

      offy = 1
      if self.path_y1 < self.path_y0:
        offy = -1

      print("coll:", self.path_x0, self.path_x1 + offx)
      for coll in range(self.path_x0, self.path_x1 + offx):
        if slope is math.inf:
          print("row1:", self.path_y0, self.path_y1)
          for roww in range(self.path_y0, self.path_y1, offy):
            print(roww, coll)
            self.cells[roww][coll] = "."
        else:
          print("sloppy", slope, offy)
          for roww in range(0, slope + 1, offy):
            coldiff = coll - self.path_x0
            yy = roww + self.path_y0 + slope * coldiff
            print("row2:", yy, coll)
            self.cells[yy][coll] = "."


