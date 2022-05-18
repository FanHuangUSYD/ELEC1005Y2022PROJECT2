# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""


from tkinter import CENTER
import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT

from game import Game

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

background = pygame.image.load('images/background.jpg')

start_img_off = pygame.image.load('images/start_btn.png')
start_img = pygame.image.load('images/start_btnOn.png')

exit_img_off = pygame.image.load('images/exit_btn.png')
exit_img = pygame.image.load('images/exit_btnOn.png')

scroll_clsd_off = pygame.image.load('images/test1scroll_ac.png')
scroll_clsd = pygame.image.load('images/test1scroll.png')

scroll_opnd = pygame.image.load('images/scroll_opnd1.png')


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

title_font = pygame.font.Font("images/Fonts/Wicked_Mouse.ttf", 35)
instruct_font = pygame.font.Font('images/Fonts/Minecraft.ttf', 14)


starting_message_back = title_font.render("Gluttonous", True, (0, 0, 0))
starting_message = title_font.render("Gluttonous", True, (255, 191, 0))

instruct_msg = instruct_font.render("Navigate around the", True, (106, 78, 66))
instruct_msg1 = instruct_font.render("screen with", True, (106, 78, 66))
instruct_msg2 = instruct_font.render("arrow keys.", True, (106, 78, 66))

instruct_msg3 = instruct_font.render("Eat as many fruits", True, (106, 78, 66))
instruct_msg4 = instruct_font.render("as possible and", True, (106, 78, 66))
instruct_msg5 = instruct_font.render("avoid crashing.", True, (106, 78, 66))

exit_instruction = pygame.USEREVENT + 0 #this creates a custom event, at the 24th ID as the first 23 are reserved

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
        screen.blit(active_img, (x, y) )
        if click[0] == 1 and action != None:
            if parameter != None:
                action(parameter)
            else:
                action()
    else:
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
    message_display('crashed', 
                    game.settings.width / 2 * 15,
                    game.settings.height / 3 * 15, 
                    white)# can change to wasted here
    time.sleep(1)
        
def initial_interface(): #menu
    intro = True
    stop_loop = False
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT or intro == False:
                quitgame()

        screen.fill(white) #starting screen display
        screen.blit(background, (0, 0))

        screen.blit(starting_message_back,
                   (game.settings.width / 5.9 * 15, 
                    game.settings.height / 4.6 * 15))

        screen.blit(starting_message,  
                   (game.settings.width / 6.2 * 15, 
                    game.settings.height / 4.7 * 15))

        button('', 80, 185, 100, 45, start_img_off, start_img, game_loop, 'human') #start button
        button('', 240, 185, 100, 45, exit_img_off, exit_img, quitgame) #exit button
        button('', 165, 280, 90, 35, scroll_clsd_off, scroll_clsd, instruct_screen)

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

def instruc_exit():
    exit_instruction

def instruct_screen():
    instruct = True
    stop_loop = False
    while instruct:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
            elif event.type == exit_instruction:
                instruct = False
            
        screen.fill(white)
        screen.blit(background, (0, 0))

        screen.blit(scroll_opnd, (85 , 50))

        screen.blit(instruct_msg, (142, 117))
        screen.blit(instruct_msg1, (170,137))
        screen.blit(instruct_msg2, (170,157))

        screen.blit(instruct_msg3, (148, 193))
        screen.blit(instruct_msg4, (157,213))
        screen.blit(instruct_msg5, (157,233))

        button('', 160, 340, 100, 50, exit_img_off, exit_img, initial_interface)

        pygame.display.update()
        pygame.time.Clock().tick(15)
           

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
