import pygame
import os


class Bird:
    """
    Bird class for flappy bird game
    """

    BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird1.png"))),
                 pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird2.png"))),
                 pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird3.png"))),
                 pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird2.png")))]
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.BIRD_IMGS[0]

    def jump(self):
        """
        Make the bird jump
        """

        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        """
        Wings flapping and bird move
        """

        self.tick_count += 1

        # Makes the bird start falling
        d = self.vel*self.tick_count + 1.5*self.tick_count**2
        # Max falling speed
        if d >= 16:
            d = 16
        # Tune the jump
        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        elif self.tilt > -90:
            self.tilt -= self.ROT_VEL

    def draw(self, win):
        """
        Pick an image for the bird and rotate it
        """

        self.img_count += 1
        self.img = self.BIRD_IMGS[(self.img_count // self.ANIMATION_TIME % 4)]

        if self.tilt <= -80:
            self.img = self.BIRD_IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_img, new_rect.topleft)

    def get_mask(self):
        """
        Get mask for collision detection
        return object
        """
        return pygame.mask.from_surface(self.img)
