import numpy as np
import random

class Roberto:
    @staticmethod
    def BiomeGenerator(shape, biomeCount, minRadius, maxRadius):
        world = np.zeros(shape, dtype=int)
        while True:
            origin = (random.randint(0, shape[0] - 1), random.randint(0, shape[1] - 1))
            chosenBiome = random.randint(1, biomeCount)
            radius = random.randint(minRadius, maxRadius)
            for r in range(radius):
                coords = Roberto.GetCircumferenceAroundOrigin(origin, r)
                for c in coords:
                    if c[0] < shape[0] and c[0] >= 0 and c[1] < shape[1] and c[1] >= 0:
                        world[c[1]][c[0]] = chosenBiome
            if not 0 in world:
                break
        print(world)
        return world
            

    @staticmethod
    def GetCircumferenceAroundOrigin(origin, radius):
        if radius == 0:
            return [origin]
        coords = [
            (origin[0] + radius, origin[1]),
            (origin[0], origin[1] + radius),
            (origin[0] - radius, origin[1]),
            (origin[0], origin[1] - radius)
        ]
        d = 0
        while True:
            d += 1
            newCoord = (coords[0][0] - d, coords[0][1] + d)
            if not (newCoord in coords):
                coords.append(newCoord)
            else:
                break
        d = 0
        while True:
            d += 1
            newCoord = (coords[1][0] - d, coords[1][1] - d)
            if not (newCoord in coords):
                coords.append(newCoord)
            else:
                break
        d = 0
        while True:
            d += 1
            newCoord = (coords[2][0] + d, coords[2][1] - d)
            if not (newCoord in coords):
                coords.append(newCoord)
            else:
                break
        d = 0
        while True:
            d += 1
            newCoord = (coords[3][0] + d, coords[3][1] + d)
            if not (newCoord in coords):
                coords.append(newCoord)
            else:
                break
        return coords

if __name__ == "__main__":
    #Roberto.BiomeGenerator((10, 10), 5, 2)
    l = Roberto.BiomeGenerator((20, 20), 4, 3, 7)
    print(l)