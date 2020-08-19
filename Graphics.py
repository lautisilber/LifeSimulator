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
        for row in range(self.world.biomeMap.shape[0]):
            for col in range(self.world.biomeMap.shape[1]):                
                self.draw_rect((col * self.gridSize[1], row * self.gridSize[0]), (self.gridSize[1], self.gridSize[0]), self.world.biomes[self.world.biomeMap[row][col]].colour)

    def draw_organisms(self):
        for o in self.world.population:
            #self.draw_rect((o.position[1] * self.gridSize[1] + self.organismScale[1], o.position[0] * self.gridSize[0] + self.organismScale[0]),
            #((o.position[1] + 1) * self.gridSize[1] - self.organismScale[1], (o.position[0] + 1) * self.gridSize[0] - self.organismScale[0]),
            #o.colour)
            #self.draw_rect((o.position[1] * self.gridSize[1], o.position[0] * self.gridSize[0]),
            #((o.position[1] + 1) * self.gridSize[1], (o.position[0] + 1) * self.gridSize[0]),
            #o.colour)
            self.draw_rect((o.position[1] * self.gridSize[1], o.position[0] * self.gridSize[0]), (15, 15), o.colour)


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
    world = Environment.World((40, 60))
    dna = 'FF00FF'
    dna += '00000000'
    dna += '00000000'
    dna += '00000000'
    dna += '00000000'
    dna += '00000000'
    dna += '00000000'
    dna += '00000000'
    dna += '00000000'
    dna += '77777777'
    dna += 'AAAAAAAA'
    world.AddPopulation(dna)

    sim = Simulation((900, 600), 10, 1, world)
    sim.loop()

if __name__ == "__main__":
    main()
