import random

class DNA:
    # colour, acutism, feeding type, fotosynthesis, organic debris, carbos,
    # proteins, heal, vision, movement type, random movement chance, 2 targets movement
    
    structure = [6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 16]
    bases = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

    @staticmethod
    def GetDNAFromFlag(flag):
        if flag == 'rand' or flag == 'random':
            return DNA.GetRandomString()
        elif flag.startswith('semi') or flag.startswith('pseudo'):
            s = flag.split(' ')
            assert len(s) == 3
            return DNA.GetSemiRandomString(bool(s[1]), bool(s[2]))
        elif flag.startswith('raw'):
            s = flag.split(' ')
            assert len(s) == 2
            return DNA.GetDNAStringFromRaw(s[1])
        else:
            if ':' in flag and '-' in flag:
                assert sum(DNA.structure) == len(DNA.GetDNARawFromString(flag))
                return flag
            else:
                assert sum(DNA.structure) == len(flag)
                return DNA.GetDNAStringFromRaw(flag)
    
    @staticmethod
    def GetRandomString():
        s = ''
        for g in DNA.structure:
            for _ in range(g):
                s += random.choice(DNA.bases)
        return DNA.GetDNAStringFromRaw(s)

    @staticmethod
    def GetSemiRandomString(acuatic, feeding):
        s = ''
        for _ in range(DNA.structure[0]):
            s += random.choice(DNA.bases)

        if acuatic == 0:
            for _ in range(DNA.structure[1]):
                s += '0'
        elif acuatic == 1:
            for _ in range(DNA.structure[1]):
                s += 'F'
        else:
            for _ in range(DNA.structure[1]):
                s += random.choice(DNA.bases)

        if feeding == 0:
            for _ in range(DNA.structure[2]):
                s += '1'
        elif acuatic == 1:
            for _ in range(DNA.structure[2]):
                s += '5'
        elif acuatic == 2:
            for _ in range(DNA.structure[2]):
                s += '9'
        elif acuatic == 3:
            for _ in range(DNA.structure[2]):
                s += 'D'
        else:
            for _ in range(DNA.structure[2]):
                s += random.choice(DNA.bases)
        
                
        for g in DNA.structure[3:]:
            for _ in range(g):
                s += random.choice(DNA.bases)
        return DNA.GetDNAStringFromRaw(s)

    @staticmethod
    def GetCustomString(genes):
        assert len(genes) == len(DNA.structure)
        assert sum(DNA.structure) == sum([len(i) for i in genes])
        s = ''
        for g in genes:
            s += g
        return DNA.GetDNAStringFromRaw(s)

    @staticmethod
    def GetDNAStringFromRaw(raw):
        assert len(raw) == sum(DNA.structure)
        s = ''
        for i in range(len(DNA.structure)):
            s += str(i) + ':'
            carry = sum([i for i in DNA.structure[:i]])
            for n in range(DNA.structure[i]):
                s += raw[n + carry]
            s += '-'
        return s[:len(s) - 1]

    @staticmethod
    def GetDNARawFromString(string):
        s = string[string.find(':') + 1:]
        while True:
            if '-' in s:
                s = s.replace(s[s.find('-'):s.find(':')+1], '')
            else:
                break
        assert len(s) == sum(DNA.structure)
        return s        

#print(DNA.GetDNAStringFromRaw('FF00FF000000000000000000000000000000000000000000000000000000000000000077777777FFFFFFFF'))