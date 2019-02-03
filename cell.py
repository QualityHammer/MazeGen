from settings import *
import numpy as np
import pygame as pg


class Cell:

    def __init__(self, column, row):
        # Grid list pos
        self.column = column
        self.row = row
        # Screen pos
        self.x = self.column * CW
        self.y = self.row * CW
        # Top, Right, Bottom, Left
        self.walls = [True, True, True, True]
        self.visited = False
        self.in_stack = False
        # List of valid neighbors
        self.neighbors = []
        # The cell that came before this in A* path finding
        self.before = None
        # Distance from start to this cell
        self.current_dist = None
        # Distance from this cell to the end
        self.f_dist = None
        # Current_dist plus f_dist
        self.total_dist = None
        # Bools for if cell is in open_set or closed_set
        self.open = False
        self.closed = False
        self.path = False

    def __eq__(self, other):
        """Returns true if the cells are the same"""
        return self.column == other.column and self.row == other.row

    def falsify_walls(self):
        """Debug function to test path finding by removing all walls"""
        self.walls = [False, False, False, False]

    def set_walls(self, walls):
        """Sets walls when loading maze"""
        self.walls = walls

    def check_neighbors(self):
        """Picks a random neighbor from the grid"""
        valid = []
        for n in self.neighbors:
            neighbor_push(valid, n)

        if len(valid) > 0:
            return np.random.choice(valid)
        else:
            return False

    def get_neighbors(self, grid):
        """Gets all valid neighbors from the grid"""
        top = index(self.column, self.row - 1)
        right = index(self.column + 1, self.row)
        bottom = index(self.column, self.row + 1)
        left = index(self.column - 1, self.row)
        sides = [top, right, bottom, left]
        for side in sides:
            if side:
                self.neighbors.append(grid[side])

    def get_wall_neighbors(self, grid):
        """Gets all valid neighbors considering wall limits"""
        self.neighbors = []
        sides = []
        if not self.walls[0]:
            top = index(self.column, self.row - 1)
            sides.append(top)
        if not self.walls[1]:
            right = index(self.column + 1, self.row)
            sides.append(right)
        if not self.walls[2]:
            bottom = index(self.column, self.row + 1)
            sides.append(bottom)
        if not self.walls[3]:
            left = index(self.column - 1, self.row)
            sides.append(left)
        for side in sides:
            if side:
                self.neighbors.append(grid[side])

    def highlight(self, screen):
        """Highlights the cell in blue"""
        blue_rect = pg.Surface((CW, CW))
        blue_rect.set_alpha(100)
        blue_rect.fill(BLUE)
        screen.blit(blue_rect, (self.x, self.y))

    def show(self, screen):
        """Function to be called in draw"""
        # Maze gen
        if show_path:
            if self.in_stack:
                yellow_rect = pg.Surface((CW, CW))
                yellow_rect.set_alpha(100)
                yellow_rect.fill(YELLOW)
                screen.blit(yellow_rect, (self.x, self.y))
            if self.visited and not self.in_stack:
                purp_rect = pg.Surface((CW, CW))
                purp_rect.set_alpha(100)
                purp_rect.fill(PURPLE)
                screen.blit(purp_rect, (self.x, self.y))
        elif self.visited:
            purp_rect = pg.Surface((CW, CW))
            purp_rect.set_alpha(100)
            purp_rect.fill(PURPLE)
            screen.blit(purp_rect, (self.x, self.y))

        # A*
        if self.path:
            green_rect = pg.Surface((CW, CW))
            green_rect.set_alpha(170)
            green_rect.fill(GREEN)
            screen.blit(green_rect, (self.x, self.y))
        elif self.open:
            pg.draw.rect(screen, GREEN, (self.x, self.y, CW, CW))
        elif self.closed:
            pg.draw.rect(screen, RED, (self.x, self.y, CW, CW))

        # Lines
        if self.walls[0]:
            pg.draw.line(screen, WHITE, (self.x, self.y), (self.x + CW, self.y))
        if self.walls[1]:
            pg.draw.line(screen, WHITE, (self.x + CW, self.y), (self.x + CW, self.y + CW))
        if self.walls[2]:
            pg.draw.line(screen, WHITE, (self.x + CW, self.y + CW), (self.x + CW, self.y + CW))
        if self.walls[3]:
            pg.draw.line(screen, WHITE, (self.x, self.y + CW), (self.x, self.y))


def neighbor_push(neighbors: list, cell: Cell):
    """If the neighbor exists and isn't visited, then it's added to the list"""
    if cell and not cell.visited:
        neighbors.append(cell)


def index(col, row):
    """Returns the position in a list from column and row numbers"""
    if col < 0 or row < 0 or col > COLS - 1 or row > ROWS - 1:
        return False
    return row + col * COLS
