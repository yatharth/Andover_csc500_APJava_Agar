#!/usr/bin/env python3

__author__ = 'Yatharth Agarwal <yatharth999@gmail.com>'

"""Define board and controller classes"""

import random
import math
import itertools

import config
from players import Character, PC, NPC
from exceps import WonException, DeadException


class Board(object):
    """Draw game board"""

    def __init__(self, size):
        self.size = size
        self.gridlines = size // config.NO_OF_GRIDLINES

        self.pcs, self.npcs = [], []

    @property
    def cs(self):
        return self.pcs + self.npcs

    def add_c(self, maker):
        """Keep making characters until one doesn't overlap with anything else"""
        for i in xrange(config.MAX_PLACEMENT_TRIES):
            c = maker()
            if self.collision_with(c) is None:
                break
        else:
            raise AssertionError("couldn't place character")
        return c

    def add_npc(self):
        def maker():
            level = random.randrange(1, config.MAX_NPC_INITIAL_LEVEL) \
                if sum(npc.level == 1 for npc in self.npcs) >= config.MIN_SMALL_NPCS else 1
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
                for i in xrange(config.MAX_PLACEMENT_TRIES):
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
        c_min, c_max = max(0, min(coords) - config.VIEW_SIDE_PADDING), min(1, max(coords) + config.VIEW_SIDE_PADDING)

        m = self.size / (c_max - c_min)
        k = - m * c_min

        return lambda c: m*c + k

    def draw_gridlines(self, conv):
        stroke(color(0, 0, 0.75))
        strokeWeight(0)
        # offset = (self.size % config.NO_OF_GRIDLINES) / 2
        # for c in range(offset, self.size + offset, config.NO_OF_GRIDLINES):
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
        self.board = Board(config.SIZE)

        for _ in xrange(config.NO_OF_NPCS):
            self.board.add_npc()
        for _ in xrange(config.NO_OF_PCS):
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
                (config.LONG_TOAST_LENGTH if len(self.toasts) == 1 else config.SHORT_TOAST_LENGTH):
            self.toasts = self.toasts[1:]
            self.toast_started = millis()

        if self.toasts:
            message = self.toasts[0]

            fill(color(0, 0, 0.25, 0.5))
            strokeWeight(0)
            rect(0, config.SIZE - 60, config.SIZE, 50)

            textAlign(CENTER)
            textSize(30)
            fill(color(0, 0, 1, 0.5))
            text(message, config.SIZE / 2.0, config.SIZE - 25)

    def toast(self, message):
        """Add message to toaster"""
        if not self.toasts:
            self.toast_started = millis()
        self.toasts.append(message)

    def draw_title(self):
        textAlign(CENTER)

        textSize(50)
        fill(color(0, 0, 0))
        text("Agar", config.SIZE / 2.0, 100)

        textSize(30)
        fill(color(0, 0, 0.75))
        text("Press space to play", config.SIZE / 2.0, config.SIZE - 200)

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
