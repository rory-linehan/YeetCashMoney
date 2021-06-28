#!/usr/bin/env bash
count=0
mkdir -p train/
while [ 1 ]
do
  gnome-screenshot -d 1 -p --file="images/${count}.png"
  ((count++))
done
