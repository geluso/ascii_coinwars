from .coin import Coin

# penny         nickel  dime    quarter half dollar     dollar
# 2.500 g	5.000 g	2.268 g	5.670 g	11.340 g	8.1 g
# 0.750 in.  19.05 mm penny
# 0.835 in.  21.21 mm nickel
# 0.705 in.  17.91 mm dime
# 0.955 in.  24.26 mm quarter
# 1.205 in.  30.61 mm half dollar
# 1.043 in.  26.49 mm dollar

class Dollar(Coin):
    def __init__(self, game=None, is_heads=False, kind="$", x=0, y=0):
        Coin.__init__(self, game, is_heads, kind, x, y)
        self.body.coin = self
        self.shape.coin = self
        self.can_convert = False

        self.mass = 8.1 / 5.67
        self.radius = 26.49 / 24.26
        self.create_body_shape()

    def clone(self):
        dollar = Dollar(self.is_heads, self.kind, self.body.position.x, self.body.position.y)
        dollar.is_immobilized = self.is_immobilized
        return dollar

    def collide(self, other):
        if not self.is_shooting:
            return
