from settings import *


class Board:
    def __init__(self):
        self.grid = [
            [EMPTY for _ in range(GRID_SIZE)]
            for _ in range(GRID_SIZE)
        ]

    def can_place(self, piece, gx, gy):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):

                if not cell:
                    continue

                bx = gx + x
                by = gy + y

                if bx < 0 or by < 0:
                    return False

                if bx >= GRID_SIZE or by >= GRID_SIZE:
                    return False

                if self.grid[by][bx] == FILLED:
                    return False

        return True

    def place_piece(self, piece, gx, gy):
        blocks = 0

        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):

                if cell:
                    self.grid[gy + y][gx + x] = FILLED
                    blocks += 1

        cleared = self.clear_lines()

        return blocks, cleared

    def clear_lines(self):
        full_rows = []
        full_cols = []

        for y in range(GRID_SIZE):
            if all(self.grid[y]):
                full_rows.append(y)

        for x in range(GRID_SIZE):
            if all(self.grid[y][x] for y in range(GRID_SIZE)):
                full_cols.append(x)

        for y in full_rows:
            self.grid[y] = [EMPTY] * GRID_SIZE

        for x in full_cols:
            for y in range(GRID_SIZE):
                self.grid[y][x] = EMPTY

        return len(full_rows) + len(full_cols)

    def has_moves(self, pieces):
        for piece in pieces:
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    if self.can_place(piece, x, y):
                        return True

        return False