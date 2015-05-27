#!/usr/bin/env python3

__author__ = 'Yatharth Agarwal <yatharth999@gmail.com>'

from time import sleep

from board import Board


SIZE = 500
BACKGROUND_COLOR = color(255, 255, 255)
NPCS = 10

board = Board(SIZE)


def setup():
    print "Setting up"
    size(SIZE, SIZE)
    colorMode(HSB, 1)

    for i in range(NPCS):
        board.add_npc()
    board.add_pc()
    board.add_pc()

def draw():
    background(BACKGROUND_COLOR)
    board.update()
    board.draw()

def keyPressed():
    board.keyPressed(key, keyCode)

def keyReleased():
    board.keyReleased(key, keyCode)


