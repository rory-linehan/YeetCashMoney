from datetime import datetime, timedelta
import pyautogui
import random
import time
from .. import common

# define module constants here
MODULE = 'mine_coal_barbarian_village'  # directory in vision/artifacts needs to match this
MATCH_THRESHOLD = 0.65
INVENTORY_THRESHOLD = 0.95
NAVIGATE_THRESHOLD = 0.65
BANK_THRESHOLD = 0.7
NO_REVERSE = False
REVERSE = True
BAIL = 150
INVENTORY_NUMBER = 24
SELECTOR_MATRIX = [
  'coal_inventory',
  'bank_window',
  'action_bar_full',
  'action_bar_empty',
  'sapphire',
  'ruby',
  'emerald',
  'diamond',
  'clue_geode'
]


def run(interval):
  # set up a bunch of variables used later
  end_time = datetime.now() + timedelta(seconds=interval)

  # all the strings to search for in filenames
  # that identify a specific object in Runescape
  OBJECT_SELECTOR =  [  # object matrix
    'coal_rock',
    'location_bank',
    'location_mine',
    'bank_booth',
  ]
  objects, path, COMMON_OBJECTS = common.load_objects(MODULE, OBJECT_SELECTOR, SELECTOR_MATRIX)
  if objects is not None and path is not None:
    # do not bot for longer than the configured time
    time.sleep(random.choice(range(1, 4)))
    while datetime.now() < end_time:
      inventory_box = common.calculate_inventory_box(
        [
          COMMON_OBJECTS['action_bar_full'],
          COMMON_OBJECTS['action_bar_empty']
        ],
        INVENTORY_THRESHOLD
      )
      print('inventory box: ' + str(inventory_box))
      print('checking for full inventory...')
      status, count = common.check_inventory(
        inventory_box,
        [
          COMMON_OBJECTS['coal_inventory'],
          COMMON_OBJECTS['sapphire'],
          COMMON_OBJECTS['ruby'],
          COMMON_OBJECTS['emerald'],
          COMMON_OBJECTS['diamond'],
          COMMON_OBJECTS['clue_geode']
        ],
        INVENTORY_THRESHOLD,
        INVENTORY_NUMBER
      )
      if status is True:
        print('inventory full ('+str(count)+'), navigating to bank...')
        common.navigate(
          path,
          objects['location_bank'],
          NAVIGATE_THRESHOLD,
          REVERSE
        )
        common.deposit(
          inventory_box,
          COMMON_OBJECTS,
          objects['bank_booth'],
          [
            COMMON_OBJECTS['coal_inventory'],
            COMMON_OBJECTS['sapphire'],
            COMMON_OBJECTS['ruby'],
            COMMON_OBJECTS['emerald'],
            COMMON_OBJECTS['diamond'],
            COMMON_OBJECTS['clue_geode']
          ],
          BANK_THRESHOLD,
          INVENTORY_THRESHOLD,
          INVENTORY_NUMBER
        )
        print('navigating to mine...')
        common.navigate(
          path,
          objects['location_mine'],
          NAVIGATE_THRESHOLD,
          NO_REVERSE
        )
      else:
        # if inventory empty, then check for bank and navigate to mine
        print('inventory: ' + str(count))
        if count == 0:
          result = common.find_object(
            objects['location_bank'][0],
            NAVIGATE_THRESHOLD
          )
          if result is not False:
            if len(result) > 0:
              print('navigating to mine...')
              common.navigate(
                path,
                objects['location_mine'],
                NAVIGATE_THRESHOLD,
                NO_REVERSE
              )
      time.sleep(random.choice(range(8, 12)))
      print('finding coal on screen...')
      coal = []
      while len(coal) == 0:
        for image in objects['coal_rock']:
          coal = common.find_object(
            image,
            MATCH_THRESHOLD
          )
          if len(coal) > 0:
            break
      print('found it!')
      common.move_mouse(
        coal[0][0] + common.offset('small'),
        coal[0][1] + common.offset('small'),
        'whenever'
      )
      pyautogui.click()
      common.move_mouse_randomish()
      print('waiting for inventory to change...')
      common.wait_for_inventory_to_change(
        inventory_box,
        [
          COMMON_OBJECTS['coal_inventory'],
          COMMON_OBJECTS['sapphire'],
          COMMON_OBJECTS['ruby'],
          COMMON_OBJECTS['emerald'],
          COMMON_OBJECTS['diamond'],
          COMMON_OBJECTS['clue_geode']
        ],
        INVENTORY_THRESHOLD,
        BAIL
      )
  return True
