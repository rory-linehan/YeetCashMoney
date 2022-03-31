#!/usr/local/bin/python3.7

import argparse
import sys
import os
#import pypvpnctl
import common
from flip import flipper
from bot.ml.vision.factory import train as vision_train


class DirContext:
  def __init__(self, dir):
    self._dir = dir

  def __enter__(self):
    self._cwd = os.getcwd()
    os.chdir(self._dir)
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    os.chdir(self._cwd)


parser = argparse.ArgumentParser(description='yeet cash money runner')
parser.add_argument('--mode', type=str, required=True, help='mode to run: [bot,flip]')
parser.add_argument('--config', type=str, required=True)
parser.add_argument('--vpn', action='store_true', help='use the integrated VPN functionality')
parser.add_argument('--train', action='store_true', help='train models and exit')
parser.add_argument('--classic', action='store_true', help='classic rules-based workflow')
parser.add_argument('--ml', action='store_true', help='machine learning workflow')
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()

if __name__ == "__main__":
  if args.train:
    with DirContext('ml/vision'):
      status, response = vision_train(9)  # why does the training break down if the anchors != 9?
      sys.exit(0)
  else:
    while True:
      status, response = common.get_config(args.config)
      if status is True:
        config = response[args.mode]
        if args.mode == 'flip':
          with DirContext('flip'):
            flipper.do(response[args.mode])
        elif args.mode == 'bot':
          for account in config['accounts']:
            # if args.vpn:
            #     status, message, response = pypvpnctl.connect(
            #         account['vpn']['name'],
            #         'tcp'
            #     )
            #     if status is not True:
            #         print(message)
            #         sys.exit(1)
            #rl = common.runelite()
            rl = None
            status, message = login.do(
              rl,
              account['name'],
              account['username'],
              account['password']
            )
            if status is True:
              if args.classic:
                for activity in account['activities']:
                  action = globals()[activity['name']]
                  with DirContext('bot'):
                    action.run(activity['schedule']['seconds'])
              elif args.ml:
                print("machine learning workflow not implemented")
                sys.exit(1)
            else:
              print('failed to login to account: ' + message)
            # if args.vpn:
            #     status, message, response = pypvpnctl.disconnect()
            #     if status is False:
            #         print(message)
            #         sys.exit(1)
            #     else:
            #         print('disconnected from vpn')
        else:
          print('--mode parameter invalid, expecting [flip,bot]')
          sys.exit(1)
      else:
        print('failed to load config: ' + response)
        sys.exit(1)
