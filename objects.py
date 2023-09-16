from consts import *
from collections import deque
import random as r
from math import ceil
from math import floor
import pygame
pygame.init()
clock = pygame.time.Clock()
r.seed()
screen = pygame.display.set_mode(screenSize)
apple = r.randint(0, boardDimensions[0] * boardDimensions[1]-1)
playing = True

class snake:
    def __init__(self):
        self.body = deque()
        self.heading = 0 #0 is up, go clockwise from there


def gameStart():
    global screen
    screen.fill(GREEN)
    playerSnake = snake()
    playerSnake.body.append(boardDimensions[0] * boardDimensions[1] // 2 + boardDimensions[0] // 2)
    frameTick(playerSnake)


def frameTick(playerSnake):
    global apple
    global clock
    global screen
    global playing
    global fps
    #make screen black and dont go too fast
    screen.fill(BLACK)
    clock.tick(fps)

    #check for change in direction or end of game
    for event in pygame.event.get():
        etype = event.type

        if (etype == pygame.QUIT):
            pygame.quit()
            return
        elif (etype == pygame.KEYDOWN):
            #someting happened
            if ((event.key == pygame.K_w) | (event.key == pygame.K_UP)):
                playerSnake.heading = 0
            elif ((event.key == pygame.K_d) | (event.key == pygame.K_RIGHT)):
                playerSnake.heading = 1
            elif ((event.key == pygame.K_s) | (event.key == pygame.K_DOWN)):
                playerSnake.heading = 2
            elif ((event.key == pygame.K_a) | (event.key == pygame.K_LEFT)):
                playerSnake.heading = 3
            else:
                continue
        else:
            continue

    #movement win/lose
    if (playerSnake.heading == 0):
        #up
        if (playerSnake.body[0] < boardDimensions[0]):
            playing = False
        else:
            playerSnake.body.appendleft(playerSnake.body[0] - boardDimensions[0])
    elif (playerSnake.heading == 1):
        #right
        if (playerSnake.body[0] % boardDimensions[0] == boardDimensions[0] - 1):
            playing = False
        else:
            playerSnake.body.appendleft(playerSnake.body[0] + 1)
    elif (playerSnake.heading == 2):
        #down
        if (floor(playerSnake.body[0] // boardDimensions[0]) == boardDimensions[1] - 1):
            playing = False
        else:
            playerSnake.body.appendleft(playerSnake.body[0] + boardDimensions[0])
    else:
        #left
        if (playerSnake.body[0] % boardDimensions[0] == 0):
            playing = False
        else:
            playerSnake.body.appendleft(playerSnake.body[0] - 1)

    if ((playerSnake.body[0] == apple) | (playing == False)):
        if (len(playerSnake.body) % 6 == 0):
            fps += 1
        #regenerate apple and make sure it isn't IN the snake's body
        while (playerSnake.body.count(apple) > 0):
            apple = r.randint(0, boardDimensions[0] * boardDimensions[1]-1)
    else:
        playerSnake.body.pop()
    print(playerSnake.body)

    if ((playing == True) & (playerSnake.body.count(playerSnake.body[0]) > 1)):
        playing = False

    #display
    #distance from left, distance from top, width, height
    """
    pos % boardDimensions[0] gives cells to left till wall
    floor(pos // boardDimensions[0]) gives cells above
    """
    #draw apple
    pygame.draw.circle(screen, RED, (apple % boardDimensions[0] * cellSize[0] + cellSize[0] // 2, floor(apple // boardDimensions[0]) * cellSize[1] + cellSize[1] // 2), cellSize[1] // 2)

    #draw snake
    #head
    pygame.draw.circle(screen, HEAD, (playerSnake.body[0] % boardDimensions[0] * cellSize[0] + cellSize[0] // 2, floor(playerSnake.body[0] // boardDimensions[0]) * cellSize[1] + cellSize[1] // 2), cellSize[1] // 2)
    #rest
    for j in range(len(playerSnake.body) - 1):
        i = j + 1
        segment = [playerSnake.body[i] % boardDimensions[0] * cellSize[0], floor(playerSnake.body[i] // boardDimensions[0]) * cellSize[1], cellSize[0], cellSize[1]]
        pygame.draw.ellipse(screen, GREEN, segment)

    pygame.display.update()

    if ((pygame.event.peek(pygame.QUIT)) | (playing == False)):
        pygame.quit()
        return
    frameTick(playerSnake)