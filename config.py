import ai, human

def format_prompt(option):
    msg = "  (" + option[0] + ")" + option[1:]
    return msg

def valid_responses(options):
    return [option[0] for option in options]

def display_options(screen, options, title=None, is_formatted=True):
    if title:
        screen.addstr(title + "\n")
    for option in options:
        if is_formatted:
            prompt = format_prompt(option) + "\n"
        else:
            prompt = option + "\n"
        screen.addstr(prompt)
    screen.refresh()

def response_from_options(screen, options, title=None):
    display_options(screen, options, title)
    response = screen.getkey()
    return response

class Configuration:
    def __init__(self):
        self.players = []
        self.is_configured = False

    def prompt_configuration(self, screen):
        confirmed = False
        while not confirmed:
            self.display_prompt(screen)
            confirmed = self.confirm(screen)
        self.is_configured = True

    def display_prompt(self, screen):
        options = ["default (human vs ai)", "human vs human", "ai vs ai", "custom", "xit"]
        response = response_from_options(screen, options, title="Select game type:")

        # humans
        if response is "h":
            p1 = self.human_player()
            p2 = self.human_player()
        # ais
        elif response is "a":
            p1 = self.ai_player()
            p2 = self.ai_player()
        # custom
        elif response is "c":
            p1 = self.prompt_human_or_ai(screen, prompt="Player 1: ")
            p2 = self.prompt_human_or_ai(screen, prompt="Player 2: ")
        elif response is "x":
            import sys
            sys.exit()
        # default
        else:
            p1 = self.human_player()
            p2 = self.ai_player()

        self.players = [p1, p2]

    def format_player(self, player):
        if not player.is_ai:
            return "  Human"
        else:
            return "  AI (" + str(player.difficulty) + ")"

    def confirm(self, screen):
        players_str = [self.format_player(player) for player in self.players]
        display_options(screen, players_str, title="Players:", is_formatted=False)

        options = ["yes", "no"]
        response = response_from_options(screen, options, title="Start game?")

        if response is "y":
            return True
        else:
            return False

    def prompt_human_or_ai(self, screen, prompt=""):
        options = ["human", "ai"]
        title = prompt + "Human or AI?"
        response = response_from_options(screen, options, title=title)

        if response is "h":
            player = self.human_player()
        else:
            player = self.configure_ai_player(screen)
        return player

    def human_player(self):
        player = human.HumanPlayer()
        return player

    def configure_ai_player(self, screen):
        options = ["1 easy", "5 medium", "9 hard"]
        response = response_from_options(screen, options, title="AI difficulty [1-9]:")
        difficulty = int("0123456789".index(response))

        bot = self.ai_player(difficulty)
        return bot

    def ai_player(self, ai_difficulty=8):
      bot = ai.AIPlayer(ai_difficulty=ai_difficulty)
      return bot
