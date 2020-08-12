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
            coords = Roberto.GetCircleAroundOrigin(origin, radius)
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
    def GetCircleAroundOrigin(origin, radius):
        # adapted from https://www.geeksforgeeks.org/mid-point-circle-drawing-algorithm/
        # kudos to geeksforgeeks.org
        x = radius 
        y = 0
        # Printing the initial point the  
        # axes after translation  
        points = [(x + origin[0], y + origin[1])]
        # When radius is zero only a single  
        # point be printed  
        if (radius > 0) : 
            points.append((origin[0], origin[1]))
            points.append((-x + origin[0], -y + origin[1]))
            points.append((y + origin[0], x + origin[1]))
            points.append((-y + origin[0], -x + origin[1]))
            #raster mid line
            for i in range(1, radius):
                print('epa')
                points.append((i + origin[0], origin[1]))
                points.append((-i + origin[0], origin[1]))
        # Initialising the value of P  
        P = 1 - radius  
        while x > y: 
            y += 1
            # Mid-point inside or on the perimeter 
            if P <= 0:  
                P = P + 2 * y + 1
            # Mid-point outside the perimeter  
            else:          
                x -= 1
                P = P + 2 * y - 2 * x + 1
            # All the perimeter points have  
            # already been printed  
            if (x < y): 
                break
            # Printing the generated point its reflection  
            # in the other octants after translation  
            points.append((x + origin[0], y + origin[1]))
            points.append((-x + origin[0], y + origin[1]))
            points.append((x + origin[0], -y + origin[1]))  
            points.append((-x + origin[0], -y +origin[1]))
            # raster 
            points.append((origin[0], y + origin[1]))
            points.append((origin[0], -y + origin[1]))
            for i in range(1, x):
                print('apa')
                points.append((i + origin[0], y + origin[1]))
                points.append((-i + origin[0], y + origin[1]))
                points.append((i + origin[0], -y + origin[1]))
                points.append((-i + origin[0], -y + origin[1]))
            # If the generated point on the line x = y then  
            # the perimeter points have already been printed  
            if x != y: 
                points.append((y + origin[0], x + origin[1]))
                points.append((-y + origin[0], x + origin[1]))
                points.append((y + origin[0], -x + origin[1]))  
                points.append((-y + origin[0], -x + origin[1]))
        return points

if __name__ == "__main__":
    #Roberto.BiomeGenerator((10, 10), 5, 2)
    l = Roberto.BiomeGeneratorCircle((20, 10), 4, 3, 7)
    print(l)