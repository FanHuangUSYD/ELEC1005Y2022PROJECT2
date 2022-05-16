# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""

from turtle import back
from webbrowser import BackgroundBrowser
import pygame #importing module pygame
import time #importing time module 
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE #importing the keys 
#key_down means that a key has been pressed
from pygame.locals import QUIT
from pygame import mixer

from game import Game

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
background = pygame.Color(0, 100, 0)

#all colors
green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
bright_yellow = pygame.Color(255, 255, 0)
orange = pygame.Color(204, 85, 0)
bright_orange = pygame.Color(255,83,73)

game = Game()
rect_len = game.settings.rect_len
snake = game.snake
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15)) #this sets the window size from what was set multiplied by 15
pygame.display.set_caption('SnakeGame') #names the window 
file = open("highscore.txt","r")
displayscore = file.readline()
file.close()


# sounds
crash_sound = pygame.mixer.Sound('./sound/crash.wav')
eat_sound = pygame.mixer.Sound('./sound/eat.wav')

# images
backgroundimage = pygame.image.load('./images/background.png')

def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y, color=black):
    large_text = pygame.font.SysFont('comicsansms', 50)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)

def paragraph_display(text, x, y, color=black):
    small_text = pygame.font.SysFont('comicsansms', 20)
    text_surf, text_rect = text_objects(text, small_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)


def button(msg, altmsg, x, y, w, h, inactive_color, active_color, action=None, parameter=None): #x,y,w,h are dimensions of button and the =None refers to if no parameter is given then its default is None
    mouse = pygame.mouse.get_pos() #this gets x,y coordinates of mouse
    click = pygame.mouse.get_pressed() #this determines wether or not the mouse is pressed
    if x + w > mouse[0] > x and y + h > mouse[1] > y: #mouse[0] is the x coordinate and mouse[1] is the y coordinate and this if statement determins if the mouse is in the box or not to flash green 
        pygame.draw.rect(screen, active_color, (x, y, w, h)) #could i potentially add a click sound or smt whenever the mouse is in the button? 
        msg = altmsg
        if click[0] == 1 and action != None: #click[0] == 1 is if the mouse is clicked
            if parameter != None:
                action(parameter)
            else:
                action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    smallText = pygame.font.SysFont('comicsansms', 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)


def quitgame():
    pygame.quit()
    quit()


def crash():
    pygame.mixer.Sound.play(crash_sound)
    message_display('crashed', game.settings.width / 2 * 15, game.settings.height / 3 * 15, white)
    file = open("scores.txt",'a')
    file.write(f"{str(snake.score)}" + "\n")
    file.close()
    file = open("scores.txt","r")
    score = file.readlines()
    i = 0
    check = 0
    highscore = 0
    while i < len(score):
        num = int(score[i])
        if check < num:
            highscore = num
            check = num
            i = i + 1
        else:
            i = i + 1
    file2 = open("highscore.txt","w")
    highscore = str(highscore)
    file2.write(highscore)
    file2.close

        




def initial_interface():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        file2 = open("highscore.txt","r")
        screen.fill(background) #background refers to background colour
        message_display('SNAKE GAME!!', game.settings.width / 2 * 15, game.settings.height / 4 * 15)

        button('Go!', "CMON!!",80, 240, 80, 40, green, bright_green, game_loop, 'human') #this is the button go and it used the function 
        button('Quit', "bruh no", 270, 240, 80, 40, red, bright_red, quitgame) #this is the button quit 
        button('Difficulty', "u sure?", 170, 240 , 90, 40, orange, bright_orange, levels)

        paragraph_display("Current difficulty: easy", 210, 300, black)
        paragraph_display(f"Highscore: {file2.readline()}",210,350,black)
        pygame.display.update()
        pygame.time.Clock().tick(15)
    file2.close()


def game_loop(player, fps=10):


    game.restart_game()


    while not game.game_end():

        pygame.event.pump()

        move = human_move()

        game.do_move(move)

        screen.blit(backgroundimage, (0,0))

        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)

        pygame.display.flip()

        fpsClock.tick(fps)

    crash()


def human_move():
    direction = snake.facing

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        elif event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == ord('d'):
                direction = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                direction = 'left'
            if event.key == K_UP or event.key == ord('w'):
                direction = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                direction = 'down'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    move = game.direction_to_int(direction)
    return move

def levels():
    intro = True
    while intro:
        file2 = open("highscore.txt","r")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
        screen.fill(background)
        
        message_display('Choose your level', 210 , 240)
        paragraph_display(f"Highscore: {file2.readline()}",210,350,black)


        button('Easy', "u dum",80, 100, 80, 40, green, bright_green, difficulty_easy)
        button('Hard', "nice choice", 170, 100 , 90, 40, orange, bright_orange, difficulty_medium)
        button('XTREME', "have fun", 270, 100, 80, 40, red, bright_red, difficulty_hard)


        pygame.display.update()
        pygame.time.Clock().tick(15)
    file2.close()


def difficulty_easy():
    game_loop("human",10)

def difficulty_medium():
    game_loop("human",20)

def difficulty_hard():
    game_loop("human",30)




if __name__ == "__main__":
    initial_interface()
