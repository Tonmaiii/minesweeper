import random
from tile import Tile


class Game:
    def __init__(self, width=30, height=16, mines=99):
        self.width = width
        self.height = height
        self.mines = mines
        self.generate_board()
        self.calculate_values()

    def reveal(self, x, y):
        if self.board[y][x].mine and not self.board[y][x].flag:
            return False
        if self.board[y][x].flag:
            return True
        self.board[y][x].revealed = True
        if self.board[y][x].value == 0:
            for x, y in self.neighbors(x, y):
                if not self.board[y][x].revealed:
                    self.reveal(x, y)
        return True

    def flag(self, x, y):
        # fun boolean logic
        self.board[y][x].flag = not self.board[y][x].revealed and (
            not self.board[y][x].flag or self.flags() >= self.mines
        )

    def reveal_around(self, x, y):
        if (
            self.board[y][x].revealed
            and sum(self.board[j][i].flag for i, j in self.neighbors(x, y))
            == self.board[y][x].value
        ):
            return all(self.reveal(i, j) for i, j in self.neighbors(x, y))
        return True

    def flags(self):
        return sum(tile.flag for row in self.board for tile in row)

    def win(self):
        return all(tile.revealed or tile.mine for row in self.board for tile in row)

    def generate_board(self):
        self.board = [[Tile() for _ in range(self.width)] for _ in range(self.height)]
        self.generate_mines()

    def generate_mines(self):
        flat_board = [tile for row in self.board for tile in row]
        mines = random.sample(flat_board, self.mines)
        for tile in mines:
            tile.mine = True

    def calculate_values(self):
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if tile.mine:
                    continue
                tile.value = sum(self.board[y][x].mine for x, y in self.neighbors(x, y))

    def neighbors(self, x, y):
        return (
            (i, j)
            for i in range(x - 1, x + 2)
            for j in range(y - 1, y + 2)
            if 0 <= i < self.width and 0 <= j < self.height and (i, j) != (x, y)
        )

    def print_board(self):
        for row in self.board:
            print("".join(str(tile) for tile in row))

    def print_revealed(self):
        for row in self.board:
            print("".join(tile.get_display() for tile in row))
