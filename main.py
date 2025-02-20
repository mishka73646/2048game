import pygame
import random
import sys
import json
from os import path

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 400, 500
TILE_SIZE = 100
GRID_PADDING = 10
ANIMATION_SPEED = 20  # Скорость анимации (пикселей за кадр)

# Цвета
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Шрифты
FONT = pygame.font.Font(None, 55)
MENU_FONT = pygame.font.Font(None, 40)
SCORE_FONT = pygame.font.Font(None, 30)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

# Инициализация игрового поля
GRID_SIZE = 4  # По умолчанию
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
animations = []  # Список для хранения анимаций
score = 0
best_score = 0

# Загрузка лучшего результата
if path.exists("best_score.json"):
    with open("best_score.json", "r") as f:
        best_score = json.load(f)

def add_new_tile():
    empty_tiles = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0]
    if empty_tiles:
        i, j = random.choice(empty_tiles)
        grid[i][j] = 2 if random.random() < 0.9 else 4

def draw_grid():
    screen.fill(BACKGROUND_COLOR)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            tile_value = grid[i][j]
            tile_color = TILE_COLORS.get(tile_value, (237, 194, 46))
            pygame.draw.rect(screen, tile_color, (j * TILE_SIZE + GRID_PADDING, i * TILE_SIZE + GRID_PADDING, TILE_SIZE - 2 * GRID_PADDING, TILE_SIZE - 2 * GRID_PADDING))
            if tile_value != 0:
                text_surface = FONT.render(str(tile_value), True, (119, 110, 101))
                text_rect = text_surface.get_rect(center=(j * TILE_SIZE + TILE_SIZE // 2, i * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text_surface, text_rect)

    # Отрисовка счета
    score_text = SCORE_FONT.render(f"Score: {score}", True, (119, 110, 101))
    best_score_text = SCORE_FONT.render(f"Best: {best_score}", True, (119, 110, 101))
    screen.blit(score_text, (10, HEIGHT - 80))
    screen.blit(best_score_text, (10, HEIGHT - 50))

def move_tiles(direction):
    global grid, score, animations
    moved = False
    animations = []

    if direction == "up":
        for j in range(GRID_SIZE):
            for i in range(1, GRID_SIZE):
                if grid[i][j] != 0:
                    row = i
                    while row > 0 and grid[row - 1][j] == 0:
                        grid[row - 1][j] = grid[row][j]
                        grid[row][j] = 0
                        row -= 1
                        moved = True
                    if row > 0 and grid[row - 1][j] == grid[row][j]:
                        grid[row - 1][j] *= 2
                        score += grid[row - 1][j]
                        grid[row][j] = 0
                        moved = True
                        animations.append(((i, j), (row - 1, j), grid[row - 1][j] // 2))
                    elif row != i:
                        animations.append(((i, j), (row, j), grid[row][j]))

    elif direction == "down":
        for j in range(GRID_SIZE):
            for i in range(GRID_SIZE - 2, -1, -1):
                if grid[i][j] != 0:
                    row = i
                    while row < GRID_SIZE - 1 and grid[row + 1][j] == 0:
                        grid[row + 1][j] = grid[row][j]
                        grid[row][j] = 0
                        row += 1
                        moved = True
                    if row < GRID_SIZE - 1 and grid[row + 1][j] == grid[row][j]:
                        grid[row + 1][j] *= 2
                        score += grid[row + 1][j]
                        grid[row][j] = 0
                        moved = True
                        animations.append(((i, j), (row + 1, j), grid[row + 1][j] // 2))
                    elif row != i:
                        animations.append(((i, j), (row, j), grid[row][j]))

    elif direction == "left":
        for i in range(GRID_SIZE):
            for j in range(1, GRID_SIZE):
                if grid[i][j] != 0:
                    col = j
                    while col > 0 and grid[i][col - 1] == 0:
                        grid[i][col - 1] = grid[i][col]
                        grid[i][col] = 0
                        col -= 1
                        moved = True
                    if col > 0 and grid[i][col - 1] == grid[i][col]:
                        grid[i][col - 1] *= 2
                        score += grid[i][col - 1]
                        grid[i][col] = 0
                        moved = True
                        animations.append(((i, j), (i, col - 1), grid[i][col - 1] // 2))
                    elif col != j:
                        animations.append(((i, j), (i, col), grid[i][col]))

    elif direction == "right":
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 2, -1, -1):
                if grid[i][j] != 0:
                    col = j
                    while col < GRID_SIZE - 1 and grid[i][col + 1] == 0:
                        grid[i][col + 1] = grid[i][col]
                        grid[i][col] = 0
                        col += 1
                        moved = True
                    if col < GRID_SIZE - 1 and grid[i][col + 1] == grid[i][col]:
                        grid[i][col + 1] *= 2
                        score += grid[i][col + 1]
                        grid[i][col] = 0
                        moved = True
                        animations.append(((i, j), (i, col + 1), grid[i][col + 1] // 2))
                    elif col != j:
                        animations.append(((i, j), (i, col), grid[i][col]))

    return moved

def check_game_over():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                return False
            if i < GRID_SIZE - 1 and grid[i][j] == grid[i + 1][j]:
                return False
            if j < GRID_SIZE - 1 and grid[i][j] == grid[i][j + 1]:
                return False
    return True

def draw_menu():
    screen.fill(BACKGROUND_COLOR)
    title_text = MENU_FONT.render("2048", True, (119, 110, 101))
    size_3_text = MENU_FONT.render("1 - 3x3", True, (119, 110, 101))
    size_4_text = MENU_FONT.render("2 - 4x4", True, (119, 110, 101))
    size_5_text = MENU_FONT.render("3 - 5x5", True, (119, 110, 101))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(size_3_text, (WIDTH // 2 - size_3_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(size_4_text, (WIDTH // 2 - size_4_text.get_width() // 2, HEIGHT // 2))
    screen.blit(size_5_text, (WIDTH // 2 - size_5_text.get_width() // 2, HEIGHT // 2 + 50))

def draw_game_over():
    screen.fill(BACKGROUND_COLOR)
    game_over_text = MENU_FONT.render("Game Over!", True, (119, 110, 101))
    score_text = MENU_FONT.render(f"Your Score: {score}", True, (119, 110, 101))
    restart_text = MENU_FONT.render("Press R to Restart", True, (119, 110, 101))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

def save_best_score():
    global best_score
    if score > best_score:
        best_score = score
        with open("best_score.json", "w") as f:
            json.dump(best_score, f)

def reset_game():
    global grid, score, animations
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    score = 0
    animations = []
    add_new_tile()
    add_new_tile()

def set_grid_size(size):
    global GRID_SIZE, TILE_SIZE, grid
    GRID_SIZE = size
    TILE_SIZE = WIDTH // GRID_SIZE
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    reset_game()

def main():
    global score, best_score, GRID_SIZE
    reset_game()
    game_state = "menu"  # menu, game, game_over

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        set_grid_size(3)
                        game_state = "game"
                    elif event.key == pygame.K_2:
                        set_grid_size(4)
                        game_state = "game"
                    elif event.key == pygame.K_3:
                        set_grid_size(5)
                        game_state = "game"

            elif game_state == "game":
                if event.type == pygame.KEYDOWN:
                    moved = False
                    if event.key == pygame.K_UP:
                        moved = move_tiles("up")
                    elif event.key == pygame.K_DOWN:
                        moved = move_tiles("down")
                    elif event.key == pygame.K_LEFT:
                        moved = move_tiles("left")
                    elif event.key == pygame.K_RIGHT:
                        moved = move_tiles("right")

                    if moved:
                        add_new_tile()

                    if check_game_over():
                        save_best_score()
                        game_state = "game_over"

            elif game_state == "game_over":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    reset_game()
                    game_state = "game"

        if game_state == "menu":
            draw_menu()
        elif game_state == "game":
            draw_grid()
        elif game_state == "game_over":
            draw_game_over()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()