
#First do imports, obviously pygame
import pygame
from pygame import *

#Set the screen dimensions
WIN_WIDTH = 768
WIN_HEIGHT = 672

#Set the screen defaults
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0

#Load the spritesheet you are using by using pygame.image.load
#with the path to the spritesheet

spritesheet = pygame.image.load("Media/Graphics/megamansprites.png")

#Add the main function

def main():

    #Init pygame, create the screen, and set a caption (if you want)
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("Sprite Mapper")

    #Set x and y variables to zero, and w and h variables to 100
    x = y = 0
    w = h = 100

    #Set the key repeat so the frame resizer doesn't move too fast
    pygame.key.set_repeat(1,30)

    #Create a blank text file if it doesn't exist
    f = open("test.txt","w")
    f.close()

    #Create a while 1 loop to serve as the main loop

    while 1:

        #Use for e in pygame.event.get() to read key presses
        
        for e in pygame.event.get():

            #Raise system exit if x on window is clicked
            if e.type == QUIT: raise SystemExit, "QUIT"

            #Raise system exit if Escape is pressed
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit, "ESCAPE"

            #Keys up, down, left, right will move the spritesheet
            if e.type == KEYDOWN and e.key == K_UP:
                y = y - 1
            if e.type == KEYDOWN and e.key == K_DOWN:
                y = y + 1
            if e.type == KEYDOWN and e.key == K_LEFT:
                x = x - 1
            if e.type == KEYDOWN and e.key == K_RIGHT:
                x = x + 1

            #Home, end, delete, and pagedown will resize the frame
            if e.type == KEYDOWN and e.key == K_HOME:
                h = h - 1
            if e.type == KEYDOWN and e.key == K_END:
                h = h + 1
            if e.type == KEYDOWN and e.key == K_DELETE:
                w = w - 1
            if e.type == KEYDOWN and e.key == K_PAGEDOWN:
                w = w + 1

            #Space bar will save the code to the text file
            if e.type == KEYDOWN and e.key == K_SPACE:

                #Prompt for name of sprite on the console
                name = raw_input("Name of Sprite?")

                #Open the text file in append mode to add text to it
                f = open("test.txt","a")
                
                #Create the first line of drawing code and write it
                savedcode = "character = Surface((" + str(w) + "," + str(h) + "),pygame.SRCALPHA)" + "\n"
                f.write(savedcode)

                #Create second line and write it
                savedcode = "character.blit(spritesheet,(" + str(x) + "," + str(y) + "))" + "\n"
                f.write(savedcode)
                
                #Create third line and write it
                savedcode = "character = pygame.transform.scale(character, (" + str(w) + "*4," + str(h) + "*4))" + "\n"
                f.write(savedcode)

                #Create fourth line and write it
                savedcode = "stage = Surface((300,150),pygame.SRCALPHA)" + "\n"
                f.write(savedcode)

                #Create fifth line and write it
                savedcode = "stage.blit(character,(130,0))" + "\n"
                f.write(savedcode)

                #Create sixth line and write it
                savedcode = name + " = stage"
                f.write(savedcode)

                #Add some new line breaks and write them
                savedcode = "\n" + "\n"
                f.write(savedcode)

                #Close the text file
                f.close()

        #Back in our main loop, fill the screen with black
        screen.fill(Color("#000000"))

        #Create the frame with the current values of width(w) and height(h)
        #and fill the frame with white
        character = Surface((w,h))
        character.fill(Color("#FFFFFF"))

        #Blit the spritesheet onto the frame at it's current x, y coordinates
        #Upscale the frame times four so it's not tiny
        #Then blit the frame to the screen
        character.blit(spritesheet,(x,y))
        character = pygame.transform.scale(character,(w*4,h*4))
        screen.blit(character,(0,0))

        #And of course update the display
        pygame.display.update()

#Finally add the code to end the script
if _name_ == "__main__":
    main()

#The output for the spritemapper will be something like this:

#character = Surface((100,100),pygame.SRCALPHA)
#character.blit(spritesheet,(-18,0))
#character = pygame.transform.scale(character, (100*4,100*4))
#stage = Surface((300,150),pygame.SRCALPHA)
#stage.blit(character,(130,0))
#sprite = stage

#First a transparent surface is created that is the size of the frame
#The frame will have the spritesheet drawn to it at the right coordinates
#The frame is upscaled so it's not too small
#A larger transparent surface is created
#The frame is drawn to the larger surface
#The larger surface is stored under a unique name

#This large surface that's created has the sprite on it
#It can be drawn to the screen with screen.blit(sprite,(0,0))
#Or however you draw surfaces to the screen in your game

#I upscale the sprites in my game by multiplying their size by four
#But this might be different depending on what spritesheet you have
#and what resolution your window is

#Also if you need to center the sprite better on the transparent
#background you can adjust the value in stage.blit(character,(130,0))
#The 130 is the x position of the sprite on the transparent background

#If you want to see the transparent background when testing
#the sprite to see if it's centered, remove pygame.SRCALPHA from
#stage = Surface((300,150),pygame.SRCAPLHA)
#pygame.SRCAPLHA tells python to make the image transparent
#stage = Surface((300,150)) would create a black background

#So hope this all makes sense, make sure you type out each line of code
#because copying and pasting it won't work﻿