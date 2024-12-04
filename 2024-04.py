NEEDLE = 'XMAS'

def main(text):
  lines = text.split('\n')
  assert isSquareMatrix(lines)

  verticalLines = [getVerticalString(lines, column) for column in range(0, len(lines))]

  maxDiagonalShift = len(lines) - len(NEEDLE) + 1
  minDiagonalShift = (maxDiagonalShift - 1) * -1
  topLeftDiagonalLines = [getDiagonalString(lines, shift) for shift in range(minDiagonalShift, maxDiagonalShift)]

  invertedMatrix = getInvertedMatrix(lines)
  topRightDiagonalLines = [getDiagonalString(invertedMatrix, shift) for shift in range(minDiagonalShift, maxDiagonalShift)]

  wordsFound = 0
  wordsFound += sum([line.count(NEEDLE) + line.count(NEEDLE[::-1]) for line in lines])
  wordsFound += sum([line.count(NEEDLE) + line.count(NEEDLE[::-1]) for line in verticalLines])
  wordsFound += sum([line.count(NEEDLE) + line.count(NEEDLE[::-1]) for line in topLeftDiagonalLines])
  wordsFound += sum([line.count(NEEDLE) + line.count(NEEDLE[::-1]) for line in topRightDiagonalLines])
  
  return wordsFound

def isSquareMatrix(matrix):
  lengths = [len(row) for row in matrix]
  if min(lengths) != max(lengths):
    return False
  if len(matrix) != lengths[0]:
    return False
  return True  

def getDiagonalString(matrix, shift=0):
  size = len(matrix) - 1
  diagonal = ''

  if shift >= 0:
    for row in range(0, size + 1):
      column = row + shift
      if column > size:
        continue
      diagonal += matrix[row][column]
  else:
    for column in range(0, size + 1):
      row = column + shift * -1
      if row > size:
        continue
      diagonal += matrix[row][column]

  return diagonal

def getInvertedMatrix(matrix):
  return [string[::-1] for string in reversed(matrix)]

def getVerticalString(matrix, column):
  verticalString = ''
  for row in matrix:
    verticalString += row[column]
  return verticalString


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
