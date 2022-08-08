from game import Game
from random import seed
import curses


WIDTH = 30
HEIGHT = 16
MINES = 99


def main(stdscr: curses.window):
    initialize_colors()
    curses.mousemask(
        curses.BUTTON1_PRESSED
        | curses.BUTTON1_RELEASED
        | curses.BUTTON3_PRESSED
        | curses.BUTTON3_RELEASED
    )
    # seed(0)
    # stdscr.nodelay(True)
    curses.mouseinterval(0)

    while True:
        stdscr.clear()
        game = Game(WIDTH, HEIGHT, MINES)

        left_down = False
        right_down = False

        display_board(stdscr, game)
        stdscr.refresh()

        while True:
            if game.win():
                display_full_board(stdscr, game)
                stdscr.refresh()
                stdscr.addstr(HEIGHT, 0, "You won!")
                break

            key = stdscr.getch()
            if key == curses.KEY_MOUSE:
                _, x, y, _, bstate = curses.getmouse()
                if x in range(0, WIDTH) and y in range(0, HEIGHT):
                    if bstate & curses.BUTTON1_PRESSED:
                        left_down = True
                        if not game.reveal(x, y):
                            break
                    if bstate & curses.BUTTON3_PRESSED:
                        right_down = True
                        game.flag(x, y)

                    if left_down and right_down:
                        if not game.reveal_around(x, y):
                            break

                    if bstate & curses.BUTTON1_RELEASED:
                        left_down = False

                    if bstate & curses.BUTTON3_RELEASED:
                        right_down = False

            if key == 27:
                exit()

            display_board(stdscr, game)
            stdscr.refresh()
        display_full_board(stdscr, game)
        stdscr.addstr(HEIGHT, 0, "Boom!")
        stdscr.refresh()
        while True:
            key = stdscr.getch()
            if key == curses.KEY_MOUSE:
                _, _, _, _, bstate = curses.getmouse()
                if bstate & curses.BUTTON1_PRESSED:
                    break
                if bstate & curses.BUTTON3_PRESSED:
                    break


def display_board(stdscr: curses.window, game: Game):
    for i, row in enumerate(game.board):
        for j, tile in enumerate(row):
            char = tile.get_display()
            if char == " ":
                stdscr.addstr(i, j, char, curses.color_pair(11))
                continue
            if char == ">":
                stdscr.addstr(i, j, char, curses.color_pair(9))
                continue
            if char == "0":
                stdscr.addstr(i, j, " ", curses.color_pair(10))
                continue
            stdscr.addstr(i, j, char, curses.color_pair(int(char)))


def display_full_board(stdscr: curses.window, game: Game):
    for i, row in enumerate(game.board):
        for j, tile in enumerate(row):
            char = str(tile)
            if char == " ":
                stdscr.addstr(i, j, char, curses.color_pair(11))
                continue
            if char == "*":
                stdscr.addstr(i, j, char, curses.color_pair(9))
                continue
            if char == "0":
                stdscr.addstr(i, j, " ", curses.color_pair(10))
                continue
            stdscr.addstr(i, j, char, curses.color_pair(int(char)))


def initialize_colors():
    curses.init_pair(1, 9, 7)
    curses.init_pair(2, 2, 7)
    curses.init_pair(3, 12, 7)
    curses.init_pair(4, 1, 7)
    curses.init_pair(5, 4, 7)
    curses.init_pair(6, 3, 7)
    curses.init_pair(7, 0, 7)
    curses.init_pair(8, 8, 7)

    curses.init_pair(9, 12, 8)
    curses.init_pair(10, 15, 7)
    curses.init_pair(11, 15, 8)


curses.wrapper(main)
