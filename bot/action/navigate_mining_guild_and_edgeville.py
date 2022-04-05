import pyautogui
from .. import common

DEBUG = False
MODULE = 'navigate_mining_guild_and_edgeville'  # directory in vision/artifacts needs to match this
MATCH_THRESHOLD = 0.8
NO_REVERSE = False
REVERSE = True
COMMON_SELECTOR = []
MODULE_SELECTOR = [
  'door',
  'ladder_bottom',
  'ladder_top',
  'location_mining_guild',
  'location_edgeville_bank'
]


def run(input):
  objects, path, common_objects = common.load_objects(MODULE, MODULE_SELECTOR, COMMON_SELECTOR)
  common.random_delay_long()
  if input['direction'] == 0:
    print('finding door...')
    result = []
    while len(result) == 0:
      for image in objects['door']:
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
          break
    common.random_delay_giant()
    print('finding ladder...')
    result = []
    while len(result) == 0:
      for image in objects['ladder_bottom']:
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
          break
    common.navigate(
      path,
      objects['location_edgeville_bank'],
      MATCH_THRESHOLD,
      NO_REVERSE
    )
  elif input['direction'] == 1:
    common.navigate(
      path,
      objects['location_mining_guild'],
      MATCH_THRESHOLD,
      REVERSE
    )
