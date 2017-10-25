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
        coin = table.get_coin(x, y)
        player = self.get_current_player()

        if coin.is_heads and player.is_heads:
            was_shot = coin.shoot_at(x, y)

    def shoot_coin(self, target_x, target_y):
        coin = table.get_selected_coin()
        if coin:
            coin.shoot_to(target_x, target_y)
            self.next_turn()

    def get_current_player(self):
        return self.players[self.turn_index]

    def next_turn(self):
        self.turn_index += 1
        self.turn_index %= len(self.players)
