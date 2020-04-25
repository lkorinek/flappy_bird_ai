import pygame
import os
import random


class Pipe:
    """
    Pipe class for flappy bird game
    """

    GAP = 200
    VEL = 5
    PIPE_BOT = pygame.transform.scale2x(pygame.image.load(os.path.join("img", "pipe.png")))
    PIPE_TOP = pygame.transform.flip(PIPE_BOT, False, True)

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bot = 0
        self.passed = False
        self.set_height()

    def set_height(self):
        """
        Set the top left corner of both pipes for drawing
        """

        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bot = self.height + self.GAP

    def move(self):
        """
        Move the pipes left
        """

        self.x -= self.VEL

    def draw(self, win):
        """
        Draw the pipes
        """

        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOT, (self.x, self.bot))

    def collide(self, bird):
        """
        Check for collision with bird
        return boolean
        """

        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bot_mask = pygame.mask.from_surface(self.PIPE_BOT)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bot_offset = (self.x - bird.x, self.bot - round(bird.y))

        top_point = bird_mask.overlap(top_mask, top_offset)
        bot_point = bird_mask.overlap(bot_mask, bot_offset)

        if top_point or bot_point:
            return True
