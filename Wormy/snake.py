# Mini snake game.
# Minh Bui

import pygame, sys, random
from pygame.locals import *

# Defining constants
POINTSIZE = 10
WINDOWSWIDTH = 480
WINDOWSHEIGHT = 480
FPS = 30
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
    borderRect = drawBorder()

    # Should these variables be global?
    direction = 0
    gameStart = False
    foodpos = None
    foodsEaten = 0

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
                    wormy, foods = initStateGame(borderRect)

                    # Draw wormy and food.
                    for x, y in wormy:
                        drawPoint(x, y)

                    for foodx, foody in foods:
                        drawPoint(foodx, foody)
                        foodpos = foodx, foody

                    gameStart = True
                    updateScores(foodsEaten, borderRect)
                    
                    # Detecting input keyboard for changing direction.

                # View the top scores.
                elif topScoreRect.collidepoint(event.pos):
                    MENUSURF.blit()
                    return

            elif event.type == KEYDOWN:
                if event.key in (K_LEFT, K_a) and direction != RIGHT:
                    direction = LEFT
                elif event.key in (K_RIGHT, K_d) and direction != LEFT:
                    direction = RIGHT
                elif event.key in (K_UP, K_w) and direction != DOWN:
                    direction = UP
                elif event.key in (K_DOWN, K_s) and direction != UP:
                    direction = DOWN

        if direction and gameStart:
            print 'New food at position ({}, {}).'.format(foodpos[0], foodpos[1])
            print 'Current scores: {}'.format(foodsEaten)
            foodpos, foodsEaten = moveUpdate(wormy, borderRect, foodsEaten, foodpos, direction)
            drawPoint(foodpos[0], foodpos[1])
            updateScores(foodsEaten, borderRect)

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
    borderRect = pygame.Rect(POINTSIZE + 3, POINTSIZE + 3, POINTSIZE * (BORDERSIZE + 7) + 3, \
            POINTSIZE * (BORDERSIZE + 1) + 3)
    pygame.draw.rect(GAMESURF, BLUE, borderRect, 1)

    return borderRect

def initStateGame(borderRect):
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
    foodx, foody = placeRandFood(wormy, borderRect)
    foods.append((foodx, foody))

    return wormy, foods

def placeRandFood(wormy, borderRect):
    foodx, foody = getTopLeft(random.randint(POINTSIZE + 1, POINTSIZE * BORDERSIZE - 1),\
            random.randint(POINTSIZE + 1, POINTSIZE * BORDERSIZE - 1))
    while ((foodx, foody) in wormy \
            or not borderRect.collidepoint((foodx, foody))):
        foodx, foody = getTopLeft(random.randint(POINTSIZE + 1, POINTSIZE * BORDERSIZE - 1), \
                random.randint(POINTSIZE + 1, POINTSIZE * BORDERSIZE - 1))
    return foodx, foody

def getTopLeft(x, y):
    return (POINTSIZE * (x / POINTSIZE), POINTSIZE * (y / POINTSIZE))

def drawPoint(x, y):
    x, y = getTopLeft(x, y)
    pygame.draw.rect(MENUSURF, POINTCOLOR, (x, y, POINTSIZE, POINTSIZE))

def moveUpdate(wormy, borderRect, foodsEaten, foodpos, direction):
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
    if not checkValidMove(wormy, borderRect):
        print 'Game Over'
        terminate()

    if checkFood(wormy, oldTail, foodpos):
        foodpos = placeRandFood(wormy, borderRect)
        foodsEaten += 1

    # Draw a blank space over the moving point on the baseSurf Surface.
    moveLeft, moveTop = getTopLeft(oldTail[0], oldTail[1])
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, POINTSIZE, POINTSIZE))

    for i in range(len(wormy)):
        checkForQuit()
        MENUSURF.blit(baseSurf, (0, 0))
        drawPoint(wormy[i][0], wormy[i][1])
        pygame.display.update()
        # Note: the tick(FPS) function below makes the
        # game runs slower. Why?
        #FPSCLOCK.tick(FPS)
    return foodpos, foodsEaten

def checkValidMove(wormy, borderRect):
    # The function assumes that wormy has made its invalid move.
    # If the move is invalid then the game is over.
    # If wormy's head either hits the border or hit a portion
    # of its body, the game is over.

    head = wormy[len(wormy) - 1]
    headtop, headleft = getTopLeft(head[0], head[1])
    headRect = pygame.Rect(headtop, headleft, POINTSIZE, POINTSIZE)
    if head in wormy[0:len(wormy) - 1]\
            or not borderRect.contains(headRect):
        return False
    else:
        return True

def checkFood(wormy, oldTail, foodpos):
    # The function assumes that wormy has made its move.
    # The function checks if Wormy has eaten its food after
    # its movement. If there is food, 'extend' Wormy's length.

    head = wormy[len(wormy) - 1]
    if getTopLeft(head[0], head[1]) == getTopLeft(foodpos[0], foodpos[1]):
        wormy.insert(0, oldTail)
        return True
    return False

def updateScores(foodsEaten, borderRect):
    scoreCenter = WINDOWSWIDTH / 8, borderRect.height + (WINDOWSHEIGHT - borderRect.height) / 2
    baseSurf = MENUSURF.copy()
    scoreSurf, scoreRect = make_text(BASICFONT, "Score: " + str(foodsEaten), WHITE, scoreCenter)

    # Draw a blank rect into the updating score surface.
    pygame.draw.rect(baseSurf, BGCOLOR, (scoreRect.left, scoreRect.top, scoreRect.width, scoreRect.height))
    MENUSURF.blit(baseSurf, (0, 0))
    MENUSURF.blit(scoreSurf, scoreRect)

if __name__ == '__main__':
    main()
