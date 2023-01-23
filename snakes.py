# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 09:18:18 2022

@author: Paul Knytl
"""

import curses
import random
import time

def splashScreen(window):
    with open('logo.txt') as file:
        for line in file:
            buffer = file.readline()
            window.addstr(buffer)
    window.refresh()
    time.sleep(5)
    

def updateWindow(window):
    window.clear()
    window.border()
    window.refresh()
    return None
    
#Need to update this to move the snake along
def moveSnake(location: list, direction):  
    if direction == curses.KEY_UP: 
        location.insert(0, [location[0][0] - 1, location[0][1]])
    elif direction == curses.KEY_DOWN:
        location.insert(0, [location[0][0] + 1, location[0][1]])
    elif direction == curses.KEY_LEFT: 
        location.insert(0, [location[0][0], location[0][1] - 1])
    elif direction == curses.KEY_RIGHT:
        location.insert(0, [location[0][0], location[0][1] + 1])
    else:
        return location
    
    location.pop()
       
    return location

def checkState(h, w, snake_loc, food_loc, score):
    game_state = ''
    #check edges
    if (snake_loc[0][0] == h-1) or (snake_loc[0][0] == 0) or (snake_loc[0][1] == w-1) or (snake_loc[0][1] == 0):
        game_state = 'Dead!'
    #check self
    elif snake_loc[0] in snake_loc[1:]:
        game_state = 'Dead!'
    #check food
    elif snake_loc[0] in food_loc:
        score += 10
        snake_loc.append(food_loc) 
        food_loc = [[random.randint(1,h-2), random.randint(1, w-2)]]
    else:
        game_state = ''
        
    return snake_loc, food_loc, score, game_state
    
def drawSnake(window, snake_loc, snake_sprite):
    for segment in snake_loc:
        window.addch(segment[0], segment[1], snake_sprite)
    window.refresh()
        
def main(screen):
    #Initialize Window
    h, w = screen.getmaxyx()
    window = curses.newwin(h, w, 0, 0)
    curses.noecho()
    curses.cbreak()
    window.keypad(True)
    curses.curs_set(0)
    timeout = 100
    window.timeout(timeout)
    splashScreen(window)
    
    #Initialize objects
    snake_loc = [[random.randint(1,h-2), random.randint(1, w-2)]]
    food_loc = [[random.randint(1,h-2), random.randint(1, w-2)]]
    snake_sprite = curses.ACS_DIAMOND
    food_sprite = curses.ACS_BULLET
    
    window.addch(food_loc[0][0], food_loc[0][1], food_sprite)
    drawSnake(window, snake_loc, snake_sprite)
      
    key = ''
    game_state = ''
    score = 0
    last_key = 0
    
    #Main loop
    while key != ord('q') and game_state != 'Dead!':
        
        #Get next action
        key = window.getch()
        if key == -1: key = last_key
        snake_loc = moveSnake(snake_loc, key)
        
        #update screen
        window.clear()
        window.addch(food_loc[0][0], food_loc[0][1], food_sprite) #draw food
        drawSnake(window, snake_loc, snake_sprite)
        window.border()
        window.refresh()
        
        #check and update game state
        snake_loc, food_loc, score, game_state = checkState(h, w, snake_loc, 
                                                            food_loc, score)
        last_key = key
        
    if key == ord('q'): game_state = 'Quit'    
    
    #Handle game end screen
    #window.clear()
    window.addstr(h//2, w//2 - 7, game_state + ' - Score: {}'.format(score))
    window.refresh()
    time.sleep(5)
    
curses.wrapper(main)
