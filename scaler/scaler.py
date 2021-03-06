from enum import Enum
import logging


class Modes(Enum):
    '''Enumerates the different scale modes'''
    Major = 1
    NaturalMinor = 2
    HarmonicMinor = 3
    MelodicMinor = 4

    @staticmethod
    def isMinor(mode):
        '''True if mode is one of the minor modes'''
        return (mode == Modes.NaturalMinor or mode == Modes.HarmonicMinor or 
                mode == Modes.MelodicMinor)


class Chords(Enum):
    '''Enumerates chords types'''
    Diminished = 1
    Minor = 2
    Major = 3
    Augmented = 4


logging.basicConfig(level=logging.DEBUG)

# 0 = C


scale_division = {}
scale_division[Modes.Major] = [2, 2, 1, 2, 2, 2, 1]
scale_division[Modes.NaturalMinor] = [2, 1, 2, 2, 1, 2, 2]
scale_division[Modes.HarmonicMinor] = [2, 1, 2, 2, 1, 3, 1]
scale_division[Modes.MelodicMinor] = [2, 1, 2, 2, 2, 2, 1]

scaleChords = {}
scaleChords[Modes.Major] = [Chords.Major, Chords.Minor, Chords.Minor,
                            Chords.Major, Chords.Major, Chords.Minor,
                            Chords.Diminished]
scaleChords[Modes.NaturalMinor] = [Chords.Minor, Chords.Diminished,
                                   Chords.Major, Chords.Minor, Chords.Minor,
                                   Chords.Major, Chords.Major]
scaleChords[Modes.HarmonicMinor] = [Chords.Minor, Chords.Diminished,
                                    Chords.Augmented, Chords.Minor,
                                    Chords.Major, Chords.Major,
                                    Chords.Diminished]
scaleChords[Modes.MelodicMinor] = [Chords.Minor, Chords.Diminished, 
                                   Chords.Major, Chords.Minor, Chords.Minor, 
                                   Chords.Major, Chords.Major]

class Key():
    keys = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 
            'Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F']
    keysm = ['A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 
             'Ab', 'Eb', 'Bb', 'F', 'C', 'G', 'D']

    def __init__(self, key_signature, mode):
        '''Key constructor. Checks the signature and generate scales'''
        Key.keyCheck(key_signature)
        self.signature = key_signature
        self.mode = mode

        self.buildEnharmonicScale()
        self.buildHarmonicScale()

        self.buildTriadScale()
        self.buildDegreeScale()

    def buildEnharmonicScale(self):
        enharmonic_root = Enharmonic.toIndex(self.getName())
        self.enharmonic_scale = [enharmonic_root]
        offset = 0
        for i in range(0, 6):
            offset += scale_division[self.mode][i]
            self.enharmonic_scale.append((enharmonic_root + offset) % 12)

    def buildHarmonicScale(self):
        tonic_order = Enharmonic.toOrder(self.getName())
        self.harmonic_scale = []
        self.triad_scale = []
        for i in range(0, 7):
            self.harmonic_scale.append(
                Enharmonic.toNote(self.enharmonic_scale[i], (i +
                                  tonic_order) % 7))

    def buildTriadScale(self):
        for i in range(1, 8):
            self.triad_scale.append(self.buildTriad(i))

    def buildDegreeScale(self):
        degrees = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']
        self.degree_scale= []
        deg_list = []
        typ_list = []

        for i in range(0, 7):
            lowT = Enharmonic.interval(
                Enharmonic.toIndex(self.triad_scale[i][0]),
                Enharmonic.toIndex(self.triad_scale[i][1]))
            highT = Enharmonic.interval(
                Enharmonic.toIndex(self.triad_scale[i][1]),
                Enharmonic.toIndex(self.triad_scale[i][2]))

            typ = 'undef'

            low = lowT[0]
            high = highT[0]
            if low == 3:
                if high == 3:
                    typ = 'd'
                    deg = degrees[i].lower() + u'\xb0'
                elif high == 4:
                    typ = 'm'
                    deg = degrees[i].lower()
            elif low == 4:
                if high == 3:
                    typ = 'M'
                    deg = degrees[i].upper()
                elif high == 4:
                    typ = 'A'
                    deg = degrees[i].upper() + '+'

            if typ == 'undef':
                print(low, high)

            self.degree_scale.append((typ, deg))

    def getEnharmonicScale(self):
        '''Returns the scale with enharmonic index'''
        return self.enharmonic_scale

    def getHarmonicScale(self):
        '''Returns the scale with note names'''
        return self.harmonic_scale

    def getChordScale(self):
        '''Returns '''
        return self.triad_scale

    def ppChordScale(self):
        '''Pretty-prints the chord scale'''
        r = ''
        r += '-'*43
        r += '\n'
        # Scale
        for i in range(2, -1, -1):
            r += '| {:3s} | {:3s} | {:3s} | {:3s} | {:3s} | {:3s} | {:3s} |\n'.format(
                self.triad_scale[0][i],
                self.triad_scale[1][i],
                self.triad_scale[2][i],
                self.triad_scale[3][i],
                self.triad_scale[4][i],
                self.triad_scale[5][i],
                self.triad_scale[6][i])


        r += '\n'
        r += '-'*43
        # Chords
        

        r += '\n'
        r += '|'
        for i in range(0, 7):
            r += ' {:3s}{}|'.format(self.triad_scale[i][0],
                                    self.degree_scale[i][0])
        r += '\n'
        r += '|'
        for i in range(0, 7):
            r += ' {:4s}|'.format(self.degree_scale[i][1])
        r += '\n'

        return r

    def getCircleProgression(self):
        progression = []
        curr = 0
        for i in range(0, 7):
            progression.append((self.degree_scale[curr % 7][1]))
            curr += 3

        return progression

    def isMinor(self):
        '''Returns True if key is minor'''
        return Modes.isMinor(self.mode)

    def getName(self):
        '''Gives the name of the key corresponding to the signature'''
        if self.isMinor():
            return Key.keysm[self.signature]
        else:
            return Key.keys[self.signature]

    def degreeOf(self, note_name):
        '''Returns the degree of a note'''
        if note_name in harmonic_scale:
            return harmonic_scale.index(note_name) + 1

    def buildTriad(self, degree):
        '''Builds a triad for degree in the key'''
        return [self.harmonic_scale[(degree - 1) % 7],
                self.harmonic_scale[(degree - 1 + 2) % 7], 
                self.harmonic_scale[(degree - 1 + 4) % 7]]

    def print(self):
        print('Key : ', self.getName(), 'm' if self.isMinor() else '')
        #print('Scale : ', self.getEnharmonicScale())
        print('Scale : ', self.getHarmonicScale())
        print('Chords')
        self.ppChordScale()
        print('Circle : ', self.getCircleProgression())


    @staticmethod
    def keyCheck(key_signature):
        '''Checks validity of a key signature'''
        if key_signature < -7 or key_signature > 7:
            raise Exception("not a key")

    @staticmethod
    def sharps(key_signature):
        return abs(key_signature) if key_signature >= 0 else 0

    @staticmethod
    def flats(key_signature):
        return abs(key_signature) if not key_signature >= 0 else 0

    @staticmethod
    def keySharps(number):
        '''
        Returns the key which has number of sharps
        :param number: number of sharps
        :type number: int

        :return: The key name
        :rtype: KeyName
        '''
        if number > 7 or number < 0:
            raise Exception("invalid parameter")
        return keys[number]

    @staticmethod
    def keyFlats(number):
        '''Returns the key which has number of flats'''
        if number > 7 or number < 0:
            raise Exception("invalid parameter")
        return keys[-number]


class Enharmonic():
    dflat = ['Dbb', 'Db', 'Ebb', 'Eb', 'Fb', 'Gbb', 'Gb', 'Abb', 'Ab', 'Bbb', 
            'Bb', 'Cb']
    flat = ['C', 'Db', 'D', 'Eb', 'Fb', 'F', 'Gb', 'G', 'Ab', 'A', 
           'Bb', 'Cb']
    dsharp = ['B##', 'C#', 'C##', 'D#', 'D##', 'E#', 'F#', 'F##', 'G#', 'G##',
            'A#', 'A##']
    sharp = ['B#', 'C#', 'D', 'D#', 'E', 'E#', 'F#', 'G', 'G#', 'A',
            'A#', 'B']

    order_set = 'CDEFGAB'

    def __init__(self, index):
        Enharmonic.enhCheck(index)
        self.index = index

    @staticmethod
    def enhCheck(enh_index):
        if enh_index < 0 or enh_index > 11:
            raise Exception("not an enharmonic index")

    @staticmethod
    def toIndex(note_name):
        '''Gets the enharmonic number for note_name'''
        if note_name in Enharmonic.sharp:
            return Enharmonic.sharp.index(note_name)
        elif note_name in Enharmonic.flat:
            return Enharmonic.flat.index(note_name)
        elif note_name in Enharmonic.dflat:
            return Enharmonic.dflat.index(note_name)
        elif note_name in Enharmonic.dsharp:
            return Enharmonic.dsharp.index(note_name)
        else:
            raise Exception("no such note" + str(note_name))

    @staticmethod
    def toNote(enh_index, targetOrder):
        if Enharmonic.toOrder(Enharmonic.flat[enh_index]) == targetOrder:
            return Enharmonic.flat[enh_index]
        elif Enharmonic.toOrder(Enharmonic.sharp[enh_index]) == targetOrder:
            return Enharmonic.sharp[enh_index]
        elif Enharmonic.toOrder(Enharmonic.dflat[enh_index]) == targetOrder:
                return Enharmonic.dflat[enh_index]
        elif Enharmonic.toOrder(Enharmonic.dsharp[enh_index]) == targetOrder:
            return Enharmonic.dsharp[enh_index]
        else:
            print("(enhDeg: " + str(enh_index) + " target: " + str(targetOrder) + 
                  ")")
            print("Candidates were : " + flatEnharmonics[enh_index] + " and " + 
                  sharpEnharmonics[enh_index])
            print("minor " + dflatEnharmonics[enh_index])
            raise Exception("degree lookup failed")


    @staticmethod
    def toOrder(note_name):
        letter = note_name[0]
        return Enharmonic.order_set.index(letter)

    @staticmethod
    def interval(enh1, enh2):
        intervals = [(0, 'P1'),
                     (1, 'm2'),
                     (2, 'M2'),
                     (3, 'm3'),
                     (4, 'M3'),
                     (5, 'P4'),
                     (6, 'A4'), 
                     (7, 'P5'), 
                     (8, 'm6'),
                     (9, 'M6'),
                     (10, 'm7'), 
                     (11, 'M7'),
                     (12, 'P8')]
        delta = (enh2 - enh1) % 12
        return intervals[delta]

if __name__ == '__main__':
    #for i in range(-7, 8):
    for m in Modes:
        k = Key(-2, m)
        print(k.ppChordScale())
