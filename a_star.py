"""
TO IMPROVE IMAGE SCANNING ACCURACY:
- increase rows (~ line 246, a_star.py)
- increase array values (~ line 7, image_det.py)
"""

import pygame
import random
from image_det import *
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* Path Finding Algorithm')

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows
    
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.colour == RED

    def is_open(self):
        return self.colour == GREEN
    
    def is_barrier(self):
        return self.colour == BLACK
    
    def is_start(self):
        return self.colour == ORANGE
    
    def is_end(self):
        return self.colour == TURQUOISE
    
    def reset(self):
        self.colour = WHITE    # (=) or (==) ?

    def make_closed(self):
        self.colour = RED

    def make_open(self):
        self.colour = GREEN

    def make_barrier(self):
        self.colour = BLACK

    def make_start(self):
        self.colour = ORANGE

    def make_end(self):
        self.colour = TURQUOISE

    def make_path(self):
        self.colour = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False
    

def calculate_f(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, start, current, draw):
    end = current
    while current in came_from:
        # set current to current element in came_from, which points to previous value (where current came from)
        current = came_from[current]
        current.make_path()
        draw()
    start.colour = ORANGE
    end.colour = TURQUOISE


def algorithm(draw, grid, start, end):
    count = 0

    # efficient way to get smallest element of queue
    open_set = PriorityQueue()

    # start node put into open set
    open_set.put((0, count, start)) 

    # from where nodes were accessed
    came_from = {} 

    # g score: shortest distance from start current node
    # set all nodes to inf g_score
    g_score = {spot: float("inf") for row in grid for spot in row} 

    # start node g_score as 0
    g_score[start] = 0 

    # f score: estimated distance from start to end
    f_score = {spot: float("inf") for row in grid for spot in row}

    try:
        f_score[start] = calculate_f(start.get_pos(), end.get_pos())
    except AttributeError:
        print("Attempted to run without start and end node")
        return
    
    # helps to see if node is in open set
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # get node associated with smallest element
        current = open_set.get()[2]

        # remove from hash
        open_set_hash.remove(current)

        # found path
        if current == end:
            reconstruct_path(came_from, start, end, draw)
            return True
        
        # consider all neighbours of current node
        for neighbour in current.neighbours:
            # +1 because we've moved over 1 node away from start
            temp_g_score = g_score[current] + 1

            # if found better path, new node is now current and add to hash if not already present
            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + calculate_f(neighbour.get_pos(), end.get_pos())

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)

                    if neighbour != end:
                        neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width, clear_all = False, clear_path = False, draw_barriers = False, randoms = False):
    win.fill(WHITE)

    if randoms:
        for row in grid:
            for node in row:
                if not (node.colour == ORANGE or node.colour == TURQUOISE):
                    random_colour = random.randint(1,3) # 1 or 2
                    if random_colour == 1:
                        node.colour = BLACK
                    else:
                        node.colour = WHITE

    elif draw_barriers:
        set_width(WIDTH)
        for row in grid:
            for node in row:
                if not (node.colour == ORANGE or node.colour == TURQUOISE):
                    get_colour = get_pixel_colour(node.x, node.y)
                    node.colour = get_colour
    else:
        for row in grid:
            for node in row:
                if not clear_all:
                    node.draw(win)

                    if clear_path and (node.colour == RED or node.colour == GREEN or node.colour == PURPLE):
                        node.colour = WHITE
                elif clear_all:
                    node.colour = WHITE


    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_position(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col


def main(win, width):
    rows = 50     # set to factors of WIDTH (originally 50)
    grid = make_grid(rows, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, rows, width)

                try:
                    spot = grid[row][col]
                except IndexError:
                    print("Attempted to draw outside of frame")

                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, rows, width)

                try:
                    spot = grid[row][col]
                except IndexError:
                    print("Attempted to draw outside of frame")
                spot.reset()

                if spot == start:
                    start = None
                if spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and not started:
                    draw(win, grid, rows, width, clear_all=True)
                    start = None
                    end = None

                if event.key == pygame.K_SPACE and not started:
                    draw(win, grid, rows, width, clear_path=True)
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)
                    algorithm(lambda: draw(win, grid, rows, width), grid, start, end)
                
                if event.key == pygame.K_RETURN and not started:
                    draw(win, grid, rows, width, draw_barriers=True)

                if event.key == pygame.K_r and not started:
                    draw(win, grid, rows, width, randoms=True)
                    
    pygame.quit()


if __name__ == "__main__":
    main(WIN, WIDTH)