import os
import json
#from .src.keras_yolo3 import train as ky3_train
#from .src.keras_yolo3 import gen_anchors


def train(num_anchors):
    cwd = os.getcwd()
    with open('labels', 'rt') as handle:
        labels = handle.read().split('\n')[:-1]
    gen_anchors.run(
        num_anchors,
        'voc/train/annotations/',
        'voc/train/images/',
        'cache/train.pkl',
        labels
    )
    with open('anchors', 'rt') as handle:
        anchors = json.loads(handle.read())
    # clear cache
    # this prevents a few errors that are impossible to root cause
    #"""
    try:
        for f in ['train', 'validation']:
            os.remove('/cache/'+f+'.pkl')
    except FileNotFoundError:
        pass
    #"""
    ky3_train._main_({
        "model": {
            "min_input_size":       64,
            "max_input_size":       128,
            "anchors":              anchors,
            "labels":               labels
        },

        "train": {
            "train_image_folder":   "voc/train/images/",
            "train_annot_folder":   "voc/train/annotations/",
            "cache_name":           "cache/train.pkl",

            "train_times":          16,
            "batch_size":           1,
            "learning_rate":        1e-4,
            "nb_epochs":            100,
            "warmup_epochs":        3,
            "ignore_thresh":        0.5,
            "gpus":                 "0",

            "grid_scales":          [1, 1, 1],
            "obj_scale":            4,
            "noobj_scale":          1,
            "xywh_scale":           1,
            "class_scale":          1,

            "tensorboard_dir":      "logs",
            "saved_weights_name":   "models/vision.h5",
            "debug":                True
        },

        "valid": {
            #"valid_image_folder":   "/voc/validation/images/",
            #"valid_annot_folder":   "/voc/validation/annotations/",
            "valid_image_folder":   "",
            "valid_annot_folder":   "",
            "cache_name":           "/cache/validation.pkl",

            "valid_times":          1
        }
    })

    return True, 'trained vision model'
