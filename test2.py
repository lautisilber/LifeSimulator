width, height = 10, 10
map_= [['·' for x in range(width)]for y in range(height)]

def FillCircle(origin, radius):    
    a, b = radius - 1, radius - 1
    r = radius
    epsilon_ = 2.2
    points = list()

    for y in range(height):
        for x in range(width):
            if (x-a)**2 + (y-b)**2 <= (r**2 - epsilon_**2):
                points.append((y - a + origin[0], x - b + origin[1]))
    return points

l = FillCircle((3, 300), 4)

print(l)
print('---')

for p in l:
    map_[p[0]][p[1]] = "#"
for line in map_:
    print(' '.join(line))