import pygame
from pygame import *
import datetime
from threading import Timer
from basic_set_up import *

class Entity(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

class Arrow(Entity):
	def __init__(self, x, y, player):
		Entity.__init__(self)
		self.xvel = 0
		self.yvel = 0
		self.sheet = pygame.image.load("arrow.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (16*4, 8*4))
		self.rect = Rect(x, y, 16*4, 8*4)
		arrow_target = pygame.mouse.get_pos()
		self.when_shot = datetime.datetime.now().second
		

		line_x = float(player.rect.x - arrow_target[0])
		line_y = float(player.rect.y - arrow_target[1])
		slope = line_x/line_y
		if slope > 0:
			if line_x > 0:
				self.image = pygame.transform.flip(self.image, True, False)
		else:
			if line_x > 0:
				self.image = pygame.transform.flip(self.image, True, False)
		if abs(line_x) > abs(line_y):
			if line_x > 0:
				change_inX = -25
			else:
				change_inX = 25
			change_inY = line_y / (line_x / change_inX)
		else:
			if line_y > 0:
				change_inY = -25
			else:
				change_inY = 25
			change_inX = line_x / (line_y / change_inY)

		if arrow_target[0] < self.rect.x:
			self.xvel = change_inX
		elif arrow_target[0] > self.rect.x:
			self.xvel = change_inX

		if arrow_target[1] < self.rect.y:
			self.yvel = change_inY
		elif arrow_target[1] > self.rect.y:
			self.yvel = change_inY

	def update(self, entities_dict):
		if self.xvel > 0:
			# slowing velocity
			self.xvel -= 0.1
		if self.xvel < 0:
			self.xvel += 0.1
		if self.yvel > 0:
			self.yvel -= 0.1
		if self.yvel < 0:
			self.yvel += 0.1

		self.rect.x += self.xvel
		self.rect.y += self.yvel

		if round(self.xvel, 2) == 0 or round(self.yvel, 2) == 0:
			if (datetime.datetime.now().second-self.when_shot) >= 1:
				entities_dict["arrows"].remove(self)
				self.xvel = 0
				self.yvel = 0
				entities_dict["entities"].remove(self)
				self.kill()