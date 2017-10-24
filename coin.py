import pymunk
from pymunk import Vec2d
from pymunk import pygame_util

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

    def apply_force(self, dx, dy, magnitude):
        self.body.velocity = Vec2d(dx, dy) / 10 * 2
        return
        angle = Vec2d(dx, dy).angle
        dx, dy = self.point_on_circle(angle)
        dy = -dy

        magnitude *= 10 * 2
        dx += self.x
        dy += self.y
        #self.body.apply_force_at_world_point(Vec2d.unit() * magnitude, (dx, dy))


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
 
