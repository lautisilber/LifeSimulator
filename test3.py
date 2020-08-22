import pygame
import numpy as np

class App:
    def __init__(self, size, world):
        pygame.init()

        self.size = size
        self.screen = pygame.display.set_mode((900, 600))

        self.running = True

        self.world = world

        self.gridSize = self.get_world_grid()

        print(self.gridSize)

    def get_world_grid(self):
        width = 900 / self.size[1]
        height = 600 / self.size[0]
        return (int(width), int(height))

    def draw_world(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):                
                if self.world[row][col]:
                    #self.draw_rect((col * self.gridSize[1], row * self.gridSize[0]), (self.gridSize[1], self.gridSize[0]), (255, 255, 255))
                    self.draw_quad((255, 255, 255), (row, col))
                    self.draw_quad((255, 255, 0), (row, col), 0.90)                  

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

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill((0, 0, 0))
            self.draw_world()
            pygame.display.update()
        pygame.quit()

def main():
    size = (4, 6)
    w = np.zeros(size, dtype=bool)
    w[2][2] = True
    #w[0][1] = True
    #w[1][0] = True
    #w[1][1] = True
    a = App(size, w)
    a.loop()

if __name__ == "__main__":
    main()