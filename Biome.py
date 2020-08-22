class Biome:
    biomeNames = ['empty', 'grassland', 'forest', 'jungle', 'savanna', 'desert', 'wetland', 'tundra', 'artic', 'reef', 'marine', 'ocean']

    def __init__(self, index):
        self.index = index
        self.name = Biome.biomeNames[self.index]
        self.colour = Biome.GetColourFromName(self.name)
        self.light = Biome.GetLightFromName(self.name)
        self.temperature = Biome.GetTempFromName(self.name)
        self.humidity = Biome.GetHumFromName(self.name)
        self.organicDebris = 0

    @staticmethod
    def GetColourFromName(name):
        colDict = {
            'empty' : (192, 192, 192),
            'grassland' : (0, 255, 0),
            'forest' : (0, 135, 0),
            'jungle' : (153, 255, 102),
            'savanna' : (255, 153, 0),
            'desert' : (255, 255, 0),
            'wetland' : (0, 153, 153),
            'tundra' : (204, 255, 255),
            'artic' : (255, 255, 255),
            'reef' : (153, 255, 255),
            'marine' : (0, 255, 255),
            'ocean' : (0, 102, 204)
        }
        return colDict[name]

    @staticmethod 
    def GetLightFromName(name):
        # Light level is 0 - 100
        lightDict = {
            'empty' : 0,
            'grassland' : 70,
            'forest' : 60,
            'jungle' : 80,
            'savanna' : 90,
            'desert' : 100,
            'wetland' : 50,
            'tundra' : 40,
            'artic' : 20,
            'reef' : 80,
            'marine' : 50,
            'ocean' : 10
        }
        return lightDict[name]

    @staticmethod 
    def GetTempFromName(name):
        # Temperature level is 0 - 100
        tempDict = {
            'empty' : 0,
            'grassland' : 40,
            'forest' : 50,
            'jungle' : 80,
            'savanna' : 90,
            'desert' : 100,
            'wetland' : 50,
            'tundra' : 10,
            'artic' : 5,
            'reef' : 70,
            'marine' : 30,
            'ocean' : 15
        }
        return tempDict[name]

    @staticmethod 
    def GetHumFromName(name):
        # Humidity level is 0 - 100
        tempDict = {
            'empty' : 0,
            'grassland' : 50,
            'forest' : 60,
            'jungle' : 95,
            'savanna' : 35,
            'desert' : 5,
            'wetland' : 85,
            'tundra' : 25,
            'artic' : 5,
            'reef' : 100,
            'marine' : 100,
            'ocean' : 100
        }
        return tempDict[name]