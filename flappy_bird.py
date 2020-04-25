import pygame
import neat
import os
from bird import Bird
from pipe import Pipe
from base import Base

pygame.font.init()


class FlappyBird:
    """
    Flappy bird game
    """

    BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bg.png")))
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config-feedforward.txt")

    def __init__(self, win_width=500, win_height=800):
        self.win_width = win_width
        self.win_height = win_height
        self.size = (win_width, win_height)
        self.gen = 0
        self.neat_init()

    def neat_init(self):
        """
        Initialize neat algorithm
        """
        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation, self.CONFIG_PATH)

        self.population = neat.Population(self.config)
        self.population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.population.add_reporter(stats)

    def on_init(self, genomes, config):
        """
        Initialize before the main loop
        """

        pygame.init()
        self.win = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Flappy bird")
        self.clock = pygame.time.Clock()
        self.score = 0
        self.gen += 1

        self.nets = []
        self.ge = []
        self.birds = []

        for _, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.nets.append(net)
            self.birds.append(Bird(230, 350))
            self.ge.append(genome)

        self.base = Base(self.win_height)
        self.pipes = [Pipe(self.win_width + 200)]
        self.run = True

    def on_event(self, event):
        """
        Check for events
        """

        if event.type == pygame.QUIT:
            self.run = False
            pygame.quit()
            quit()

    def on_loop(self):
        """
        Compute changes in the game
        """

        self.clock.tick(30)
        self.base.move()
        self.pipe_movement()

        if not self.birds:
            self.run = False

    def pipe_movement(self):
        """
        Move pipes and check for collision with bird
        """

        pipe_idx = 0
        if self.birds[0].x > self.pipes[0].x + self.pipes[0].PIPE_TOP.get_width():
            pipe_idx = 1

        for idx, bird in enumerate(self.birds):
            bird.move()
            self.ge[idx].fitness += 0.1

            output = self.nets[idx].activate((bird.y, abs(bird.y - self.pipes[pipe_idx].height),
                                              abs(bird.y - self.pipes[pipe_idx].bot)))

            if output[0] > 0.5:
                bird.jump()

            if bird.y + bird.img.get_height() >= self.win_height - 70 or bird.y < 0:
                self.birds.pop(idx)
                self.nets.pop(idx)
                self.ge.pop(idx)

        for pipe in self.pipes:
            pipe.move()
            for idx, bird in enumerate(self.birds):
                if pipe.collide(bird):
                    self.ge[idx].fitness -= 1
                    self.birds.pop(idx)
                    self.nets.pop(idx)
                    self.ge.pop(idx)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True

                    self.score += 1
                    for genome in self.ge:
                        genome.fitness += 5
                    self.pipes.append(Pipe(600))

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                self.pipes.remove(pipe)

    def on_render(self):
        """
        Render all graphics
        """

        self.win.blit(self.BG_IMG, (0, 0))
        self.base.draw(self.win)
        for bird in self.birds:
            bird.draw(self.win)
        for pipe in self.pipes:
            pipe.draw(self.win)

        # Show score
        text = self.SCORE_FONT.render("Score: " + str(self.score), 1, (255, 255, 255))
        self.win.blit(text, (self.win_width - 10 - text.get_width(), 10))

        # Show generation
        text = self.SCORE_FONT.render("Gen: " + str(self.gen), 1, (255, 255, 255))
        self.win.blit(text, (10, 10))

        pygame.display.update()

    def main(self, genomes, config):
        """
        Creates the main loop
        """
        self.on_init(genomes, config)

        while self.run:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

    def run_neat(self):
        """
        Run neat(NeuroEvolution of Augmenting Topologies) algorithm
        """
        self.population.run(self.main, 50)


if __name__ == "__main__":
    flappy = FlappyBird()
    flappy.run_neat()
