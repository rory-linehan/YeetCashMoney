from .. import common

DEBUG = False
MODULE = 'navigate_mining_guild_and_edgeville'  # directory in vision/artifacts needs to match this
NAVIGATE_THRESHOLD = 0.65
NO_REVERSE = False
REVERSE = True
COMMON_SELECTOR = []
# all the strings to search for in filenames
# that identify a specific object in Runescape
MODULE_SELECTOR = [
  'location_mining_guild',
  'location_edgeville'
]


def run(input):
  objects, path, common_objects = common.load_objects(MODULE, MODULE_SELECTOR, COMMON_SELECTOR)
  if input['direction'] == 0:
    common.navigate(
      path,
      objects['location_edgeville'],
      NAVIGATE_THRESHOLD,
      NO_REVERSE
    )
  elif input['direction'] == 1:
    common.navigate(
      path,
      objects['location_mining_guild'],
      NAVIGATE_THRESHOLD,
      REVERSE
    )
