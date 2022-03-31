#!/usr/bin/env bash

cp -v ../ml/vision/labels ../ml/vision/src/labelImg/data/predefined_classes.txt && \
cd ../ml/vision/src/labelImg && \
python3.7 labelImg.py