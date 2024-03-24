import pygame

WIDTH = 800
HEIGHT = 800
FPS = 60


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Graphics Pipeline")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pygame.display.set_caption(f"Graphics Pipeline - FPS: {self.clock.get_fps()}")
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
