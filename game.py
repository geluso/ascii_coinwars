import table
import player

class Game():
    def __init__(self):
        self.table = table.Table()

        p1 = player.Player(is_ai=False, is_heads=True)
        p2 = player.Player(is_ai=True, is_heads=False)

        self.players = [p1, p2]
        self.turn_index = 0

    def select_coin(self, x, y):
        coin = self.table.get_coin(x, y)
        player = self.get_current_player()

        if coin is None:
            return None

        # prevent the player from selecting coins
        # that aren't in their control.
        if coin.is_heads is player.is_heads:
            return coin
        return None

    def shoot_coin(self, coin, x, y):
        if coin is None:
            return
        was_shot = coin.shoot_at(x, y)
        self.next_turn()

    def get_current_player(self):
        return self.players[self.turn_index]

    def next_turn(self):
        self.turn_index += 1
        self.turn_index %= len(self.players)
