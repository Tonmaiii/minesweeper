class Tile:
    def __init__(self, mine=False):
        self.mine = mine
        self.revealed = False
        self.value = None
        self.flag = False

    def __str__(self):
        if self.mine:
            return "*"
        return str(self.value)

    def get_display(self):
        return ">" if self.flag else str(self) if self.revealed else " "
