class WelcomeScreen:
    def __init__(self, screen):
        self.screen = screen

    def display_title_screen(self):
        title = """
     ____ ___ ___ _   _
    / ___/ _ \_ _| \ | |
   | |  | | | | ||  \| |
   | |__| |_| | || |\  |
    \____\___/___|_| \_|
__        ___    ____  ____  
\ \      / / \  |  _ \/ ___| 
 \ \ /\ / / _ \ | |_) \___ \ 
  \ V  V / ___ \|  _ < ___) |
   \_/\_/_/   \_\_| \_\____/ 

        """
        self.screen.addstr(title + "\n")
        self.screen.refresh()
