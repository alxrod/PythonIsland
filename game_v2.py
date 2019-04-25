#! /user/bin/python

import pygame
from pygame import *
import datetime
from threading import Timer

# Gathering data from my own files:
from levels import *
from basic_set_up import *
from tiles import *
from player import *
from enemy_1 import *
from enemy_2 import *
from dev_testing import *
from arrow import *


def main():
	pygame.init()
	screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
	pygame.display.set_caption("Lux in Tenebris")
	timer = pygame.time.Clock()

	# player options:
	up = down = left = right = attack = craft = open_invent = False

	# Insert information for background image here:

	# Creates groups for all of the types of entities/sprites
	entities = pygame.sprite.Group()
	walls = []
	enemies = [[],[],]
	crates = []
	sticks = []
	string = []
	weapons = []
	arrows = []
	entities_dict = {"walls":walls, 
					 "crates": crates, 
					 "enemies": enemies, 
					 "sticks": sticks,
					 "string": string,
					 "entities": entities,
					 "weapons": weapons,
					 "arrows": arrows
					 }

	cur_level = Level(levels_list[0][0], entities_dict, levels_list[0][1], levels_list[0][2], 0)

	player = Player(cur_level.start_x, cur_level.start_y)
	inventory = Inventory()
	entities_dict["entities"].add(player)

	camera = cur_level.camera

	# This is the main update loop:
	print "displayed text"
	last_time_text_displayed = -1
	# -1 is not the natural state of a time variable which shows program no text needs to be displayed
	need_to_display = False

	while 1:
		cur_weapon_level = player.weapon_level
		cur_health = player.hp
		# This is for calculating FPS
		# begining_of_frame = datetime.datetime.now().microsecond

		# These are the boolean querries to determine the status of the keys
		for e in pygame.event.get():
			if e.type == QUIT: raise SystemExit, "QUIT"
			if e.type == KEYDOWN and e.key == K_ESCAPE:
				raise SystemExit, "ESCAPE"
			if e.type == KEYDOWN and e.key == K_w:
				up = True
			if e.type == KEYDOWN and e.key == K_s:
				down = True
			if e.type == KEYDOWN and e.key == K_a:
				left = True
			if e.type == KEYDOWN and e.key == K_d:
				right = True
			if e.type == KEYDOWN and e.key == K_SPACE:
				running = True
			if pygame.mouse.get_pressed() == (1,0,0):
				attack = True
			if e.type == KEYDOWN and e.key == K_c:
				if craft:
					craft = False
				else:
					craft = True
			if e.type == KEYDOWN and e.key == K_e:
				if open_invent:
					open_invent = False
				else:
					open_invent = True

			if e.type == KEYUP and e.key == K_w:
				up = False
			if e.type == KEYUP and e.key == K_s:
				down = False
			if e.type == KEYUP and e.key == K_a:
				left = False
			if e.type == KEYUP and e.key == K_d:
				right = False
			if pygame.mouse.get_pressed() == (0,0,0):
				attack = False

			# This creates background: 
		for y in range(128):
			for x in range(128):
				screen.blit(bg, (128*x, 128*y))

		for w in entities_dict["walls"]:
			if isinstance(w, ExitBlock) and pygame.sprite.collide_rect(player, w):
				cur_level.update(entities_dict, player)

		for s in entities_dict["sticks"]:
			s.update(player, entities_dict)
		for s in entities_dict["string"]:
			s.update(player, entities_dict)


		player.update(up, down, left, right, attack, entities_dict, screen, camera)

			# for b in bullets:
			# 	b.update(entities_dict)

		camera = cur_level.camera
		camera.update(player)

		for c in entities_dict["crates"]:
			c.update(player, entities_dict, screen)

		for eType in entities_dict["enemies"]:
			for e in eType:
				e.update(entities_dict, screen, attack, cur_level, player)

		for w in entities_dict["walls"]:
			if isinstance(w, Grass):
				screen.blit(w.image, camera.apply(w))

		for e in entities_dict["entities"]:
			if isinstance(e, Player) or isinstance(e, Enemy_1) or isinstance(e, Stick) or isinstance(e, String) or isinstance(e,Grass) or isinstance(e,Arrow):
				pass
			screen.blit(e.image, camera.apply(e))

		for s in entities_dict["sticks"]:
			screen.blit(s.image, camera.apply(s))
		for s in entities_dict["string"]:
			screen.blit(s.image, camera.apply(s))

		screen.blit(player.image, camera.apply(player))
		if (player.xvel == 0 and player.yvel == 0) or attack:
			# print "blitty"
			screen.blit(player.weapon.image, camera.apply(player.weapon))

		for eType in enemies:
			for e in eType:
				screen.blit(e.image, camera.apply(e))	
				health_bar = Health_Bar(e)
				if e.last_time_lost != -1 and (datetime.datetime.now().second - e.last_time_lost) <= 1:
					screen.blit(health_bar.bar_bg, camera.apply(health_bar))
					screen.blit(health_bar.bar, camera.apply(health_bar))

				if (e.xvel == 0 and e.yvel == 0):
					screen.blit(e.weapon.image, camera.apply(e.weapon))

		# Calculating FPS(This is really only for dev purposes!)
		# end_of_frame = datetime.datetime.now().microsecond
		# print "Current FPS:" + str(1000000.0/float(end_of_frame-begining_of_frame))
		
		for a in entities_dict["arrows"]:
			a.update(entities_dict)
			screen.blit(a.image, camera.apply(a))

		should_show = False
		for w in entities_dict["walls"]:
			if isinstance(w, WorkBench):
				w.update(player,inventory,screen,craft,attack,entities_dict)
				should_show = w.should_show_invent

		inventory.update(player)
		if open_invent or should_show:
			screen.blit(inventory.bg_surface, (inventory.rect.x, inventory.rect.y))
			for i in inventory.item_rects:
				screen.blit(inventory.item_box, (i.x, i.y))
				i_index = inventory.item_rects.index(i)
				try:
					screen.blit(inventory.item_icons[i_index], (i.x+10, i.y+8))
					font=pygame.font.Font(None,24)

					# # render text
					label = font.render(str(inventory.num_in_slot[i_index]), 1, (1,1,1))
					screen.blit(label, (i.x+48, i.y+48))

				except:
					pass



		# This portion of the update is for all text to be displayed!
		if need_to_display and (last_time_text_displayed-datetime.datetime.now().second) <= 4:
			font=pygame.font.Font(None,48)

			# render text
			label = font.render("Your Weapon is Now Level " + str(player.weapon_level), 1, (243,196,49))
			screen.blit(label, (300, 24))

			if (datetime.datetime.now().second - last_time_text_displayed) == 3:
				need_to_display = False
				last_time_text_displayed = -1

		if cur_weapon_level != player.weapon_level:
			# Now we make it an actual time
			last_time_text_displayed = datetime.datetime.now().second
			need_to_display = True

		x = 32
		y = 32
 		for h in range(player.hp/20):
 			heart_sheet = pygame.image.load("heart.png")
			heart_image = heart_sheet
			heart_image = pygame.transform.scale(heart_image, (16*2, 16*2))
			screen.blit(heart_image, (x, y))
			x += 32

		x = 32
		y = 64
		for e in range(player.xp/5):
 			heart_sheet = pygame.image.load("xp_bar.png")
			heart_image = heart_sheet
			heart_image = pygame.transform.scale(heart_image, (16, 16))
			screen.blit(heart_image, (x, y))
			x += 16
		# if cur_health != player.hp:
		# 	screen.fill(Color("#8A0707"))


		pygame.display.update()

if  __name__ == "__main__":
	main()

























