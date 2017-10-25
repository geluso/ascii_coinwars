import coin

# penny         nickel  dime    quarter half dollar     dollar
# 2.500 g	5.000 g	2.268 g	5.670 g	11.340 g	8.1 g
# 0.750 in.  19.05 mm penny
# 0.835 in.  21.21 mm nickel
# 0.705 in.  17.91 mm dime
# 0.955 in.  24.26 mm quarter
# 1.205 in.  30.61 mm half dollar
# 1.043 in.  26.49 mm dollar

class Nickel(coin.Coin):
    def __init__(self, is_heads=False, kind="n", x=0, y=0):
        coin.Coin.__init__(self, is_heads, kind, x, y)
        self.body.coin = self
        self.shape.coin = self

        self.mass = 5 / 5.67
        self.radius = 21.21 / 24.26
        self.create_body_shape()

    def clone(self):
        nickel = Nickel(self.is_heads, self.kind, self.body.position.x, self.body.position.y)
        nickel.is_immobilized = self.is_immobilized
        return nickel

    def collide(self, other):
        if not self.is_shooting:
            return
        # nickels immobilize!
        if other.is_heads is not self.is_heads:
          other.is_immobilized = True
          other.is_recently_immobilized = True
