import pymunk
from pymunk import Vec2d
from pymunk import pygame_util

COIN_COLLISION = 1
# penny         nickel  dime    quarter half dollar     dollar
# 2.500 g	5.000 g	2.268 g	5.670 g	11.340 g	8.1 g
# 0.750 in.  19.05 mm penny
# 0.835 in.  21.21 mm nickel
# 0.705 in.  17.91 mm dime
# 0.955 in.  24.26 mm quarter
# 1.205 in.  30.61 mm half dollar
# 1.043 in.  26.49 mm dollar

class Coin:
    def __init__(self, game=None, is_heads=False, kind="q", x=0, y=0):
        self.game = game
        self.is_heads = is_heads
        self.kind = kind
        self.x = x
        self.y = y
        self.ticks = 0

        self.is_shooting = False
        self.is_immobilized = False
        self.is_recently_immobilized = False
        self.remind_cant_select = False
        self.is_recently_converted = False
        self.is_recently_resisted_conversion = False
        self.can_convert = True

        self.mass = 1
        self.radius = 1
        self.create_body_shape()

    def create_body_shape(self):
        inertia = pymunk.moment_for_circle(self.mass, 0, self.radius, (0,0))
        self.body = pymunk.Body(self.mass, inertia)
        self.body.position = self.x, self.y

        self.shape = pymunk.Circle(self.body, self.radius, (0,0))
        self.shape.elasticity = .99
        self.shape.friction = 0.68
        self.shape.collision_type = 1

        self.shape.coin = self
        self.body.coin = self

    def collide(self, other):
        pass

    def is_last_on_team(self):
        if self.game is None:
            return False
        coins_on_team = self.game.table.tails
        if self.is_heads:
            coins_on_team = self.game.table.heads
        return len(coins_on_team) == 1

    def clone(self):
        coin = Coin(self.is_heads, self.kind, self.body.position.x, self.body.position.y)
        coin.is_immobilized = self.is_immobilized
        return coin

    def is_dirty(self):
        return True

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

    def shoot_at(self, x, y):
        if self.is_immobilized:
            return False
        dx = x - self.roundX()
        dy = y - self.roundY()
        magnitude = (dx * dx + dy * dy) ** .5
        magnitude = round(magnitude)

        return self.apply_force(dx, dy, magnitude)

    def apply_force(self, dx, dy, magnitude):
        if self.is_immobilized:
            return False

        self.is_shooting = True
        self.body.velocity = Vec2d(dx, dy) / 10 * 2
        return True

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
 
