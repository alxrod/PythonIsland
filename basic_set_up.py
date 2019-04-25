#! /user/bin/python

import pygame
from pygame import *
import datetime
from threading import Timer
from tiles import *
from arrow import *

# Initializing variables:

WIN_WIDTH = 800
WIN_HEIGHT = 700
HALF_WIDTH = WIN_WIDTH / 2
HALF_HEIGHT = WIN_HEIGHT /2

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

# This just sets up a parrent class for all the other sprites
class Entity(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

# This is the camera class and its two companion functions

class Camera(object):
	def __init__(self, camera_func, width, height):
		self.camera_func = camera_func
		self.state = Rect(0, 0, width, height)

	def apply(self, target):
		return target.rect.move(self.state.topleft)

	def update(self, target):
		self.state = self.camera_func(self.state, target.rect)

# This func is mostly for testing and trying to adjust angle
def simple_camera(camera, target_rect):
	l, t, _, _ = target_rect
	_, _, w, h = camera
	return Rect(-l+WIN_WIDTH, -t+WIN_HEIGHT, w, h)

def complex_camera(camera, target_rect):
	l = target_rect.x
	t = target_rect.y 
	
	_, _, w, h = camera
	l, t, _, _, = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

	l = min(0, l)
	t = min (0, t)

	return Rect(l, t, w, h)

class Health_Bar(Entity):
	def __init__(self,  host):
		Entity.__init__(self)
		self.health_bar_size = 0
		for i in range(host.hp / 20):
			self.health_bar_size += 20
		self.bar = Surface((self.health_bar_size, 8)).convert()
		self.bar_bg = Surface((100, 8)).convert()
		self.bar.fill(Color("#ff0000"))
		self.bar_bg.fill(Color("#000000"))
		self.rect = Rect(host.rect.x, host.rect.y-16, self.health_bar_size, 8)

	def update(host):
		for i in range(host.hp / 20):
			self.health_bar_size += 20

class Stick(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.rect = Rect(x+48, y+48, 16*3, 16*3)

		self.sheet = pygame.image.load("stick.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (16*3, 16*3))

	def update(self, player, entities_dict):
		if pygame.sprite.collide_rect(self, player):
			for i in player.inventory:
				if not i:
					print "Picking up stick for first time."
					i.append(self)
					entities_dict["sticks"].remove(self)
					entities_dict["entities"].remove(self)
					return "added"
					
				else:
					for e in i:
						if isinstance(e, Stick):
							print "Something in the first slot."
							i.append(self)
							entities_dict["sticks"].remove(self)
							entities_dict["entities"].remove(self)
							print "added it to first slot!"
							print player.inventory
							return "added"
						else:
							print "inventory full"
	def give_player(self, player):
		for i in player.inventory:
			if not i:
				i.append(self)
				return "added"
					
			else:
				for e in i:
					if isinstance(e, Stick):
						i.append(self)
						return "added"
					else:
						print "inventory full"

class String(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.rect = Rect(x+48, y+48, 16*3, 16*3)

		self.sheet = pygame.image.load("string.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (16*3, 16*3))

	def update(self, player, entities_dict):
		if pygame.sprite.collide_rect(self, player):
			for i in player.inventory:
				if not i:
					print "Picking up stick for first time."
					i.append(self)
					entities_dict["string"].remove(self)
					entities_dict["entities"].remove(self)
					return "added"
					
				else:
					for e in i:
						if isinstance(e, String):
							print "Something in the first slot."
							i.append(self)
							entities_dict["string"].remove(self)
							entities_dict["entities"].remove(self)
							print "added it to first slot!"
							print player.inventory
							return "added"
						else:
							print "inventory full"

	def give_player(self, player):
		for i in player.inventory:
			if not i:
				i.append(self)
				return "added"
					
			else:
				for e in i:
					if isinstance(e, String):
						i.append(self)
						return "added"
					else:
						print "inventory full"
class Bow(Entity):
	def __init__(self, player):
		Entity.__init__(self)
		self.rect = Rect(player.rect.x+80, player.rect.y+32, 16*4, 16*4)

		self.sheet = pygame.image.load("bow.png")
		self.images = []
		self.sheet_size = self.sheet.get_size()
		self.cur_image = 0
		self.cell_width = 16
		self.cell_height = 16

		for y in range(0, self.sheet_size[1], self.cell_height):
			for x in range(0, self.sheet_size[0], self.cell_width):
				surface = pygame.Surface((self.cell_height, self.cell_height),pygame.SRCALPHA)
				surface.blit(self.sheet, (0,0), ( x, y, self.cell_width, self.cell_height))
				surface = pygame.transform.scale(surface, (16*4,16*4))
				self.images.append(surface)

		
		self.image = self.images[0]
		self.original_image = self.image
		self.areAttacking = False
		self.just_started_attack = False
		self.shouldReset = True
		self.anim_sets = {
						"shoot_side": [self.images[1],
									   self.images[1],
									   self.images[2],
									   self.images[2],
									   self.images[3],
									   self.images[3],
									   self.images[2],
									   self.images[2],
									   self.images[1],
									   self.images[1],],
						"shoot_up":   [self.images[5],
									   self.images[5],
									   self.images[6],
									   self.images[6],
									   self.images[7],
									   self.images[7],
									   self.images[5],
									   self.images[5],
									   self.images[6],
									   self.images[6],]  
		}
		self.test_img = self.images[0]
		self.test_img = pygame.transform.flip(self.test_img, True, False)
		self.anim_count = 0 


	def update(self, player):
		if self.shouldReset == True:
			# print "should reset image"
			self.anim_count = 0
			self.image = self.original_image

		if player.direction == "right":
			self.rect.y = player.rect.y+48
			self.rect.x = player.rect.x+64
		if player.direction == "left":
			self.image = self.images[0]
			self.image = pygame.transform.flip(self.image, True, False)
			self.rect.y = player.rect.y+48
			self.rect.x = player.rect.x-8
		if player.direction == "up":
			self.image = self.images[4]
			self.rect.y = player.rect.y
			self.rect.x = player.rect.x+74
		if player.direction == "down":
			self.image = self.images[4]
			self.rect.y = player.rect.y+54
			self.rect.x = player.rect.x+64 

		if self.areAttacking == True and self.just_started_attack == False:
			pass

	def attack(self, player, enemies, entities, entities_dict):
		if player.direction == "left":
			# Attack enemy based on their collision with so
			if self.anim_count > 9:
				self.anim_count = 0
			self.image = self.anim_sets["shoot_side"][self.anim_count]
			self.image = pygame.transform.flip(self.image, True, False)
			self.anim_count += 1

			if self.anim_count == 5:
				print "Creating arrow"
				arrow = Arrow(self.rect.x, self.rect.y, player)
				entities_dict["entities"].add(arrow)
				entities_dict["arrows"].append(arrow)


 		if player.direction == "right":
 			# Attack enemy based on their collision with so
			if self.anim_count > 9:
				self.anim_count = 0
			self.image = self.anim_sets["shoot_side"][self.anim_count]
			self.anim_count += 1

			if self.anim_count == 5:
				print "Creating arrow"
				arrow = Arrow(self.rect.x, self.rect.y, player)
				entities_dict["entities"].add(arrow)
				entities_dict["arrows"].append(arrow)
		if player.direction == "down":
			# Attack enemy based on their collision with so
			if self.anim_count > 9:
				self.anim_count = 0
			self.image = self.anim_sets["shoot_up"][self.anim_count]
			self.anim_count += 1

			if self.anim_count == 5:
				print "Creating arrow"
				arrow = Arrow(self.rect.x, self.rect.y, player)
				entities_dict["entities"].add(arrow)
				entities_dict["arrows"].append(arrow)
		if player.direction == "up":
			# Attack enemy based on their collision with so
			if self.anim_count > 9:
				self.anim_count = 0
			self.image = self.anim_sets["shoot_up"][self.anim_count]
			self.anim_count += 1

			if self.anim_count == 5:
				print "Creating arrow"
				arrow = Arrow(self.rect.x, self.rect.y, player)
				entities_dict["entities"].add(arrow)
				entities_dict["arrows"].append(arrow)

	def give_player(self, player, entities_dict):
		player.weapon = self
		for i in player.inventory:
				if not i:
					print "Picking up bow for first time."
					i.append(self)
					entities_dict["weapons"].append(self)
					entities_dict["entities"].add(self)
					return "added"
					
				else:
					for e in i:
						if isinstance(e, Bow):
							print"Can't stack bows"
							return "can't add"
						else:
							print "inventory full"

class Inventory(Entity):
	def __init__(self):
		Entity.__init__(self)
		self.rect = Rect(50, 300, 176*4, 22*4)
		self.sheet1 = pygame.image.load("inventory_bg.png")
		self.sheet2 = pygame.image.load("item_box.png")
		self.bg_surface = self.sheet1
		self.bg_surface = pygame.transform.scale(self.bg_surface, (176*4, 22*4))
		self.item_box = self.sheet2
		self.item_box = pygame.transform.scale(self.item_box, (18*4, 18*4))
		self.item_rects = []
		self.item_icons = [Surface((16*3,16*3)).fill(Color("#EEDBA8")),
						   Surface((16*3,16*3)).fill(Color("#EEDBA8")),
						   Surface((16*3,16*3)).fill(Color("#EEDBA8")),
						   Surface((16*3,16*3)).fill(Color("#EEDBA8")),
						   Surface((16*3,16*3)).fill(Color("#EEDBA8")),
						   Surface((16*3,16*3)).fill(Color("#EEDBA8")),
						   Surface((16*3,16*3)).fill(Color("#EEDBA8")),
						   Surface((16*3,16*3)).fill(Color("#EEDBA8")),]
		self.num_in_slot = [0,0,0,0,0,0,0,0]
		x = 86
		y = 306
		for i in range(8):
			rect = Rect(x, y, 18*4,18*4)
			self.item_rects.append(rect)
			x += 20*4
	def update(self,player):
		for i in player.inventory:
			if i:
				nes_icon =  i[0].image
				i_index = player.inventory.index(i)
				self.item_icons[i_index] = nes_icon
				self.num_in_slot[i_index] = len(i)






