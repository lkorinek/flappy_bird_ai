import pygame
import os


class Base:
    """
    Pipe class for flappy bird game
    """

    BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("img", "base.png")))
    WIDTH = BASE_IMG.get_width()
    VEL = 5

    def __init__(self, win_height):
        self.y = win_height - 70
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """
        Move both bases left
        """

        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        """
        Move the bases
        """

        win.blit(self.BASE_IMG, (self.x1, self.y))
        win.blit(self.BASE_IMG, (self.x2, self.y))
