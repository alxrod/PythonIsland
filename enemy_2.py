#! /user/bin/python

import pygame
from pygame import *
import datetime
from threading import Timer

from enemy_1 import *
from basic_set_up import *

class Enemy_2(Enemy_1):
	def __init__(self, x, y):
		Enemy_1.__init__(self, x, y)
		self.weapon_level = 2
		# Want different appearance than standard enemy
		self.image.fill(Color("#009900"))
