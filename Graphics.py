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
        self.organismScale = self.get_organism_scale(0.1)

    def get_world_grid(self):
        width = self.size[0] / self.world.size[1]
        height = self.size[1] / self.world.size[0]
        return (int(width), int(height))

    def get_organism_scale(self, scalingFactor):
        if scalingFactor < 0:
            scalingFactor = 0
        elif scalingFactor > 1:
            scalingFactor = 1
        dy = round(self.gridSize[0] * ((1 - scalingFactor) / 2))
        dx = round(self.gridSize[1] * ((1 - scalingFactor) / 2))
        return (dy, dx)

    def draw_world(self):
        for row in range(self.world.size[0]):
            for col in range(self.world.size[1]):                
                self.draw_quad(self.world.biomes[row][col].colour, (row, col))

    def draw_organisms(self):
        for o in self.world.population:
            self.draw_quad((255, 0, 255), o.position, 0.75)

    def draw_quad(self, col, coords, scale=1):
        if scale == 1:
            upleft = (coords[1] * self.gridSize[0], coords[0] * self.gridSize[1])
            self.draw_rect(upleft, self.gridSize, col)
        else:
            upleft = (coords[1] * self.gridSize[0], coords[0] * self.gridSize[1])
            offset = (1 - scale) * 0.5
            self.draw_rect((round(upleft[0] + offset * self.gridSize[0]), round(upleft[1] + offset * self.gridSize[1])), (round(self.gridSize[0] * scale), round(self.gridSize[1] * scale)), col)

    def draw_rect(self, upleft, bottomright, col):
        pygame.draw.rect(self.screen, col, (upleft[0], upleft[1], bottomright[0], bottomright[1]))

    def window_title(self):
        pygame.display.set_caption('Lyber Engine - {:.2f} fps'.format(self.clock.get_fps()))

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.window_title()
            self.screen.fill((0, 0, 0))

            self.world.Loop()
            self.draw_world()
            self.draw_organisms()

            self.deltaTime = self.clock.tick(self.fps)
            pygame.display.update()
        pygame.quit()

def main():
    import numpy as np

    world = Environment.World((40, 60))
    world.CreateWorld()

    dna = 'FF00FF'
    dna += '00000000'
    dna += '00000000'
    dna += '00000000'
    dna += '00000000'
    dna += '00000000'
    dna += '00000000'
    dna += '00000000'
    dna += '99999999'
    dna += 'EEEEEEEE'
    dna += 'FFFFFFFF'
    dna += '0404FFFF' + '05050000'
    world.AddPopulation(dna)

    sim = Simulation((900, 600), 60, 1, world)
    sim.loop()

if __name__ == "__main__":
    main()
