import ai, human

def format_prompt(option):
    msg = "(" + option[0] + ")" + option[1:]
    return msg

def valid_responses(options):
    return [option[0] for option in options]

def response_from_options(screen, options):
    for option in options:
        prompt = format_prompt(option) + "\n"
        screen.addstr(prompt)
    screen.refresh()
    response = screen.getkey()
    return response

class Configuration:
    def __init__(self):
        self.players = []
        self.is_configured = False

    def prompt_configuration(self, screen):
        options = ["default", "human vs human", "ai vs ai", "custom"]
        response = response_from_options(screen, options)

        # default
        if response is "d":
            p1 = self.human_player()
            p2 = self.ai_player()
        # humans
        elif response is "h":
            p1 = self.human_player()
            p2 = self.human_player()
        # ais
        elif response is "a":
            p1 = self.ai_player()
            p2 = self.ai_player()
        # custom
        elif response is "c":
            p1 = self.prompt_human_or_ai(screen)
            p2 = self.prompt_human_or_ai(screen)
        elif response is "x":
            import sys
            sys.exit()

        self.players = [p1, p2]
        self.is_configured = True
        return self.players

    def prompt_human_or_ai(self, screen):
        options = ["human", "ai"]
        response = response_from_options(screen, options)

        if response is "h":
            player = self.human_player()
        elif response is "a":
            player = self.configure_ai_player(screen)
        else:
            print("invalid input")
            sys.exit()
        return player

    def human_player(self):
        player = human.HumanPlayer()
        return player

    def configure_ai_player(self, screen):
        screen.addstr("AI strength [1-9]: \n")
        response = screen.getkey()
        number = int("123456789".index(response))

        # manually adjust because lower is actually
        # harder, which is non-intuitive for input.
        difficulty = 10 - number
      
        bot = self.ai_player(difficulty)
        return bot

    def ai_player(self, ai_difficulty=8):
      bot = ai.AIPlayer(ai_difficulty=ai_difficulty)
      return bot
