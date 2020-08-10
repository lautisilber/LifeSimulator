class DNA:
    @staticmethod
    def RmEnergy(org):
        assert isinstance(org, Org)
        org.energy -= 1

class Org:
    def __init__(self, energy):
        self.energy = energy

    def DoIt(self):
        DNA.RmEnergy(self)
        print(self.energy)

o = Org(10)
for _ in range(10):
    o.DoIt()
