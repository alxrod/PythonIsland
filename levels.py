import pygame
from pygame import *

level1Map = [
		"uw7*5                  ",
		"WGGCS                  ",
		"WGG(S     ^wsssssss7wwU",
		"WBGGS     %GGGGGGGGGGGW",
		"WG8GS     %GGGGGGGBGGGW",
		"W8GG$sssss4GGGGGWGGGGGW",
		"WG8GCGGBGGGGGGGGWGGBGGW",
		"WGGGGGGGGGGGGGGGWGGGGGW",
		"!wwwwwwwwwwwwwwwYGGGGGW",
		"WGGGGGGGGGGGGGGGGGGGGGW",
		"WGGGGGGGGGGGGGGGGGGGGGW",
		"WGGGGGGwwwwwwwwwwwwwww#",
		"WGGGGGGGGGGGGGGGGGGGGGW",
		"WGGGGGGGGGGGGGGGGGGGGGW",
		"WGGGGGGGGGGGGGGGGGGGGGW",
		"!wwwwwwwwwwwwwwGGGGGGGW",
		"WGGGGGGGGGGGGGGGGGGGGGW",
		"WGGGGGGGGGGGGGGGGGGGGGW",
		"WGGGGGGGGGGGGGGGGGGGGGW",
		"WGGGGGGGwwwwww@wwwwwwwY",
		"WGGGGGGGGGGGGGW        ",
		"WGGGGGGGGGGGGGW        ",
		"WGGGGGGGGGGGGGW        ",
		"uwwwwwwwwUGGGGW        ",
		"         WGGGGW        ",
		"         WGGGGW        ",
		"         WGGGGW        ",
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

levels_list = []
levels_list.append([level1Map, 128, 128])
levels_list.append([level2Map, 512, 128])
levels_list.append([level3Map, 512, 128])

# Sets up black background for all level
sheet = pygame.image.load("tiles/background.png")
bg = sheet
bg = pygame.transform.scale(bg, (32*4, 32*4))

# This is for the creation/updates of levels:

from enemy_1 import *
from enemy_2 import *
from tiles import *
from basic_set_up import *

class Level(object):
	def __init__(
			self,
			level_design,
			entities_dict,
			player_start_x,
			player_start_y,
			level_map_index):

		self.index = level_map_index
		self.start_x = player_start_x
		self.start_y = player_start_y

		self.construct(level_design, entities_dict)

		total_level_width = len(level_design[0])*32
		total_level_height = len(level_design)*32

		self.camera = Camera(complex_camera, total_level_width, total_level_height)

		print "Level Initiated"

	def update(self, entities_dict, player):
		print "Updating old level..."

		self.deconstruct(entities_dict)

		next_level = levels_list[self.index+1]
		self.start_x = next_level[1]
		self.start_y = next_level[2]

		self.construct(next_level[0], entities_dict)

		total_level_width = len(next_level[0][0])*32
		total_level_height = len(next_level[0])*32

		self.camera = Camera(complex_camera, total_level_width, total_level_height)

		player.rect.x = self.start_x
		player.rect.y = self.start_y

	def deconstruct(self, entities_dict):
		print "Deconstructing old level..."

		# Only have to repeat 15 times because there are so many entities for pygame
		for i in range(15):
			for w in entities_dict["walls"]:
				entities_dict["entities"].remove(w)
				entities_dict["walls"].remove(w)
			for c in entities_dict["crates"]:
				entities_dict["entities"].remove(c)
				entities_dict["crates"].remove(c)
			for eType in entities_dict["enemies"]:
				for e in eType:
					entities_dict["entities"].remove(e)
					eTIndex = entities_dict["enemies"].index(eType)
					entities_dict["enemies"][eTIndex].remove(e)

	def construct(self, level_design, entities_dict):
		print "Constructing new level..."

		x = y = 0

		for row in level_design:
			for col in row:
				if col == "W":
					w = Wall(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)
				if col == "w":
					w = Wall(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)
					w.image = pygame.transform.rotate(w.image, 90)

				if col == "6":
					w = Wall_Cliff(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)
					w.image = pygame.transform.rotate(w.image, 90)
				if col == "u":
					w = Wall_Corner(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)

				if col == "U":
					w = Wall_Corner(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)
					w.image = pygame.transform.rotate(w.image, 270)
				if col == "y":
					w = Wall_Corner(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)
					w.image = pygame.transform.rotate(w.image, 90)

				if col == "Y":
					w = Wall_Corner(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)
					w.image = pygame.transform.rotate(w.image, 180)

				if col == "&":
					w = Wall_End_Cliff(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)
					w.image = pygame.transform.rotate(w.image, 90)


				if col == "7":
					w = Wall_End(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)
					w.image = pygame.transform.rotate(w.image, 90)


				if col == "*":
					w = Cliff_End(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)
					w.image = pygame.transform.rotate(w.image, 90)

				if col == "!":
					w = Wall_Tri(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)
				if col == "@":
					w = Wall_Tri(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)
					w.image = pygame.transform.rotate(w.image, 270)
				if col == "#":
					w = Wall_Tri(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)
					w.image = pygame.transform.rotate(w.image, 180)

				if col == "S":
					w = Side_Cliff(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)

				if col == "s":
					w = Side_Cliff(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)
					w.image = pygame.transform.rotate(w.image, 90)

				if col == "%":
					w = Side_Cliff(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)
					w.image = pygame.transform.rotate(w.image, 180)

				if col == "$":
					w = Corner_Cliff1(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)

				if col == "4":
					w = Corner_Cliff1(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)
					w.image = pygame.transform.rotate(w.image, 90)

				if col == "5":
					w = Corner_Cliff2(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)

				if col == "^":
					w = Corner_Cliff2(x, y)
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)
					w.image = pygame.transform.rotate(w.image, 90)

				if col == "8":
					s = Stick(x, y)
					entities_dict['sticks'].append(s)
					entities_dict["entities"].add(s)

					# Behind them:
					g = Grass(x, y)
					entities_dict['walls'].append(g)
					entities_dict["entities"].add(g)

				if col == "(":
					w = WorkBench(x, y)
					print col
					print row
					entities_dict['walls'].append(w)
					entities_dict["entities"].add(w)

					# Behind them:
					g = Grass(x, y)
					entities_dict['walls'].append(g)
					entities_dict["entities"].add(g)

				if col == "G":
					g = Grass(x, y)
					entities_dict['walls'].append(g)
					entities_dict["entities"].add(g)
				if col == "P":
					p = Path(x, y)
					entities_dict['walls'].append(p)
					entities_dict["entities"].add(p)

				if col == "E":
					e = ExitBlock(x, y)
					entities_dict['walls'].append(e)
					entities_dict["entities"].add(e)
				if col == "B":
					e = Enemy_1(x, y)
					entities_dict["enemies"][0].append(e)
					entities_dict["entities"].add(e)

					# Behind them:
					g = Grass(x, y)
					entities_dict['walls'].append(g)
					entities_dict["entities"].add(g)

				if col == "b":
					e = Enemy_2(x, y)
					entities_dict["enemies"][1].append(e)
					entities_dict["entities"].add(e)

					# Behind them:
					g = Grass(x, y)
					entities_dict['walls'].append(g)
					entities_dict["entities"].add(g)
				if col == "C":
					c = Crate(x, y)
					entities_dict["crates"].append(c)
					entities_dict["entities"].add(c)

					g = Grass(x, y)
					entities_dict['walls'].append(g)
					entities_dict["entities"].add(g)
				x += 128
			y += 128
			x = 0




























