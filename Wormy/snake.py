# Mini snake game.
# Minh Bui

import pygame, sys, random
from pygame.locals import *

# Defining constants
POINTSIZE = 4
WINDOWSWIDTH = 640
WINDOWSHEIGHT = 480
FPS = 30
BASICFONTSIZE = 20
TITLEFONTSIZE = 120
INITSNAKELEN = 4

# RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 204, 0)
BLUE = (0, 50, 255)
RED = (255, 0, 0)

BORDERCOLOR = BLUE
SYSTEMTEXTSCOLOR = WHITE
POINTCOLOR = WHITE
TITLETEXTCOLOR = RED


def main():
    global BASICFONT, TITLEFONT, MENUSURF, GAMESURF, TOPSCORESURF, INPUTSURF

    pygame.init()
    MENUSURF = pygame.display.set_mode((WINDOWSWIDTH, WINDOWSHEIGHT))
    pygame.display.set_caption('Wormy')

    # Defining font
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    TITLEFONT = pygame.font.Font('freesansbold.ttf', TITLEFONTSIZE)

    menuObj = []
    # Creating text for title
    menuObj.append(make_text(TITLEFONT, 'Wormy', GREEN, (WINDOWSWIDTH / 2, WINDOWSHEIGHT / 3)))
    menuObj.append(make_text(BASICFONT, 'by Minh Bui', RED, \
        (WINDOWSWIDTH / 2 + (menuObj[len(menuObj) - 1][1].right - WINDOWSWIDTH / 2) / 2, \
        WINDOWSHEIGHT / 2)))

    # Creating text button for the main menu.
    menuObj.append(make_text(BASICFONT, 'Start', WHITE, \
            (WINDOWSWIDTH / 2, WINDOWSHEIGHT/2 + WINDOWSHEIGHT/3)))
    menuObj.append(make_text(BASICFONT, 'Top scores', WHITE, \
            (WINDOWSWIDTH / 2, menuObj[len(menuObj) - 1][1].center[1] + WINDOWSHEIGHT / 15)))


    # Main game loop.
    while True:
        # Draw menu objects.
        drawOnSurface(MENUSURF, menuObj)
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

        pygame.display.update()

def make_text(font, text, color, center):
    textSurf = font.render(text, True, color)
    textRect = textSurf.get_rect()
    textRect.center = center
    return textSurf, textRect

def drawOnSurface(mainSurf, listSD):
    for surf, rect in listSD:
        mainSurf.blit(surf, rect)

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    return


if __name__ == '__main__':
    main()
