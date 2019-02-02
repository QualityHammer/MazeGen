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

    def set_walls(self, walls):
        self.walls = walls

    def check_neighbors(self, grid):
        """Picks a random neighbor from the grid"""
        neighbors = []

        sides = [
            grid[index(self.column, self.row - 1)],       # TOP
            grid[index(self.column + 1, self.row)],     # RIGHT
            grid[index(self.column, self.row + 1)],     # BOTTOM
            grid[index(self.column - 1, self.row)]      # LEFT
        ]
        for side in sides:
            neighbor_push(neighbors, side)

        if len(neighbors) > 0:
            return np.random.choice(neighbors)
        else:
            return False

    def highlight(self, screen):
        """Highlights the cell in blue"""
        blue_rect = pg.Surface((CW, CW))
        blue_rect.set_alpha(100)
        blue_rect.fill(BLUE)
        screen.blit(blue_rect, (self.x, self.y))

    def show(self, screen):
        """Function to be called in draw"""
        if self.walls[0]:
            pg.draw.line(screen, WHITE, (self.x, self.y), (self.x + CW, self.y))
        if self.walls[1]:
            pg.draw.line(screen, WHITE, (self.x + CW, self.y), (self.x + CW, self.y + CW))
        if self.walls[2]:
            pg.draw.line(screen, WHITE, (self.x + CW, self.y + CW), (self.x + CW, self.y + CW))
        if self.walls[3]:
            pg.draw.line(screen, WHITE, (self.x, self.y + CW), (self.x, self.y))

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


def neighbor_push(neighbors: list, cell: Cell):
    """If the neighbor exists and isn't visited, then it's added to the list"""
    if cell and not cell.visited:
        neighbors.append(cell)


def index(col, row):
    """Returns the position in a list from column and row numbers"""
    if col < 0 or row < 0 or col > COLS - 1 or row > ROWS - 1:
        return False
    return row + col * COLS
