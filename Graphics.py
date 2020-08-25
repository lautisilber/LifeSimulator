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
            self.draw_quad(o.colour, o.position, 0.75)

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

def main(fps):
    import numpy as np

    world = Environment.World((20, 30))
    world.CreateWorld()

    dna1 = 'FF00FF'
    dna1 += '00000000'
    dna1 += '99999999'
    dna1 += '00000000'
    dna1 += '00000000'
    dna1 += '00000000'
    dna1 += '00000000'
    dna1 += '00000000'
    dna1 += '55555555'
    dna1 += 'EEEEEEEE'
    dna1 += 'FFFFFFFF'
    dna1 += '0D0DFFFF' + '05050000'
    world.AddPopulation(dna1)

    dna2 = 'FF0000'
    dna2 += '00000000'
    dna2 += '55555555'
    dna2 += '00000000'
    dna2 += '00000000'
    dna2 += '00000000'
    dna2 += '00000000'
    dna2 += '00000000'
    dna2 += '99999999'
    dna2 += 'EEEEEEEE'
    dna2 += 'FFFFFFFF'
    dna2 += '0E0E0000' + '05050000'
    world.AddPopulation(dna2)

    sim = Simulation((900, 600), fps, 1, world)
    sim.loop()

def get_int_input(prompt):
    data = 0
    end = False
    while True:
        i = input(prompt)
        try:
            if float(str(i)).is_integer():
                data = int(float(str(i)))
                end = True
            else:
                print('please type in an integer')
        except:
            print('not a valid input!')
        if end:
            break
    return data

if __name__ == "__main__":
    main(get_int_input('fps: '))
