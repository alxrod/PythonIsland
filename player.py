#! /user/bin/python

import pygame
from pygame import *
import datetime
from threading import Timer
from basic_set_up import *

from bullet import *
from tiles import *

class Player(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)

		self.hp = 100
		self.xp = 0
		self.xvel = 0
		self.yvel = 0
		self.onGround = True
		self.weapon_level = 1
		self.unlocked_shooting = True
		self.last_hit = -1

		self.rect = Rect(x, y, 20*4,32*4)
		self.last_rect = Rect(x, y, 20*4, 32*4)

		self.sheet = pygame.image.load("player.png")
		self.sheet_size = self.sheet.get_size()
		self.cur_image = 0
		self.cell_width = 32
		self.cell_height = 32

		self.images = []
		self.direction = "up"

		self.weapon = Player_Weapon(self)
		
		self.inventory = [[],[],[],[],[],[],[],[]]

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
			"attack_1_up": [self.images[20],
							self.images[21],
							self.images[22],
						 ],
			"attack_1_right": [self.images[23],
							self.images[23],
							self.images[24],
							self.images[24],
							self.images[25],
							self.images[25],
						 ],
			"attack_1_left": [self.images[26],
							   self.images[26],
							   self.images[27],
							   self.images[27],
							   self.images[28],
							   self.images[28],
						 ],
			"attack_1_down": [self.images[29],
							self.images[29],
							self.images[30],
							self.images[30],
							self.images[31],
							self.images[31],
						 ],
		}

		self.up_counter = 0
		self.down_counter = 0
		self.right_counter = 0
		self.left_counter = 0
		self.attack_counter = 0

		# self.image = self.images[0]
		print "Init Health:"
		print self.hp

	def update( self,
				up, 
				down,
				left,
				right, 
				attack,
				entities_dict,
				screen,
				camera):

		self.last_rect = self.rect.copy()


		if up:
			self.yvel = -20
			if self.up_counter >= 10:
				self.up_counter = 0
			self.up_counter += 1
			self.image = self.anim_sets["run_up"][self.up_counter]
			self.direction = "up"
				
		if down:
			self.yvel = 20
			if self.down_counter >= 10:
				self.down_counter = 0
			self.down_counter += 1
			self.image = self.anim_sets["run_down"][self.down_counter]
			self.direction = "down"
		if left:
			self.xvel = -20
			if self.left_counter >= 10:
				self.left_counter = 0
			self.left_counter += 1
			self.image = self.anim_sets["run_left"][self.left_counter]
			self.direction = "left"
		if right: 
			self.xvel = 20
			if self.right_counter >= 10:
				self.right_counter = 0
			self.right_counter += 1
			self.image = self.anim_sets["run_right"][self.right_counter]
			self.direction = "right"

		if attack == False:
			self.last_hit = -1
			self.attack_counter = 0

		self.weapon.update(self)

		if self.weapon.areAttacking:
			self.xvel = 0
			self.yvel = 0

		if attack and (abs(datetime.datetime.now().microsecond-self.last_hit) >= 500000 or self.last_hit == -1):


			if self.direction == "up":
				self.image = self.images[0]
				self.attack_counter += 1

				if isinstance(self.weapon, Bow):
					if self.attack_counter % 10 == 0:
						self.last_hit = datetime.datetime.now().microsecond
					else:
						self.weapon.shouldReset = False
						self.weapon.areAttacking = True

						self.last_hit = -1
			
						if (self.attack_counter-1) % 10 == 0:
							self.weapon.just_started_attack = True
						self.weapon.attack(self, entities_dict["enemies"], entities_dict["entities"], entities_dict)
						self.weapon.just_started_attack = False

				else:
					# These are temperary additions
					if self.attack_counter % 3 == 0:
						self.last_hit = datetime.datetime.now().microsecond
						self.weapon.hit_vel = 5
					else:
						self.weapon.shouldReset = False
						self.weapon.areAttacking = True

						self.last_hit = -1
			
						self.weapon.hit_vel += 5
					
						if (self.attack_counter-1) % 3 == 0:
							self.weapon.just_started_attack = True
						self.weapon.attack(self, entities_dict["enemies"],entities_dict["entities"], entities_dict)
						self.weapon.just_started_attack = False

			if self.direction == "down":
				self.image = self.images[15]
				self.attack_counter += 1

				# These are temperary additions
				if isinstance(self.weapon, Bow):
					if self.attack_counter % 10 == 0:
						self.last_hit = datetime.datetime.now().microsecond
					else:
						self.weapon.shouldReset = False
						self.weapon.areAttacking = True

						self.last_hit = -1
			
						if (self.attack_counter-1) % 10 == 0:
							self.weapon.just_started_attack = True
						self.weapon.attack(self, entities_dict["enemies"], entities_dict["entities"], entities_dict)
						self.weapon.just_started_attack = False
				else:
					if self.attack_counter % 3 == 0:
						self.last_hit = datetime.datetime.now().microsecond
						# Just repositioning the weapon
						self.weapon.hit_vel = 5
					else:
						self.weapon.shouldReset = False
						self.weapon.areAttacking = True

						self.last_hit = -1
						self.weapon.hit_vel -= 5
						
						if (self.attack_counter-1) % 3 == 0:
							self.weapon.just_started_attack = True
						self.weapon.attack(self, entities_dict["enemies"], entities_dict["entities"], entities_dict)
						self.weapon.just_started_attack = False

			if self.direction == "left":
				
				self.image = self.images[10]
				self.attack_counter += 1

				if isinstance(self.weapon, Bow):    
					if self.attack_counter % 10 == 0:
						self.last_hit = datetime.datetime.now().microsecond
					else:
						self.weapon.shouldReset = False
						self.weapon.areAttacking = True

						self.last_hit = -1
			
						if (self.attack_counter-1) % 10 == 0:
							self.weapon.just_started_attack = True
						self.weapon.attack(self, entities_dict["enemies"], entities_dict["entities"], entities_dict)
						self.weapon.just_started_attack = False
				# These are temperary additions
				else:
					if self.attack_counter % 3 == 0:
						self.last_hit = datetime.datetime.now().microsecond
						self.weapon.hit_vel = 5
					else:
						self.weapon.shouldReset = False
						self.weapon.areAttacking = True

						self.last_hit = -1
					
						self.weapon.hit_vel += 5
						if (self.attack_counter-1) % 3 == 0:
							self.weapon.just_started_attack = True
						self.weapon.attack(self, entities_dict["enemies"],entities_dict["entities"],entities_dict)
						self.weapon.just_started_attack = False
					

			if self.direction == "right":
				self.image = self.images[5]
				self.attack_counter += 1
				if isinstance(self.weapon, Bow):
					if self.attack_counter % 10 == 0:
						self.last_hit = datetime.datetime.now().microsecond
					else:
						self.weapon.shouldReset = False
						self.weapon.areAttacking = True

						self.last_hit = -1
			
						if (self.attack_counter-1) % 10 == 0:
							self.weapon.just_started_attack = True
						self.weapon.attack(self, entities_dict["enemies"], entities_dict["entities"], entities_dict)
						self.weapon.just_started_attack = False
				else:
					# These are temperary additions
					if self.attack_counter % 3 == 0:
						self.last_hit = datetime.datetime.now().microsecond
						# Just repositioning the weapon
						self.weapon.hit_vel = -5
					else:
						self.weapon.shouldReset = False
						self.weapon.areAttacking = True
						self.last_hit = -1
						self.weapon.hit_vel -= 5

						if (self.attack_counter-1) % 3 == 0:
							self.weapon.just_started_attack = True
						self.weapon.attack(self, entities_dict["enemies"],entities_dict["entities"], entities_dict)
						self.weapon.just_started_attack = False
							


		if not(left or right):
			self.xvel = 0

		if not (up or down):
			self.yvel = 0

		if self.xvel == 0 and self.yvel == 0 and attack == False:
			if self.direction == "up":
				self.image = self.images[0]
			if self.direction == "down":
				self.image = self.images[15]
			if self.direction == "right":
				self.image = self.images[5]
			if self.direction == "left":
				self.image = self.images[10]

		if attack == False:
				self.weapon.areAttacking = False
				self.weapon.shouldReset = True

		self.rect.x += self.xvel
		self.rect.y += self.yvel

		self.collide(entities_dict["walls"], entities_dict["enemies"])

	def collide(self, walls, enemies):
		for w in walls:
			# Just temporarily centering the rect relation to the image before testing collision
			if pygame.sprite.collide_rect(self, w):
				# Just need a quick reset.
				if isinstance(w, ExitBlock) or isinstance(w, Grass) or isinstance(w, Path) or isinstance(w, WorkBench):
					pass
				else: 
					self.rect = self.last_rect
					print "Collision!"
		for eType in enemies:
			for e in eType:
				if pygame.sprite.collide_rect(self, e):
					self.rect = self.last_rect
					print "Collided with Enemy"


class Player_Weapon(Entity):
	def __init__(self, player):
		Entity.__init__(self)
		self.rect = Rect(player.rect.x+80, player.rect.y+64, 8*2,16*2)	

		self.sheet = pygame.image.load("short_sword.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (8*4, 16*4))
		self.original_image = self.image
		self.areAttacking = False
		self.just_started_attack = False
		self.shouldReset = True
		self.hit_vel = 5


	def update(self, player):  
		if self.shouldReset == True:
			# print "should reset image"
			self.image = self.original_image

		if player.direction == "right":
			self.rect.y = player.rect.y+20
			self.rect.x = player.rect.x+80
		if player.direction == "left":
			self.rect.y = player.rect.y+20
			self.rect.x = player.rect.x+8
		if player.direction == "up":
			self.rect.y = player.rect.y-8
			self.rect.x = player.rect.x+83
		if player.direction == "down":
			self.rect.y = player.rect.y+40
			self.rect.x = player.rect.x+74

		if self.areAttacking == True and self.just_started_attack == False:
			if player.direction == "left":
				self.rect.y += 37
				self.rect.x -= 36
			elif player.direction == "right":
				self.rect.y += 40
			elif player.direction == "down":
				self.rect.y += 56
			elif player.direction == "up":
				pass


	def attack(self, player, enemies, entities, entities_dict):
		if player.direction == "left":
			self.image = pygame.transform.rotate(self.original_image, 90)
			if player.attack_counter == 1:
				self.rect.y += 37
				self.rect.x -= 36
			self.rect.x -= self.hit_vel


			# Attack enemy based on their collision with so
			for e in enemies[0]:
				if pygame.sprite.collide_rect(self, e) and player.weapon_level >= 1:
					e.hp -= 20*player.weapon_level
					e.last_time_lost = datetime.datetime.now().second
					if (player.rect.x - e.rect.x) < 0:
						e.rect.x += 48
					else:
						e.rect.x -= 48
					if e.hp <= 0:
						e.death(entities_dict)
						if player.xp < 100:
							player.xp+=5
						entities.remove(e)
						enemies[0].remove(e)

			for e in enemies[1]:
				if pygame.sprite.collide_rect(self, e) and player.weapon_level >= 2:
					e.hp -= 20*player.weapon_level
					e.last_time_lost = datetime.datetime.now().second
					if (player.rect.x - e.rect.x) < 0:
						e.rect.x += 48
					else:
						e.rect.x -= 48
					if e.hp <= 0:
						e.death(entities_dict)
						if player.xp < 100:
							player.xp+=5
						entities.remove(e)
						enemies[0].remove(e)

 		if player.direction == "right":
 			self.image = pygame.transform.rotate(self.original_image, -90)
			if player.attack_counter == 1:
				self.rect.y += 40
			self.rect.x -= self.hit_vel


			# Attack enemy based on their collision with so
			for e in enemies[0]:
				if pygame.sprite.collide_rect(self, e) and player.weapon_level >= 1:
					e.hp -= 20*player.weapon_level
					e.last_time_lost = datetime.datetime.now().second
					if (player.rect.x - e.rect.x) < 0:
						e.rect.x += 48
					else:
						e.rect.x -= 48
					if e.hp <= 0:
						e.death(entities_dict)
						if player.xp < 100:
							player.xp+=5
						entities.remove(e)
						enemies[0].remove(e)

			for e in enemies[1]:
				if pygame.sprite.collide_rect(self, e) and player.weapon_level >= 2:
					e.hp -= 20*player.weapon_level
					e.last_time_lost = datetime.datetime.now().second
					if (player.rect.x - e.rect.x) < 0:
						e.rect.x += 48
					else:
						e.rect.x -= 48
					if e.hp <= 0:
						e.death(entities_dict)
						if player.xp < 100:
							player.xp+=5
						entities.remove(e)
						enemies[0].remove(e)

		if player.direction == "down":
 			self.image = pygame.transform.rotate(self.original_image, 180)
			if player.attack_counter == 1:
				self.rect.y += 56
			self.rect.y -= self.hit_vel


			# Attack enemy based on their collision with so
			for e in enemies[0]:
				if pygame.sprite.collide_rect(self, e) and player.weapon_level >= 1:
					e.hp -= 20*player.weapon_level
					e.last_time_lost = datetime.datetime.now().second
					if (player.rect.x - e.rect.x) < 0:
						e.rect.x += 48
					else:
						e.rect.x -= 48
					if e.hp <= 0:
						e.death(entities_dict)
						if player.xp < 100:
							player.xp+=5
						entities.remove(e)
						enemies[0].remove(e)

			for e in enemies[1]:
				if pygame.sprite.collide_rect(self, e) and player.weapon_level >= 2:
					e.hp -= 20*player.weapon_level
					e.last_time_lost = datetime.datetime.now().second
					if (player.rect.x - e.rect.x) < 0:
						e.rect.x += 48
					else:
						e.rect.x -= 48
					if e.hp <= 0:
						e.death(entities_dict)
						if player.xp < 100:
							player.xp+=5
						entities.remove(e)
						enemies[0].remove(e)

		if player.direction == "up":
 			self.image = self.original_image
			if player.attack_counter == 1:
				pass
			self.rect.y -= self.hit_vel


			# Attack enemy based on their collision with so
			for e in enemies[0]:
				if pygame.sprite.collide_rect(self, e) and player.weapon_level >= 1:
					e.hp -= 20*player.weapon_level
					e.last_time_lost = datetime.datetime.now().second
					if (player.rect.x - e.rect.x) < 0:
						e.rect.x += 48
					else:
						e.rect.x -= 48
					if e.hp <= 0:
						e.death(entities_dict)
						if player.xp < 100:
							player.xp+=5
						entities.remove(e)
						enemies[0].remove(e)

			for e in enemies[1]:
				if pygame.sprite.collide_rect(self, e) and player.weapon_level >= 2:
					e.hp -= 20*player.weapon_level
					e.last_time_lost = datetime.datetime.now().second
					if (player.rect.x - e.rect.x) < 0:
						e.rect.x += 48
					else:
						e.rect.x -= 48
					if e.hp <= 0:
						e.death(entities_dict)
						if player.xp < 100:
							player.xp+=5
						entities.remove(e)
						enemies[0].remove(e)









