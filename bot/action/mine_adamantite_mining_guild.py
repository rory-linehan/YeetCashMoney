from datetime import datetime, timedelta
import pyautogui
import random
import time
from .. import common

# define module constants here
MODULE = 'mine_adamantite_mining_guild'  # directory in vision/artifacts needs to match this
MATCH_THRESHOLD = 0.96
INVENTORY_THRESHOLD = 0.95
NAVIGATE_THRESHOLD = 0.75
NO_REVERSE = False
REVERSE = True
BAIL = 75
INVENTORY_NUMBER = 26
COMMON_SELECTOR = [
  'adamantite_inventory',
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
  MODULE_SELECTOR = [
    'adamantite_rock',
    'bank_chest',
    'location_mine'
  ]
  # do not bot for longer than the configured time
  while datetime.now() < end_time:
    objects, path, common_objects = common.load_objects(MODULE, MODULE_SELECTOR, COMMON_SELECTOR)
    if objects is not None and path is not None:
      inventory_items = [
        common_objects['adamantite_inventory'],
        common_objects['sapphire'],
        common_objects['ruby'],
        common_objects['emerald'],
        common_objects['diamond'],
        common_objects['clue_geode']
      ]
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
      common.navigate(
        path,
        objects['bank_chest'],
        NAVIGATE_THRESHOLD,
        True
      )
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
            if 'adamantite' in image:
              result = common.find_object(
                image,
                0.99
              )
            else:
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
      print('mining adamantite...')
      common.navigate(
        path,
        objects['location_mine'],
        NAVIGATE_THRESHOLD,
        False
      )
      time.sleep(random.choice(range(5, 8)))
      inventory_full = False
      while inventory_full is False:
        print('looking for adamantite rock...')
        adamantite = []
        while len(adamantite) == 0:
          for image in objects['adamantite_rock']:
            adamantite = common.find_object(
              image,
              MATCH_THRESHOLD
            )
            if len(adamantite) > 0:
              common.move_mouse(
                adamantite[0][0] + common.offset('small'),
                adamantite[0][1] + common.offset('small'),
                'now'
              )
              pyautogui.click()
              common.move_mouse_randomish()
              break
          objects, path, common_objects = common.load_objects(MODULE, MODULE_SELECTOR, COMMON_SELECTOR)
        common.wait_for_inventory_to_change(
          inventory_box,
          [common_objects['adamantite_inventory']],
          INVENTORY_THRESHOLD,
          BAIL
        )
        inventory_full, count = common.check_inventory(
          inventory_box,
          inventory_items,
          INVENTORY_THRESHOLD,
          INVENTORY_NUMBER
        )
        print('inventory count: ' + str(count))
  return True
