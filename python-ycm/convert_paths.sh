#!/usr/bin/env bash

cd ml/vision/voc/train && \
python3.7 convert_annotation_paths.py --prefix "/mnt/projects" --new "/home/rory"
