import pygame
from constants import LIMITS, WINDOW_HEIGHT, WINDOW_WIDTH


class Paddle(pygame.sprite.Sprite):
    """Paddle class"""

    def __init__(self, position, color=None):
        super().__init__()

        # Default size
        self.size = (WINDOW_WIDTH * 0.017, WINDOW_WIDTH * 0.17)

        # Default speed
        self.speed = 0

        if not color:
            color = (204, 255, 0)
        self.refresh_rect(color)

        # Starting positions
        if position == "left":
            self.rect.x = LIMITS["left"]
        elif position == "right":
            self.rect.x = LIMITS["right"] - self.size[0]

        self.rect.y = LIMITS["down"] // 2

    def refresh_rect(self, color):
        """Updates the sprite / rect based on self.size"""
        self.image = pygame.Surface(self.size)
        self.image.fill(color)
        self.rect = self.image.get_rect()

    # ===============================================
    def update(self):
        self.rect.y += self.speed
        self.constrain()

    def constrain(self):
        if self.rect.y < LIMITS["up"]:
            self.rect.y = LIMITS["up"]
        if self.rect.y > LIMITS["down"] - self.size[1]:
            self.rect.y = LIMITS["down"] - self.size[1]



