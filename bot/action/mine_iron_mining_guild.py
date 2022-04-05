from datetime import datetime, timedelta
import pyautogui
import random
import time
from .. import common

# define module constants here
MODULE = 'mine_iron_mining_guild'  # directory in vision/artifacts needs to match this
MATCH_THRESHOLD = 0.8
INVENTORY_THRESHOLD = 0.95
NAVIGATE_THRESHOLD = 0.7
NO_REVERSE = False
REVERSE = True
BAIL = 5
INVENTORY_NUMBER = 26
COMMON_SELECTOR = [
  'iron_inventory',
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
  'iron_rock',
  'bank_chest',
  'iron_spot',
  'bank_chest',
  'in_place'
]


def run(input):
  # set up a bunch of variables used later
  end_time = datetime.now() + timedelta(seconds=input['interval'])
  objects, path, common_objects = common.load_objects(MODULE, MODULE_SELECTOR, COMMON_SELECTOR)
  if objects is not None and path is not None:
    inventory_items = [
      common_objects['iron_inventory'],
      common_objects['sapphire'],
      common_objects['ruby'],
      common_objects['emerald'],
      common_objects['diamond'],
      common_objects['clue_geode']
    ]
    # do not bot for longer than the configured time
    while datetime.now() < end_time:
      inventory_box = common.calculate_inventory_box(
        [
          common_objects['action_bar_full'],
          common_objects['action_bar_empty']
        ],
        INVENTORY_THRESHOLD
      )
      print('inventory box: ' + str(inventory_box))
      print('checking for full inventory...')
      status, count = common.check_inventory(
        inventory_box,
        inventory_items,
        INVENTORY_THRESHOLD,
        INVENTORY_NUMBER
      )
      if status is True:
        print('inventory full ('+str(count)+'), depositing...')
        bank_is_open = False
        while bank_is_open is False:
          # find and click the bank chest
          for image in objects['bank_chest']:
            result = common.find_object(image, MATCH_THRESHOLD)
            if len(result) > 0:
              pyautogui.moveTo(
                result[0][0] + common.offset('tiny'),
                result[0][1] + common.offset('tiny'),
                0.1
              )
              pyautogui.leftClick()
              break
          time.sleep(random.choice(range(4, 6)))
          # let's make sure the bank window is actually open
          for image in common_objects['bank_window']:
            result = common.find_object(image, MATCH_THRESHOLD)
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
                  x = result[0][0]
                  y = result[0][1]
                  common.move_mouse(
                    x + random.choice(range(2, 7)),
                    y + random.choice(range(2, 7)),
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
          for image in objects['iron_spot']:
            result = common.find_object(
              image,
              NAVIGATE_THRESHOLD
            )
            if len(result) > 0:
              pyautogui.moveTo(
                result[0][0] + 15,
                result[0][1] + 15,
                0.1
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
        print('mining iron...')
        inventory_full = False
        while inventory_full is False:
          for image in objects['iron_rock']:
            iron = common.find_object(
              image,
              MATCH_THRESHOLD
            )
            if len(iron) > 0:
              common.move_mouse(
                iron[0][0] + common.offset('small'),
                iron[0][1] + common.offset('small'),
                'now'
              )
              pyautogui.click()
              common.move_mouse_randomish()
              common.random_delay_short()
              if count >= INVENTORY_NUMBER - 2:
                break
          inventory_full, count = common.check_inventory(
            inventory_box,
            inventory_items,
            INVENTORY_THRESHOLD,
            INVENTORY_NUMBER
          )
          print('inventory count: ' + str(count))
  return True
