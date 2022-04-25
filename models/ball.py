import random
import pygame
from constants import LIMITS, WINDOW_WIDTH, WINDOW_HEIGHT

pygame.init()


"""sound class, handles loading and playing the sounds"""


class Sound:
    def __init__(self) -> None:
        self.paddle_bounce_sound = pygame.mixer.Sound("Assets/paddle.ogg")
        self.wall_bounce_sound = pygame.mixer.Sound("Assets/wall.ogg")
        self.score_sound = pygame.mixer.Sound("Assets/score.ogg")

    def play_wall(self):
        self.wall_bounce_sound.play()

    def play_paddle(self):
        self.paddle_bounce_sound.play()

    def play_score(self):
        self.score_sound.play()


class Ball(pygame.sprite.Sprite):
    """
    Model of a (bouncing) ball.
    If gravity is True, the ball will obey to gravity (aka fall down).
    """

    def __init__(
        self, paddles, gravity=False, color=None, size=WINDOW_WIDTH * 0.04, power=False
    ):
        """Constructor"""
        super().__init__()

        self.sound = Sound()
        self.paddles = paddles
        self.size = size
        # The ball is a circle
        self.image = pygame.Surface((size, size))
        self.image.set_colorkey((0, 0, 0))

        if not color:
            color = (204, 255, 0)
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect()

        # Spawn in the middle of the screen
        self.rect.x = LIMITS["right"] // 2
        self.rect.y = LIMITS["down"] // 2

        # Start without moving
        self.hspeed = 0
        self.vspeed = 0

        # power
        self.power = power

        # each player can only have 1 power shot per game
        self.p1_power, self.p2_power = 1, 1

        # Gravity and off limits booleans
        self.respect_gravity = gravity
        self.off_limits = False

        # score
        self.p1_score, self.p2_score = 0, 0

        # time
        self.scoretime = 0
        # point font
        self.smallfont = pygame.font.Font(
            "freesansbold.ttf", round(WINDOW_WIDTH * 0.05)
        )
        self.bigfont = pygame.font.Font("freesansbold.ttf", round(WINDOW_WIDTH * 0.08))
        # countdown timer value
        self.countdown_value = " "
        self.countdown_text = self.smallfont.render(
            self.countdown_value, True, (0, 0, 0)
        )
        # display who scored
        self.who_scored_value = " "
        self.who_scored_text = self.bigfont.render(
            self.who_scored_value, True, (0, 0, 0)
        )

    def launch(
        self, direction=None, hspeed=WINDOW_WIDTH * 0.007, vspeed=WINDOW_HEIGHT * 0.010
    ):
        """Launches the ball up in the air"""
        direction = random.choice(["left", "right"])
        self.hspeed = hspeed
        if direction == "left":
            self.hspeed = -self.hspeed
        if direction == "right":
            self.hspeed = +self.hspeed
        self.vspeed = vspeed

    def reset(self):
        self.off_limits = False
        self.rect.x = LIMITS["right"] // 2
        self.rect.y = LIMITS["down"] // 2
        self.hspeed, self.vspeed = 0, 0
        self.scoretime = pygame.time.get_ticks()
        # reset counter values and who scored text
        self.countdown_value = " "
        self.who_scored_value = " "
        self.power = False

    def update(self):
        """Convenience method"""

        # The vertical speed decreases over time when subject to gravity
        if self.respect_gravity:
            self.vspeed += 1

        # If the ball is not off limits, make it move
        if not self.off_limits:
            self.scoretime = pygame.time.get_ticks()
            self.rect.x += self.hspeed
            self.rect.y += self.vspeed
        else:
            self.restart_counter()

        # Check the ball did not go off limitss
        if self.rect.x > LIMITS["right"] - self.size:
            self.sound.play_score()
            self.rect.x = LIMITS["right"] - self.size
            self.who_scored_value = "Player 1!"
            self.p1_score += 1
            self.off_limits = True
        elif self.rect.x < LIMITS["left"]:
            self.sound.play_score()
            self.who_scored_value = "Player 2!"
            self.p2_score += 1
            self.rect.x = LIMITS["left"]
            self.off_limits = True

        # Check whether we need to bounce the ball
        if self.rect.y > LIMITS["down"] - self.size:
            self.rect.y = LIMITS["down"] - self.size
            self.bounce("vertical")
            self.sound.play_wall()
        elif self.rect.y < LIMITS["up"]:
            self.rect.y = LIMITS["up"]
            self.bounce("vertical")
            self.sound.play_wall()

        # paddle bounce logic
        if pygame.sprite.spritecollide(self, self.paddles, False):
            self.sound.play_paddle()
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[
                0
            ].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.hspeed > 0:
                self.bounce("horizontal")
            if abs(self.rect.left - collision_paddle.right) < 10 and self.hspeed < 0:
                self.bounce("horizontal")
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.vspeed < 0:
                self.rect.top = collision_paddle.bottom
                self.bounce("vertical")
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.vspeed > 0:
                self.rect.bottom = collision_paddle.top
                self.bounce("vertical")

        # Prevent the ball from bouncing for ever when on the ground
        if (
            self.respect_gravity
            and -1 < self.vspeed < 1
            and self.rect.y >= LIMITS["down"] - (self.size + 5)
        ):
            self.vspeed = 0

    # handles logic of displaying for 3 seconds, uses clock
    def restart_counter(self):
        curr_time = pygame.time.get_ticks()

        if curr_time - self.scoretime <= 1000:
            self.countdown_value = 3
        if 1000 < curr_time - self.scoretime <= 2000:
            self.countdown_value = 2
        if 2000 < curr_time - self.scoretime <= 3000:
            self.countdown_value = 1
        if curr_time - self.scoretime >= 3000:
            self.reset()
            self.launch()
        self.who_scored_text = self.bigfont.render(
            self.who_scored_value, True, (255, 255, 255)
        )
        self.countdown_text = self.smallfont.render(
            str(self.countdown_value), True, (255, 255, 255)
        )

    def bounce(self, direction=None, power=True):
        """Bounce the ball"""

        # Horizontal bounces slightly increase horizontal speed
        if direction in ("right", "left", "horizontal"):
            # self.hspeed = -self.hspeed * 0.8
            self.hspeed *= -1.03

        # Vertical bounces increase vertical speed
        if direction in ("up", "down", "vertical"):
            # self.vspeed = -self.vspeed * 0.5
            self.vspeed *= -1.03
        # Power bounce: increase the speed of the ball
        if self.power:
            self.hspeed *= 1.4
            self.vspeed *= 1.2
