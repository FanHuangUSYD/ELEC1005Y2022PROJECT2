# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""

from pickle import TRUE
from tkinter import CENTER
import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT

from game import Game

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

background = pygame.image.load('images/background.jpg')
start_img = pygame.image.load('images/start_btn.png')
start_img_ac = pygame.image.load('images/start_btnOn.png')
exit_img = pygame.image.load('images/exit_btn.png')
exit_img_ac = pygame.image.load('images/exit_btnOn.png')


green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
bright_yellow = pygame.Color(255, 255, 0)

game = Game()
rect_len = game.settings.rect_len
snake = game.snake
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15))
pygame.display.set_caption('Gluttonous')

crash_sound = pygame.mixer.Sound('./sound/crash.wav')

custom_font = pygame.font.Font("images/Wicked_Mouse.ttf", 35)
custom_font_back = pygame.font.Font("images/Wicked_Mouse.ttf", 35)

starting_message_back = custom_font_back.render("Gluttonous", TRUE, (0, 0, 0))
starting_message = custom_font.render("Gluttonous", TRUE, (255, 191, 0))



def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y, color=black):
    large_text = pygame.font.SysFont('comicsansms', 50)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()


def button(msg, x, y, w, h, inactive_img, active_img, action=None, parameter=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y: #checks if the current mouse coordinates collide with the buttons coordinates
        pygame.draw.rect(screen, 0 ,(x, y, w, h))
        screen.blit(active_img, (x, y) )
        if click[0] == 1 and action != None:
            if parameter != None:
                action(parameter)
            else:
                action()
    else:
        pygame.draw.rect(screen, 0, (x, y, w, h))
        screen.blit(inactive_img, (x, y))

    smallText = pygame.font.SysFont('comicsansms', 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)


def quitgame():
    pygame.quit()
    quit()


def crash(): #when the player crashes to themselves, a sound plays and a defeat message displays
    pygame.mixer.Sound.play(crash_sound)
    message_display('crashed', game.settings.width / 2 * 15, game.settings.height / 3 * 15, white)# can change to wasted here
    time.sleep(1)


def initial_interface(): #menu
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(white) #starting screen display
        screen.blit(background, (0, 0))
        screen.blit(starting_message_back, (game.settings.width / 5.9 * 15, game.settings.height / 4.6 * 15))
        screen.blit(starting_message, (game.settings.width / 6.2 * 15, game.settings.height / 4.7 * 15))

        #message_display('Gluttonous', game.settings.width / 2 * 15, game.settings.height / 4 * 15)

        button('', 80, 210, 80, 40, start_img, start_img_ac, game_loop, 'human') #start button
        button('', 240, 210, 80, 40, exit_img, exit_img_ac, quitgame) #exit button

        pygame.display.update()
        pygame.time.Clock().tick(15)


def game_loop(player, fps=10):
    game.restart_game()

    while not game.game_end():

        pygame.event.pump()

        move = human_move()
        fps = 5

        game.do_move(move)

        screen.fill(black)
        screen.blit(background, (0, 0)) #displaying the background during game

        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)

        pygame.display.flip()

        fpsClock.tick(fps)

    crash()


def human_move():
    direction = snake.facing #stores the current direction

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        elif event.type == KEYDOWN: #when any of the arrow keys are pressed, checks which one is pressed
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


if __name__ == "__main__":
    initial_interface()
