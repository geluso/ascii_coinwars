import pymunk
from pymunk import Vec2d
from pymunk import pygame_util

import math
import random
from collections import defaultdict

class Coin:
    def __init__(self, is_heads=False, kind="q", x=0, y=0):
        self.is_heads = is_heads
        self.kind = kind
        self.x = x
        self.y = y
        self.ticks = 0

        mass = 1
        radius = 1
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))

        self.body = pymunk.Body(mass, inertia)
        self.body.position = self.x, self.y

        self.shape = pymunk.Circle(self.body, radius, (0,0))
        self.shape.elasticity = 0.95
        self.shape.friction = 0.68

    def tick(self):
        return
        self.ticks -= 1
        if self.ticks < 0:
            return
        self.x += self.dx
        self.y += self.dy

    def roundX(self):
        return round(self.body.position[0])
    def roundY(self):
        return round(self.body.position[1])

    def apply_force(self, dx, dy, magnitude):
        angle = Vec2d(dx, dy).angle
        dx, dy = self.point_on_circle(angle)
        dy = -dy

        magnitude *= 10
        self.body.apply_force_at_local_point(Vec2d.unit() * magnitude, (dx, dy))

        self.dx = dx
        self.dy = dy
        self.ticks = magnitude

    def point_on_circle(self, angle):
        from math import cos, sin, pi
        #center of circle, angle in degree and radius of circle
        center = [0,0]
        radius = 1
        x = center[0] + (radius * cos(angle))
        y = center[1] + (radius * sin(angle))

        return x,y

    def __str__(self):
        result = self.kind
        if (self.is_heads):
            result = result.upper()
        return result

    def __repr__(self):
        return f"{str(self)} ({self.x},{self.y})"

class Board:
    def __init__(self, rows=50, cols=50):
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

        cc = Coin(x=25, y=20, is_heads=True)

        t1 = Coin(x=10, y=10, is_heads=True)
        t2 = Coin(x=20, y=10, is_heads=True)
        t3 = Coin(x=30, y=10, is_heads=True)
        t4 = Coin(x=40, y=10, is_heads=True)

        h1 = Coin(x=10, y=30, is_heads=False)
        hh1 = Coin(x=19, y=29, is_heads=False)
        hhh1 = Coin(x=19, y=31, is_heads=False)
        h2 = Coin(x=20, y=30, is_heads=False)
        h3 = Coin(x=30, y=30, is_heads=False)
        h4 = Coin(x=40, y=30, is_heads=False)

        self.coins = [t1, t2, t3, t4, cc, h1, hh1, h2, hhh1, h3, h4]
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
      # is the line going left?
      if self.path_x1 < self.path_x0:
          self.path_x0, self.path_x1 = self.path_x1, self.path_x0
          self.path_y0, self.path_y1 = self.path_y1, self.path_y0

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
      minn = min(self.path_y0, self.path_y1)
      maxx = max(self.path_y0, self.path_y1)

      minn = round(minn)
      maxx = round(maxx)
      for yy in range(minn, maxx):
        self.cells[yy][self.path_x0] = "."

    def draw_horizontal_path(self):
      left = min(self.path_x0, self.path_x1)
      right = max(self.path_x0, self.path_x1)

      left = round(left)
      right = round(right)
      for xx in range(left, right):
        self.cells[self.path_y0][xx] = "."

    def draw_top_right_path(self):
      miny = min(self.path_y0, self.path_y1)
      maxy = max(self.path_y0, self.path_y1)
      left = min(self.path_x0, self.path_x1)
      right = max(self.path_x0, self.path_x1)
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

    def draw_bottom_right_path(self):
      miny = min(self.path_y0, self.path_y1)
      maxy = max(self.path_y0, self.path_y1)
      left = min(self.path_x0, self.path_x1)
      right = max(self.path_x0, self.path_x1)
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

    def tick(self):
        dt = 1.0/60
        self.space.step(dt)
        is_animated = False
        still_on_board = []
        for coin in self.coins:
            if (not coin.body.is_sleeping):
                is_animated = True
            if not (coin.roundX() < 0 or coin.roundY() < 0 or coin.roundX() > self.cols or coin.roundY() > self.rows):
                still_on_board.append(coin)

        self.coins = still_on_board
        return is_animated


