import pymunk
from pymunk import Vec2d
from pymunk import pygame_util

class Coin:
    def __init__(self, is_heads=False, kind="s", x=0, y=0):
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

class Board:
    def __init__(self, rows=50, cols=50):
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 0.0)

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

        for coin in self.coins:
            self.space.add(coin.body, coin.shape)

    def tick(self):
        dt = 1.0/60
        self.space.step(dt)
        is_animated = False
        for coin in self.coins:
            coin.tick()
            if (coin.ticks > 0):
                is_animated = True
        return is_animated

