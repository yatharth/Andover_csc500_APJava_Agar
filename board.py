#!/usr/bin/env python3

__author__ = 'Yatharth Agarwal <yatharth999@gmail.com>'

import random
import math

from players import Player, PC, NPC, MaxLevelException, DeadException


class WinException(Exception):
    pass

class LoseException(Exception):
    pass


class Board(object):
    RUNNING = 'r'
    DEAD = 'd'
    WON = 'w'

    def __init__(self, size):
        self.size = size

        self.pcs, self.npcs = [], []
        self.state = self.RUNNING
        self.player = None

    @property
    def cs(self):
        return self.pcs + self.npcs

    def add_c(self, maker):
        first = True
        while first or self.colliders(c) is not None:
            first = False
            c = maker()

        return c

    def add_npc(self):
        def maker():
            level = random.randrange(1, 4) if sum(npc.level == 1 for npc in self.npcs) >= 5 else 1
            x, y = random.random(), 0
            return NPC(len(self.npcs), level, x, y)

        npc = self.add_c(maker)
        self.npcs.append(npc)

    def add_pc(self, label=None):
        def maker():
            x = (1 / 4.0) + (random.random()) * (1 / 2.0)
            return PC(len(self.pcs), 2, x, 0.5, label)

        pc = self.add_c(maker)
        self.pcs.append(pc)

    def keyPressed(self, key, keyCode):
        for pc in self.pcs:
            pc.keyPressed(key, keyCode)

    def keyReleased(self, key, keyCode):
        for pc in self.pcs:
            pc.keyReleased(key, keyCode)

    def colliders(self, c):
        for other in self.cs:
            if c is not other and c.collides(other):
                return other

    def collisions(self):
        for c in self.cs:
            other = self.colliders(c)
            if other is not None:
                return c, other
        return None, None

    def handle_collisions(self):
        # TODO: collide elastically (need to change velocity as property and add resetter for after some updates)

        c, other = self.collisions()
        while (c, other) != (None, None):
            if c.level != other.level:
                eaten = c if c.level < other.level else other
                eater = c if other is eaten else other

                try:
                    eater.level += eaten.level
                except MaxLevelException:
                    self.state = self.WON
                    self.player = eater
                    return

                if eaten in self.npcs:
                    self.npcs.remove(eaten)
                    self.add_npc()
                else:
                    try:
                        eaten.level -= 1
                    except DeadException:
                        self.pcs.remove(eaten)
                        if not self.pcs:
                            self.state = self.DEAD
                            self.player = eaten
                            return
                    else:
                        if eaten in self.pcs:
                            eaten.x = eaten.y = self.size / 2.0
                            while self.colliders(eaten) is not None:
                                eaten.x += self.size / 10.0
                            eaten.temporary_label = random.choice(("You got eaten!", "Be careful!", "Small fish"))
                            eaten.temporary_end = millis() + 1500


            else:
                # TODO: collide reflectively
                direction = -math.atan2(c.y - other.y, c.x - other.x)
                for i in range(100):
                    c.update(direction, Player(0, other.level, 0, 0).velocity)  # TODO: make more elegant
                    other.update(direction + math.pi, Player(0, other.level, 0, 0).velocity)  # FIXME: check after direction minus change

                    if not c.collides(other):
                        break
                else:
                    # FIXME: sometime pass through each other
                    print "didn't uncollide", direction, c.direction, other.direction
            c, other = self.collisions()

    def update(self):
        for c in self.cs:
            c.update()

        self.handle_collisions()

    def draw(self):
        # TODO: draw based on viewports
        # TODO: accomodate two pcs' viewports

        if self.state == self.RUNNING:
            for c in self.cs:
                c.draw(lambda x: x*self.size)
        else:
            if self.state == self.DEAD:
                message = "'{}' died :(".format(self.player.label)  # TODO: make more elegant
            elif self.state == self.WON:
                if self.player in self.pcs:
                    message = "'{}' won!".format(self.player.label)
                else:
                    message = "The AI won before you...".format(self.player)

            textSize(20)
            fill(color(0, 0, 0))
            text(message, self.size / 4.0, self.size / 2.0)