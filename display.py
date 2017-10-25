class Display:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.cursorx = 0
        self.cursory = 0
        self.selected_coin = None

    def draw(self):
        screen = self.screen
        game = self.game

        screen.clear()

        screen.addstr("                    COIN WARS" + "\n")
        screen.addstr("* N=nickel D=dime Q=quarter $=dollar coin\n")
        screen.addstr("* Nickels immobilize a coin for a turn.\n")
        screen.addstr("* Dimes convert coins between heads and tails.\n")
        screen.addstr("* Dollars and dimes can't be converted.\n")
        screen.addstr("* Take turns. Knock all other coins off to win.\n")
        screen.addstr(f"\n")

        coin_hud = f"Heads: {game.table.heads_str}   Tails: {game.table.tails_str}"
        if len(game.table.heads) == 0 and len(game.table.tails) == 0:
            coin_hud += "    MUTUAL DESTRUCTION!!"
        elif len(game.table.heads) == 0:
            coin_hud += "    TAILS wins!!"
        elif len(game.table.tails) == 0:
            coin_hud += "    HEADS wins!!"
        else:
            coin_hud += "   Turn: "
            if game.get_current_player().is_heads:
                coin_hud += "heads"
            else:
                coin_hud += "tails"
        screen.addstr(coin_hud + "\n")

        if len(game.table.header) > 0:
          screen.addstr("Header: " + game.table.header + "\n")

        x, y = self.cursorx, self.cursory
        selected = self.selected_coin
        table_str = game.table.draw(x, y, selected)

        screen.addstr(table_str)
        screen.refresh()

    def draw_path_coin_to_cursor(self, coin):
        if coin is None:
            return

    def clear(self):
        self.selected_coin = None

    def move_cursor_left(self):
        self.cursorx -= 1

    def move_cursor_down(self):
        self.cursory += 1

    def move_cursor_up(self):
        self.cursory -= 1

    def move_cursor_right(self):
        self.cursorx += 1

    def update_path(self):
        if self.selected_coin is not None:
            x, y = self.cursorx, self.cursory
            table.set_path(self.selected_coin, x, y)

    def highlight_next_coin(self):
        # select own coins from heads or tails if
        # no coin is currently selected. otherwise
        # select from opponent coins to target.
        pass

    def select_or_shoot_coin(self):
        x, y = self.cursorx, self.cursory
        if self.selected_coin is None:
            self.selected_coin = self.game.select_coin(x, y)
        else:
            self.game.shoot_coin(self.selected_coin, x, y)
            self.selected_coin = None

    def quit():
        import sys
        sys.exit()
