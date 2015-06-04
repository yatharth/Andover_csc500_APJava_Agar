#!/usr/bin/env python3

__author__ = 'Yatharth Agarwal <yatharth999@gmail.com>'

"""Define exceptions for communication between layers of abstraction"""


class AgarException(Exception):
    """Represent abstract behavior for custom exceptions"""

    def __init__(self, player):
        super(AgarException, self).__init__()
        self.player = player


class WonException(AgarException):
    pass


class DeadException(AgarException):
    pass
