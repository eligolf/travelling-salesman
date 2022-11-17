import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import random
import time
import math
import os
import tkinter as tk
from itertools import permutations
from tkinter import messagebox
#-------------------------------------

# Settings
WIDTH = 600
HEIGHT = 500
WIN_WIDTH = WIDTH + 160
WIN_HEIGHT = HEIGHT
TITLE = 'Travelling Salesperson'
FPS = 30

SCREEN = pygame.Rect(0, 0, WIDTH, HEIGHT)
MENU = pygame.Rect(WIDTH, 0, WIN_WIDTH, HEIGHT)
SCREEN_CENTER = (WIN_WIDTH + WIDTH)/2

RADIUS = 5

pygame.font.init()
FONT = pygame.font.SysFont('Helvetica', 24, bold = True)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#------ Main object -------------------------------

class Calc:

    def __init__(self):
        
        # Init window
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        # Number of cities when starting program
        self.number = 9

    def run(self):
        
        # Parameters and arrays
        self.best_dist = self.number*WIDTH
        self.cities = []
        self.distance = [[0] * self.number for _ in range(self.number)]
        
        # Generate cities and draw start screen          
        self.random_points()
        self.draw()
        
        self.calc = True
        while self.calc:
            self.clock.tick(FPS)
            self.events()

    def events(self):
        for event in pygame.event.get():
            
                if pygame.MOUSEBUTTONUP and pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()

                    if self.new_rect.collidepoint(pos):
                        self.calc = False
                        self.run()

                    if self.run_rect.collidepoint(pos):
                        self.start_calc()
                        
                if event.type == pygame.KEYDOWN:
                    if event.unicode == '+' and self.number < 10:
                        self.number += 1
                        self.calc = False
                        self.run()
                    if event.unicode == '-' and self.number > 2:
                        self.calc = False
                        self.number -= 1
                        self.run()
                    
                if event.type == pygame.QUIT:
                    self.calc = False
                    pygame.quit()
                    
    def draw(self):
        
        # Background color left and right side
        pygame.draw.rect(self.win, BLACK, SCREEN)
        pygame.draw.rect(self.win, GREY, MENU)

        # Buttons and text
        self.run_text, self.run_rect = self.create_text('Run', SCREEN_CENTER, WIN_HEIGHT - 100)
        self.new_text, self.new_rect = self.create_text('New', SCREEN_CENTER, WIN_HEIGHT - 50)
        self.create_text('Cities (+/-): ' + str(self.number), SCREEN_CENTER, 100)
        
        # Cities
        for city in range(len(self.cities)):
            x, y = self.cities[city].x, self.cities[city].y
            pygame.draw.circle(self.win, WHITE, (x, y), RADIUS)        
        
        # Update display
        pygame.display.flip()
        
    def start_calc(self):
        
        self.t1 = time.clock()
        for path in permutations(self.cities):
            dist_sum = 0
            for city in range(self.number - 1):
                a, b = path[city], path[city+1]
                dist_sum += self.distance[a.index][b.index]
            if dist_sum < self.best_dist:
                self.best_dist = dist_sum
                self.best_path = path
                self.draw_path(RED)
        self.t2 = time.clock()
        
        # Draw optimal path
        self.draw_path(GREEN)

        # Print complete message
        self.complete()

#------- Helper functions ------------------------------
        
    def complete(self):
        tk.Tk().withdraw()
        messagebox.showinfo('Completed', '  It took ' + str(round(self.t2-self.t1, 3)) + ' seconds to run with ' + str(self.number) + ' cities to visit. \n\n  The optimal path is ' + str(self.best_dist) + ' pixels long.')

    def draw_path(self, color):
        
        # Background
        pygame.draw.rect(self.win, BLACK, SCREEN)

        # Current path
        for city in range(len(self.best_path)-1):
            x_start, y_start = self.best_path[city].x - 1, self.best_path[city].y - 1
            x_end, y_end = self.best_path[city+1].x - 1, self.best_path[city+1].y - 1
            pygame.draw.line(self.win, color, (x_start, y_start), (x_end, y_end), RADIUS-1)

        # Cities
        for city in range(len(self.cities)):
            x, y = self.cities[city].x, self.cities[city].y
            pygame.draw.circle(self.win, WHITE, (x, y), RADIUS)

        # Update display    
        pygame.display.flip()

    def random_points(self):
        
        # City coordinates
        for city in range(self.number):
            x, y = random.randint(RADIUS, WIDTH-RADIUS), random.randint(RADIUS, HEIGHT-RADIUS)
            self.cities.append(City(x, y, city))
            
        # Calculate distance between each node
        for city in range(self.number):
            for neighbor in range(self.number):
                dx, dy = abs(self.cities[city].x - self.cities[neighbor].x), abs(self.cities[city].y - self.cities[neighbor].y)
                self.distance[city][neighbor] = round(math.sqrt(dx ** 2 + dy ** 2))

    def create_text(self, text, x, y):
        text = FONT.render(text, True, WHITE, BLACK)
        rect = text.get_rect()
        rect.center = (x, y)

        rect_padding = pygame.Rect(rect[0]-10, rect[1]-3, rect[2]+20, rect[3]+6)
        pygame.draw.rect(self.win, BLACK, rect_padding)
        self.win.blit(text, rect)

        return text, rect

#------ City object -------------------------------

class City:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        
#------- Main code ------------------------------

def main():
    Calc().run()
    pygame.quit()

os.environ['SDL_VIDEO_CENTERED'] = '1'
main()
