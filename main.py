'''
Mr Quadrilateral
Created by Gavin P

TODO: Create new level backgrounds
TODO: Create new block themes
TODO: Implement moving enemy AI
TODO: Add the ability to change the player starting position, key position, and flag position through the editor
TODO: Add a playtest button to the editor
TODO: Add expandable lava
TODO: Add the ability to expand blocks in the editor
TODO: Modify the editor to be more user friendly
TODO: Add the ability to exit out of any mode and go back to the main menu
'''

import pygame as pyg
from math import floor

# Screen setup
screenw = 720
screenh = 480
exit = False
pyg.init()
screen = pyg.display.set_mode((screenw,screenh))
pyg.display.set_caption("Mr. Quadrilateral")
fps = 240

debug = True

# Color setup, does not refrence anything
black = (0,0,0)
white = (255,255,255)
gray = (63,63,63)
light_gray = (127,127,127)
red = (255,0,0)
yellow = (255,255,0)
lava_yellow = (255,183,0)

# All of the following can be put into their own file as long as you also import pygame as pyg. Recommended file name is "assets.py"

# Function that splits sprites
def addframe(x, image, size):
	frame = pyg.Surface((size[0], size[1]), pyg.SRCALPHA)
	frame.blit(image, (x, 0))
	return frame

# Importing the logo
logo = pyg.transform.scale(pyg.image.load("images/logo.png").convert_alpha(), (600,120))

# Defining spritesheets; place to store all of the sprites
playersheet, lavasheet, flagsheet, playtestsheet = [], [], [], []

# Rectangle enemy sprite
enemyimg = pyg.transform.scale(pyg.image.load("images/enemy.png").convert(), (60, 30))
enemyimg_flipped = pyg.transform.flip(enemyimg, True, False)

# Key sprite
key = pyg.transform.scale(pyg.image.load("images/key.png").convert_alpha(), (14, 20))

# Editor playtest button
playtest = pyg.transform.scale(pyg.image.load("images/playtestbutton.png").convert_alpha(), (120, 60))
playtestsheet.append(addframe(0, playtest, (60, 60)))
playtestsheet.append(addframe(-60, playtest, (60, 60)))

# Player sprites
playerimg = pyg.transform.scale(pyg.image.load("images/player.png").convert(), (120,30))
playerandlavasize = (30,30)
playersheet.append(addframe(0, playerimg, playerandlavasize))
playersheet.append(addframe(-30, playerimg, playerandlavasize))
playersheet.append(addframe(-60, playerimg, playerandlavasize))
playersheet.append(addframe(-90, playerimg, playerandlavasize))
playersheet_flipped = []
for i in range(len(playersheet)):
	playersheet_flipped.append(pyg.transform.flip(playersheet[i], True, False))
	
# Lava sprites
lavaimg = pyg.transform.scale(pyg.image.load("images/lava.png").convert_alpha(), (60,30))
lavasheet.append(addframe(0, lavaimg, playerandlavasize))
lavasheet.append(addframe(-30, lavaimg, playerandlavasize))

# Flag sprites
flagimg = pyg.transform.scale(pyg.image.load("images/flag.png").convert_alpha(), (180, 60))
flagsize = (30,60)
flagsheet.append(addframe(0, flagimg, flagsize))
flagsheet.append(addframe(-30, flagimg, flagsize))
flagsheet.append(addframe(-60, flagimg, flagsize))
flagsheet.append(addframe(-90, flagimg, flagsize))
flagsheet.append(addframe(-120, flagimg, flagsize))
flagsheet.append(addframe(-150, flagimg, flagsize))

# Second style block sprite
blockimg = pyg.transform.scale(pyg.image.load("images/style2block.png").convert(), (30,30))

# Setting icon
pyg.display.set_icon(playersheet[0])

# Loading sound
jump_sound = pyg.mixer.Sound("jumping.ogg")

# Loading fonts
main_font = pyg.font.Font("nesfont.otf", 28)
small_main_font = pyg.font.Font("nesfont.otf", 14)
calibri_font = pyg.font.SysFont("calibri", 20, bold=True)

# End of assets.py

# Class for box that will go into the level class
class Box:
	def update_rects(self):
		self.rectbox_outline = pyg.Rect(self.x, self.y, self.width, self.height) # Rectangle to draw for box outline
		self.rectbox_outline2 = pyg.Rect(self.x+2, self.y+2, self.width-4, self.height-4) # Second rectangle to draw for box outline
		self.rectbox_main = pyg.Rect(self.x+4, self.y+4, self.width-8, self.height-8) # Rectangle to draw for the main box
	def __init__(self, x, y, width=1, height=1, style=1):
		self.initinputs = (x, y, width, height, style)
		self.x = x*30
		self.y = y*30
		self.style = style
		if self.style == 1:
			self.width = width*30
			self.height = height*30
		if self.style == 2:
			self.width = 30
			self.height = 30
		self.update_rects()
	def update(self):
		self.update_rects()
		if self.style == 1:
			pyg.draw.rect(screen, black, self.rectbox_outline) # Box outline
			pyg.draw.rect(screen, gray, self.rectbox_outline2)
			pyg.draw.rect(screen, light_gray, self.rectbox_main) # Main box
		if self.style == 2:
			screen.blit(blockimg, (self.x, self.y))
	def getRect(self):
		return self.rectbox_outline

# Class for spike that will go into the level class
class Spike:
	def __init__(self, x, y, style=1):
		self.initinputs = (x, y, style)
		self.x = x*30
		self.y = y*30
		self.style = style
		if self.style == 1:
			self.rectbox1 = pyg.Rect(self.x+10, self.y, 10, 10)
			self.rectbox2 = pyg.Rect(self.x+5, self.y+10, 20, 10)
			self.rectbox3 = pyg.Rect(self.x, self.y+20, 30, 10)
			self.points = [(self.x, self.y+30), (self.x+15, self.y), (self.x+30, self.y+30)]
		if self.style == 2:
			self.rectbox1 = pyg.Rect(self.x+10, self.y+20, 10, 10)
			self.rectbox2 = pyg.Rect(self.x+5, self.y+10, 20, 10)
			self.rectbox3 = pyg.Rect(self.x, self.y, 30, 10)
			self.points = [(self.x, self.y), (self.x+30, self.y), (self.x+15, self.y+30)]
	def update(self):
		pyg.draw.polygon(screen, white, self.points)
		pyg.draw.polygon(screen, black, self.points, 3)
	def getRect(self):
		return (self.rectbox1, self.rectbox2, self.rectbox3)

# Class for lava that will go into the level class
class Lava:
	def __init__(self, x, y):
		self.initinputs = (x, y)
		self.x = x*30
		self.y = y*30
		self.frame = 0
		self.rectbox = pyg.Rect(self.x, self.y, 30, 30)
	def update(self):
		if universalcycle > fps//2: # Change these to speed up animation
			self.frame = 1
		else:
			self.frame = 0
		screen.blit(lavasheet[self.frame], (self.x,self.y))
	def getRect(self):
		return self.rectbox

# Class for moving enemies that will go into the level class
class MovingEnemy:
	def update_rect(self):
		self.rectbox = pyg.Rect(self.x, self.y, 60, 30)
	def __init__(self, x, y):
		self.initinputs = (x, y)
		self.x = x*30
		self.y = y*30
		self.direction = "Right"
		self.update_rect()
	def update(self):
		self.update_rect()
		if self.direction == "Right":
			screen.blit(enemyimg, (self.x, self.y))
		elif self.direction == "Left":
			screen.blit(enemyimg_flipped, (self.x, self.y))
	def getRect(self):
		return self.rectbox

# Level class that updates and stores all parts of the level
class Level:
	def update_rects(self):
		self.objectrects = []
		for object in self.objects:
			self.objectrects.append(object.getRect())
			if pyg.mouse.get_pressed()[2] and editor_on and object.getRect().collidepoint(pyg.mouse.get_pos()):
				self.objects.remove(object)
		self.enemyrects = []
		for enemy in self.enemies:
			if type(enemy).__name__ == "Spike":
				self.enemyrects.append(enemy.getRect()[0])
				self.enemyrects.append(enemy.getRect()[1])
				self.enemyrects.append(enemy.getRect()[2])
				if pyg.mouse.get_pressed()[2] and editor_on and not pyg.Rect(pyg.mouse.get_pos(), (1, 1)).collidelist(enemy.getRect()) == -1:
					self.enemies.remove(enemy)
			else:
				self.enemyrects.append(enemy.getRect())
				if pyg.mouse.get_pressed()[2] and editor_on and enemy.getRect().collidepoint(pyg.mouse.get_pos()):
					self.enemies.remove(enemy)
	def __init__(self, starting_pos, flagpole, key_pos, objects, enemies):
		self.og_starting_pos = starting_pos
		self.starting_pos = (starting_pos[0]*30, starting_pos[1]*30)
		self.objects = objects
		self.enemies = enemies
		self.og_flagpole = flagpole
		self.flagpole = (flagpole[0]*30, flagpole[1]*30)
		self.og_key_pos = key_pos
		self.key_pos = key_pos
		self.key_rect = pyg.Rect(-1, -1, 0, 0)
		if self.key_pos == []:
			self.flagframe = 1
		else:
			self.flagframe = 0
			self.key_pos = (self.key_pos[0]*30, self.key_pos[1]*30)
		self.update_rects()
	def update(self):
		screen.blit(flagsheet[self.flagframe], self.flagpole)
		self.update_rects()
		for enemy in self.enemies:
			enemy.update()
		for object in self.objects:
			object.update()
		if not self.key_pos == [] and not player1.keycollected:
			if universalcycle < fps//2:
				self.key_rect = screen.blit(key, (self.key_pos[0]+8, self.key_pos[1]+4))
			else:
				self.key_rect = screen.blit(key, (self.key_pos[0]+8, self.key_pos[1]+6))
	def getflagpoleRect(self):
		return pyg.Rect(self.flagpole[0], self.flagpole[1], 30, 60)
	# Function to output the code in a level in a python code-like format
	def getLevelCode(self):
		def join(lst):
			output_lst = []
			for i in range(0, len(lst), 2):
				output_lst.append(lst[i] + lst[i+1])
			return output_lst
		object_variables = []
		enemy_variables = []
		for object in self.objects:
			object_variables.append(str(type(object))[17:][:-2])
			object_variables.append(str(object.initinputs))
		for enemy in self.enemies:
			enemy_variables.append(str(type(enemy))[17:][:-2])
			enemy_variables.append(str(enemy.initinputs))
		object_variables_joined = str(join(object_variables)).replace("'", "")
		enemy_variables_joined = str(join(enemy_variables)).replace("'", "")
		return "Level(\n{},\n{},\n{},\n{},\n{}\n)".format(self.og_starting_pos, self.og_flagpole, self.og_key_pos, object_variables_joined, enemy_variables_joined)

editorlevels = (

"fake_level",

# Blank level used in the editor
Level(
[5, 5], # Player starting position
[23, 14], # Flagpole position
[], # Key postion, if no key, leave empty
[],
[]
)

)

levels = (

# Level 1
Level(
[5, 5], # Player starting position
[23, 14], # Flagpole position
[21, 15], # Key postion, if no key, leave empty
[Box(10, 11, 2, 2), Box(7, 14, 1, 1, style=2)], # All objects
[Spike(10, 15), Spike(11, 13, style=2), Spike(2, 15), MovingEnemy(14, 15)] # All enemies
),

# Level 2

Level(
[0, 0],
[12, 14],
[12, 0],
[Box(11, 15, 1, 1, 2), Box(11, 14, 1, 1, 2), Box(13, 13, 1, 1, 2), Box(13, 14, 1, 1, 2), Box(13, 15, 1, 1, 2), Box(11, 13, 1, 1, 2), Box(0, 7, 1, 1, 2), Box(1, 5, 1, 1, 2), Box(2, 6, 1, 1, 2), Box(3, 5, 1, 1, 2), Box(11, 0, 1, 1, 2), Box(11, 1, 1, 1, 2), Box(12, 1, 1, 1, 2), Box(13, 1, 1, 1, 2), Box(14, 1, 1, 1, 2), Box(15, 1, 1, 1, 2), Box(16, 1, 1, 1, 2), Box(17, 1, 1, 1, 2), Box(18, 1, 1, 1, 2), Box(19, 1, 1, 1, 2), Box(20, 2, 1, 1, 2), Box(23, 4, 1, 1, 2), Box(23, 3, 1, 1, 2), Box(20, 1, 1, 1, 2), Box(22, 4, 1, 1, 2), Box(21, 4, 1, 1, 2), Box(19, 4, 1, 1, 2), Box(18, 4, 1, 1, 2), Box(20, 4, 1, 1, 2), Box(17, 4, 1, 1, 2), Box(10, 13, 1, 1, 2), Box(10, 12, 1, 1, 2), Box(14, 12, 1, 1, 2), Box(14, 13, 1, 1, 2), Box(13, 6, 1, 1, 2), Box(11, 6, 1, 1, 2), Box(16, 4, 1, 1, 2), Box(15, 4, 1, 1, 2), Box(15, 5, 1, 1, 2), Box(14, 5, 1, 1, 2)],
[Lava(0, 15), Lava(10, 15), Lava(9, 15), Lava(8, 15), Lava(1, 15), Lava(2, 15), Lava(3, 15), Lava(4, 15), Lava(5, 15), Lava(6, 15), Lava(7, 15), Lava(14, 15), Lava(15, 15), Lava(16, 15), Lava(17, 15), Lava(18, 15), Lava(19, 15), Lava(20, 15), Lava(21, 15), Lava(22, 15), Lava(23, 15), Spike(18, 2, 2), Spike(23, 0, 2), Spike(13, 12, 1)]
),

# Level 3

Level(
[12, 12],
[23, 0],
[0, 15],
[Box(1, 14, 1, 1, 2), Box(2, 13, 1, 1, 2), Box(2, 14, 1, 1, 2), Box(2, 15, 1, 1, 2), Box(2, 12, 1, 1, 2), Box(0, 12, 1, 1, 2), Box(2, 11, 1, 1, 2), Box(2, 10, 1, 1, 2), Box(2, 8, 1, 1, 2), Box(1, 4, 1, 1, 2), Box(2, 4, 1, 1, 2), Box(4, 4, 1, 1, 2), Box(3, 4, 1, 1, 2), Box(5, 4, 1, 1, 2), Box(6, 4, 1, 1, 2), Box(7, 4, 1, 1, 2), Box(8, 4, 1, 1, 2), Box(10, 4, 1, 1, 2), Box(10, 4, 1, 1, 2), Box(8, 4, 1, 1, 2), Box(8, 4, 1, 1, 2), Box(23, 2, 1, 1, 2), Box(22, 2, 1, 1, 2), Box(20, 2, 1, 1, 2), Box(19, 2, 1, 1, 2), Box(17, 2, 1, 1, 2), Box(16, 2, 1, 1, 2), Box(3, 2, 1, 1, 2), Box(4, 2, 1, 1, 2), Box(6, 2, 1, 1, 2), Box(7, 2, 1, 1, 2), Box(9, 2, 1, 1, 2), Box(10, 2, 1, 1, 2), Box(11, 2, 1, 1, 2), Box(13, 2, 1, 1, 2), Box(14, 2, 1, 1, 2), Box(17, 4, 1, 1, 2), Box(16, 4, 1, 1, 2), Box(15, 4, 1, 1, 2), Box(9, 4, 1, 1, 2), Box(11, 4, 1, 1, 2), Box(12, 4, 1, 1, 2), Box(13, 4, 1, 1, 2), Box(14, 4, 1, 1, 2), Box(19, 6, 1, 1, 2), Box(18, 8, 1, 1, 2), Box(17, 8, 1, 1, 2), Box(16, 8, 1, 1, 2), Box(15, 8, 1, 1, 2), Box(14, 8, 1, 1, 2), Box(13, 8, 1, 1, 2), Box(11, 8, 1, 1, 2), Box(10, 8, 1, 1, 2), Box(10, 15, 1, 1, 2), Box(8, 13, 1, 1, 2), Box(6, 12, 1, 1, 2), Box(5, 12, 1, 1, 2), Box(6, 10, 1, 1, 2), Box(7, 9, 1, 1, 2)],
[Lava(0, 6), Lava(15, 2), Lava(12, 2), Lava(8, 2), Lava(5, 2), Spike(11, 7, 1), Spike(15, 7, 1), Lava(9, 15), Lava(8, 15), Lava(7, 15), Lava(6, 15), Lava(5, 15), Lava(4, 15), Lava(3, 15), Lava(14, 12), Lava(15, 12), Lava(16, 12), Lava(17, 12), Lava(18, 12), Lava(19, 12), Lava(20, 12), Lava(21, 12), Lava(22, 12), Lava(21, 8), Lava(23, 12)]
)

)

# Player class that handles movement, collision, and displaying the player 
class Player:
	def __init__(self):
		self.size = 30
		self.x = currentlevel.starting_pos[0]
		self.y = currentlevel.starting_pos[1]
		self.jumpcount = 0
		self.velocity = 1
		self.allowjump = True
		self.modx = self.x
		self.mody = self.y
		self.modxv = False
		self.modyv = False
		self.modrectxv = False
		self.modrectyv = False
		self.modrectxyv = False
		self.enemycycle = 0
		self.facing = "Right"
		self.frame = 0
		self.allowmove = True
		self.flagcycle = 0
		self.keycollected = False
	def walk(self, direction):
		# Change the following values (e.g. self.x-1) to affect distance/speed
		if self.allowmove:
			if direction == "Left":
				self.modx = self.x-1
			if direction == "Right":
				self.modx = self.x+1
			self.facing = direction
		if self.modx >= 0 and self.modx <= screenw-self.size:
			self.modxv = True
		else:
			self.modxv = False
	# Jumping
	def startjumping(self):
		if self.allowjump:
			self.velocity = -1.25 # Change this to affect jumping height
			pyg.mixer.Sound.play(jump_sound)
	def update(self):
		global levelnumber, currentlevel
		self.mody = self.y+self.velocity
		if self.velocity <= 1.25: # Change this to affect falling height
			self.velocity += 0.01 # Change this to affect speed
		if self.velocity <= 0:
			self.frame = 1
		else:
			self.frame = 0
		# Collision detection
		if self.mody >= screenh-self.size:
			self.modyv = False
			setytofull = True
		elif self.mody <= 0:
			self.modyv = False
			setytofull = False
		else:
			self.modyv = True
			setytofull = False
		modrect = pyg.Rect(round(self.modx), round(self.mody), self.size, self.size)
		modrectx = pyg.Rect(round(self.modx), round(self.y), self.size, self.size)
		modrecty = pyg.Rect(round(self.x), round(self.mody), self.size, self.size)
		if modrect.collidelist(currentlevel.objectrects) == -1 and self.modxv and self.modyv:
			self.modrectxyv = True
		else:
			self.modrectxyv = False
		if modrectx.collidelist(currentlevel.objectrects) == -1 and self.modxv:
			self.modrectxv = True
		else:
			self.modrectxv = False
		if modrecty.collidelist(currentlevel.objectrects) == -1 and self.modyv:
			self.modrectyv = True
			self.allowjump = False
		else:
			self.modrectyv = False
			self.allowjump = True
		# Stops player from jumping if hitting a block above them
		if self.velocity < 0:
			if modrecty.collidelist(currentlevel.objectrects) != -1 or not self.modyv:
				self.velocity = 0.25
		# Implementation of collision detection
		if self.modrectxyv:
			self.x = self.modx
			self.y = self.mody
		else:
			if self.modrectxv and self.modrectyv:
				pass
			else:
				if self.modrectxv:
					self.x = self.modx
				if self.modrectyv:
					self.y = self.mody
		if not self.mody >= 0:
			self.allowjump = False 
		if setytofull:
			self.y = screenh-self.size
		# Detects if the player is colliding with any enemies or if the restart button is being pressed
		newrect = pyg.Rect(round(self.x), round(self.y), self.size, self.size)
		if newrect.collidelist(currentlevel.enemyrects) != -1 or keys[pyg.K_r]:
			if not keys[pyg.K_r]:
				self.allowmove = False
			self.allowjump = False
			self.frame = 2
			self.enemycycle += 1
			self.velocity = 0
			if self.enemycycle >= fps//5 or keys[pyg.K_r]:
				self.enemycycle = 0
				self.keycollected = False
				self.x = currentlevel.starting_pos[0]
				self.y = currentlevel.starting_pos[1]
				self.velocity = 1
				self.modx = self.x
				self.allowmove = True
		else:
			self.enemycycle = 0
		# Detects if there is a key, and if so, if the player is colliding with the key
		if currentlevel.key_pos == []:
			self.keycollected = True
		elif newrect.colliderect(currentlevel.key_rect):
			self.keycollected = True
		# Detects if the player is colliding with the flagpole and has collected the key
		if newrect.colliderect(currentlevel.getflagpoleRect()) and self.keycollected:
			self.allowmove = False
			self.allowjump = False
			self.frame = 3
			self.flagcycle += 1
			currentlevel.flagframe = 2
			self.velocity = 0
			if self.flagcycle >= fps:
				self.flagcycle = 0
				levelnumber += 1
				try:
					currentlevel = levels[levelnumber]
				except:
					print("End of game reached!")
				self.keycollected = False
				self.x = currentlevel.starting_pos[0]
				self.y = currentlevel.starting_pos[1]
				self.allowmove = True
				self.allowjump = True
			if self.flagcycle >= fps//8:
				currentlevel.flagframe = 3
			if self.flagcycle >= fps//4:
				currentlevel.flagframe = 4
			if self.flagcycle >= fps*(3/8):
				currentlevel.flagframe = 5
		else:
			self.flagcycle = 0
		if self.facing == "Right": 
			screen.blit(playersheet[self.frame], (round(self.x),round(self.y)))
		elif self.facing == "Left":
			screen.blit(playersheet_flipped[self.frame], (round(self.x),round(self.y)))

button_desc = ""
accept_clicks = True

class Button:
	def __init__(self, x, y, text, centered=False, small=False, highlighted=True, desc=None):
		self.x = x
		self.y = y
		self.text = text
		self.color = red
		self.isclicked = False
		self.centered = centered
		self.small = small
		self.highlighted = highlighted
		self.desc = desc
	def update(self):
		self.isclicked = False  
		global button_desc
		if self.small:
			text = small_main_font.render(self.text, True, self.color)
			shadow_text = small_main_font.render(self.text, True, black)
		else:
			text = main_font.render(self.text, True, self.color)
			shadow_text = main_font.render(self.text, True, black)
		if self.centered:
			textrect = text.get_rect(center=(self.x, self.y))
		else:
			textrect = text.get_rect(topleft=(self.x, self.y))
		screen.blit(shadow_text, (textrect.x+3, textrect.y+3))
		screen.blit(text, (textrect.x, textrect.y))
		if textrect.collidepoint(pyg.mouse.get_pos()):
			if self.highlighted:
				self.color = light_gray
				if not self.desc == None:
					button_desc = self.desc
			mousedown = False
			for event in pyg.event.get():
				if event.type == pyg.MOUSEBUTTONDOWN:
					if event.button == 1:
						mousedown = True
				else:
					mousedown = False
			self.isclicked = mousedown
		else:
			self.color = red
		return self.isclicked

startbutton = Button(screenw//2, screenh//2-40, "Play", centered=True, desc="Play a variety of game modes!")
editorbutton = Button(screenw//2, screenh//2+20, "Editor", centered=True, desc="Create, play, and share your own levels!")
optionsbutton = Button(screenw//2, screenh//2+80, "Options", centered=True, desc="Access options such as volume, resolution, and controls!")
exitbutton = Button(screenw//2, screenh//2+140, "Exit", centered=True, desc="Exit the game!")
credits = Button(5, 0, "Created by Gavin P", small=True, highlighted=False)

options_back = Button(screenw//2, screenh//2+140, "Back", centered=True, desc="Go back to the main menu!")

options = False

game_start = False
fade_start = False
fade_frame = 0

editor_on = False
editor_totally_on = False

fmbdown = False

def update_fade():
	fade_surface = pyg.Surface((screenw, screenh))
	fade_surface.set_alpha(fade_frame)
	fade_surface.fill(black)
	screen.blit(fade_surface, (0,0))

editor_mode = "Box"
universalcycle = 0

# Main loop
while not exit:
	pyg.time.Clock().tick(fps)
	screen.fill(gray)
	if game_start:
		keys = pyg.key.get_pressed()
		if keys[pyg.K_a] or keys[pyg.K_LEFT]:
			player1.walk("Left")
		if keys[pyg.K_d] or keys[pyg.K_RIGHT]:
			player1.walk("Right")
		currentlevel.update()
		if not editor_totally_on:
			player1.update()
			# Debug option (Activate by pressing the alt key)
			if debug and keys[pyg.K_LALT] or debug and keys[pyg.K_RALT]:
				editor_on = True
			else:
				editor_on = False
		if editor_on:
			for i in range(24):
				pyg.draw.line(screen, black, (30*i, 0), (30*i, screenh))
			for i in range(16):
				pyg.draw.line(screen, black, (0, 30*i), (screenw, 30*i))
			def tilewise_coords(tuple):
				return (floor(tuple[0]/30), floor(tuple[1]/30))
			mouse_pos = pyg.mouse.get_pos()
			
			mouse_pos_text = calibri_font.render("Mouse (exact): "+str(mouse_pos), True, white)
			screen.blit(mouse_pos_text, (5, 5))
			
			mouse_pos_tilewise = tilewise_coords(mouse_pos)
			mouse_pos_text_tilewise = calibri_font.render("Mouse (tile): "+str(mouse_pos_tilewise), True, white)
			screen.blit(mouse_pos_text_tilewise, (5, 25))
			
			mouse_rect = pyg.Rect(pyg.mouse.get_pos(), (1, 1))
			
			editor_mode_text = calibri_font.render("Editor mode: "+editor_mode, True, white)
			screen.blit(editor_mode_text, (5, 45))

			# Editor code
			if pyg.mouse.get_pressed()[0] and mouse_rect.collidelist(currentlevel.objectrects) == -1 and mouse_rect.collidelist(currentlevel.enemyrects) == -1:
				if editor_mode == "Box":
					currentlevel.objects.append(Box(mouse_pos_tilewise[0], mouse_pos_tilewise[1], 1, 1))
				if editor_mode == "Box2":
					currentlevel.objects.append(Box(mouse_pos_tilewise[0], mouse_pos_tilewise[1], 1, 1, style=2))
				if editor_mode == "Spike":	
					currentlevel.enemies.append(Spike(mouse_pos_tilewise[0], mouse_pos_tilewise[1]))
				if editor_mode == "Spike2":	
					currentlevel.enemies.append(Spike(mouse_pos_tilewise[0], mouse_pos_tilewise[1], style=2))
				if editor_mode == "Lava":
					currentlevel.enemies.append(Lava(mouse_pos_tilewise[0], mouse_pos_tilewise[1]))
				if editor_mode == "MovingEnemy":
					currentlevel.enemies.append(MovingEnemy(mouse_pos_tilewise[0], mouse_pos_tilewise[1]))
		# Fade out code
		if fade_out_start:
			if fade_frame >= 0:
				fade_frame -= 4
			else:
				fade_out_start = False
			update_fade()
		# Full editor menu logic
		if editor_totally_on:
			playtestbutton = screen.blit(playtestsheet[0], (15, screenh-75))
			if fmbdown and playtestbutton.collidepoint(mouse_pos):
				pass
	else:
		# Handles the menu logic
		screen.blit(logo, (60,screenh//4-90))
		if options:
			if options_back.update():
				options = False
		else:
			if optionsbutton.update():
				options = True
			exit = exitbutton.update()
			if editorbutton.update():
				fade_start = True
				levelnumber = 1
				currentlevel = editorlevels[levelnumber]
				player1 = Player()
				editor_on = True
				editor_totally_on = True
			if startbutton.update():
				fade_start = True			
				levelnumber = 0
				currentlevel = levels[levelnumber]
				player1 = Player()
		credits.update()
		# Prints descriptions for the selected menu buttons
		pyg.draw.rect(screen, black, (0, screenh-60, screenw, 60))
		pyg.draw.line(screen, red, (0, screenh-60), (screenw, screenh-60), 2)
		rendered_button_desc = calibri_font.render(button_desc, True, white)
		screen.blit(rendered_button_desc, (10, screenh-40))
		# Fade in code
		if fade_start:
			if fade_frame <= 255:
				fade_frame += 4
			else:
				fade_start = False
				fade_out_start = True
				game_start = True
			update_fade()
	# Non-repeating event detection
	fmbdown = False
	for event in pyg.event.get():
		if event.type == pyg.QUIT:
			exit = True
		if game_start:
			if event.type == pyg.KEYDOWN:
				if event.key == pyg.K_SPACE or event.key == pyg.K_w or event.key == pyg.K_UP:
					if not editor_totally_on:
						player1.startjumping()
				if event.key == pyg.K_s or event.key == pyg.K_DOWN:
					if player1.velocity >= -0.5:
						player1.velocity = 1.45
				if editor_on:
					if event.key == pyg.K_1:
						editor_mode = "Box"
					if event.key == pyg.K_2:
						editor_mode = "Box2"
					if event.key == pyg.K_3:
						editor_mode = "Spike"
					if event.key == pyg.K_4:
						editor_mode = "Spike2"
					if event.key == pyg.K_5:
						editor_mode = "Lava"
					if event.key == pyg.K_6:
						editor_mode = "MovingEnemy"
				if event.key == pyg.K_q and editor_totally_on:
					print(currentlevel.getLevelCode())
			if event.type == pyg.MOUSEBUTTONDOWN:
				if event.button == 1:
					fmbdown = True
	# Universal cycle
	universalcycle += 1
	if universalcycle == fps:
		universalcycle = 0
	pyg.display.update()
# End of program
pyg.quit()
quit()