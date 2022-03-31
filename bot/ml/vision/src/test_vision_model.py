import os
import json
import cv2
from keras_yolo3.utils.utils import get_yolo_boxes, makedirs
from keras_yolo3.utils.bbox import draw_boxes
from keras_yolo3 import gen_anchors
from keras.models import load_model
from tqdm import tqdm


class DirContext:
  def __init__(self, dir):
    self._dir = dir

  def __enter__(self):
    self._cwd = os.getcwd()
    os.chdir(self._dir)
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    os.chdir(self._cwd)


def run(input_file, output_path, anchors, labels, thresholds):
  ###############################
  #   Set some parameter
  ###############################
  net_h, net_w = 416, 416  # a multiple of 32, the smaller the faster
  obj_thresh, nms_thresh = thresholds['obj'], thresholds['nms']

  ###############################
  #   Load the model
  ###############################
  #os.environ['CUDA_VISIBLE_DEVICES'] = str((0, 1))
  infer_model = load_model('models/vision.h5')

  ###############################
  #   Predict bounding boxes
  ###############################
  video_out = output_path + input_file.split('/')[-1]
  video_reader = cv2.VideoCapture(input_file)

  nb_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
  frame_h = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
  frame_w = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))

  video_writer = cv2.VideoWriter(video_out,
                                 cv2.VideoWriter_fourcc(*'MPEG'),
                                 50.0,
                                 (frame_w, frame_h))

  # the main loop
  batch_size = 1
  images = []
  start_point = 0  # %
  show_window = True
  for i in tqdm(range(nb_frames)):
    _, image = video_reader.read()

    if (float(i + 1) / nb_frames) > start_point / 100.:
      images += [image]

      if (i % batch_size == 0) or (i == (nb_frames - 1) and len(images) > 0):
        # predict the bounding boxes
        batch_boxes = get_yolo_boxes(infer_model, images, net_h, net_w, anchors,
                                     obj_thresh, nms_thresh)

        for i in range(len(images)):
          # draw bounding boxes on the image using labels
          draw_boxes(images[i], batch_boxes[i], labels, obj_thresh)
          # show the video with detection bounding boxes
          if show_window:
            cv2.imshow('video with bboxes', images[i])
        images = []
      if show_window and cv2.waitKey(1) == 27: break  # esc to quit

  if show_window:
    cv2.destroyAllWindows()
  video_reader.release()
  video_writer.release()


if __name__ == '__main__':
  with DirContext('ml/vision'):
    with open('labels', 'rt') as handle:
      labels = handle.read().split('\n')[:-1]
    gen_anchors.run(
      9,
      'voc/train/annotations/',
      'voc/train/images/',
      'cache/train.pkl',
      labels
    )
    with open('anchors', 'rt') as handle:
      anchors = json.loads(handle.read())
    run(
      '/home/rory/Videos/machine_learning/login_0.m4v',
      'cache',
      anchors,
      labels,
      {'obj': 0.5, 'nms': 0.8}
    )
