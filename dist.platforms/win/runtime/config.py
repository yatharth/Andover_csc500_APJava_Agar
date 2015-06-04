#!/usr/bin/env python3

__author__ = 'Yatharth Agarwal <yatharth999@gmail.com>'

"""Hold constants for game configuration"""


SIZE = 500                              # size of window (in px)
RADIUS_CONSTANT = 600.0                 # increase to make grid seem larger
BACKGROUND_COLOR = color(255, 255, 255) # color of background (in RGB)
VIEW_SIDE_PADDING = 0.2                 # how much you can see around you (in % of grid)
NO_OF_GRIDLINES = 20                    # grid lines (no)

NO_OF_NPCS = 35                         # non-playable characters at any time (no)
NO_OF_PCS = 2                           # playable characters to start with (no)
MIN_SMALL_NPCS = 20                     # smallest, non-moving NPCs at any time (no)
MAX_NPC_INITIAL_LEVEL = 5               # max level of spawning NPCs

LONG_TOAST_LENGTH = 2500                # duration of toasts normally (in milliseconds)
SHORT_TOAST_LENGTH = 500                # duration of toasts with others queued (in milliseconds)
MAX_PLACEMENT_TRIES = 1000              # times to try placing a character without overlap (no)
