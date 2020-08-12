
# Python3 program for implementing  
# Mid-Point Circle Drawing Algorithm  
  
def midPointCircleDraw(origin, radius):
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
        #raster
        for i in range(1, radius):
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
            points.append((i + origin[0], y + origin[1]))
            points.append((-i + origin[0], y + origin[1]))
            points.append((i + origin[0], -y + origin[1]))
            points.append((-i + origin[0], -y + origin[1]))
        # If the generated point on the line x = y then  
        # the perimeter points have already been printed  
        if x != y:
            print('papa')
            points.append((y + origin[0], x + origin[1]))
            points.append((-y + origin[0], x + origin[1]))
            points.append((y + origin[0], -x + origin[1]))  
            points.append((-y + origin[0], -x + origin[1]))
            # raster
    return points

def main():
    import numpy as np
    world = np.zeros((15, 15), dtype=str)
    for i in range(len(world)):
        for n in range(len(world[0])):
            world[i][n] = '.'
    l = midPointCircleDraw((7, 7), 5)
    for c in l:
        if c[0] >= 0 and c[0] < 15 and c[1] >= 0 and c[1] < 15:
            world[c[0]][c[1]] = '@'
    print(world)
                              
# Driver Code 
if __name__ == '__main__': 
      
    # To draw a circle of radius 3  
    # centred at (0, 0)  
    main()
  
  
# Contributed by: SHUBHAMSINGH10 
# Improved by: siddharthx_07 
