#!/usr/bin/env python3

__author__ = 'Yatharth Agarwal <yatharth999@gmail.com>'

"""Map keys for decoding raw key data"""

from collections import defaultdict

from java.awt.event import KeyEvent
from java.lang.reflect import Modifier


KEY_NAMES = defaultdict(lambda: 'UNKNOWN')

for f in KeyEvent.getDeclaredFields():
    if Modifier.isStatic(f.getModifiers()):
        name = f.getName()
        if name.startswith("VK_"):
            KEY_NAMES[f.getInt(None)] = name[3:]