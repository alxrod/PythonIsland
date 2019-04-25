#! /user/bin/python

import pygame
from pygame import *
import datetime
from threading import Timer
import random

from tiles import *
from basic_set_up import *

class Enemy_1(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.xvel = 12
		self.yvel = 0
		self.hp = 100

		self.rect = Rect(x, y, 20*4,32*4)
		self.last_rect = Rect(x, y, 20*4,32*4)

		self.last_attack = -1

		self.sheet = pygame.image.load("savage1.png")
		self.sheet_size = self.sheet.get_size()
		self.cur_image = 0
		self.cell_width = 32
		self.cell_height = 32
		self.direction = "right"
		self.weapon_level = 1

		self.last_time_lost = -1

		self.weapon = Enemy_Weapon(self)

		self.images = []

		for y in range(0, self.sheet_size[1], self.cell_height):
			for x in range(0, self.sheet_size[0], self.cell_width):
				surface = pygame.Surface((self.cell_height, self.cell_height),pygame.SRCALPHA)
				surface.blit(self.sheet, (0,0), ( x, y, self.cell_width, self.cell_height))
				surface = pygame.transform.scale(surface, (32*4,32*4))
				self.images.append(surface)

		self.image = self.images[0]

		self.anim_sets = {
			"run_up": [self.images[0], 
					   self.images[0], 
					   self.images[1], 
					   self.images[1], 
					   self.images[2], 
					   self.images[2], 
					   self.images[0], 
					   self.images[0], 
					   self.images[3], 
					   self.images[3], 
					   self.images[4], 
					   self.images[4]
					  ],

			"run_right": [self.images[5],
						  self.images[5],
						  self.images[6],
						  self.images[6],
						  self.images[7],
						  self.images[7],
						  self.images[5],
						  self.images[5],
						  self.images[8],
						  self.images[8],
						  self.images[9],
						  self.images[9]
						 ],

			"run_left": [self.images[10],
						  self.images[10],
						  self.images[11],
						  self.images[11],
						  self.images[12],
						  self.images[12],
						  self.images[10],
						  self.images[10],
						  self.images[13],
						  self.images[13],
						  self.images[14],
						  self.images[14]
						 ],
			"run_down": [self.images[15],
						  self.images[15],
						  self.images[16],
						  self.images[16],
						  self.images[17],
						  self.images[17],
						  self.images[15],
						  self.images[15],
						  self.images[18],
						  self.images[18],
						  self.images[19],
						  self.images[19]
						 ],
			"attack_left": [self.images[26],
						    self.images[26],
						    self.images[27],
						    self.images[27],
						    self.images[28],
						    self.images[28],
						 ],
			"attack_right": [self.images[23],
						    self.images[23],
						    self.images[24],
						    self.images[24],
						    self.images[25],
						    self.images[25],
						 ],
		}

		self.up_counter = 0
		self.down_counter = 0
		self.right_counter = 0
		self.left_counter = 0
		self.attack_counter = 0






	def update(self, entities_dict, screen, attack, cur_level, player):
		self.last_rect = self.rect.copy()
		self.rect.x += self.xvel

		if self.left_counter >= 10:
			self.left_counter = 0

		self.left_counter += 1
		if self.xvel < 0:
			self.image = self.anim_sets["run_left"][self.left_counter]
		else:
			self.image = self.anim_sets["run_right"][self.left_counter]

		self.collide(entities_dict["walls"], player)
		self.attack_player(player, attack, entities_dict["walls"], cur_level)

		if self.weapon.areAttacking == False:
			if self.xvel == 0:
				if self.direction == "right":
					self.xvel = 12
				if self.direction == "left":
					self.xvel = -12
			self.attack_counter = 0


	def collide(self, walls, player):
		for w in walls:
			if pygame.sprite.collide_rect(self, w):
				# Just need a quick reset.
				if isinstance(w, ExitBlock) or isinstance(w, Grass) or isinstance(w, Path):
					pass
				else: 
					self.rect = self.last_rect
					self.xvel = -(self.xvel)
					if self.xvel < 0:
						self.direction = "left"
					elif self.xvel >= 0:
						self.direction = "right"
		if pygame.sprite.collide_rect(self, player):
			self.rect = self.last_rect

	def attack_player(self, player, ifPlayerIsAttacking, walls, cur_level):
		self.weapon.update(self)
		if abs(self.rect.x-player.rect.x) <= 84 and abs(self.rect.y-player.rect.y) <= 84:
			print "Fire"
			if self.direction == "left":
				self.image = self.images[10]
			elif self.direction == "right":
				self.image = self.images[5]
			if self.last_attack == -1:
				self.xvel = 0
				self.attack_counter += 1

				if self.attack_counter % 5 == 0:
					if self.direction == "left":
						self.weapon.hit_vel = 5
					elif self.direction == "right":
						self.weapon.hit_vel = -5
				else:
					if self.direction == "left":
						self.weapon.hit_vel += 5
					elif self.direction == "right":
						self.weapon.hit_vel -= 5
				self.weapon.shouldReset = False
				self.weapon.areAttacking = True
				self.last_hit = -1

				if (self.attack_counter - 1) % 5 == 0:
					self.weapon.just_started_attack = True

				self.weapon.attack(self, player, ifPlayerIsAttacking, walls)
				self.weapon.just_started_attack = False

		if abs(self.rect.x-player.rect.x) > 84 or abs(self.rect.y-player.rect.y) > 84:
			self.weapon.areAttacking = False
	def death(self, entities_dict):
		for i in range(random.randint(1,2)):
			string_x = self.rect.x + random.randint(32,96)
			string_y = self.rect.y + random.randint(32,96)
			string = String(string_x, string_y)
			entities_dict["string"].append(string)
			entities_dict["entities"].add(string)

class Enemy_Weapon(Entity):
	def __init__(self, enemy):
		Entity.__init__(self)
		self.rect = Rect(enemy.rect.x+80, enemy.rect.y+64, 8*2,16*2)	

		self.sheet = pygame.image.load("spear.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (8*4, 16*4))
		self.original_image = self.image
		self.areAttacking = False
		self.just_started_attack = False
		self.shouldReset = True
		self.hit_vel = 5


	def update(self, enemy,):  
		if self.shouldReset == True:
			self.image = self.original_image

		if enemy.direction == "right":
			self.rect.y = enemy.rect.y+20
			self.rect.x = enemy.rect.x+80
		if enemy.direction == "left":
			self.rect.y = enemy.rect.y+20
			self.rect.x = enemy.rect.x+8
		if enemy.direction == "up":
			self.rect.y = enemy.rect.y-8
			self.rect.x = enemy.rect.x+83
		if enemy.direction == "down":
			self.rect.y = enemy.rect.y+40
			self.rect.x = enemy.rect.x+74

		if self.areAttacking == True and self.just_started_attack == False:
			if enemy.direction == "left":
				self.rect.y += 37
				self.rect.x -= 36
			elif enemy.direction == "right":
				self.rect.y += 40
			elif enemy.direction == "down":
				self.rect.y += 56
			elif enemy.direction == "up":
				pass


	def attack(self, enemy, player, ifPlayerIsAttacking, walls):

		# self.rect.y += 40

		if enemy.direction == "left":
			self.image = pygame.transform.rotate(self.original_image, 90)
			if enemy.attack_counter == 1:
				self.rect.y += 40
				self.rect.x -= 36
			self.rect.x -= self.hit_vel

			if enemy.attack_counter % 6 == 0:
				if pygame.sprite.collide_rect(self, player) and player.weapon_level >= enemy.weapon_level:
					if ifPlayerIsAttacking == False:
						player.hp -= 20
						if player.hp <= 0:
							pygame.event.post(pygame.event.Event(QUIT))
							pass


						if enemy.direction == "right":
							enemy.xvel = 12
						if enemy.direction == "left":
							enemy.xvel = -12
		

		if enemy.direction == "right":
			self.image = pygame.transform.rotate(self.original_image, -90)
			if enemy.attack_counter == 1:
				self.rect.y += 40
			self.rect.x -= self.hit_vel

			if enemy.attack_counter % 6 == 0:
				if pygame.sprite.collide_rect(self, player) and player.weapon_level >= enemy.weapon_level:
					if ifPlayerIsAttacking == False:
						player.hp -= 20
						if player.hp <= 0:
							pygame.event.post(pygame.event.Event(QUIT))
							pass


						if enemy.direction == "right":
							enemy.xvel = 12
						if enemy.direction == "left":
							enemy.xvel = -12

		
 		

		if enemy.direction == "down":
 			self.image = pygame.transform.rotate(self.original_image, 180)
			if enemy.attack_counter == 1:
				self.rect.y += 56
			self.rect.y -= self.hit_vel


			# Attack enemy based on their collision with so
			if enemy.attack_counter % 6 == 0:
				if pygame.sprite.collide_rect(self, player) and player.weapon_level >= enemy.weapon_level:
					if ifPlayerIsAttacking == False:
						player.hp -= 20
						if player.hp <= 0:
							# pygame.event.post(pygame.event.Event(QUIT))
							pass


						if enemy.direction == "right":
							enemy.xvel = 12
						if enemy.direction == "left":
							enemy.xvel = -12

	

		if enemy.direction == "up":
 			self.image = self.original_image
			if enemy.attack_counter == 1:
				pass
			self.rect.y -= self.hit_vel

			# Attack enemy based on their collision with so
			if enemy.attack_counter % 6 == 0:
				if pygame.sprite.collide_rect(self, player) and player.weapon_level >= enemy.weapon_level:
					if ifPlayerIsAttacking == False:
						player.hp -= 20
						if player.hp <= 0:
							# pygame.event.post(pygame.event.Event(QUIT))
							pass


						if enemy.direction == "right":
							enemy.xvel = 12
						if enemy.direction == "left":
							enemy.xvel = -12

		










		
