#! /user/bin/python

import pygame
from pygame import *
import datetime
from threading import Timer

WIN_WIDTH = 800
WIN_HEIGHT = 700
HALF_WIDTH = WIN_WIDTH / 2
HALF_HEIGHT = WIN_HEIGHT /2

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

def main(): 
	pygame.init()
	screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
	pygame.display.set_caption("Lux in Tenebris")
	timer = pygame.time.Clock()

	up = down = left = right = running = attack = shoot = False

	# Just creating black background where there are no tiles

		# self.sheet = pygame.image.load("player.png")
		# self.sheet_size = self.sheet.get_size()
		# self.num_images = 3
		# self.cur_image = 0
		# self.cell_width = 128
		# self.cell_height = 128
		# self.images = []
		# for y in range(0, self.sheet_size[1], self.cell_height):
		# 	for x in range(0, self.sheet_size[0], self.cell_width):
		# 		surface = pygame.Surface((self.cell_width, self.cell_height))
		# 		surface.blit(self.sheet, (0,0), (x, y, self.cell_width, self.cell_height))
		# 		self.images.append(surface)


	
	bg = Surface((64, 64))
	bg.fill(Color("#000000"))


	entities = pygame.sprite.Group()
	walls = []
	enemies = [[],[]]
	crates = []
	bullets = []

	level1Map = [
		"WWWWWWWW               ",
		"W      W               ",
		"W      W  WWWWWWWWWWWWW",
		"W      W  W     B     W",
		"W      W  W           W",
		"W      WWWW     W     W",
		"W               W     W",
		"W               W     W",
		"WWWWWWWWWWWWWWWWW     W",
		"W                     W",
		"W                     W",
		"W      WWWWWWWWWWWWWWWW",
		"W                     W",
		"W     b               W",
		"W            	        W",
		"WWWWWWWWWWWWWWW       W",
		"W                     W",
		"W                  C  W",
		"W                     W",
		"W   b   WWWWWWWWWWWWWWW",
		"W             W        ",
		"W             W        ",
		"W             W        ",
		"WWWWWWWWWW    W        ",
		"         W    W        ",
		"         W    W        ",
		"         W    W        ",
		"         WEEEEW        ",
	]

	level2Map = [
		"   WWWWWWWW                                        ",
		"   W      W                                        ",
		"   W      W                                        ",
		"   W      WWWWWWWWWWWWWWWWWWWWWWWWWWWW             ",
		"   W                                 W             ",
		"   W                     b           W             ",
		"   W                                 W             ",
		"   W                     B           W             ",
		"WWWW            WWWWWWW     WWWW     W             ",
		"W               W     W     W  W     W             ",
		"W               W     W     W  W     WWWWWWWWWWWWWW",
		"W               W     W     W  W                  E",
		"W               W     W     W  W                  E",
		"W               W     W     W  W                  E",
		"WWWWWWWWWWWWWWWWW     W     W  WWWWWWWWWWWWWWWWWWWW",
		"                      W     W                      ",
		"                      W     W                      ",
		"                      W     W                      ",
		"                      W     W                      ",
		"                      W     W                      ",
		"                   WWWW     WWWW                   ",
		"                   W           W                   ",
		"                   W           W                   ",
		"                   W           W                   ",
		"                   W           W                   ",
		"                   W           W                   ",
		"                   W           W                   ",
		"                   W           W                   ",
		"                   WWWWWWWWWWWWW                   ",

	]

	level3Map = [
		"   WWWWWWWWW                                       ",
		"   W       WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
		"   W                                              E",
		"   W                                              E",
		"   W                                              E",
		"   W                                              E",
		"   WWWWWWW     WWWWWWWWWW  WWWWWWWWW   WWWWWW     E",
		"          WWWWW          WW         WWW      WWWWWW",
		"                                                   ",
		"             WWWWW                                 ",
		"            W     W                                ",
		"            W     W                                ",
		"            W     W                                ",
		"             WWWWW                                 ",
	]



	# def __init__(self, string_design, walls, crates, enemies, camera, entities):

	levels = []
	levels.append([level1Map, 64, 65])
	levels.append([level2Map, 416, 128])
	levels.append([level3Map, 416, 128])

	cur_level = Level(levels[0][0], walls, crates, enemies, entities, levels[0][1], levels[0][2], 0)

	player = Player(cur_level.start_x, cur_level.start_y)
	entities.add(player)
	camera = cur_level.camera
	while 1:
		begining_of_frame = datetime.datetime.now().microsecond
		timer.tick(60)

		# E is a type of input like a key from the user.

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
			if e.type == KEYDOWN and e.key == K_x:
				attack = True
			if e.type == KEYDOWN and e.key == K_c:
				shoot = True

			if e.type == KEYUP and e.key == K_w:
				up = False
			if e.type == KEYUP and e.key == K_s:
				down = False
			if e.type == KEYUP and e.key == K_a:
				left = False
			if e.type == KEYUP and e.key == K_d:
				right = False
			if e.type == KEYUP and e.key == K_x:
				attack = False
			if e.type == KEYUP and e.key == K_c:
				shoot = False

		for y in range(64):
			for x in range(64):
				# blit means copy to display surface
				screen.blit(bg, (x * 64, y * 64))

		# self, ExitBlock, walls, crates, enemies, entities, player, levels
		for w in walls:
			if isinstance(w, ExitBlock) and pygame.sprite.collide_rect(player, w):
				cur_level.update(walls, crates, enemies, entities, player, levels)

		player.update(up, down, left, right, running, attack, shoot, enemies, entities, walls, bullets, screen, camera)
		
		for b in bullets:
			b.update(entities, bullets)


		camera = cur_level.camera

		camera.update(player)
		for c in crates:
			c.update(player, crates, entities)
		
		for eType in enemies:
			for e in eType:
				e.update(walls)
				e.attack_player(player, screen, attack, cur_level)
		for e in entities:
			screen.blit(e.image, camera.apply(e))
		print player.rect.x
		print player.rect.y

		pygame.display.update()

				# Calculating FPS
		end_of_frame = datetime.datetime.now().microsecond
		print begining_of_frame
		print end_of_frame
		print "Current FPS:" + str(1000000.0/float(end_of_frame-begining_of_frame))

class Camera(object):
	def __init__(self, camera_func, width, height):
		self.camera_func = camera_func
		# The Original rectangle size of the camera.
		self.state = Rect(0, 0, width, height)

	def apply(self, target):
		# Move the target of the camera to the player away from the topleft where 
		# the camera starts
		return target.rect.move(self.state.topleft)

	def update(self, target):
		# Camera_func will either be simple or complex camera from bellow \/
		self.state=self.camera_func(self.state, target.rect)


# These guys spit out a rectangle that is the correct size to update to.
# l is the x position on screen, t is y position on screen, w and h are the dimensions of the camera target area
def simple_camera(camera, target_rect):
	l, t, _, _ = target_rect
	_, _, w, h = camera
	return Rect(-l+WIN_WIDTH, -t+WIN_HEIGHT, w, h)

def complex_camera(camera, target_rect):
	l = target_rect.x
	t = target_rect.y 
	_, _, w, h = camera
	print "before"
	print l
	print t
	l, t, _, _, = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h
	print "after"
	print h
	print w

	l = min(0, l)
	l = max(-(camera.width-WIN_WIDTH), l)
	t = max(-(camera.height-WIN_HEIGHT), t)
	t = min (0, t)
	return Rect(l, t, w, h)

class Level(object):
	def __init__(self, string_design, walls, crates, enemies, entities, player_start_x, player_start_y, level_map_index):
		x = y = 0
		self.index = level_map_index
		self.start_x = player_start_x
		self.start_y = player_start_y
		# Constructing level
		for row in string_design: 
			for col in row:
				if col == "W":
					w = Wall(x, y)
					walls.append(w)
					entities.add(w)
				if col == "E":
					e = ExitBlock(x, y)
					walls.append(e)
					entities.add(e)
				if col == "B":
					b = Enemy(x, y)
					enemies[0].append(b)
					entities.add(b)
				if col == "b":
					b = HardEnemy(x, y)
					enemies[1].append(b)
					entities.add(b)
				if col == "C":
					c = Crate(x, y)
					crates.append(c)
					entities.add(c)

				x += 64
			y += 64
			x = 0
		total_level_width = len(string_design[0])*64
		total_level_height = len(string_design)*64
		self.camera = Camera(complex_camera, total_level_width, total_level_height)
		print self

	def update(self, walls, crates, enemies, entities, player, levels):
		print "Level Variables that should have changed:"
		for i in range(15):
			for w in walls:
				entities.remove(w)
				walls.remove(w)
			for c in crates:
				entities.remove(c)
				crates.remove(c)
			for eType in enemies:
				for e in eType:
					entities.remove(e)
					eTIndex = enemies.index(eType)
					enemies[eTIndex].remove(e)

		next_level_info = levels[self.index+1]

		x = y = 0
		self.index += 1
		self.start_x = next_level_info[1]
		self.start_y = next_level_info[2]
		# Constructing level
		for row in next_level_info[0]: 
			for col in row:
				if col == "W":
					w = Wall(x, y)
					walls.append(w)
					entities.add(w)
				if col == "E":
					e = ExitBlock(x, y)
					walls.append(e)
					entities.add(e)
				if col == "B":
					b = Enemy(x, y)
					enemies[0].append(b)
					entities.add(b)
				if col == "b":
					b = HardEnemy(x, y)
					enemies[1].append(b)
					entities.add(b)
				if col == "C":
					c = Crate(x, y)
					crates.append(c)
					entities.add(c)

				x += 64
			y += 64
			x = 0
		total_level_width = len(next_level_info[0][0])*64
		total_level_height = len(next_level_info[0])*64
		self.camera = Camera(complex_camera, total_level_width, total_level_height)

		player.rect.x = self.start_x
		player.rect.y = self.start_y




class Entity(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

class Bullet(Entity):
	def __init__(self, x, y, player):
		Entity.__init__(self)
		self.xvel = 0
		self.yvel = 0
		self.image = Surface((32,16))
		self.image.fill(Color("#FF0066"))
		self.image.convert()
		self.rect = Rect(x, y, 32, 16)
		bullet_target = pygame.mouse.get_pos()
		self.when_shot = datetime.datetime.now().second
		

		line_x = float(player.rect.x - bullet_target[0])
		line_y = float(player.rect.y - bullet_target[1])
		print "These ae the bullet stats:"
		print player.rect.x
		print player.rect.y
		print bullet_target[0]
		print bullet_target[1]
		slope = line_x/line_y
		if abs(line_x) > abs(line_y):
			if line_x > 0:
				change_inX = -12
			else:
				change_inX = 12
			change_inY = line_y / (line_x / change_inX)
		else:
			if line_y > 0:
				change_inY = -12
			else:
				change_inY = 12
			change_inX = line_x / (line_y / change_inY)

		if bullet_target[0] < self.rect.x:
			self.xvel = change_inX
		elif bullet_target[0] > self.rect.x:
			self.xvel = change_inX

		if bullet_target[1] < self.rect.y:
			self.yvel = change_inY
		elif bullet_target[1] > self.rect.y:
			self.yvel = change_inY

class Enemy(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.xvel = 8
		self.yvel = 0
		self.onGround = True
		self.image = Surface((64, 64))
		self.image.fill(Color("#00FF00"))
		self.image.convert()
		self.rect = Rect(x, y, 64, 64)
		self.last_rect = Rect(x, y, 64, 64)

	def update(self, walls):
		self.last_rect = self.rect.copy()
		self.rect.left += self.xvel

		self.collide(self.xvel, self.yvel, walls)
	def collide(self, xvel, yvel, walls):
		for w in walls:
			if pygame.sprite.collide_rect(self, w):
				self.rect = self.last_rect
				self.xvel = -(self.xvel)
	def attack_player(self, player, display, player_attack, cur_level):
		if pygame.sprite.collide_rect(self, player) and player_attack != True:
			player.rect.x = cur_level.start_x
			player.rect.y = cur_level.start_y
			display.fill(Color("#FF0000"))

class HardEnemy(Enemy):
	def __init__(self, x, y):
		Enemy.__init__(self, x, y)
		self.image.fill(Color("#009900"))

	def attack_player(self, player, display, player_attack, cur_level):
		if pygame.sprite.collide_rect(self, player):
			if player.weapon_level < 2:
				player.rect.x = cur_level.start_x
				player.rect.y = cur_level.start_y
				display.fill(Color("#FF0000"))
			elif player_attack != True:
				player.rect.x = cur_level.start_x
				player.rect.y = cur_level.start_y
				display.fill(Color("#FF0000"))





class Player(Entity): 
	def __init__(self, x, y):
		Entity.__init__(self)
		self.xvel = 0
		self.yvel = 0
		self.onGround = True

		self.rect = Rect(x, y, 32, 32)
		self.last_rect = Rect(x, y, 32, 32)

		self.sheet = pygame.image.load("player.png")
		self.sheet_size = self.sheet.get_size()
		self.num_images = 3
		self.cur_image = 0
		self.cell_width = 32
		self.cell_height = 32
		self.images = []
		for y in range(0, self.sheet_size[1], self.cell_height):
			for x in range(0, self.sheet_size[0], self.cell_width):
				surface = pygame.Surface((self.cell_width, self.cell_height))
				surface.blit(self.sheet, (0,0), (x, y, self.cell_width, self.cell_height))
				self.images.append(surface)

		self.image = self.images[0]
		print self.images[0]
		
		
		self.weapon_level = 1
		self.unlocked_shooting = True
		self.last_shot = datetime.datetime.now().second

	def update(self, up, down, left, right, running, attack, shoot, enemies, entities, walls, bullets, screen, camera):
		self.last_rect =  self.rect.copy()
		if up:
			self.yvel = -10

			if self.cur_image > 9:
				self.cur_image = 0
			self.image = self.images[self.cur_image]
			self.cur_image += 1
			
			
		if down:
			self.yvel = 10
		if running:
			if up or down:
				self.yvel = 16
			if left or right:
				self.xvel = 16
		if left:
			self.xvel = -10
		if right:
			self.xvel = 10
		if attack:
			self.attack_enemy(enemies, entities)
		if self.unlocked_shooting:
			cur_time = datetime.datetime.now().second
			if shoot and (cur_time - self.last_shot) >= 1:
				bullet = Bullet(self.rect.x, self.rect.y, self)
				entities.add(bullet)
				bullets.append(bullet)
				self.last_shot = cur_time
				



		if not self.onGround:
			pass
		if not(left or right):
			self.xvel = 0
		if not (up or down):
			self.yvel = 0

		self.rect.left += self.xvel
		self.rect.top += self.yvel

		self.collide(walls)

	def collide(self, walls):
		for w in walls:
			if pygame.sprite.collide_rect(self, w):
				if isinstance(w, ExitBlock):
					pass
				else:
					self.rect = self.last_rect

	def attack_enemy(self, enemies, entities):
		for e in enemies[0]:
			if pygame.sprite.collide_rect(self, e) and self.weapon_level >= 1:
				entities.remove(e)
				enemies[0].remove(e)
		for e in enemies[1]:
			if pygame.sprite.collide_rect(self, e) and self.weapon_level >= 2:
				entities.remove(e)
				enemies[1].remove(e)


				

class Wall(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.image = Surface((64, 64))
		self.image.convert()
		self.image.fill(Color("#DDDDDD"))
		self.rect = Rect(x, y, 64, 64)

	def update(self):
		pass

class Crate(Wall):
	def __init__(self, x, y):
		Wall.__init__(self, x, y)
		self.image.fill(Color("#F4A460"))

	def update(self, player, crates, entities):
		self.upgrade_player_weapon(player, crates, entities)

	def upgrade_player_weapon(self, player, crates, entities):
		if pygame.sprite.collide_rect(self, player):
			player.weapon_level += 1
			print "Upgrading player weapon to " + str(player.weapon_level)
			entities.remove(self)
			crates.remove(self)


class ExitBlock(Wall):
	def __init__(self, x, y):
		Wall.__init__(self, x, y)
		self.image.fill(Color("#0033FF"))

		
if __name__ == "__main__":
	main()

