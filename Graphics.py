import pygame
import Environment

class Simulation:
    def __init__(self, size, fps, simSpeed, world):
        pygame.init()
        
        self.fps = fps
        self.simSpeed = simSpeed

        self.deltaTime = 0

        self.size = size
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.running = True

        self.world = world
        self.gridSize = self.get_world_grid()

    def get_world_grid(self):
        width = self.size[0] / self.world.size[0]
        height = self.size[1] / self.world.size[1]
        return (int(width), int(height))

    def draw_world(self):
        row = 0
        col = 0
        for grid in self.world.grid:
            self.draw_rect((col * self.gridSize[0], row * self.gridSize[1]), ((col + 1) * self.gridSize[0], (row + 1) * self.gridSize[1]), grid.colour)
            col += 1
            if col >= self.world.size[0]:
                col = 0
                row +=1


    def draw_rect(self, upleft, bottomright, col):
        pygame.draw.rect(self.screen, col, (upleft[0], upleft[1], bottomright[0], bottomright[1]))

    def window_title(self):
        pygame.display.set_caption('Phyber_2D Engine - {:.2f} fps'.format(self.clock.get_fps()))

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.window_title()
            self.screen.fill((0, 0, 0))

            self.draw_world()

            self.deltaTime = self.clock.tick(self.fps)
            pygame.display.update()
        pygame.quit()

def main():
    world = Environment.World(24)

    sim = Simulation((600, 600), 15, 1, world)
    sim.loop()

if __name__ == "__main__":
    main()