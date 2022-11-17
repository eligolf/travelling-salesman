# Travelling Salesperson
The travelling salesperson is a mathematical problem where the following is asked: "Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city?". The problem is described further here: https://en.wikipedia.org/wiki/Travelling_salesman_problem

# Showcase
Below is a video showcasing the process of the genetic algorithm. It starts from a random tour of the cities and then through "evolution" and mutations it finds better tours until it reaches the end generation. It doesn't always find the optimum, sometimes it gets stuck in a local optimum. By tweaking population size, mutation rate and other parameters you can try to get an better result. The showcase below is for 20 randomly placed cities which is around the limit of what the current code can handle on my machine. 



# The repo
In this repository you find two different apporaches of solving the problem; the brute force method and using a genetic algorithm. The first one checks all possible combinations while the other uses a random start state and then "genetically" gets better each iteration from mutations. Read more in the attached "Process.png" about the genetic algorithm process. 

