# this script parses my windows path from
# labelImg's PascalVOC formatted XML annotation files

import os
import argparse

argparser = argparse.ArgumentParser(
  description='convert windows env paths to linux paths')

argparser.add_argument(
  '--prefix',
  help='prefix to remove: everything up to root YCM directory',
  required=True)
argparser.add_argument(
  '--new',
  help='replace with this',
  required=True)

if __name__ == '__main__':
  args = argparser.parse_args()
  for file in os.listdir('annotations'):
    with open(os.path.join('annotations', file), 'rt') as read:
      xml = read.read()
      xml = xml.replace(args.prefix, args.new).replace('\\', '/')
      with open(os.path.join('annotations', file), 'wt') as write:
        write.write(xml)
