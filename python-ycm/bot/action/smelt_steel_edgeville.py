from datetime import datetime, timedelta
import pyautogui
import random
import time
from python.bot import common

MODULE = 'smelt_steel_al-kharid'  # directory in vision/artifacts needs to match this
MATCH_THRESHOLD = 0.8
BANK_THRESHOLD = 0.6
INVENTORY_THRESHOLD = 0.95
NAVIGATE_THRESHOLD = 0.65
NO_REVERSE = False
REVERSE = True
BAIL = 20
INVENTORY_NUMBER_STEEL_BARS = 10
INVENTORY_NUMBER_ORES = 20
COMMON_MATRIX = [
    'bank_window',
    'action_bar_full',
    'action_bar_empty',
    'iron_inventory',
    'coal_inventory',
    'iron_bank',
    'coal_bank',
    'steel_bar_inventory'
]


def run(interval):
    # set up a bunch of variables used later
    end_time = datetime.now() + timedelta(seconds=interval)

    # all the strings to search for in filenames
    # that identify a specific object in Runescape
    om = [  # object matrix
        'bank_booth',
        'location_bank',
        'location_furnace',
        'furnace_actual',
        'menu_steel_bar'
    ]
    objects, path, COMMON_OBJECTS = common.load_objects(MODULE, om, COMMON_MATRIX)
    if objects is not None and path is not None:
        time.sleep(random.choice(range(1, 12)))
        # do not bot for longer than the configured time
        while datetime.now() < end_time:
            print('calculating inventory box...')
            inventory_box = common.calculate_inventory_box(
                [
                    COMMON_OBJECTS['action_bar_full'],
                    COMMON_OBJECTS['action_bar_empty']
                ],
                INVENTORY_THRESHOLD
            )
            print('inventory box: ' + str(inventory_box))
            _, steel_bars = common.check_inventory(
                inventory_box,
                [
                    COMMON_OBJECTS['steel_bar_inventory']
                ],
                INVENTORY_THRESHOLD,
                INVENTORY_NUMBER_STEEL_BARS
            )
            print('steel bars: (' + str(steel_bars) + ')')
            if steel_bars == 0:
                # assume that if there are no steel bars in inventory
                # that we're close to the bank and ready to rock and roll
                print('getting iron and coal...')
                common.withdraw(
                    inventory_box,
                    COMMON_OBJECTS,
                    objects['bank_booth'],
                    [
                        COMMON_OBJECTS['iron_bank'],
                        COMMON_OBJECTS['coal_bank']
                    ],
                    [
                        COMMON_OBJECTS['iron_inventory'],
                        COMMON_OBJECTS['coal_inventory']
                    ],
                    BANK_THRESHOLD,
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
                while steel_bars < 10:
                    common.random_delay_short()
                    print('selecting furnace...')
                    furnace_menu = []
                    while len(furnace_menu) == 0:
                        for image in objects['furnace_actual']:
                            furnace = common.find_object(image, MATCH_THRESHOLD)
                            if len(furnace) > 0:
                                common.move_mouse(
                                    furnace[0][0] + common.offset('small'),
                                    furnace[0][1] + common.offset('small'),
                                    'now'
                                )
                                pyautogui.click()
                                break
                        time.sleep(random.choice(range(2, 6)))
                        # find bronze bar menu option on screen
                        for image in objects['menu_steel_bar']:
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
                    print('waiting for steel bars to be done...')
                    changed = True
                    while changed is True:
                        changed = common.wait_for_inventory_to_change(
                            inventory_box,
                            [
                                COMMON_OBJECTS['steel_bar_inventory']
                            ],
                            MATCH_THRESHOLD,
                            BAIL
                        )
                        if changed is False:
                            # if the inventory waiter bails,
                            # update steel_bars for the while check
                            _, steel_bars = common.check_inventory(
                                inventory_box,
                                [
                                    COMMON_OBJECTS['steel_bar_inventory']
                                ],
                                INVENTORY_THRESHOLD,
                                INVENTORY_NUMBER_STEEL_BARS
                            )
                            print('bronze bars: (' + str(steel_bars) + ')')

            else:
                print('depositing inventory (' + str(steel_bars) + ')...')
                common.deposit(
                    inventory_box,
                    COMMON_OBJECTS,
                    objects['bank_booth'],
                    [
                        COMMON_OBJECTS['steel_bar_inventory']
                    ],
                    BANK_THRESHOLD,
                    INVENTORY_THRESHOLD,
                    0
                )
    return True
