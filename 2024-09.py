from collections import defaultdict

class Chunk:
  from_: int
  to: int

def main(disk_map):
  disk = build_layout(disk_map)
  compacted_disk = compact_layout(disk)
  return calc_checksum(compacted_disk)

def mainDefragmented(disk_map):
  disk = build_layout(disk_map)
  compacted_disk = consolidate_layout(disk)
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
      compacted[fist_empty_index] = compacted.pop()
    except (ValueError, IndexError):
      break
  return compacted

def consolidate_layout(disk):
  compacted = disk.copy()
  files_hash, space_hash = create_chunks_hashmap(disk)
  space_list = list(space_hash.values())

  for file_id, file in reversed(files_hash.items()):
    for space_index, space in enumerate(space_list):
      space_len = space.to - space.from_ + 1
      file_len = file.to - file.from_ + 1

      if (space.from_ > file.from_):
        continue
      
      if (file_len <= space_len):
        for block_index in range(space.from_, space.from_ + file_len):
          compacted[block_index] = file_id

        for block_index in range(file.from_, file.from_ + file_len):
          compacted[block_index] = None
        
        space.from_ = space.from_ + file_len
        if space.from_ > space.to:
          del space_list[space_index]

        break

  return compacted

def create_chunks_hashmap(disk):
  files_hash = defaultdict(Chunk)
  space_hash = defaultdict(Chunk)
  last_file_id = 0

  for position, block in enumerate(disk):
    if block is None:
      chunk = space_hash[last_file_id]
    else:
      chunk = files_hash[block]
      last_file_id = block

    chunk.from_ = position if not hasattr(chunk, 'from_') else chunk.from_
    chunk.to = position

  return files_hash, space_hash

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

with open('2024-09-input.txt') as f:
    challengeInput = f.read()

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
print(_test(
  'consolidating',
  '00992111777.44.333....5555.6666.....8888..',
  ''.join([str(block) if block is not None else '.' for block in consolidate_layout(build_layout(sample))])
))
print(_test(
  'consolidated checksum',
  2858,
  calc_checksum(consolidate_layout(build_layout(sample)))
))

print('Challenge one:', main(challengeInput))
print('Challenge two:', mainDefragmented(challengeInput))
