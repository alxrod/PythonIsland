import pygame
from pygame import *
import datetime
from threading import Timer
from basic_set_up import *

class Wall(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)

		self.rect = Rect(x, y, 32*4, 32*4)

		self.sheet = pygame.image.load("tiles/wall.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (32*4, 32*4))
		# self.image = Surface((8*4,32*4))
		# self.image.fill(Color("#000000"))

	def update(self):
		pass

class Wall_Corner(Wall):
	def __init__(self, x, y):
		Wall.__init__(self, x, y)


		# Change texture soon
		self.rect = Rect(x, y, 32*4, 32*4)
		self.sheet = pygame.image.load("tiles/wall_corner.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (32*4, 32*4))

class Wall_Cliff(Wall):
	def __init__(self, x, y):
		Wall.__init__(self, x, y)


		# Change texture soon
		self.rect = Rect(x, y, 32*4, 32*4)
		self.sheet = pygame.image.load("tiles/wall_cliff.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (32*4, 32*4))

class Wall_Tri(Wall):
	def __init__(self, x, y):
		Wall.__init__(self, x, y)


		# Change texture soon
		self.rect = Rect(x, y, 32*4, 32*4)
		self.sheet = pygame.image.load("tiles/wall_tri.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (32*4, 32*4))


class Wall_End_Cliff(Wall):
	def __init__(self, x, y):
		Wall.__init__(self, x, y)

		# Change texture soon
		self.rect = Rect(x, y, 32*4, 32*4)
		self.sheet = pygame.image.load("tiles/wall_end_cliff.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (32*4, 32*4))

class Wall_End(Wall):
	def __init__(self, x, y):
		Wall.__init__(self, x, y)


		# Change texture soon
		self.rect = Rect(x, y, 32*4, 32*4)
		self.sheet = pygame.image.load("tiles/wall_end.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (32*4, 32*4))

class Cliff_End(Wall):
	def __init__(self, x, y):
		Wall.__init__(self, x, y)


		# Change texture soon
		self.rect = Rect(x, y, 32*4, 32*4)
		self.sheet = pygame.image.load("tiles/Cliff_End.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (32*4, 32*4))


class Grass(Wall):
	def __init__(self, x, y):
		Wall.__init__(self, x, y)

		# Change texture soon
		self.rect = Rect(x, y, 32*4, 32*4)
		self.sheet = pygame.image.load("tiles/grass.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (32*4, 32*4))

class Side_Cliff(Wall):
	def __init__(self, x, y):
		Wall.__init__(self, x, y)


		# Change texture soon
		self.rect = Rect(x, y, 32*4, 32*4)
		self.sheet = pygame.image.load("tiles/side_cliff.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (32*4, 32*4))

class Corner_Cliff1(Wall):
	def __init__(self, x, y):
		Wall.__init__(self, x, y)

		# Change texture soon
		self.rect = Rect(x, y, 32*4, 32*4)
		self.sheet = pygame.image.load("tiles/corner_cliff1.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (32*4, 32*4))

class Corner_Cliff2(Wall):
	def __init__(self, x, y):
		Wall.__init__(self, x, y)


		# Change texture soon
		self.rect = Rect(x, y, 32*4, 32*4)
		self.sheet = pygame.image.load("tiles/corner_cliff2.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (32*4, 32*4))

class Path(Wall):
	def __init__(self, x, y):
		Wall.__init__(self, x, y)

		# Change texture soon
		self.rect = Rect(x, y, 32*4, 32*4)
		self.sheet = pygame.image.load("tiles/walkway.png")
		self.image = self.sheet
		self.image = pygame.transform.scale(self.image, (32*4, 32*4))

class Crate(Wall):
	def __init__(self, x, y):
		Wall.__init__(self, x, y)

		self.sheet = pygame.image.load("crate.png")
		self.sheet_size = self.sheet.get_size()
		self.cur_image = 0
		self.cell_width = 32
		self.cell_height = 32

		self.images = []

		for y in range(0, self.sheet_size[1], self.cell_height):
			for x in range(0, self.sheet_size[0], self.cell_width):
				surface = pygame.Surface((self.cell_height, self.cell_height),pygame.SRCALPHA)
				surface.blit(self.sheet, (0,0), ( x, y, self.cell_width, self.cell_height))
				surface = pygame.transform.scale(surface, (32*4,32*4))
				self.images.append(surface)

		self.image = self.images[0]

		self.anim_sets = {
			"open_crate": [self.images[0],
						  self.images[1],
						  self.images[2],
						  self.images[3],
						 ],
		}

		self.open_counter = 0

	def update(self, player, entities_dict, screen):
		if pygame.sprite.collide_rect(self, player):
			if self.open_counter <= 3:
				self.image = self.anim_sets["open_crate"][self.open_counter]
				self.open_counter += 1
				if self.open_counter == 3: 
					print "Upgrading player weapon to " + str(player.weapon_level)
					player.weapon_level += 1


class ExitBlock(Wall):
	def __init__(self, x, y):
		Wall.__init__(self, x, y)
		self.image.fill(Color("#0033FF"))

class WorkBench(Wall):
	def __init__(self, x, y):
		Wall.__init__(self, x, y)


		# Change texture soon
		self.rect = Rect(x, y, 24*4, 16*4)
		self.sheet = pygame.image.load("workbench.png")
		self.image = self.sheet

		self.sheet1 = pygame.image.load("craft_bg.png")
		self.sheet2 = pygame.image.load("item_box.png")
		self.sheet3 = pygame.image.load("wrong_amounts.png")
		self.image = pygame.transform.scale(self.image, (32*4, 32*4))
		self.bg_surface = self.sheet1
		self.bg_surface = pygame.transform.scale(self.bg_surface, (177*4, 75*4))
		self.craft_should_open = False
		self.should_show_invent = False

		self.item_box = self.sheet2
		self.item_box = pygame.transform.scale(self.item_box, (18*4, 18*4))

		self.recipe_cords = [58, 175]

		self.recipes = {Bow: [[String,String,String],
							  [Stick,Stick,Stick]],
						# "arrow": ["Stick", "Stone"]
		}


	def update(self, player, inventory, screen, craft, attack, entities_dict):
		
		if pygame.sprite.collide_rect(self, player) and craft:
			self.should_show_invent = True
			screen.blit(self.bg_surface, (50, 100))
			for r in self.recipes:
				screen.blit(self.item_box, (self.recipe_cords[0], self.recipe_cords[1]))

				self.item_box = self.sheet2
				self.item_box = pygame.transform.scale(self.item_box, (18*4, 18*4))

				temp = r(player)
				screen.blit(temp.image, (self.recipe_cords[0]+12, self.recipe_cords[1]+4))
			x = 186
			for i in self.recipes[r]:
				screen.blit(self.item_box, (x, self.recipe_cords[1]))
				temp = i[0](0,0)

				font=pygame.font.Font(None,24)
				label = font.render(str(len(i)), 1, (1,1,1))

				screen.blit(temp.image, (x+8, self.recipe_cords[1]+8))
				screen.blit(label, (x+48, self.recipe_cords[1]+48))
				x += 22*4

			if attack:
				mouse_cords = pygame.mouse.get_pos()
				if mouse_cords[0] >= self.recipe_cords[0]-64 and mouse_cords[0]<=self.recipe_cords[0]+64 and mouse_cords[1] >= self.recipe_cords[1]-64 and mouse_cords[1]<=self.recipe_cords[1]+64:
					have_enough = {Stick: False,
								   String: False
					}

					no_craftables = True

					for i in player.inventory:
						i_index = player.inventory.index(i)

						if i and isinstance(i[0], Stick):
							no_craftables = False
							try: 
								# This makes sure it doesnt subtract two with no need.
								print i[2]
								for e in range(3):
									del i[-1]
								have_enough[Stick] = True
							except:
								pass

							if i == []:
								inventory.num_in_slot[i_index] = 0
								inventory.item_icons[i_index] = Surface((16*3,16*3)).fill(Color("#E9E9E9"))

								print inventory.item_icons

						if i and isinstance(i[0], String):
							no_craftables = False
							try: 
								# This makes sure it doesnt subtract two with no need.
								print i[2]
								for e in range(3):
									del i[-1]
								have_enough[String] = True
							except:
								pass

							if i == []:
								inventory.num_in_slot[i_index] = 0
								inventory.item_icons[i_index] = Surface((16*3,16*3)).fill(Color("#E9E9E9"))

	
					should_craft = False
					for i in have_enough:
						if have_enough[i]:
							print "You have materials"
							should_craft = True
						else:
							print "You lack materials"
							should_craft = False
					if should_craft:
						bow = Bow(player)
						bow.give_player(player,entities_dict)
					else:
						# self.item_box.fill(Color("#ff0000"))
						self.item_box = self.sheet3
						self.item_box = pygame.transform.scale(self.item_box, (18*4, 18*4))
						for c in have_enough:
							print c
							if have_enough[c]:
								for c in range(3):
									if isinstance(c, String):
										temp = String(0,0)
									elif isinstance(c, Stick):
										temp = String(0,0)
									temp.give_player(player)

		else:
			self.should_show_invent = False

		