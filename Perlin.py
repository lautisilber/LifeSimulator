import noise
import numpy as np

class Perlin:
    @staticmethod
    def Perlin(shape, scale, octaves, persistence, lacunarity):
        assert len(shape) == 2
        world = np.zeros(shape)
        for i in range(shape[0]):
            for j in range(shape[1]):
                world[i][j] = noise.pnoise2(i/scale, 
                                            j/scale, 
                                            octaves=octaves, 
                                            persistence=persistence, 
                                            lacunarity=lacunarity, 
                                            repeatx=1024, 
                                            repeaty=1024, 
                                            base=0)
        return world.tolist()

if __name__ == "__main__":
    l = Perlin.Perlin((512, 512), 100, 6, 0.5, 2)
    print(l)