from datetime import datetime, timedelta
import pyautogui
import random
import time
from .. import common

# define global constants here
MODULE = 'mine_copper_tin_se_varrock'  # directory in vision/artifacts needs to match this
MATCH_THRESHOLD = 0.5
INVENTORY_THRESHOLD = 0.95
NAVIGATE_THRESHOLD = 0.65
NO_REVERSE = False
REVERSE = True
BAIL = 20
INVENTORY_NUMBER = 25
COMMON_SELECTOR = [
  'bank_booth',
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
    'tin_rock',
    'copper_rock',
    'tin_inventory',
    'copper_inventory',
    'location_bank',
    'location_mine'
  ]
  objects, path, common_objects = common.load_objects(MODULE, MODULE_SELECTOR, COMMON_SELECTOR)
  if objects is not None and path is not None:
    ores = [
      ['tin', objects['tin_rock'], objects['tin_inventory']],
      ['copper', objects['copper_rock'], objects['copper_inventory']]
    ]
    # do not bot for longer than the configured time
    time.sleep(random.choice(range(1, 4)))
    while datetime.now() < end_time:
      for (ore_name, ore_images, ore_inventory) in [random.choice(ores)]:
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
          [
            objects['tin_inventory'],
            objects['copper_inventory'],
            common_objects['sapphire'],
            common_objects['ruby'],
            common_objects['emerald'],
            common_objects['diamond'],
            common_objects['clue_geode']
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
            NO_REVERSE
          )
          common.deposit(
            inventory_box,
            common_objects,
            [
              objects['tin_inventory'],
              objects['copper_inventory'],
              common_objects['sapphire'],
              common_objects['ruby'],
              common_objects['emerald'],
              common_objects['diamond'],
              common_objects['clue_geode']
            ],
            MATCH_THRESHOLD,
            INVENTORY_THRESHOLD,
            INVENTORY_NUMBER
          )
          print('navigating to mine...')
          common.navigate(
            path,
            objects['location_mine'],
            NAVIGATE_THRESHOLD,
            REVERSE
          )
        else:
          # if inventory empty, then check for bank and navigate to mine
          print('inventory: ' + str(count))
          if count == 0:
            r = common.find_object(objects['location_bank'][0], NAVIGATE_THRESHOLD)
            if r is not False:
              if len(r) > 0:
                print('navigating to mine...')
                common.navigate(
                  path,
                  objects['location_mine'],
                  NAVIGATE_THRESHOLD,
                  REVERSE
                )
        print('finding ' + ore_name + ' on screen...')
        common.random_delay_short()
        ore = []
        while len(ore) == 0:
          for image in ore_images:
            ore = common.find_object(image, MATCH_THRESHOLD)
        print('found it!')
        common.move_mouse(ore[0][0] + common.offset('small'), ore[0][1] + common.offset('small'), 'whenever')
        pyautogui.click()
        print('waiting for inventory to change...')
        common.wait_for_inventory_to_change(
          inventory_box,
          [
            ore_inventory,
            common_objects['sapphire'],
            common_objects['ruby'],
            common_objects['emerald'],
            common_objects['diamond'],
            common_objects['clue_geode']
          ],
          MATCH_THRESHOLD,
          BAIL
        )
        common.move_mouse_randomish()
  return True
