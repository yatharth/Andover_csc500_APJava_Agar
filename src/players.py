#!/usr/bin/env python3

__author__ = 'Yatharth Agarwal <yatharth999@gmail.com>'

"""Define player classes"""

import math
import random

from src import config
from keys import KEY_NAMES
from exceps import DeadException


class Character(object):
    """Behave like a general character"""

    CLASS_NAME = 'p'
    DEAD_LEVEL = 0

    def __init__(self, id_, level, x, y):
        self.id, self._level = id_, level
        self.x, self.y = x, y

    def __str__(self):
        return "<{} id={} level={}>".format(self.CLASS_NAME, self.id, self.level)

    def __repr__(self):
        return "<{} x={} y={} r={}>".format(str(self)[1:-1], self.x, self.y, self.radius)

    @property
    def level(self):
        return int(self._level)

    @level.setter
    def level(self, value):
        """Adjust level, dying as appropriate"""
        self._level = value
        if self.level <= self.DEAD_LEVEL:
            raise DeadException(self)

    @property
    def radius(self):
        return self.level / config.RADIUS_CONSTANT

    # @radius.setter
    # def radius(self, value):
    #     """Update level based on radius (useful for absorbing areas or volumes)"""
    #     self.level = config.RADIUS_CONSTANT * value

    @property
    def velocity(self):
        """Calculate velocity according to complex math"""
        # TODO: make feel more natural
        return (1.0 / (math.log(self.level) / math.log(20) + 1)) * (1 / 200.0)

    @velocity.setter
    def velocity(self, value):
        raise NotImplemented


    @staticmethod
    def shade(level):
        return ((level + 1) / 20.0) % 0.8

    @property
    def color(self):
        return color(self.shade(self.level), 0.75, 0.75)

    @property
    def stroke_color(self):
        return color(self.shade(self.level), 1, 1)

    def collides(self, other):
        """Check if overlapping"""
        return dist(self.x, self.y, other.x, other.y) <= self.radius + other.radius

    def eat(self, other):
        """Grow based on how significant the food is"""
        # self.radius = math.pow(self.radius**3 + other.radius**3, 1/3.0)
        self.level = self._level + float(other.level) / self.level

    def update(self, direction=None, velocity=None):
        """Move appropriately (and overridably), rebounding off of walls"""

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

    def draw(self, conv):
        """Calculate diamater and draw blob"""
        fill(self.color)
        stroke(self.stroke_color)
        strokeWeight(4)
        diameter = conv(self.x + self.radius) - conv(self.x - self.radius)
        ellipse(conv(self.x), conv(self.y), diameter, diameter)



class PC(Character, object):
    """Make character playable"""

    CLASS_NAME = 'pc'
    DEAD_LEVEL = 1

    DEFAULT_LABELS = ['arrows', 'wasd', 'l,./', '=[]\\']
    DIR_NAMES = (
        ('RIGHT', 'UP', 'LEFT', 'DOWN'),
        ('d', 'w', 'a', 's'),
        ('/', 'l', ',', '.'),
        ('\\', '=', '[', ']'),
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
        self.label = label if label is not None else self.DEFAULT_LABELS[self.id]  # TODO: allow name entry
        self.dir_name = self.DIR_NAMES[self.id]

        self.max_level = 1
        self._directions = set()

    def __str__(self):
        return self.label

    @property
    def level(self):
        return super(PC, self).level

    @level.setter
    def level(self, value):
        Character.level.fset(self, value)
        self.max_level = max(self.max_level, value)

    @property
    def direction(self):
        """Calculate direction based on keys pressed"""
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

    @direction.setter
    def direction(self, value):
        """Fake setting of value for the general rebounding code"""
        pass

    @property
    def velocity(self):
        return len(self._directions) and super(PC, self).velocity

    @property
    def stroke_color(self):
        return color(self.shade(self.level - 1), 1, 1)

    def keyPressed(self, key, keyCode):
        """Note that a key was pressed if two weren't already"""
        if len(self._directions) < 2:
            try:
                self._directions.add(
                    self.dir_name.index(key) if key != CODED else self.dir_name.index(KEY_NAMES[keyCode]))
            except ValueError:
                pass

    def keyReleased(self, key, keyCode):
        try:
            self._directions.discard(
                self.dir_name.index(key) if key != CODED else self.dir_name.index(KEY_NAMES[keyCode]))
        except ValueError:
            pass

    def draw(self, conv):
        """Draw label below blob"""
        super(PC, self).draw(conv)

        # label = self.label
        # if self.temporary_label is not None:
        #     if millis() > self.temporary_end:
        #         self.temporary_label = None
        #     else:
        #         label = self.temporary_label

        textAlign(CENTER)
        textSize(12)
        fill(color(0, 0, 0, 0.75))
        text(self.label, conv(self.x), conv(self.y + self.radius + 0.015))


class NPC(Character, object):
    """Represent non-playable character"""

    CLASS_NAME = 'npc'

    def __init__(self, id_, level, x, y):
        super(NPC, self).__init__(id_, level, x, y)
        self.direction = random.random() * (2*math.pi)

    @property
    def velocity(self):
        """Remain stationary if level 1"""
        return self.level - 1 and super(NPC, self).velocity

    def update(self, direction=None, velocity=None):
        """Change velocity a little randomly"""
        self.direction += random.randint(-1, 1) * random.random() * (2*math.pi) / 35.0
        super(NPC, self).update(direction, velocity)

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
