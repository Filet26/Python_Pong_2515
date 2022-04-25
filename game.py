import pygame, sys

from constants import WINDOW_HEIGHT, WINDOW_WIDTH

from screens.comp_Screen import CompScreen

from screens.intro_screen import IntroScreen

from screens.game_over import GameOver


class StateManager:
    """_state manager class, changes screen based on buttons clicked_"""

    """
    default mode is intro
    """

    def __init__(self):
        self.mode = "intro"
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen = None
        self.winner = ""

    """
    intro method, displays the intro screen, and takes the value returned
    which is the game mode selected
    """

    def intro(self):
        self.screen = IntroScreen(self.window)
        result = self.screen.loop()
        self.mode = result
        self.statemanage()

    """ranked method, displays the ranked screen, closes screen when quit"""

    def ranked(self):
        self.screen = CompScreen(self.window, None, self.mode)
        result = self.screen.loop()
        self.mode = result[0]
        if self.mode == "end":
            self.mode = "end"
        self.winner = [result[1], result[2]]
        self.statemanage()

    """practice mode, same as ranked, but less functions"""

    def practice(self):
        self.screen = None
        result = self.screen.loop()
        self.mode = result
        print("practice")

    """end card, can replay or quit"""

    def end_card(self, winner):
        self.screen = GameOver(self.window, winner)
        result = self.screen.loop()
        self.mode = result
        self.statemanage()

    """state manager class, runs method based on the mode"""

    def statemanage(self):
        if self.mode == "intro":
            self.intro()
        if self.mode == "ranked":
            self.ranked()
        if self.mode == "practice":
            self.ranked()
        if self.mode == "end":
            self.end_card(self.winner)
        if self.mode == "quit":
            self.screen.running = False


def main():
    # create instance of statemanager
    state_manager = StateManager()
    # initialize pygame mixer, and play sound
    pygame.mixer.init()
    bg_tunes = pygame.mixer.Sound("Assets/hampter.ogg")
    bg_tunes.set_volume(0.2)
    bg_tunes.play()
    # run state manager,
    pygame.init()
    state_manager.statemanage()


if __name__ == "__main__":
    main()
