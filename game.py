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

        t1 = Coin(x=10, y=10)
        t2 = Coin(x=20, y=10)
        t3 = Coin(x=30, y=10)
        t4 = Coin(x=40, y=10)

        h1 = Coin(x=10, y=30, is_heads=True)
        h2 = Coin(x=20, y=30, is_heads=True)
        h3 = Coin(x=30, y=30, is_heads=True)
        h4 = Coin(x=40, y=30, is_heads=True)

        self.coins = [t1, t2, t3, t4, h1, h2, h3, h4]
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

    def draw_path(self, p0, p1):
        pass


