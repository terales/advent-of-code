def main(reportsPile):
  safeReportCount = 0
  reports = reportsPile.split('\n')
  measurementsRaw = [report.split(' ') for report in reports]
  
  measurements = []
  for report in measurementsRaw:
    measurements.append([int(raw) for raw in report])

  for report in measurements:
    # print(report, 'monotonic' if isMonotonic(report) else 'fluctuating', 'gradual' if isGradual(report) else 'sudden')
    if isMonotonic(report) and isGradual(report):
      safeReportCount += 1

  print(safeReportCount)

def isMonotonic(report):
  previousDirection = None

  for index, measurement in enumerate(report):
    try:
      measurementNext = report[index + 1]
    except IndexError:
      break
    
    direction = measurement > measurementNext if measurement != measurementNext else None

    if previousDirection != direction and previousDirection is not None:
      return False
    else:
      previousDirection = direction
    
  return True

def isGradual(report):
  for index, measurement in enumerate(report):
    try:
      measurementNext = report[index + 1]
    except IndexError:
      break

    change = abs(measurement - measurementNext)

    if not (change >= 0 and change <= 3):
      return False
  return True

reportsPile = '''
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
'''.strip()

main(reportsPile)