class Display:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.cursorx = game.table.cols // 2
        self.cursory = game.table.rows // 2 + 1
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
        self.resolve_cursor_movement()

    def move_cursor_down(self):
        self.cursory += 1
        self.resolve_cursor_movement()

    def move_cursor_up(self):
        self.cursory -= 1
        self.resolve_cursor_movement()

    def move_cursor_right(self):
        self.cursorx += 1
        self.resolve_cursor_movement()

    def update_path(self):
        if self.selected_coin is not None:
            x, y = self.cursorx, self.cursory
            table.set_path(self.selected_coin, x, y)

    def target_next_coin(self):
        self.resolve_cursor_movement()
         
        # pick a friendly piece first, then aim
        # it at an enemy piece
        if self.selected_coin is None:
            coin = self.move_cursor_to_next_friendly_coin()
        else:
            coin = self.move_cursor_to_next_enemy_coin()
        self.cursorx = coin.roundX()
        self.cursory = coin.roundY()

    def move_cursor_to_next_friendly_coin(self):
        friendlies = self.game.table.tails
        if self.game.get_current_player().is_heads:
            friendlies = self.game.table.heads

        coin_under_cursor = self.game.table.get_coin(self.cursorx, self.cursory)
        if coin_under_cursor is None:
            return friendlies[0]
        elif coin_under_cursor.is_heads is not self.game.get_current_player().is_heads:
            return friendlies[0]
        else:
            index = friendlies.index(coin_under_cursor)
            index += 1
            index %= len(friendlies)
            return friendlies[index]

    def move_cursor_to_next_enemy_coin(self):
        enemies = self.game.table.heads
        if self.game.get_current_player().is_heads:
            enemies = self.game.table.tails

        coin_under_cursor = self.game.table.get_coin(self.cursorx, self.cursory)
        # start from the top if there's no coin under the cursor
        if coin_under_cursor.is_heads is None:
            return enemies[0]
        # or if the cursor is over one of your own
        if coin_under_cursor.is_heads is self.game.get_current_player().is_heads:
            return enemies[0]
        # otherwise, move to the next enemy
        else:
            index = enemies.index(coin_under_cursor)
            index += 1
            index %= len(enemies)
            return enemies[index]

    def select_or_shoot_coin(self):
        self.resolve_cursor_movement()

        x, y = self.cursorx, self.cursory
        if self.selected_coin is None:
            coin = self.game.select_coin(x, y)
            if coin and coin.is_immobilized:
                coin.remind_cant_select = True
            else:
                self.selected_coin = self.game.select_coin(x, y)
        else:
            self.game.shoot_coin(self.selected_coin, x, y)
            self.selected_coin = None

    def resolve_cursor_movement(self):
        self.game.table.show_turn_message = False
        for coin in self.game.table.coins:
            coin.is_recently_converted = False
            coin.is_recently_immobilized = False
            coin.remind_cant_select = False
            coin.is_recently_resisted_conversion = False

    def quit():
        import sys
        sys.exit()
