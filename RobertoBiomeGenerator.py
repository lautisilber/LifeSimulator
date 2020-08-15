import numpy as np
import random

class Roberto:
    @staticmethod
    def BiomeGeneratorDiamond(shape, biomeCount, minRadius, maxRadius):
        inverseShape = (shape[1], shape[0])
        world = np.zeros(inverseShape, dtype=int)
        while True:
            origin = (random.randint(0, inverseShape[0] - 1), random.randint(0, inverseShape[1] - 1))
            chosenBiome = random.randint(1, biomeCount)
            radius = random.randint(minRadius, maxRadius)
            for r in range(radius):
                coords = Roberto.GetDiamondAroundOrigin(origin, r)
                for c in coords:
                    if c[0] < inverseShape[0] and c[0] >= 0 and c[1] < inverseShape[1] and c[1] >= 0:
                        world[c[0]][c[1]] = chosenBiome
            if not 0 in world:
                break
        return world.tolist()

    @staticmethod
    def BiomeGeneratorCircle(shape, biomeCount, minRadius, maxRadius):
        inverseShape = (shape[1], shape[0])
        world = np.zeros(inverseShape, dtype=int)
        while True:
            origin = (random.randint(0, inverseShape[0] - 1), random.randint(0, inverseShape[1] - 1))
            chosenBiome = random.randint(1, biomeCount)
            radius = random.randint(minRadius, maxRadius)
            coords = Roberto.FillCircle(origin, radius, shape)
            for c in coords:
                if c[0] < inverseShape[0] and c[0] >= 0 and c[1] < inverseShape[1] and c[1] >= 0:
                    world[c[0]][c[1]] = chosenBiome
            if not 0 in world:
                break
        print (world)
        return world.tolist()

    @staticmethod
    def GetDiamondAroundOrigin(origin, radius):
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

    @staticmethod
    def FillCircle(origin, radius, shape):    
        a, b = radius - 1, radius - 1
        r = radius
        epsilon_ = 2.2
        points = list()

        for y in range(shape[1]):
            for x in range(shape[0]):
                if (x-a)**2 + (y-b)**2 <= (r**2 - epsilon_**2):
                    points.append((y - a + origin[0], x - b + origin[1]))
        return points

if __name__ == "__main__":
    #Roberto.BiomeGenerator((10, 10), 5, 2)
    l = Roberto.BiomeGeneratorCircle((20, 10), 4, 3, 7)
    print(l)