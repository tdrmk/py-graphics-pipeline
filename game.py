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
        self.update_func = []
        self.draw_func = []

    def add_update_func(self, func):
        self.update_func.append(func)

    def add_draw_func(self, func):
        self.draw_func.append(func)

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
        caption = f"Graphics Pipeline - FPS: {self.clock.get_fps():.2f}"
        pygame.display.set_caption(caption)
        # dt = seconds since last frame
        dt = self.clock.get_time() / 1000.0
        for func in self.update_func:
            func(dt)
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        for func in self.draw_func:
            func()
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
