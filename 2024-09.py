def main(disk_map):
  disk = build_layout(disk_map)
  compacted_disk = compact_layout(disk)
  return calc_checksum(compacted_disk)

def build_layout(disk_map):
  disk_map_iter = iter(disk_map + '0')
  disk = []
  file_id = 0
  for file_size, space_size in zip(disk_map_iter, disk_map_iter):
    disk += [file_id] * int(file_size)
    disk += [None] * int(space_size)
    file_id += 1
  return disk

def compact_layout(disk):
  compacted = disk.copy()
  while True:
    try:
      fist_empty_index = compacted.index(None)
    except ValueError:
      break
    compacted[fist_empty_index] = compacted.pop()    
  return compacted

def calc_checksum(disk):
  checksum = 0
  for block_position, file_id in enumerate(disk):
    if file_id is not None:
      checksum += block_position * int(file_id)
  return checksum

def _test(name, expected, actual):
  return 'Test {name}.\nExpected: {expected},\nActual:   {actual}\n'.format(
    name=name,
    expected=expected,
    actual=actual
  )

sample = '''
2333133121414131402
'''.strip()

print(_test(
  'layout',
  '00...111...2...333.44.5555.6666.777.888899',
  ''.join([str(block) if block is not None else '.' for block in build_layout(sample)])
))
print(_test(
  'compacting',
  '0099811188827773336446555566',
  ''.join([str(block) if block is not None else '.' for block in compact_layout(build_layout(sample))])
))
print(_test(
  'checksum',
  1928,
  calc_checksum(compact_layout(build_layout(sample)))
))

print(main(sample))
