import pygame

from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from .game_screen import GameScreen


class CompScreen(GameScreen):
    """_Main game screen, for both practice and competive_

    Args:
        GameScreen (_Screen_): _Inherits from gamescreen class_
    """    

    def __init__(self, *args, **kwargs):
        # Call the parent constructor
        super().__init__(*args, **kwargs)
        # load fonts 
        self.titlefont = pygame.font.Font("freesansbold.ttf", round(WINDOW_WIDTH *0.05))
        self.smallfont = pygame.font.Font("freesansbold.ttf", round(WINDOW_WIDTH *0.03))
        # the center border line
        self.strip = pygame.Rect(WINDOW_WIDTH / 2 - 2, 0, 2, WINDOW_HEIGHT)

    def process_event(self, event):
        # handles the up and down movements, and also the power shot key
        # each player only gets 1 power shot move per game

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.p2.speed -= 7
            if event.key == pygame.K_DOWN:
                self.p2.speed += 7
            if event.key == pygame.K_q:
                self.p1.speed -= 7
            if event.key == pygame.K_a:
                self.p1.speed += 7
            if event.key == pygame.K_LCTRL:
                if self.ball.p1_power == 1:
                    self.ball.power = True
                    self.ball.p1_power = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.p2.speed += 7
            if event.key == pygame.K_DOWN:
                self.p2.speed -= 7
            if event.key == pygame.K_q:
                self.p1.speed += 7
            if event.key == pygame.K_a:
                self.p1.speed -= 7
            if event.key == pygame.K_RCTRL:
                if self.ball.p2_power == 1:
                    self.ball.power = True
                    self.ball.p2_power = 0
        pass

    def print_score(self):
        # prints the scores of the player
        self.window.blit(
            self.smallfont.render(f"Player 1: {self.ball.p1_score}", True, (255, 255, 255)),
            (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 25),
        )
        self.window.blit(
            self.smallfont.render(f"Player 2: {self.ball.p2_score}", True, (255, 255, 255)),
            (WINDOW_WIDTH // 1.9, WINDOW_HEIGHT // 25),
        )

        

    def process_loop(self):
        # set caption
        if self.mode == "practice":
            pygame.display.set_caption("Practice")
        else:
            pygame.display.set_caption("Ranked mode!")
        # Update the ball position
        self.ball.update()

        # Update the paddles' positions
        self.paddles.update()

        # Blit everything
        self.paddles.draw(self.window)
        self.window.blit(self.ball.image, self.ball.rect)

        # display the score for each player
        self.print_score()

        # Blit everything
        pygame.draw.rect(self.window, (100, 100, 100), self.strip)
        self.window.blit(
            self.ball.countdown_text,
            (WINDOW_WIDTH // 2 - 0.05 * WINDOW_WIDTH, WINDOW_HEIGHT // 2),
        )
        self.window.blit(
            self.ball.who_scored_text,
            (WINDOW_WIDTH // 2 - 0.18 * WINDOW_WIDTH, WINDOW_HEIGHT // 3),
        )
        self.window.blit(
            self.smallfont.render(
                f"Speed: Y: {round(self.ball.vspeed, 2)}: X: {round(self.ball.hspeed, 2)}",
                True,
                (255, 255, 255),
            ),
            (0.10 * WINDOW_WIDTH, WINDOW_HEIGHT - 0.10 * WINDOW_HEIGHT),
        )

        # visual effect for when the ball is off limits
        if self.ball.off_limits == True:
            self.bgcolor = (155, 155, 155)
        else:
            self.bgcolor = (35, 31, 32)

        
        #end game if either player hits 10 points
        if (
            self.ball.p1_score == 10 or self.ball.p2_score == 10
        ) and self.mode == "ranked":
            self.running = False
            return ["end", self.ball.p1_score, self.ball.p2_score]

        return ["end", "None", "None"]
