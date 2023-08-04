import pygame
import sys
import random
import pygame_gui

# Konstansok a tábla méretéhez és a cellák méretéhez
SCREEN_SIZE = 900
GRID_SIZE = 30
CELL_SIZE = SCREEN_SIZE // GRID_SIZE

# Színek
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Inicializáljuk a Pygame-t
pygame.init()

# Ablak létrehozása
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('Tic-Tac-Toe')

# Új játéktábla inicializálása
board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Ellenőrzi, hogy a tábla megtelt-e
def is_board_full(board):
    return all(all(cell != ' ' for cell in row) for row in board)

# Ellenőrzi a nyerő állapotot
def check_winner(board, player):
    # Vízszintes és függőleges ellenőrzés
    for i in range(GRID_SIZE):
        if all(board[i][j] == player for j in range(GRID_SIZE)):
            return True
        if all(board[j][i] == player for j in range(GRID_SIZE)):
            return True
    # Átlós ellenőrzés
    if all(board[i][i] == player for i in range(GRID_SIZE)):
        return True
    if all(board[i][GRID_SIZE - 1 - i] == player for i in range(GRID_SIZE)):
        return True
    return False

# Ellenőrzi, hogy a megadott lépéssel a megadott játékos nyer-e
def is_winning_move(board, row, col, player):
    temp_board = [row[:] for row in board]
    temp_board[row][col] = player
    return check_winner(temp_board, player)

# Robot lépése könnyű fokozatban (véletlenszerűen)
def robot_move_easy(board):
    empty_cells = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE) if board[row][col] == ' ']
    if empty_cells:
        return random.choice(empty_cells)
    return None

# Robot lépése nehéz fokozatban (logikusan)
def robot_move_hard(board):
    # (Az előző robot_move() tartalma)
    pass

# Játék ciklus
def main():
    turn = 'X'
    running = True

    # Inicializáljuk a gombokhoz szükséges GUI-t
    pygame_gui.init()
    gui_manager = pygame_gui.UIManager((SCREEN_SIZE, SCREEN_SIZE))

    # Könnyű nehézségi gomb
    easy_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 10), (100, 50)), text='Könnyű', manager=gui_manager)
    
    # Nehéz nehézségi gomb
    hard_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 10), (100, 50)), text='Nehéz', manager=gui_manager)

    robot_move_func = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Gomb események kezelése
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == easy_button:
                        robot_move_func = robot_move_easy
                    elif event.ui_element == hard_button:
                        robot_move_func = robot_move_hard

            # Kezeljük az UI eseményeket
            gui_manager.process_events(event)

        # Rajzolás
        screen.fill(WHITE)

        for x in range(0, SCREEN_SIZE, CELL_SIZE):
            pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_SIZE))
            pygame.draw.line(screen, BLACK, (0, x), (SCREEN_SIZE, x))

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                center_x = col * CELL_SIZE + CELL_SIZE // 2
                center_y = row * CELL_SIZE + CELL_SIZE // 2
                if board[row][col] == 'X':
                    pygame.draw.line(screen, BLACK, (center_x - 10, center_y - 10), (center_x + 10, center_y + 10))
                    pygame.draw.line(screen, BLACK, (center_x + 10, center_y - 10), (center_x - 10, center_y + 10))
                elif board[row][col] == 'O':
                    pygame.draw.circle(screen, BLACK, (center_x, center_y), 10)

        gui_manager.update(1/60)
        gui_manager.draw_ui(screen)

        pygame.display.flip()

        if check_winner(board, 'X'):
            print("Játékos X nyert!")
            running = False
        elif check_winner(board, 'O'):
            print("Játékos O nyert!")
            running = False
        elif is_board_full(board):
            print("Döntetlen!")
            running = False

        # Robot lépése
        if turn == 'O' and not check_winner(board, 'X') and not check_winner(board, 'O') and robot_move_func is not None:
            row, col = robot_move_func(board)
            if row is not None and col is not None:
                board[row][col] = turn
                turn = 'X'

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
