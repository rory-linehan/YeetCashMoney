from datetime import datetime, timedelta
import pyautogui
import random
import time
from .. import common

# define module constants here
MODULE = 'smelt_bronze_al-kharid'  # directory in vision/artifacts needs to match this
MATCH_THRESHOLD = 0.65
INVENTORY_THRESHOLD = 0.9
NAVIGATE_THRESHOLD = 0.65
NO_REVERSE = False
REVERSE = True
BAIL = 20
INVENTORY_NUMBER_BRONZE_BARS = 10
INVENTORY_NUMBER_ORES = 20
COMMON_SELECTOR = [
  'bank_window',
  'action_bar_full',
  'action_bar_empty',
  'tin_inventory',
  'tin_bank',
  'copper_inventory',
  'copper_bank',
  'bronze_bar_inventory'
]


def run(interval):
  # set up a bunch of variables used later
  end_time = datetime.now() + timedelta(seconds=interval)

  # all the strings to search for in filenames
  # that identify a specific object in Runescape
  MODULE_SELECTOR = [
    'location_bank',
    'location_furnace',
    'furnace_actual',
    'menu_bronze_bar',
    'bank_booth',
  ]
  objects, path, common_objects = common.load_objects(MODULE, MODULE_SELECTOR, COMMON_SELECTOR)
  if objects is not None and path is not None:
    time.sleep(random.choice(range(1, 12)))
    # do not bot for longer than the configured time
    while datetime.now() < end_time:
      print('calculating inventory box...')
      inventory_box = common.calculate_inventory_box(
        [
          common_objects['action_bar_full'],
          common_objects['action_bar_empty']
        ],
        INVENTORY_THRESHOLD
      )
      print('inventory box: ' + str(inventory_box))
      _, bronze_bars = common.check_inventory(
        inventory_box,
        [
          common_objects['bronze_bar_inventory']
        ],
        INVENTORY_THRESHOLD,
        INVENTORY_NUMBER_BRONZE_BARS
      )
      print('bronze bars: (' + str(bronze_bars) + ')')
      if bronze_bars == 0:
        # assume that if there are no bronze bars in inventory
        # that we're close to the bank and ready to rock and roll
        print('getting tin and copper...')
        common.withdraw(
          inventory_box,
          common_objects,
          objects['bank_booth'],
          [
            common_objects['tin_bank'],
            common_objects['copper_bank']
          ],
          [
            common_objects['tin_inventory'],
            common_objects['copper_inventory']
          ],
          MATCH_THRESHOLD,
          INVENTORY_THRESHOLD,
          INVENTORY_NUMBER_ORES
        )
        print('navigating to furnace...')
        common.navigate(
          path,
          objects['location_furnace'],
          NAVIGATE_THRESHOLD,
          NO_REVERSE
        )
        common.random_delay_long()
        while bronze_bars < 10:
          common.random_delay_short()
          print('selecting furnace...')
          furnace_menu = []
          while len(furnace_menu) == 0:
            for image in objects['furnace_actual']:
              furnace = common.find_object(
                image,
                0.8
              )
              if len(furnace) > 0:
                common.move_mouse(
                  furnace[0][0],
                  furnace[0][1],
                  'now'
                )
                pyautogui.click()
                break
            time.sleep(random.choice(range(2, 6)))
            # find bronze bar menu option on screen
            for image in objects['menu_bronze_bar']:
              furnace_menu = common.find_object(image, INVENTORY_THRESHOLD)
              if len(furnace_menu) > 0:
                common.move_mouse(
                  furnace_menu[0][0] + common.offset('small'),
                  furnace_menu[0][1] + common.offset('medium'),
                  'whenever'
                )
                pyautogui.leftClick()
                break
          common.move_mouse_randomish()
          print('waiting for bronze bars to be done...')
          changed = True
          while changed is True:
            changed = common.wait_for_inventory_to_change(
              inventory_box,
              [
                common_objects['bronze_bar_inventory']
              ],
              INVENTORY_THRESHOLD,
              BAIL
            )
            if changed is False:
              # if the inventory waiter bails,
              # update bronze_bars for the while check
              _, bronze_bars = common.check_inventory(
                inventory_box,
                [
                  common_objects['bronze_bar_inventory']
                ],
                INVENTORY_THRESHOLD,
                INVENTORY_NUMBER_BRONZE_BARS
              )
              print('bronze bars: (' + str(bronze_bars) + ')')

      else:
        print('navigating to bank...')
        common.navigate(
          path,
          objects['location_bank'],
          NAVIGATE_THRESHOLD,
          REVERSE
        )
        print('depositing inventory (' + str(bronze_bars) + ')...')
        common.deposit(
          inventory_box,
          common_objects,
          objects['bank_booth'],
          [
            common_objects['bronze_bar_inventory']
          ],
          MATCH_THRESHOLD,
          INVENTORY_THRESHOLD,
          0
        )
  return True
