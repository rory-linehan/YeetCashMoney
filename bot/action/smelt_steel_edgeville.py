from datetime import datetime, timedelta
import pyautogui
from .. import common

DEBUG = False
MODULE = 'smelt_steel_edgeville'  # directory in vision/artifacts needs to match this
MATCH_THRESHOLD = 0.8
BANK_THRESHOLD = 0.6
INVENTORY_THRESHOLD = 0.995
NAVIGATE_THRESHOLD = 0.65
NO_REVERSE = False
REVERSE = True
BAIL = 100
INVENTORY_NUMBER_STEEL_BARS = 8
INVENTORY_NUMBER_ORES = 27
SELECTOR_MATRIX = [
  'inventory_box_empty',
  'bank_window',
  'action_bar_full',
  'action_bar_empty',
  'iron_inventory',
  'coal_inventory',
  'iron_bank',
  'coal_bank',
  'steel_bar_inventory',
  'menu_steel_bar',
  'not_smelting'
]


def start_smelting(objects, COMMON_OBJECTS):
  print('selecting furnace...')
  for image in objects['furnace_actual']:
    furnace = common.find_object(
      image,
      MATCH_THRESHOLD
    )
    if len(furnace) > 0:
      common.move_mouse(
        furnace[0][0] + common.offset('tiny'),
        furnace[0][1] + common.offset('tiny')
      )
      pyautogui.click()
      common.move_mouse_randomish()
      break
  print('selecting steel bar menu option...')
  furnace_menu = []
  while len(furnace_menu) == 0:
    for image in COMMON_OBJECTS['menu_steel_bar']:
      furnace_menu = common.find_object(
        image,
        INVENTORY_THRESHOLD
      )
      if len(furnace_menu) > 0:
        common.move_mouse(
          furnace_menu[0][0] + common.offset('small'),
          furnace_menu[0][1] + common.offset('medium'),
          'whenever'
        )
        pyautogui.leftClick()
        common.move_mouse_randomish()
        return


def run(interval):
  # set up a bunch of variables used later
  end_time = datetime.now() + timedelta(seconds=interval)

  # all the strings to search for in filenames
  # that identify a specific object in Runescape
  OBJECT_SELECTOR = [  # object matrix
    'bank_booth',
    'location_bank',
    'location_furnace',
    'furnace_actual'
  ]
  # do not bot for longer than the configured time
  while datetime.now() < end_time:
    objects, path, COMMON_OBJECTS = common.load_objects(MODULE, OBJECT_SELECTOR, SELECTOR_MATRIX)
    print('calculating inventory box...')
    inventory_box = common.calculate_inventory_box(
      [
        COMMON_OBJECTS['inventory_box_empty']
      ],
      MATCH_THRESHOLD,
      DEBUG
    )
    print('inventory box: ' + str(inventory_box))
    # assume that if there are no steel bars in inventory
    # that we're close to the bank and ready to rock and roll
    print('getting iron and coal...')
    common.withdraw(
      inventory_box,
      COMMON_OBJECTS,
      objects['bank_booth'],
      [
        COMMON_OBJECTS['iron_bank'],
        COMMON_OBJECTS['coal_bank'],
        COMMON_OBJECTS['coal_bank']  # need to fill the rest of the inventory with coal
      ],
      [
        COMMON_OBJECTS['iron_inventory'],
        COMMON_OBJECTS['coal_inventory']
      ],
      BANK_THRESHOLD,
      INVENTORY_THRESHOLD,
      INVENTORY_NUMBER_ORES,
      DEBUG
    )
    _, steel_bars = common.check_inventory(
      inventory_box,
      [
        COMMON_OBJECTS['steel_bar_inventory']
      ],
      MATCH_THRESHOLD,
      INVENTORY_NUMBER_STEEL_BARS
    )
    start_smelting(objects, COMMON_OBJECTS)
    while steel_bars < INVENTORY_NUMBER_STEEL_BARS:
      changed = common.wait_for_inventory_to_change(
        inventory_box,
        [
          COMMON_OBJECTS['steel_bar_inventory']
        ],
        MATCH_THRESHOLD,
        BAIL
      )
      if changed is False:
        not_smelting = common.find_object(
          COMMON_OBJECTS['not_smelting'][0],
          INVENTORY_THRESHOLD
        )
        if len(not_smelting) > 0:  # probably gained a level, restart smelting
          start_smelting(objects, COMMON_OBJECTS)
      done, steel_bars = common.check_inventory(
        inventory_box,
        [
          COMMON_OBJECTS['steel_bar_inventory']
        ],
        MATCH_THRESHOLD,
        INVENTORY_NUMBER_STEEL_BARS
      )
      print('steel bars: ('+str(steel_bars)+')')
      if done:
        print('depositing inventory ('+str(steel_bars)+')...')
        common.deposit(
          inventory_box,
          COMMON_OBJECTS,
          objects['bank_booth'],
          [
            COMMON_OBJECTS['steel_bar_inventory'],
            COMMON_OBJECTS['iron_inventory']
          ],
          BANK_THRESHOLD,
          INVENTORY_THRESHOLD,
          0
        )
  return True
