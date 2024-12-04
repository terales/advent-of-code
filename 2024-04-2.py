def main(text):
  lines = text.split('\n')
  matrix = [list(line) for line in lines]
  assert isSquareMatrix(matrix)

  aPositions = getAPositions(matrix)
  validStrokes = ['MS', 'SM']
  validCrossCount = 0

  for aRow, aColumn in aPositions:
    strokeTopLeft = matrix[aRow - 1][aColumn - 1] + matrix[aRow + 1][aColumn + 1]
    strokeBottomLeft = matrix[aRow + 1][aColumn - 1] + matrix[aRow - 1][aColumn + 1]

    if strokeTopLeft in validStrokes and strokeBottomLeft in validStrokes:
      validCrossCount += 1

  return validCrossCount

def getAPositions(matrix):
  aPositions = []
  start = 1
  stop = len(matrix) - 1

  for row in range(start, stop):
    for column in range(start, stop):
      cell = matrix[row][column]
      if cell == 'A':
        aPositions.append((row, column))

  return aPositions

def isSquareMatrix(matrix):
  lengths = [len(row) for row in matrix]
  if min(lengths) != max(lengths):
    return False
  if len(matrix) != lengths[0]:
    return False
  return True


sample = '''
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

debugSample = '''
.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
'''.strip()

with open('2024-04-input.txt') as f:
    wordSearchInput = f.read()


print(main(sample))
print(main(debugSample))
print(main(wordSearchInput))
