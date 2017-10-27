import table
import human
import ai

class Game():
    def __init__(self):
        self.table = table.Table()

        p1 = human.HumanPlayer(is_heads=True)
        #p1 = ai.AIPlayer(is_heads=True)
        p2 = ai.AIPlayer(is_heads=False)

        self.players = [p1, p2]
        self.turn_index = -1
        self.next_turn()

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

    def is_game_over(self):
        return len(self.table.heads) is 0 or len(self.table.heads) is 0

    def turn_message(self):
        if len(self.table.heads) is 0 and len(self.table.heads) is 0:
            return "MUTUAL DESTRUCTION"
        if len(self.table.heads) is 0:
            return "TAILS WINS"
        elif len(self.table.heads) is 0:
            return "HEADS WINS"

        player = self.get_current_player()
        turn = " TURN"

        if self.players[0].__class__ is self.players[1].__class__:
            if player.is_heads:
                turn = "HEADS" + turn
            else:
                turn = "TAILS" + turn
        elif player.__class__ is human.HumanPlayer:
            turn = "YOUR" + turn
        elif player.__class__ is ai.AIPlayer:
            turn = "AI" + turn
        else:
            turn = str(player.__class__)
        return turn

    def next_turn(self):
        if self.is_game_over():
            return

        self.turn_index += 1
        self.turn_index %= len(self.players)
        self.table.show_turn_message = self.turn_message()
            
