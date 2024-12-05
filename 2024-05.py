from collections import defaultdict

def main(input):
  rules, updates = [section.split('\n') for section in input.split('\n\n')]
  pageOrder = getPageOrder(rules)

  validUpdates = []
  for update in updates:
    pagesUpdated = update.split(',')
    if isUpdateInValidOrder(pagesUpdated, pageOrder):
      validUpdates.append(pagesUpdated)

  middlePages = [update[len(update)//2] for update in validUpdates]

  return sum([int(page) for page in middlePages])

def getPageOrder(rules):
  order = defaultdict(set)
  for rule in rules:
    former, latter = rule.split('|')
    order[former].add(latter)
  return order

def isUpdateInValidOrder(pagesUpdated, pageOrder):
  for pageIndex, page in enumerate(pagesUpdated):
    nextPages = pageOrder[page]

    nextPageIndexes = []
    for nextPage in nextPages:
      try:
        nextPageIndexes.append(pagesUpdated.index(nextPage))
      except ValueError:
        continue

    if any([pageIndex > nextPageIndex for nextPageIndex in nextPageIndexes]):
      return False
  return True


sample = '''
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''.strip()


print(main(sample))
