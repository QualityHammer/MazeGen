import pygame as pg


# Pathfinder algorithm
class AStar:

    def __init__(self):
        # Grid that will have cells added to it
        self.grid = []
        self.open_set = []
        self.closed_set = []
        self.start = None
        self.end = None

    def load_grid(self, grid):
        """Loads the grid from a generated maze"""
        self.grid = grid
        for cell in self.grid:
            # cell.falsify_walls()
            cell.get_wall_neighbors(self.grid)
        self.start = self.grid[0]
        self.end = self.grid[-1]
        self.start.current_dist = 0
        self.start.f_dist = heuristic(self.start, self.end)
        self.start.total_dist = self.start.current_dist + self.start.f_dist
        self.open_set.append(self.start)
        self.start.open = True
        return True

    @staticmethod
    def reconstruct(end):
        """Reconstructs the path solution and returns it as a list"""
        current = end
        path = []
        while current.before:
            current.path = True
            current.closed = False
            path.append(current)
            current = current.before
        return path

    def search(self, screen):
        # closest = self.open_set[0]
        t = pg.time.get_ticks()
        while self.open_set:
            # Gets new closest cell
            winner = 0
            for i in range(len(self.open_set)):
                if self.open_set[i].f_dist < self.open_set[winner].f_dist:
                    winner = i
                elif self.open_set[i].f_dist == self.open_set[winner].f_dist:
                    if self.open_set[i].current_dist > self.open_set[winner].current_dist:
                        winner = i
            closest = self.open_set[winner]

            # If the cell is the end then the search is done
            if closest == self.end:
                self.reconstruct(closest)
                print('maze solved in: {}seconds'.format((pg.time.get_ticks() - t) / 1000))

            # Removes cell from open_set and adds to closed_set
            self.open_set.remove(closest)
            closest.open = False
            self.closed_set.append(closest)
            closest.closed = True

            for n in closest.neighbors:
                if n.closed:
                    continue
                # Gets distance from start to neighbor
                temp_dist = closest.current_dist + 1

                # Adds to open_set if not in already
                if n.open:
                    n.current_dist = temp_dist
                else:
                    n.current_dist = temp_dist
                    self.open_set.append(n)
                    n.open = True

                # Updates distance calculations
                n.before = closest
                n.f_dist = heuristic(n, self.end)
                n.total_dist = n.current_dist + n.f_dist
                # Updates cell color
                n.show(screen)

            # Updates cell color
            closest.show(screen)
            pg.display.update()


def heuristic(a, b):
    """Gets the heuristic distance between 2 cells"""
    return abs(a.column - b.column) + abs(a.row - b.row)
