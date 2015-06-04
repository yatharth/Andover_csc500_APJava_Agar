#!/usr/bin/env python3

__author__ = 'Yatharth Agarwal <yatharth999@gmail.com>'

"""Bring everything (almost copy-pasted) into one file

This is necessary because of a bug in the Python processing implementation that doesn't let one export apps otherwise.
"""

import launcher
launcher.create()



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
SHORT_TOAST_LENGTH = 300                # duration of toasts with others queued (in milliseconds)
MAX_PLACEMENT_TRIES = 1000              # times to try placing a character without overlap (no)



from collections import defaultdict

from java.awt.event import KeyEvent
from java.lang.reflect import Modifier


KEY_NAMES = defaultdict(lambda: 'UNKNOWN')

for f in KeyEvent.getDeclaredFields():
    if Modifier.isStatic(f.getModifiers()):
        name = f.getName()
        if name.startswith("VK_"):
            KEY_NAMES[f.getInt(None)] = name[3:]
            
class AgarException(Exception):
    """Represent abstract behavior for custom exceptions"""

    def __init__(self, player):
        super(AgarException, self).__init__()
        self.player = player



class WonException(AgarException):
    pass


class DeadException(AgarException):
    pass


import math
import random


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
        return self.level / RADIUS_CONSTANT

    # @radius.setter
    # def radius(self, value):
    #     """Update level based on radius (useful for absorbing areas or volumes)"""
    #     self.level = RADIUS_CONSTANT * value

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



import itertools

class Board(object):
    """Draw game board"""

    def __init__(self, size):
        self.size = size
        self.gridlines = size // NO_OF_GRIDLINES

        self.pcs, self.npcs = [], []

    @property
    def cs(self):
        return self.pcs + self.npcs

    def add_c(self, maker):
        """Keep making characters until one doesn't overlap with anything else"""
        for i in xrange(MAX_PLACEMENT_TRIES):
            c = maker()
            if self.collision_with(c) is None:
                break
        else:
            raise AssertionError("couldn't place character")
        return c

    def add_npc(self):
        def maker():
            level = random.randrange(1, MAX_NPC_INITIAL_LEVEL) \
                if sum(npc.level == 1 for npc in self.npcs) >= MIN_SMALL_NPCS else 1
            x, y = random.random(), random.random()
            return NPC(len(self.npcs), level, x, y)

        npc = self.add_c(maker)
        self.npcs.append(npc)

    def add_pc(self, label=None):
        def maker():
            x, y = 1 / 4.0 + random.random() / 2.0, 0.5
            return PC(len(self.pcs), 2, x, y, label)

        pc = self.add_c(maker)
        self.pcs.append(pc)

    def keyPressed(self, key, keyCode):
        for pc in self.pcs:
            pc.keyPressed(key, keyCode)

    def keyReleased(self, key, keyCode):
        for pc in self.pcs:
            pc.keyReleased(key, keyCode)

    def collision_with(self, c):
        """Return collisions with a certain character, if any"""
        for other in self.cs:
            if c is not other and c.collides(other):
                return other

    def collision(self):
        """Return collisions between any characters, if any"""
        for c in self.cs:
            other = self.collision_with(c)
            if other is not None:
                return c, other
        return None, None

    def handle_collisions(self):
        """Make the characters collide and eat"""
        # TODO: collide elastically (need to change velocity as property and add resetter for after some updates)

        c, other = self.collision()
        while (c, other) != (None, None):

            # if different levels, eat
            if c.level != other.level:
                eaten = c if c.level < other.level else other
                eater = c if eaten is other else other
                eater.eat(eaten)

                # check for win case
                if self.pcs and max(pc.level for pc in self.pcs) > 1 + max(npc.level for npc in self.npcs):
                    raise WonException(eater)

                # kill if NPC and spawn a new one
                if eaten in self.npcs:
                    self.npcs.remove(eaten)
                    self.add_npc()

                # if PC, diminish level
                else:
                    try:
                        eaten.level -= 1

                    # if dead, toast or error out
                    except DeadException as e:
                        self.pcs.remove(eaten)
                        yield "{} died".format(eaten)

                        if not self.pcs:
                            raise e

                    # reset to center
                    else:
                        if eaten in self.pcs:
                            eaten.x = eaten.y = 0.5
                            while self.collision_with(eaten) is not None:
                                eaten.x = (eaten.x + 0.1) % 1
                                if eaten.x == 0.5:
                                    raise AssertionError("couldn't reset pc")

                            yield random.choice(("You got eaten!", "Be careful!", "Small fish in a big pond..."))

            # if same level, collide reflectively
            else:
                direction = - math.atan2(c.y - other.y, c.x - other.x)
                for i in xrange(MAX_PLACEMENT_TRIES):
                    c.update(direction, Character.velocity.fget(c))
                    other.update(direction + math.pi, Character.velocity.fget(other))
                    if not c.collides(other):
                        break
                else:
                    raise AssertionError("didn't uncollide")

            c, other = self.collision()

    def update(self):
        """Move characters and handle collisions"""
        for c in self.cs:
            c.update()

        for toast in self.handle_collisions():
            yield toast

    def make_conv(self):
        """Generate appropriate viewport and return mapper"""
        # TODO: since can't control x and y independently, can't maintain constant scale viewport for one player

        if not self.pcs:
            return lambda c: c * self.size

        coords = tuple(itertools.chain(*((pc.x, pc.y) for pc in self.pcs)))
        c_min, c_max = max(0, min(coords) - VIEW_SIDE_PADDING), min(1, max(coords) + VIEW_SIDE_PADDING)

        m = self.size / (c_max - c_min)
        k = - m * c_min

        return lambda c: m*c + k

    def draw_gridlines(self, conv):
        stroke(color(0, 0, 0.75))
        strokeWeight(0)
        # offset = (self.size % NO_OF_GRIDLINES) / 2
        # for c in range(offset, self.size + offset, NO_OF_GRIDLINES):
        for raw_c in xrange(0, self.gridlines):
            c = conv(float(raw_c) / self.gridlines)
            line(c, 0, c, self.size)
            line(0, c, self.size, c)

    def draw(self):
        conv = self.make_conv()
        self.draw_gridlines(conv)
        for c in self.cs:
            c.draw(conv)

class Controller(object):
    """Handle board and draw play screen"""

    def __init__(self):
        self.playing = False
        self.spectating = False
        self.toasts, self.toast_started = [], None

    def init(self):
        self.playing = True
        self.board = Board(SIZE)

        for _ in xrange(NO_OF_NPCS):
            self.board.add_npc()
        for _ in xrange(NO_OF_PCS):
            self.board.add_pc()

    def keyPressed(self, key, keyCode):
        if not self.playing and key == ' ':
            self.init()
        if self.playing:
            self.board.keyPressed(key, keyCode)

    def keyReleased(self, key, keyCode):
        if self.playing:
            self.board.keyReleased(key, keyCode)

    def draw_toast(self):
        """Draw toasts as overlays"""

        if self.toasts and millis() >= self.toast_started + \
                (LONG_TOAST_LENGTH if len(self.toasts) == 1 else SHORT_TOAST_LENGTH):
            self.toasts = self.toasts[1:]
            self.toast_started = millis()

        if self.toasts:
            message = self.toasts[0]

            fill(color(0, 0, 0.25, 0.5))
            strokeWeight(0)
            rect(0, SIZE - 60, SIZE, 50)

            textAlign(CENTER)
            textSize(30)
            fill(color(0, 0, 1, 0.5))
            text(message, SIZE / 2.0, SIZE - 25)

    def toast(self, message):
        """Add message to toaster"""
        if not self.toasts:
            self.toast_started = millis()
        self.toasts.append(message)

    def draw_title(self):
        textAlign(CENTER)

        textSize(50)
        fill(color(0, 0, 0))
        text("Agar", SIZE / 2.0, 100)

        textSize(30)
        fill(color(0, 0, 0.75))
        text("Press space to play", SIZE / 2.0, SIZE - 200)

    def draw_levels(self):
        """Show percentages to next level"""

        if not self.board.pcs:
            return

        textAlign(LEFT)
        textSize(12)
        fill(color(0, 0, 0))

        text("Percent to next level:", 20, 20)

        for i, pc in enumerate(self.board.pcs):
            percent = int(pc._level % 1 * 100)
            text("{}: {}%".format(pc, percent), 20, 40 + 20*i)

    def draw(self):
        """Draw board and handle events"""

        # ask to replay after giving time for the game's end to sink in
        if self.spectating and not self.toasts:
            self.playing = self.spectating = False

        # draw board
        if self.playing:
            try:
                for toast in self.board.update():
                    self.toast(toast)
            except DeadException as e:
                self.spectating = True
                self.toast("You lost! Max level: {}.".format(int(e.player.max_level)))
            except WonException as e:
                self.spectating = True
                self.toast("You win! Level {}.".format(e.player.level))
            else:
                self.board.draw()
                self.draw_levels()
                self.draw_toast()

        # show play screen
        else:
            self.draw_title()



controller = Controller()

def setup():
    print "Setting up"
    size(SIZE, SIZE)
    colorMode(HSB, 1)
    frame.setTitle("Agar")


def draw():
    background(BACKGROUND_COLOR)
    controller.draw()

def keyPressed():
    controller.keyPressed(key, keyCode)

def keyReleased():
    controller.keyReleased(key, keyCode)
