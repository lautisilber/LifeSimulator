
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
        # If the generated point on the line x = y then  
        # the perimeter points have already been printed  
        if x != y:
            print('papa')
            points.append((y + origin[0], x + origin[1]))
            points.append((-y + origin[0], x + origin[1]))
            points.append((y + origin[0], -x + origin[1]))  
            points.append((-y + origin[0], -x + origin[1]))

    return points

def midPointCircleFill(origin, radius):
    x = radius 
    y = 0
    # Printing the initial point the  
    # axes after translation  
    points = [(x + origin[0], y + origin[1])]
    # When radius is zero only a single  
    # point be printed  
    if (radius > 0) : 
        points.append((origin[0], origin[1]))
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
        # If the generated point on the line x = y then  
        # the perimeter points have already been printed  
        if x != y:
            points.append((y + origin[0], x + origin[1]))

    return points

def midPoint(X1,Y1,X2,Y2):  
    # calculate dx & dy 
    line = list()
    dx = X2 - X1  
    dy = Y2 - Y1    
    # initial value of decision parameter d  
    d = dy - (dx/2)  
    x = X1 
    y = Y1    
    # Plot initial given point  
    # putpixel(x,y) can be used to print pixel  
    # of line in graphics  
    line.append((x, y)) 
    # iterate through value of X  
    while (x < X2): 
        x=x+1
        # E or East is chosen 
        if(d < 0): 
            d = d + dy  
  
        # NE or North East is chosen  
        else: 
            d = d + (dy - dx)  
            y=y+1
        # Plot intermediate points  
        # putpixel(x,y) is used to print pixel  
        # of line in graphics  
        line.append((x, y))  
    return line

def main():
    import numpy as np
    world = np.zeros((15, 15), dtype=str)
    for i in range(len(world)):
        for n in range(len(world[0])):
            world[i][n] = '.'
    l = midPointCircleFill((7, 7), 5)
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
