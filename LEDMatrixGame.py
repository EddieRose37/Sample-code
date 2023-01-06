from time import sleep
from tkinter import Tk, Label, Entry
import unicornhathd as hat

hat.brightness(0.5)
hat.enable_addressing()
hat.setup_buffer(16, 16)
hat.setup_display(0, 0, 0, 0)

mode = None
while not mode in ['8x8', '16x16']:
    mode = input('8x8 or 16x16 grid? ')

mode = int(mode.split('x')[0])

def key(event):
    global up, down, left, right, main
    if event.keysym == 'Up':
        up = True

    elif event.keysym == 'Down':
        down = True

    elif event.keysym == 'Left':
        left = True

    elif event.keysym == 'Right':
        right = True

    elif event.keysym == 'Return':
        main = True

    elif event.keysym == 'q':
        root.destroy()

root = Tk()
root.bind_all('<Key>', key)

cols = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255), "yellow": (255, 255, 0), "cyan": (0, 255, 255), "purple": (255, 0, 255)}
white = cols["white"]
black = cols["black"]
red = cols["red"]
green = cols["green"]
blue = cols["blue"]
yellow = cols["yellow"]
cyan = cols["cyan"]
purple = cols["purple"]

if mode == 8:
    def set_block(x, y, col):
        x = x * 2
        y = y * 2
        hat.set_pixel(x, y, col[0], col[1], col[2])
        hat.set_pixel(x+1, y, col[0], col[1], col[2])
        hat.set_pixel(x, y+1, col[0], col[1], col[2])
        hat.set_pixel(x+1, y+1, col[0], col[1], col[2])
else:
    def set_block(x, y, col):
        hat.set_pixel(x, y, col[0], col[1], col[2])


def display_grid(col1=(0, 255, 0), col2=(0, 0, 255)):
    var = True
    for x in range(mode):
        for y in range(mode):
            if var:
                col = col1
                var = False
            else:
                col = col2
                var = True
            set_block(x, y, col)
        if var:
            var = False
        else:
            var = True
    hat.show()

up, down, left, right, main = False, False, False, False, False
running = True
winner = None
players = [input("Player 1: "), input("Player 2: ")]
running = True
game_count = 0
game_count_data = ["first", "second", "third"]

grid = []
for x in range(mode):
    row = []
    for y in range(mode):
        row.append(0)
    grid.append(row)

def clear_board():
    hat.clear()

    for x in range(mode):
        for y in range(mode):
            sqr = grid[x][y]
            if sqr == 1:
                set_block(x, y, cyan)

            elif sqr == 2:
                set_block(x, y, yellow)

            elif sqr == 3:
                set_block(x, y, red)

while running:
    previous = [[0, 0], [mode-1, mode-1]]

    while winner == None:
        col = data[1]
        x, y = previous[data[0]][0], previous[data[0]][1]

        for data in [[0, blue, 0, 1, mode-1], [1, green, mode-1, 2, 0]]:
            previous[data[0]] = [x, y]

            if up:
                if y < mode-1:
                    y += 1
                up = False

            elif down:
                if y > 0:
                    y -= 1
                down = False

            elif left:
                if x > 0:
                    x -= 1
                left = False

            elif right:
                if x < mode-1:
                    x += 1
                right = False

            elif main:
                if grid[x][y] == 0:
                    if y == data[2]:
                        grid[x][y] = data[3]
                        col = purple
                    else:
                        try:
                            _x, _y = False, False
                            for _x in [x-1, x, x+1]:
                                if not _x in [-1, mode]:
                                    for _y in [y-1, y, y+1]:
                                        if not _y in [-1, mode]:
                                            if grid[_x][_y] == data[3]:
                                                grid[x][y] = data[3]
                                                col = purple
                                            if y == data[4]:
                                                winner = players[data[0]]
                        except Exception as error:
                            print(error)
                    main = False

            clear_board()
            set_block(x, y, col)
            hat.show()
            root.update()

            sleep(0.2)

    for x in range(mode):
        for y in range(mode):
            if grid[x][y] in [1, 2]:
                grid[x][y] = 3

    if not len(game_count_data) == game_count:
        print("Congratulations {0}! You won the {1} game!".format(winner, game_count_data[game_count]))
    else:
        print("Congratulations {0}! You won game no.{1}!".format(winner, game_count))

    game_count += 1
    winner = None
    ans = None
    answers = ["Y", "N"]

    while not ans in answers:
        ans = input("Do you want to play again? (Y/N) ").upper()

    running = [True, False][answers.index(ans)]