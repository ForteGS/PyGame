# Mini snake game.
# Minh Bui

import pygame, sys, random
from pygame.locals import *

# Defining constants
POINTSIZE = 10
WINDOWSWIDTH = 640
WINDOWSHEIGHT = 640
FPS = 60
BASICFONTSIZE = 20
TITLEFONTSIZE = 120
INITSNAKELEN = 4
BORDERSIZE = WINDOWSHEIGHT / POINTSIZE - POINTSIZE

UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'

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
BGCOLOR = BLACK


def main():
    global BASICFONT, TITLEFONT, DISPLAYSURF, MENUSURF, GAMESURF, TOPSCORESURF, INPUTSURF, FPSCLOCK

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    MENUSURF = pygame.display.set_mode((WINDOWSWIDTH, WINDOWSHEIGHT))
    GAMESURF = MENUSURF.copy()
    TOPSCORESURF = MENUSURF.copy()
    INPUTSURF = MENUSURF.copy()

    pygame.display.set_caption('Wormy')

    # Defining font
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    TITLEFONT = pygame.font.Font('freesansbold.ttf', TITLEFONTSIZE)

    # Main menu components: title and menu options.
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

    startSurf, startRect = menuObj[2]
    topScoreSurf, topScoreRect = menuObj[3]

    # Main game components: Wormy, border, system text message, 
    # scores, and food.
    gameObj = []
    #drawBorder()

    direction = 0
    gameStart = False

    # Draw menu object.
    drawOnSurface(MENUSURF, menuObj)
    # Main game loop.
    while True:
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                # Clicked on start button.
                if startRect.collidepoint(event.pos):
                    MENUSURF.blit(GAMESURF, (0, 0))
                    wormy, foods = initStateGame()

                    # Draw wormy and food.
                    for x, y in wormy:
                        drawPoint(x, y)

                    for foodx, foody in foods:
                        drawPoint(foodx, foody)

                    gameStart = True

                    # Detecting input keyboard for changing direction.

                # View the top scores.
                elif topScoreRect.collidepoint(event.pos):
                    MENUSURF.blit()
                    return

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    direction = LEFT
                elif event.key in (K_RIGHT, K_d):
                    direction = RIGHT
                elif event.key in (K_UP, K_w):
                    direction = UP
                elif event.key in (K_DOWN, K_s):
                    direction = DOWN

        if direction and gameStart:
            moveUpdate(wormy, direction)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

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
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def drawBorder(message = None):
    pygame.draw.rect(GAMESURF, BLUE, \
            (POINTSIZE - 2, POINTSIZE - 2, POINTSIZE * BORDERSIZE + 1, POINTSIZE * BORDERSIZE + 1), 1)
    return

def initStateGame():
    # There should be a list of point that belongs to the snake.
    # The first point in the list belongs to the snake.
    wormy = []
    foods = []
    for i in range (INITSNAKELEN):
        x, y = getTopLeft((BORDERSIZE + INITSNAKELEN) / 2 + i * POINTSIZE,\
                (BORDERSIZE + INITSNAKELEN) / 2)
        wormy.append((x, y))

    # Random an init food.
    # Have to consider the border line too.
    # The food cannot be outside the border line.
    foodx, foody = placeRandFood(wormy)
    foods.append((foodx, foody))

    return wormy, foods

def placeRandFood(wormy):
    foodx, foody = getTopLeft(random.randint(POINTSIZE + 1, POINTSIZE * BORDERSIZE - 1),\
            random.randint(POINTSIZE + 1, POINTSIZE * BORDERSIZE - 1))
    while ((foodx, foody) in wormy):
        foodx, foody = getTopLeft(random.randint(POINTSIZE + 1, POINTSIZE * BORDERSIZE - 1), \
                random.randint(POINTSIZE + 1, POINTSIZE * BORDERSIZE - 1))
    return foodx, foody

def getTopLeft(x, y):
    return (POINTSIZE * (x / POINTSIZE), POINTSIZE * (y / POINTSIZE))

def drawPoint(x, y):
    x, y = getTopLeft(x, y)
    pygame.draw.rect(MENUSURF, POINTCOLOR, (x, y, POINTSIZE, POINTSIZE))
    return

def moveUpdate(wormy, direction):
    # This function does not check valid move.

    # Assign to the head first.
    oldhead = wormy[len(wormy) - 1]

    oldTail = wormy[0]

    # Update the body's and tail's coordinates.
    for i in range(len(wormy) - 1):
        wormy[i] = wormy[i + 1]

    # Update the head's coordinates.
    if direction == UP:
        wormy[len(wormy) - 1] = getTopLeft(oldhead[0], oldhead[1] - POINTSIZE)
    elif direction == DOWN:
        wormy[len(wormy) - 1] = getTopLeft(oldhead[0], oldhead[1] + POINTSIZE)
    elif direction == LEFT:
        wormy[len(wormy) - 1] = getTopLeft(oldhead[0] - POINTSIZE, oldhead[1])
    elif direction == RIGHT:
        wormy[len(wormy) - 1] = getTopLeft(oldhead[0] + POINTSIZE, oldhead[1])

    baseSurf = MENUSURF.copy()

    # Draw a blank space over the moving point on thte baseSurf Surface.
    moveLeft, moveTop = getTopLeft(oldTail[0], oldTail[1])
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, POINTSIZE, POINTSIZE))

    for i in range(len(wormy)):
        checkForQuit()
        MENUSURF.blit(baseSurf, (0, 0))
        drawPoint(wormy[i][0], wormy[i][1])
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
