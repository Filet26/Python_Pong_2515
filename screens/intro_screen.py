import pygame
from .base_screen import Screen
from constants import *
import sys


class IntroScreen(Screen):
    """Intro screen, has two options, ranked and practice mode"""

    def __init__(self, *args, **kwargs):
        # Call the parent constructor
        super().__init__(*args, **kwargs)
        # load the fonts
        self.titlefont = pygame.font.Font(
            "freesansbold.ttf", round(WINDOW_WIDTH * 0.05)
        )
        self.smallfont = pygame.font.Font(
            "freesansbold.ttf", round(WINDOW_WIDTH * 0.03)
        )
        self.bg = pygame.transform.scale(
            pygame.image.load("Assets/tim.png"), (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        # default mode
        self.mode = "intro"

        # ranked button
        self.rankedbutton = pygame.Rect(
            WINDOW_WIDTH // 2 + (0.10 * WINDOW_WIDTH),
            WINDOW_HEIGHT // 2,
            WINDOW_HEIGHT * 0.3,
            WINDOW_HEIGHT * 0.2,
        )
        # practice button
        self.practicebutton = pygame.Rect(
            WINDOW_WIDTH // 2 - (0.4 * WINDOW_WIDTH),
            WINDOW_HEIGHT // 2,
            WINDOW_HEIGHT * 0.3,
            WINDOW_HEIGHT * 0.2,
        )

    # renders text
    def render_text(self):
        self.title_text = self.titlefont.render(
            "Select The Game Mode!", True, (245, 255, 255)
        )
        self.ranked_text = self.smallfont.render("Ranked!", True, (0, 0, 0))
        self.practice_text = self.smallfont.render("Practice!", True, (0, 0, 0))
        self.window.blit(self.title_text, (WINDOW_WIDTH // 5, WINDOW_HEIGHT // 5))
        self.window.blit(
            self.ranked_text,
            (
                self.rankedbutton.x + self.rankedbutton.width // 3.9,
                self.rankedbutton.y + self.rankedbutton.height // 2.5,
            ),
        )
        self.window.blit(
            self.practice_text,
            (
                self.practicebutton.x + self.practicebutton.width // 4.6,
                self.practicebutton.y + self.practicebutton.height // 2.5,
            ),
        )

    # checks which button user has clicked and returns value based on it
    def process_event(self, event):
        """_if user clicks on ranked button,
        the mode will be set to ranked, same for practice_

        Args:
            event (_thing_): _pygame event_
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.rankedbutton.collidepoint(pos):
                self.mode = "ranked"
                self.running = False
            elif self.practicebutton.collidepoint(pos):
                self.mode = "practice"
                self.running = False

    # process loop, blits stuff
    def process_loop(self):
        pygame.display.set_caption("Welcome to my game!: Intro")
        self.window.blit(self.bg, (0, 0))
        # draw buttons on screen
        pygame.draw.rect(self.window, (255, 0, 13), self.rankedbutton)
        pygame.draw.rect(self.window, (255, 82, 13), self.practicebutton)
        self.render_text()
        pygame.display.update()
        return self.mode
