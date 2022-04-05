from datetime import datetime, timedelta
import pyautogui
import random
import time
from .. import common

# define module constants here
MODULE = 'mine_coal_mining_guild'  # directory in vision/artifacts needs to match this
MATCH_THRESHOLD = 0.8
INVENTORY_THRESHOLD = 0.95
NAVIGATE_THRESHOLD = 0.7
NO_REVERSE = False
REVERSE = True
BAIL = 100
INVENTORY_NUMBER = 26
COMMON_SELECTOR = [
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
MODULE_SELECTOR = [
  'coal_rock',
  'bank_chest',
  'coal_spot',
  'bank_chest',
  'in_place'
]


def run(input):
  # set up a bunch of variables used later
  end_time = datetime.now() + timedelta(seconds=input['interval'])
  objects, path, common_objects = common.load_objects(MODULE, MODULE_SELECTOR, COMMON_SELECTOR)
  inventory_box = common.calculate_inventory_box(
    [
      common_objects['inventory_box_empty']
    ],
    MATCH_THRESHOLD
  )
  print('inventory box: ' + str(inventory_box))
  # do not bot for longer than the configured time
  while datetime.now() < end_time:
    objects, path, common_objects = common.load_objects(MODULE, MODULE_SELECTOR, COMMON_SELECTOR)
    inventory_items = [
      common_objects['coal_inventory'],
      common_objects['sapphire'],
      common_objects['ruby'],
      common_objects['emerald'],
      common_objects['diamond'],
      common_objects['clue_geode']
    ]
    print('checking for full inventory...')
    full, count = common.check_inventory(
      inventory_box,
      inventory_items,
      INVENTORY_THRESHOLD,
      INVENTORY_NUMBER
    )
    if full is True:
      print('inventory full ('+str(count)+'), depositing...')
      bank_is_open = False
      while bank_is_open is False:
        # find and click the bank chest
        for image in objects['bank_chest']:
          result = common.find_object(
            image,
            MATCH_THRESHOLD
          )
          if len(result) > 0:
            common.move_mouse(
              result[0][0] + common.offset('tiny'),
              result[0][1] + common.offset('tiny'),
              'whenever'
            )
            pyautogui.leftClick()
            break
        time.sleep(random.choice(range(4, 6)))
        # let's make sure the bank window is actually open
        for image in common_objects['bank_window']:
          result = common.find_object(
            image,
            MATCH_THRESHOLD
          )
          if len(result) > 0:
            bank_is_open = True
      # deposit items
      deposited = False
      while deposited is False:
        for item in inventory_items:
          print('depositing item: ' + str(item))
          for image in item:
            result = common.find_object(
              image,
              INVENTORY_THRESHOLD
            )
            if len(result) > 0:
              # we only want to select items within the inventory, given by `box`
              if (inventory_box[0][0] < result[0][0] < inventory_box[1][0]) and \
                  (inventory_box[0][1] < result[0][1] < inventory_box[1][1]):
                common.move_mouse(
                  result[0][0] + common.offset('tiny'),
                  result[0][1] + common.offset('tiny'),
                  'now'
                )
                pyautogui.leftClick()
                break
          full, count = common.check_inventory(
            inventory_box,
            inventory_items,
            INVENTORY_THRESHOLD,
            INVENTORY_NUMBER
          )
          if count == 0:
            deposited = True
            break
          else:
            print('inventory still has something in it: (' + str(count) + ')')
    else:
      print('heading to mining spot...')
      in_place = False
      while in_place is False:
        common.move_mouse_randomish()
        for image in objects['coal_spot']:
          result = common.find_object(
            image,
            NAVIGATE_THRESHOLD
          )
          if len(result) > 0:
            common.move_mouse(
              result[0][0] + common.offset('tiny'),
              result[0][1] + common.offset('tiny'),
              'whenever'
            )
            pyautogui.leftClick()
            time.sleep(random.choice(range(8, 10)))
        for image in objects['in_place']:
          result = common.find_object(
            image,
            MATCH_THRESHOLD
          )
          if len(result) > 0:
            in_place = True
      print('mining coal...')
      full = False
      while full is False:
        for image in objects['coal_rock']:
          result = common.find_object(
            image,
            MATCH_THRESHOLD
          )
          if len(result) > 0:
            common.move_mouse(
              result[0][0] + common.offset('small'),
              result[0][1] + common.offset('small'),
              'now'
            )
            pyautogui.leftClick()
            common.move_mouse_randomish()
            common.wait_for_inventory_to_change(
              inventory_box,
              inventory_items,
              INVENTORY_THRESHOLD,
              BAIL
            )
            if count >= INVENTORY_NUMBER - 2:
              break
        full, count = common.check_inventory(
          inventory_box,
          inventory_items,
          INVENTORY_THRESHOLD,
          INVENTORY_NUMBER
        )
        print('inventory count: ' + str(count))
  return True
