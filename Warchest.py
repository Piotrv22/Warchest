import pygame
import sys
import numpy as np

# Inicjalizacja biblioteki Pygame
pygame.init()

# Ustawienia okna
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

# Kolory
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Tworzenie okna
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Kółko i krzyżyk')
screen.fill(BG_COLOR)

# Tworzenie planszy
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Rysowanie linii planszy
def draw_lines():
    # Pionowe linie
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    # Poziome linie
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)

# Rysowanie kół i krzyżyków
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

# Wpisywanie wartości do planszy
def mark_square(row, col, player):
    board[row][col] = player

# Sprawdzanie, czy plansza jest pełna
def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True

# Sprawdzanie, czy jest zwycięzca
def check_win(player):
    # Sprawdzanie wierszy
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_win_line(row, 0, row, 2)
            return True
    # Sprawdzanie kolumn
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_win_line(0, col, 2, col)
            return True
    # Sprawdzanie przekątnych
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_win_line(0, 0, 2, 2)
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        draw_win_line(0, 2, 2, 0)
        return True
    return False

# Rysowanie linii zwycięstwa
def draw_win_line(row1, col1, row2, col2):
    pygame.draw.line(screen, (255, 0, 0), (col1 * SQUARE_SIZE + SQUARE_SIZE // 2, row1 * SQUARE_SIZE + SQUARE_SIZE // 2), (col2 * SQUARE_SIZE + SQUARE_SIZE // 2, row2 * SQUARE_SIZE + SQUARE_SIZE // 2), WIN_LINE_WIDTH)

# Restart gry
def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

draw_lines()

# Pętla gry
player = 1
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)
                if board[clicked_row][clicked_col] == 0:
                    mark_square(clicked_row, clicked_col, player)
                    if check_win(player):
                        game_over = True
                    else:
                        if is_board_full():
                            game_over = True
                        else:
                            player = player % 2 + 1
                    draw_figures()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 1
                game_over = False

    pygame.display.update()
