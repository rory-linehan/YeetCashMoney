#!/usr/bin/env bash

sudo apt install -y gcc libc6-dev && \
sudo apt install -y libx11-dev xorg-dev libxtst-dev libpng++-dev && \
sudo apt install -y xcb libxcb-xkb-dev x11-xkb-utils libx11-xcb-dev libxkbcommon-x11-dev && \
sudo apt install -y libxkbcommon-dev && \
sudo apt install -y xsel xclip && \
go build -o ycm cmd/golang-ycm/main.go