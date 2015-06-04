#!/usr/bin/env python3

__author__ = 'Yatharth Agarwal <yatharth999@gmail.com>'

"""Run game"""

import config
from board import Controller


controller = Controller()

def setup():
    print "Setting up"
    size(config.SIZE, config.SIZE)
    colorMode(HSB, 1)
    frame.setTitle("Agar")


def draw():
    background(config.BACKGROUND_COLOR)
    controller.draw()

def keyPressed():
    controller.keyPressed(key, keyCode)

def keyReleased():
    controller.keyReleased(key, keyCode)
