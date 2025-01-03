import numpy as np
NEEDLE = 'XMAS'

def main(text):
  lines = text.split('\n')
  matrix = np.array([list(line) for line in lines])
  rows, columns = matrix.shape
  diagonals = np.arange(start=(rows - 1) * -1, stop=rows, step=1)
  assert rows == columns

  horisontal = lines
  vertical = [''.join(matrix[:,column]) for column in range(0, columns)]
  bottomLeft = [''.join(np.diagonal(matrix, offset=diagonal)) for diagonal in diagonals]
  bottomRight = [''.join(np.diagonal(np.fliplr(matrix), offset=diagonal)) for diagonal in diagonals]

  wordsFound = 0
  wordsFound += sum([line.count(NEEDLE) + line.count(NEEDLE[::-1]) for line in horisontal])
  wordsFound += sum([line.count(NEEDLE) + line.count(NEEDLE[::-1]) for line in vertical])
  wordsFound += sum([line.count(NEEDLE) + line.count(NEEDLE[::-1]) for line in bottomLeft])
  wordsFound += sum([line.count(NEEDLE) + line.count(NEEDLE[::-1]) for line in bottomRight])
  
  return wordsFound


fistSample = '''
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
'''.strip()

fistDebugSample = '''
....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
'''.strip()

with open('2024-04-input.txt') as f:
    wordSearchInput = f.read()


print(main(fistSample))
print(main(fistDebugSample))
print(main(wordSearchInput))
