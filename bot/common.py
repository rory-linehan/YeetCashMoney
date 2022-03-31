import pyautogui
import cv2
import numpy as np
import random
import time
import os
import glob

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1
LEFT_CLICK = 0
RIGHT_CLICK = 1
INVENTORY_SIZE = 26


def random_delay_short():
  time.sleep(random.choice([0.2, 0.25, 0.3, 0.4, 0.72, 0.8, 1]))


def random_delay_long():
  time.sleep(random.choice([1, 1.25, 1.32, 1.46, 1.72, 1.85, 2]))


# load all images that will be used to identify
# in-game objects for the current module
def load_objects(module, matrix, common_matrix):
  objects = {}
  navigation = []
  common = {}
  for (dirpath, dirnames, filenames) in os.walk(os.path.join('vision/artifacts', module)):
    if 'navigation' in dirpath:
      # intuitive sorting does not work with numbers when they're in a string
      files_sorted = []
      for filename in filenames:
        number = int(filename.replace('.png', ''))
        files_sorted.append((number, filename))
      navigation = [(index, os.path.join(dirpath, filename)) for index, filename in sorted(files_sorted)]
    else:
      for filename in filenames:
        for m in matrix:
          if m not in objects:
            objects[m] = []
          if m in filename:
            objects[m].extend([os.path.join(dirpath, filename)])
  for (dirpath, dirnames, filenames) in os.walk(os.path.join('vision/artifacts', 'common')):
    for filename in filenames:
      for m in common_matrix:
        if m not in common:
          common[m] = []
        if m in filename:
          common[m].extend([os.path.join(dirpath, filename)])
  return objects, navigation, common


# generate a random offset of pixels so that clicks are
# different and not in the top left corner of an object
def offset(size):
  if size == 'tiny':
    return random.choice([3, 4, 5])
  elif size == 'small':
    return random.choice([6, 8, 10])
  elif size == 'medium':
    return random.choice([12, 16, 20])
  elif size == 'large':
    return random.choice([24, 36, 40])
  else:
    return random.choice([1, 2])  # err on the side of caution


def adjust_perspective_randomly():
  key = random.choice(['up', 'down'])
  pyautogui.keyDown(key)
  random_delay_short()
  pyautogui.keyUp(key)


def move_mouse(x, y, when):
  # TODO: need a function that generates a random x, y within set boundaries of like 20 pixels
  if when == 'now':
    pyautogui.moveTo(x, y, random.choice([0.1, 0.15, 0.2, 0.25, 0.3, 0.4]))
  else:
    pyautogui.moveTo(
      x,
      y,
      random.choice([0.5, 0.65, 0.8, 0.92, 1, 1.1]),  # random total mouse move time
      random.choice([  # random movement style
        pyautogui.easeInQuad,
        pyautogui.easeOutQuad,
        pyautogui.easeInBounce,
        pyautogui.easeInElastic
      ])
    )


def move_mouse_randomish():
  current = pyautogui.position()
  pyautogui.moveTo(
    current[0] + random.choice(range(50, 150)),
    current[1] + random.choice(range(50, 150)),
    random.choice([0.5, 0.55, 0.6, 0.8]),  # random total mouse move time
    random.choice([  # random movement style
      pyautogui.easeInQuad,
      pyautogui.easeOutQuad,
      pyautogui.easeInOutQuad,
      pyautogui.easeInBounce,
      pyautogui.easeInElastic
    ])
  )


# returns all instances of image on the screen
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html#display-image
def find_object(image, threshold):
  try:
    haystack = cv2.cvtColor(np.array(
      pyautogui.screenshot('/tmp/ycm-cache/screenshot.png')),
      cv2.COLOR_RGB2BGR
    )
    needle = cv2.imread(image)
    result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)
    location = np.where(result >= threshold)
    for filename in glob.glob('/tmp/ycm-cache/*.png'):
      os.remove(filename)
    # this returns two tuples for each object found
    return list(zip(*location[::-1]))
  except SystemError as err:
    print('SystemError exception while finding image ('+str(image)+'): ' + str(err))
    return False


def calculate_inventory_box(markers, threshold):
  # find the inventory so we can calculate a box around it
  result = []
  while len(result) == 0:
    for marker in markers:
      for image in marker:
        result += find_object(image, threshold)
        if len(result) > 0:
          # inventory box coordinates
          return [
            [result[0][0] + 200, result[0][1] - 300],
            [result[0][0] + 400, result[0][1]]
          ]


def calculate_bank_box(markers, threshold):
  # find the bank window so we can calculate a box around it
  result = []
  while len(result) == 0:
    for marker in markers:
      for image in marker:
        result += find_object(image, threshold)
        if len(result) > 0:
          # bank box coordinates
          return [
            [result[0][0], result[0][1]],
            [result[0][0] + 500, result[0][1] + 800]
          ]


def check_inventory(
    box,
    items,
    threshold,
    inventory_number
):
  total = 0
  for item in items:
    for image in item:
      result = find_object(image, threshold)
      if len(result) > 0:
        for r in result:
          if (box[0][0] < r[0] < box[1][0]) and (box[0][1] < r[1] < box[1][1]):
            total += 1
        break
  if total >= inventory_number:
    return True, total
  else:
    return False, total


# bail=None to wait for an inventory change forever.
def wait_for_inventory_to_change(
    box,
    items,
    threshold,
    bail
):
  before = 0
  for item in items:
    for image in item:
      result = find_object(image, threshold)
      for r in result:
        if box[0][0] < r[0] < box[1][0] and box[0][1] < r[1] < box[1][1]:
          before += len(result)
  after = before
  tried = 0
  while before == after:
    after = 0
    for item in items:
      for image in item:
        result = find_object(image, threshold)
        for r in result:
          if box[0][0] < r[0] < box[1][0] and box[0][1] < r[1] < box[1][1]:
            after += len(result)
    if bail is not None:
      tried += 1
      if tried >= bail:
        print('common.wait_for_inventory_to_change is bailing out after '+str(bail)+' tries!')
        return False
    else:
      print('you have instructed common.wait_for_inventory_to_change '
            'to never bail out of this loop. '
            'you will see this message until the end of time, '
            'or until it finds your object. '
            'xkcd.com/1411')
  return True


def navigate(
    sequence,
    destination,
    threshold,
    reverse
):
  sorted_sequence = sorted(sequence, reverse=reverse)
  for step, _ in enumerate(sorted_sequence):
    time.sleep(random.choice(range(2, 5)))
    result = []
    while len(result) == 0:
      # if no destination, look for next step
      print('looking for step (' + str(step) + '): ' + str(sorted_sequence[step]))
      result = []
      while len(result) == 0:
        result = find_object(sorted_sequence[step][1], threshold)
        if len(result) > 0:
          print('found next step ('+str(step)+') at ' + str(result))
          pyautogui.moveTo(
            result[0][0] + offset('small'),
            result[0][1] + offset('small')
          )
          pyautogui.click()
          move_mouse_randomish()
  # wait for a bit to get into optimal position to find destination
  time.sleep(random.choice(range(5, 8)))
  # get to destination
  result = []
  while len(result) == 0:
    for d in destination:
      result.extend(find_object(d, threshold))

  print('found destination at ' + str(result))
  move_mouse(
    result[0][0] + random.choice(range(2, 10)),
    result[0][1] + random.choice(range(2, 10)),
    'now'
  )
  pyautogui.click()
  random_delay_long()
  return True


# bank_booth and bank_window are just objects, which consist of a list of filenames:
# object = ['path/to/image_of_object.png',...]
# items is a list of objects:
# [[object],...]]
def deposit(
    box,
    common_objects,
    bank_booth,
    items,
    match_threshold,
    inventory_threshold,
    inventory_number
):
  print('selecting the bank booth...')
  bank_is_open = False
  while bank_is_open is False:
    random_delay_short()
    # find and click the bank booth
    result = []
    while len(result) == 0:
      for image in bank_booth:
        result = find_object(image, match_threshold)
        if len(result) > 0:
          pyautogui.moveTo(
            result[0][0] + offset('tiny'),
            result[0][1] + offset('tiny'),
            0.1
          )
          pyautogui.leftClick()
      time.sleep(random.choice(range(3, 6)))
      # let's make sure the bank window is actually open
      for image in common_objects['bank_window']:
        result = find_object(image, match_threshold)
        if len(result) > 0:
          bank_is_open = True
  # deposit items
  while True:
    for item in items:
      random_delay_short()
      print('depositing item: ' + str(item))
      for image in item:
        result = find_object(image, inventory_threshold)
        if len(result) > 0:
          # we only want to select items within the inventory, given by `box`
          if (box[0][0] < result[0][0] < box[1][0]) and (box[0][1] < result[0][1] < box[1][1]):
            x = result[0][0]
            y = result[0][1]
            move_mouse(
              x + random.choice(range(2, 7)),
              y + random.choice(range(2, 7)),
              'now'
            )
            pyautogui.leftClick()
            break
      random_delay_short()
      full, count = check_inventory(
        box,
        items,
        inventory_threshold,
        inventory_number
      )
      if count == 0:
        return True
      else:
        print('inventory still has something in it: (' + str(count) + ')')


def withdraw(
    inventory_box,
    common_objects,
    bank_booth,
    bank_objects,
    inventory_objects,
    bank_threshold,
    inventory_threshold,
    inventory_number
):
  print('selecting the bank booth...')
  bank_is_open = False
  while bank_is_open is False:
    random_delay_short()
    # find and click the bank booth
    result = []
    while len(result) == 0:
      for image in bank_booth:
        result = find_object(image, bank_threshold)
        if len(result) > 0:
          pyautogui.moveTo(
            result[0][0] + offset('small'),
            result[0][1] + offset('small'),
            0.1
          )
          pyautogui.leftClick()
          break
      time.sleep(random.choice(range(5, 10)))
      # let's make sure the bank window is actually open
      for image in common_objects['bank_window']:
        result = find_object(image, bank_threshold)
        if len(result) > 0:
          bank_is_open = True
          break
  bank_box = calculate_bank_box(
    [common_objects['bank_window']],
    bank_threshold
  )
  print('bank box: ' + str(bank_box))
  # withdraw items
  while True:
    for item in bank_objects:
      random_delay_long()
      # is the inventory good to go yet?
      full, count = check_inventory(
        inventory_box,
        inventory_objects,
        inventory_threshold,
        inventory_number
      )
      print('inventory count: (' + str(count) + ')')
      if count < inventory_number:
        print('withdrawing item: ' + str(item))
        for image in item:
          result = find_object(image, inventory_threshold)
          if len(result) > 0:
            if (bank_box[0][0] < result[0][0] < bank_box[1][0]) \
                and (bank_box[0][1] < result[0][1] < bank_box[1][1]):
              x = result[0][0]
              y = result[0][1]
              move_mouse(
                x + random.choice(range(1, 15)),
                y + random.choice(range(1, 5)),
                'now'
              )
              pyautogui.rightClick()
              # this selects "Withdraw 10"
              # TODO: need to refactor and abstract
              move_mouse(
                x + random.choice(range(1, 40)),
                y + random.choice(range(73, 79)),
                'now'
              )
              pyautogui.leftClick()
              random_delay_long()
              break
      else:
        return True
