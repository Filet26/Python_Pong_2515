import pygame
from .base_screen import Screen
from models import Ball, Paddle


class GameScreen(Screen):
    """Example class for a Pong game screen"""

    def __init__(self, *args, **kwargs):
        # Call the parent constructor
        super().__init__(*args, **kwargs)

        # Create objectsh()
        self.p1 = Paddle("left")
        self.p2 = Paddle("right")
        self.paddles = pygame.sprite.Group()
        self.paddles.add(self.p1, self.p2)
        self.ball = Ball(self.paddles)
        self.ball.launch()

    def process_event(self, event):
        # In this screen, we don't have events to manage - pass
        pass

    def process_loop(self):
        # Update the ball position
        self.ball.update()

        # Update the paddles' positions
        self.paddles.update()

        # Blit everything
        self.paddles.draw(self.window)
        self.window.blit(self.ball.image, self.ball.rect)

        if self.ball.off_limits:
            return True

        return False
