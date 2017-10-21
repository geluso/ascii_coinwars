import random

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

class Board:
    def __init__(self, width=50, height=40):
        self.width = width
        self.height = height

        t1 = Coin(x=10, y=10)
        t2 = Coin(x=20, y=10)
        t3 = Coin(x=30, y=10)
        t4 = Coin(x=40, y=10)

        h1 = Coin(x=10, y=30, is_heads=True)
        h2 = Coin(x=20, y=30, is_heads=True)
        h3 = Coin(x=30, y=30, is_heads=True)
        h4 = Coin(x=40, y=30, is_heads=True)

        self.coins = [t1, t2, t3, t4, h1, h2, h3, h4]
        self.highlighted = random.sample(self.coins, 1)[0]

    def __str__(self):
        result = ""
        result += "=" * self.width + "\n"
        for i in range(1, self.height-1):
            line = "|" + " " * (self.width - 2) + "|" + "\n"
            result += line
        result += "=" * self.width + "\n"

        lines = result.split("\n")
        for coin in self.coins:
            line = list(lines[coin.y])
            line[coin.x] = str(coin)

            if (coin is self.highlighted):
                line[coin.x - 1] = "("
                line[coin.x + 1] = ")"

            lines[coin.y] = line

        result = ""
        for line in lines:
          line = "".join(line)
          result += line + "\n"
        return result

