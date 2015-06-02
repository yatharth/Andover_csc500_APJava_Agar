#!/usr/bin/env python3

__author__ = 'Yatharth Agarwal <yatharth999@gmail.com>'

import math
import random
from collections import defaultdict

from java.awt.event import KeyEvent
from java.lang.reflect import Modifier


class MaxLevelException(Exception):
    pass


class DeadException(Exception):
    pass


class Player(object):
    CLASS_NAME = 'p'
    MAX_LEVEL = 40.0

    def __init__(self, id_, level, x, y):
        self.id_, self._level = id_, level
        self.x, self.y = x, y

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value
        if self.level <= 0:
            raise DeadException("{} died".format(self))

    @property
    def radius(self):
        return (self.level / self.MAX_LEVEL) * (1 / 6.0)  # TODO: match feel of online version

    @property
    def velocity(self):
        return (1.0 / (math.log(self.level) + 1)) * (1 / 200.0)

    def collides(self, other):
        return dist(self.x, self.y, other.x, other.y) <= self.radius + other.radius

    def __str__(self):
        return "<{} id_={} level={}>".format(self.CLASS_NAME, self.id_, self.level)

    def __repr__(self):
        return "{} x={} y={} r={}>".format(str(self)[:-1], self.x, self.y, self.radius)

    def update(self, direction=None, velocity=None):
        if direction is None:
            direction = self.direction
        if velocity is None:
            velocity = self.velocity
        self.x += velocity * math.cos(-direction)
        self.y += velocity * math.sin(-direction)

        if not 0 <= self.x <= 1:
            self.direction = math.pi - self.direction
            self.x = max(min(self.x, 1), 0)
        if not 0 <= self.y <= 1:
            self.direction *= -1
            self.y = max(min(self.y, 1), 0)

    def draw(self, conv, stroke_color=None):
        shade = self.level / self.MAX_LEVEL
        fill(color(shade, 0.75, 0.75))
        stroke(color(shade if stroke_color is None else stroke_color, 1, 1))
        ellipse(conv(self.x), conv(self.y), conv(self.radius*2), conv(self.radius*2))


class PC(Player, object):
    CLASS_NAME = 'pc'
    KEY_NAMES = defaultdict(lambda: 'UNKNOWN')
    DEFAULT_LABELS = ['You', 'wasd', 'l,./']
    DIR_NAMES = (
        ('RIGHT', 'UP', 'LEFT', 'DOWN'),
        ('d', 'w', 'a', 's'),
        ('/', 'l', ',', '.'),
    )
    DOUBLE_DIR_MAPS = {
        0: {
            1: 1/8.0,
            2: 1/4.0,
            3: 7/8.0,
        }, 1: {
            2: 3/8.0,
            3: 1/2.0,
        }, 2: {
            3: 5/8.0,
        },
    }

    def __init__(self, id_, level, x, y, label=None):
        super(PC, self).__init__(id_, level, x, y)
        self.label = label if label is not None else self.DEFAULT_LABELS[self.id_]

        self.temporary_label, self.temporary_end = None, None
        self.dir_name = self.DIR_NAMES[self.id_]
        self.max_level = 1
        self._directions = set()

    @property
    def level(self):
        return super(PC, self).level

    @level.setter
    def level(self, value):
        Player.level.fset(self, value)
        if self.level > self.MAX_LEVEL:
            raise MaxLevelException("{} maxed out".format(self))
        self.max_level = max(self.max_level, value)

    @property
    def velocity(self):  # cheating?
        return Player.velocity.fgets(self) + 60

    def keyPressed(self, key, keyCode):
        try:
            self._directions.add(
                self.dir_name.index(key) if key != CODED else self.dir_name.index(self.KEY_NAMES[keyCode]))
        except ValueError:
            pass


    def keyReleased(self, key, keyCode):
        try:
            self._directions.discard(
                self.dir_name.index(key) if key != CODED else self.dir_name.index(self.KEY_NAMES[keyCode]))
        except ValueError:
            pass

    @property
    def direction(self):
        l = len(self._directions)
        if l == 1:
            return tuple(self._directions)[0] * math.pi / 2.0
        elif l == 2:
            dirs = tuple(sorted(self._directions))
            return math.pi * 2 * self.DOUBLE_DIR_MAPS[dirs[0]][dirs[1]]
        # elif l == 3:
        #     return (tuple(set(range(4)) - self._directions)[0] + 2) * math.pi / 2
        else:
            return 0

    @property
    def velocity(self):
        return super(PC, self).velocity if keyPressed and (key in self.dir_name or (key == CODED and self.KEY_NAMES[keyCode] in self.dir_name)) else 0

    @direction.setter
    def direction(self, value):
        pass  # TODO: avoid need

    def draw(self, conv):
        super(PC, self).draw(conv, stroke_color=(self.level - 1)/self.MAX_LEVEL)

        label = self.label
        if self.temporary_label is not None:
            if millis() > self.temporary_end:
                self.temporary_label = None
            else:
                label = self.temporary_label

        textSize(8)
        fill(color(0, 0, 0, 0.75))
        textAlign(CENTER)
        text(label, conv(self.x), conv(self.y + self.radius + 0.02))


class NPC(Player, object):
    CLASS_NAME = 'npc'

    def __init__(self, id_, level, x, y):
        super(NPC, self).__init__(id_, level, x, y)

        self.direction = random.random() * (2*math.pi)

    def update(self, direction=None, velocity=None):
        # TODO: add AI
        # smallest = None
        # largest = None
        #
        # for other in cs:
        #     if self is other:
        #         continue
        #     # print "{}: {} < {} + {} + {}".format(self.dist(other) < - self.radius - other.radius + self.REACTION_THRESHOLD, self.dist(other), - self.radius, - other.radius,  self.REACTION_THRESHOLD)
        #     if self.dist(other) < - self.radius - other.radius + self.REACTION_THRESHOLD:
        #         if largest is None or other.level > largest.level:
        #             largest = other
        #         if smallest is None or other.level < smallest.level:
        #             smallest = other
        #
        # if largest is not None:
        #     print "largest"
        #     self.direction = math.atan2(self.y - other.y, self.x - other.x)
        # elif smallest is not None:
        #     print "smallest"
        #     self.direction = math.atan2(other.y - self.y, other.x - self.x)
        # else:
        #     self.direction += (random.randrange(3) - 1) * random.random() * 2 * math.pi / 32
        self.direction += random.randint(-1, 1) * random.random() * (2*math.pi) / 35.0

        super(NPC, self).update(direction, velocity)


for f in KeyEvent.getDeclaredFields():
    if Modifier.isStatic(f.getModifiers()):
        name = f.getName()
        if name.startswith("VK_"):
            PC.KEY_NAMES[f.getInt(None)] = name[3:]