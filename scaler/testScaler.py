import unittest

from scaler import (keyBreakdown, scaleMode, Modes, keySharps, keyFlats, enhIndex,
                    flatEnharmonic, sharpEnharmonic, noteOrder)

class TestKeyBreakdown(unittest.TestCase):
    def test_keyBreakdown(self):
        self.assertEqual(keyBreakdown(-7), ('Cb', 0, 7))
        self.assertEqual(keyBreakdown(-6), ('Gb', 0, 6))
        self.assertEqual(keyBreakdown(-5), ('Db', 0, 5))
        self.assertEqual(keyBreakdown(-4), ('Ab', 0, 4))
        self.assertEqual(keyBreakdown(-3), ('Eb', 0, 3))
        self.assertEqual(keyBreakdown(-2), ('Bb', 0, 2))
        self.assertEqual(keyBreakdown(-1), ('F', 0, 1))
        self.assertEqual(keyBreakdown(0), ('C', 0, 0))
        self.assertEqual(keyBreakdown(1), ('G', 1, 0))
        self.assertEqual(keyBreakdown(2), ('D', 2, 0))
        self.assertEqual(keyBreakdown(3), ('A', 3, 0))
        self.assertEqual(keyBreakdown(4), ('E', 4, 0))
        self.assertEqual(keyBreakdown(5), ('B', 5, 0))
        self.assertEqual(keyBreakdown(6), ('F#', 6, 0))
        self.assertEqual(keyBreakdown(7), ('C#', 7, 0))

    def test_scaleMode(self):
        # Major scale
        self.assertEqual(scaleMode(-7, Modes.Major), 
                         ['Cb', 'Db', 'Eb', 'Fb', 'Gb', 'Ab', 'Bb'])
        self.assertEqual(scaleMode(-6, Modes.Major), 
                         ['Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'F'])
        self.assertEqual(scaleMode(-5, Modes.Major), 
                         ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C'])
        self.assertEqual(scaleMode(-4, Modes.Major), 
                         ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G'])
        self.assertEqual(scaleMode(-3, Modes.Major), 
                         ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'])
        self.assertEqual(scaleMode(-2, Modes.Major), 
                         ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'])
        self.assertEqual(scaleMode(-1, Modes.Major), 
                         ['F', 'G', 'A', 'Bb', 'C', 'D', 'E'])
        self.assertEqual(scaleMode(0, Modes.Major), 
                         ['C', 'D', 'E', 'F', 'G', 'A', 'B'])
        self.assertEqual(scaleMode(1, Modes.Major), 
                         ['G', 'A', 'B', 'C', 'D', 'E', 'F#'])
        self.assertEqual(scaleMode(2, Modes.Major), 
                         ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'])
        self.assertEqual(scaleMode(3, Modes.Major), 
                         ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'])
        self.assertEqual(scaleMode(4, Modes.Major), 
                         ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'])
        self.assertEqual(scaleMode(5, Modes.Major), 
                         ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#'])
        self.assertEqual(scaleMode(6, Modes.Major), 
                         ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#'])
        self.assertEqual(scaleMode(7, Modes.Major), 
                         ['C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#'])

    def test_keySharps(self):
        self.assertEqual(keySharps(0), 'C')
        self.assertEqual(keySharps(1), 'G')
        self.assertEqual(keySharps(2), 'D')
        self.assertEqual(keySharps(3), 'A')
        self.assertEqual(keySharps(4), 'E')
        self.assertEqual(keySharps(5), 'B')
        self.assertEqual(keySharps(6), 'F#')
        self.assertEqual(keySharps(7), 'C#')

    def test_keyFlats(self):
        self.assertEqual(keyFlats(0), 'C')
        self.assertEqual(keyFlats(1), 'F')
        self.assertEqual(keyFlats(2), 'Bb')
        self.assertEqual(keyFlats(3), 'Eb')
        self.assertEqual(keyFlats(4), 'Ab')
        self.assertEqual(keyFlats(5), 'Db')
        self.assertEqual(keyFlats(6), 'Gb')
        self.assertEqual(keyFlats(7), 'Cb')

    def test_enharmonics(self):
        self.assertEqual(enhIndex('C#'), enhIndex('Db'))
        self.assertEqual(enhIndex('D#'), enhIndex('Eb'))
        self.assertEqual(enhIndex('E#'), enhIndex('F'))
        self.assertEqual(enhIndex('F#'), enhIndex('Gb'))
        self.assertEqual(enhIndex('G#'), enhIndex('Ab'))
        self.assertEqual(enhIndex('A#'), enhIndex('Bb'))
        self.assertEqual(enhIndex('B#'), enhIndex('C'))

        self.assertEqual(enhIndex('Cb'), enhIndex('B'))
        self.assertEqual(enhIndex('Fb'), enhIndex('E'))


        self.assertEqual(flatEnharmonic('C#'), 'Db')
        self.assertEqual(flatEnharmonic('D#'), 'Eb')
        self.assertEqual(flatEnharmonic('E#'), 'F')
        self.assertEqual(flatEnharmonic('E'), 'Fb')
        self.assertEqual(flatEnharmonic('F#'), 'Gb')
        self.assertEqual(flatEnharmonic('G#'), 'Ab')
        self.assertEqual(flatEnharmonic('A#'), 'Bb')
        self.assertEqual(flatEnharmonic('B'), 'Cb')
        self.assertEqual(flatEnharmonic('B#'), 'C')
        
        self.assertEqual(sharpEnharmonic('C'), 'B#')
        self.assertEqual(sharpEnharmonic('Db'), 'C#')
        self.assertEqual(sharpEnharmonic('Eb'), 'D#')
        self.assertEqual(sharpEnharmonic('Fb'), 'E')
        self.assertEqual(sharpEnharmonic('F'), 'E#')
        self.assertEqual(sharpEnharmonic('Gb'), 'F#')
        self.assertEqual(sharpEnharmonic('Ab'), 'G#')
        self.assertEqual(sharpEnharmonic('Bb'), 'A#')

    def test_noteOrder(self):
        self.assertEqual(noteOrder('B#'), 6)
        self.assertEqual(noteOrder('C'), 0)
        self.assertEqual(noteOrder('C#'), 0)
        self.assertEqual(noteOrder('Db'), 1)
        self.assertEqual(noteOrder('D'), 1)
        self.assertEqual(noteOrder('D#'), 1)
        self.assertEqual(noteOrder('Eb'), 2)
        self.assertEqual(noteOrder('E'), 2)
        self.assertEqual(noteOrder('Fb'), 3)
        self.assertEqual(noteOrder('E#'), 2)
        self.assertEqual(noteOrder('F'), 3)
        self.assertEqual(noteOrder('F#'), 3)
        self.assertEqual(noteOrder('Gb'), 4)
        self.assertEqual(noteOrder('G'), 4)
        self.assertEqual(noteOrder('G#'), 4)
        self.assertEqual(noteOrder('Ab'), 5)
        self.assertEqual(noteOrder('A'), 5)
        self.assertEqual(noteOrder('A#'), 5)
        self.assertEqual(noteOrder('Bb'), 6)
        self.assertEqual(noteOrder('B'), 6)
        self.assertEqual(noteOrder('Cb'), 0)

if __name__ == '__main__':
    unittest.main()
