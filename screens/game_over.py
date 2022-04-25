import pygame
from .base_screen import Screen
from constants import *
import sys


class GameOver(Screen):
    """Example class for a Pong game screen"""

    def __init__(self, *args, **kwargs):
        # Call the parent constructor
        super().__init__(*args, **kwargs)
        self.titlefont = pygame.font.Font("freesansbold.ttf", round(WINDOW_WIDTH *0.05))
        self.smallfont = pygame.font.Font("freesansbold.ttf", round(WINDOW_WIDTH *0.04))
        self.bg = pygame.transform.scale(
            pygame.image.load("Assets/tim.png"), (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.mode = "intro"

        # quit button
        self.quitbutton = pygame.Rect(
            WINDOW_WIDTH // 2 + (0.10 * WINDOW_WIDTH),
            WINDOW_HEIGHT // 2,
            WINDOW_HEIGHT * 0.3,
            WINDOW_HEIGHT * 0.2,
        )
        # practice button
        self.replaybutton = pygame.Rect(
            WINDOW_WIDTH // 2 - (0.4 * WINDOW_WIDTH),
            WINDOW_HEIGHT // 2,
            WINDOW_HEIGHT * 0.3,
            WINDOW_HEIGHT * 0.2,
        )

    def render_text(self):
        self.title_text = self.titlefont.render(
            f"Player 1: {self.winner[0]}   Player2: {self.winner[1]}",
            True,
            (245, 255, 255),
        )
        self.replay_text = self.smallfont.render("Replay!", True, (0, 0, 0))
        self.quit_text = self.smallfont.render("Rage Quit", True, (0, 0, 0))
        self.window.blit(self.title_text, (WINDOW_WIDTH // 6, WINDOW_HEIGHT // 5))
        self.window.blit(
            self.quit_text,
            (
                self.quitbutton.x + self.quitbutton.width // 3.9,
                self.quitbutton.y + self.quitbutton.height // 2.5,
            ),
        )
        self.window.blit(
            self.replay_text,
            (
                self.replaybutton.x + self.replaybutton.width // 4.6,
                self.replaybutton.y + self.replaybutton.height // 2.5,
            ),
        )

        # get text coordinates

    def process_event(self, event):
        '''
        has two options, replay or quit, quit will end the program
        and replay will bring the user back to the intro screen
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.quitbutton.collidepoint(pos):
                self.mode = "quit"
                self.running = False
            elif self.replaybutton.collidepoint(pos):
                self.mode = "intro"
                self.running = False

    def process_loop(self):

        """_sets caption, fille image with tim.png, 
        draws the replay and quit button on the screen_

        Returns:
            _type_: _returns the mode str:_
        """        

        pygame.display.set_caption("Game Over!!!")
        self.window.blit(self.bg, (0, 0))
        pygame.draw.rect(self.window, (255, 0, 13), self.quitbutton)
        pygame.draw.rect(self.window, (255, 82, 13), self.replaybutton)
        self.render_text()
        pygame.display.update()
        return self.mode



