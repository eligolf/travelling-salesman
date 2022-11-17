#----- Imports ------------------------------------------------------------
import random
import math
import time

# Visualization
import os
import contextlib
with contextlib.redirect_stdout(None):
    import pygame

#----- Constants ----------------------------------------------------------

# Visualization
WIDTH = 700
HEIGHT = 600
WIN_WIDTH = WIDTH
WIN_HEIGHT = HEIGHT + 100
RADIUS = 5

pygame.font.init()
FONT = pygame.font.SysFont('Helvetica', 24, bold = True)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# GA
CITIES = 20
POPULATION_SIZE = 1000
MAX_GENERATIONS = 500
ELITE_PLACES = 0.02  # How many percentage of new population to fill with the currently best path
MUTATION_RATE = 0.1

#----- GA functions ----------------------------------------------------------

def init_ga():
    
    # Array of randomly generated cities
    cities = []
    for city in range(CITIES):
        x, y = random.randint(RADIUS, WIDTH-RADIUS), random.randint(RADIUS, HEIGHT-RADIUS)
        cities.append(City(x, y, city))

    # Array of random ways to travel between the cities 
    pop = []    
    for population in range(POPULATION_SIZE):
        pop.append(random.sample(cities, CITIES))

    # Distance between each city
    dist = [[0] * CITIES for _ in range(CITIES)]
    for city in range(CITIES):
        for neighbor in range(CITIES):
            dx, dy = abs(cities[city].x - cities[neighbor].x), abs(cities[city].y - cities[neighbor].y)
            dist[city][neighbor] = round(math.sqrt(dx ** 2 + dy ** 2))

    return pop, dist, cities

def mating_pool(population, fitness):

    # Create a probability vector going from [0, fitness[0], fitness[0] + fitness[1]..... , 1]
    prob_vector = [0]
    for i in range(len(population)):
        prob_vector.append(prob_vector[i] + fitness[i])

    # Create a mating pool with a higher chance of getting high fitness than a low
    matingpool = []
    for i in range(len(population)):
        r = random.uniform(0, 1)
        index = min(range(len(prob_vector)), key=lambda i: abs(prob_vector[i]-r))
        matingpool.append(population[index-1])

    # Add the current best path to the mating pool
    matingpool[0] = population[fitness.index(max(fitness))]
        
    return matingpool

def reproduction(matingpool):

    new_population = []
    for i in range(len(matingpool)):

        # Pick 2 random parents, doesn't matter too much if they occasionally are the same.
        father = random.choice(matingpool)
        mother = random.choice(matingpool)

        # Create a child from the 2 parents, breed/crossover
        child = crossover(father, mother)

        # Mutate the child given a certain mutation rate
        child = mutate(child)

        # Add the child to the new population
        new_population.append(child)

    # Add the current best path to the new_population
    for i in range(0, int(len(matingpool)*ELITE_PLACES)):
        new_population[i] = matingpool[0]

    return new_population

def crossover(a, b):

    # Pick random number of elements from a and fill up with values from b
    r = random.randint(1, len(a))
    temp = []

    for i in range(0, len(b)):
        if b[i] not in a[0:r]:
            temp.append(b[i])

    return a[0:r] + temp

def mutate(child):

    # Only mutate according to mutation rate
    for i in range(len(child)):
        if random.uniform(0, 1) < MUTATION_RATE:
            r1 = random.randint(0, len(child)-1)
            r2 = random.randint(0, len(child)-1)
            
            temp = child[r1]
            child[r1] = child[r2]
            child[r2] = temp
            
    return child

#----- Functions --------------------------------------------------------

def events():
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()

def init_draw(cities):

    # Initialize visualization window
    surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    surface.fill(BLACK)
    for city in range(CITIES):
        x, y = cities[city].x, cities[city].y
        pygame.draw.circle(surface, WHITE, (x, y), RADIUS)

    # Draw lines
    pygame.draw.line(surface, WHITE, (0, HEIGHT+10), (WIDTH+10, HEIGHT+10), 3)

    return surface

def draw_best(win, cities, best_path, distance, generation, surface, gen_log):

    # Initialize window
    win.blit(surface, (0, 0))

    # Draws the current best path in red and best path in the end in green
    color = RED
    if generation == MAX_GENERATIONS-1:
        color = GREEN
    
    for city in range(CITIES-1):
        x_start, y_start = best_path[city].x, best_path[city].y
        x_end, y_end = best_path[city+1].x, best_path[city+1].y
        pygame.draw.line(win, color, (x_start, y_start), (x_end, y_end), RADIUS-3)

    x_start, y_start = best_path[CITIES-1].x, best_path[CITIES-1].y
    x_end, y_end = best_path[0].x, best_path[0].y
    pygame.draw.line(win, color, (x_start, y_start), (x_end, y_end), RADIUS-3)    

    # Print the current best distance
    text = FONT.render('Best: ' + str(distance) + ' pixels from generation ' + str(gen_log[-1]), True, WHITE, BLACK)
    rect = text.get_rect()
    rect.center = (WIN_WIDTH/2, WIN_HEIGHT - 70)
    win.blit(text, rect)

    # Print current generation
    text = FONT.render('Current generation: ' + str(generation), True, WHITE, BLACK)
    rect = text.get_rect()
    rect.center = (WIN_WIDTH/2, WIN_HEIGHT - 40)  
    win.blit(text, rect)
        
    pygame.display.flip()

    
#----- Classes ----------------------------------------------------------

class City:

    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index

        
class Fitness:

    def __init__(self, population, distance, generation, best_dist, best_path, gen_log):
        self.population = population
        self.distance = distance

        self.best_dist = best_dist
        self.best_path = best_path
        self.generation = generation
        self.gen_log = gen_log

        self.best = False

    def fit(self):
        dist, fitness = [], []
        for population in self.population:
            dist_sum = 0
            for city in range(CITIES - 1):
                a, b = population[city], population[city+1]
                dist_sum += self.distance[a.index][b.index]
                
            # If needed to return to home city after city tour
            a, b = population[CITIES-1], population[0]
            dist_sum += self.distance[a.index][b.index]
            
            if dist_sum < self.best_dist:
                self.best_dist = dist_sum
                self.best_path = population
                self.best = True
                
                                
            dist.append(1/dist_sum)

        if self.best:
            self.gen_log.append(self.generation)

        dist_sum = sum(dist)
        for i in range(len(dist)):
            fitness.append(dist[i]/dist_sum)

        return fitness, self.best_dist, self.best_path, self.gen_log
            
#----- Main ----------------------------------------------------------
def main():
    
    # Create CITIES random cities,  generate a random population of POPULATION_SIZE configurations and calculate distance between each city. 
    population, distance, cities = init_ga()

    # Initialize best distance and path
    best_dist = math.inf
    best_path = []

    # Initialize visualization
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    current_generation = 0
    surface = init_draw(cities)
    gen_log = []

    start = time.time()
    for generation in range(MAX_GENERATIONS):

        # Calculate fitness of current population
        fitness, best_dist, best_path, gen_log = Fitness(population, distance, generation, best_dist, best_path, gen_log).fit()
        
        # Create a mating pool
        matingpool = mating_pool(population, fitness)

        # Reproduce to make the new generation 
        population = reproduction(matingpool)

        # Draw everything
        draw_best(win, cities, best_path, best_dist, generation, surface, gen_log)

        # Be able to close window etc
        events()
    end = time.time()
    total_time = (round(end-start, 2))
    print(total_time)

#----- Run ----------------------------------------------------------
os.environ['SDL_VIDEO_CENTERED'] = '1'
main()
