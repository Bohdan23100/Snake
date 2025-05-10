import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

score = 0
block_size = 20
snake = [(100, 100), (80, 100), (60, 100)]
x_snake = block_size
y_snake = 0
font = pygame.font.Font(None, 36)
# Центр керування
center_x = WIDTH // 2
bottom_y = HEIGHT - 60

button_up    = pygame.Rect(center_x - 30, bottom_y - 90, 60, 40)  # Вгору
button_left  = pygame.Rect(center_x - 90, bottom_y - 30, 60, 40)  # Вліво
button_down  = pygame.Rect(center_x - 30, bottom_y - 30, 60, 40)  # Вниз
button_right = pygame.Rect(center_x + 30, bottom_y - 30, 60, 40)  # Вправо
button_surface = pygame.Surface((button_up.width, button_up.height))
button_surface.set_alpha(128)  # Прозорість від 0 (повністю прозоро) до 255 (непрозорість)
button_surface.fill((100, 100, 100))  # Колір кнопки\


def draw_snake(snake):
    for x, y in snake:
        pygame.draw.rect(screen, (255, 255, 255), (x, y, block_size, block_size))

def random_apple():
    return (
        random.randint(0, (WIDTH - block_size) // block_size) * block_size,
        random.randint(0, (HEIGHT - block_size) // block_size) * block_size
    )

apple = random_apple()
game_over = False

# Кнопка "Restart"
button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 40, 120, 40)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_up.collidepoint(mouse_pos):
                y_snake = -block_size
                x_snake = 0
            elif button_left.collidepoint(mouse_pos):
                x_snake = -block_size
                y_snake = 0
            elif button_down.collidepoint(mouse_pos):
                y_snake = block_size
                x_snake = 0
            elif button_right.collidepoint(mouse_pos):
                x_snake = block_size
                y_snake = 0

        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP and y_snake == 0:
                    y_snake = -block_size
                    x_snake = 0
                elif event.key == pygame.K_DOWN and y_snake == 0:
                    y_snake = block_size
                    x_snake = 0
                elif event.key == pygame.K_RIGHT and x_snake == 0:
                    x_snake = block_size
                    y_snake = 0
                elif event.key == pygame.K_LEFT and x_snake == 0:
                    x_snake = -block_size
                    y_snake = 0
            else:
                if event.key == pygame.K_SPACE:
                    # Скидання гри
                    snake = [(100, 100), (80, 100), (60, 100)]
                    x_snake = block_size
                    y_snake = 0
                    apple = random_apple()
                    score = 0
                    game_over = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    # Скидання гри
                    snake = [(100, 100), (80, 100), (60, 100)]
                    x_snake = block_size
                    y_snake = 0
                    apple = random_apple()
                    score = 0
                    game_over = False

    if not game_over:
        screen.fill((0, 0, 0))

        # Рух змійки
        x, y = snake[0]
        x += x_snake
        y += y_snake
        snake.insert(0, (x, y))

        # Перевірка на зіткнення
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or (x, y) in snake[1:]:
            game_over = True

        # Перевірка на яблуко
        snake_rect = pygame.Rect(x, y, block_size, block_size)
        apple_rect = pygame.Rect(apple[0], apple[1], block_size, block_size)

        if snake_rect.colliderect(apple_rect):
            apple = random_apple()
            score += 1
        else:
            snake.pop()

        # Малювання
        pygame.draw.rect(screen, (255, 0, 0), (apple[0], apple[1], block_size, block_size))
        draw_snake(snake)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))


        # Малювання кнопок
        screen.blit(button_surface, button_up.topleft)
        screen.blit(button_surface, button_left.topleft)
        screen.blit(button_surface, button_down.topleft)
        screen.blit(button_surface, button_right.topleft)

        # Стрілки (після кнопок!)
        button_text_up = font.render("^", True, (0, 0, 255))
        button_text_left = font.render("<", True, (0, 0, 255))
        button_text_down = font.render("v", True, (0, 0, 255))
        button_text_right = font.render(">", True, (0, 0, 255))

        screen.blit(button_text_up, (button_up.x + 15, button_up.y + 5))
        screen.blit(button_text_left, (button_left.x + 15, button_left.y + 5))
        screen.blit(button_text_down, (button_down.x + 15, button_down.y + 5))
        screen.blit(button_text_right, (button_right.x + 15, button_right.y + 5))



    else:
        screen.fill((255, 0, 0))
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 40))
        screen.blit(score_text, (WIDTH // 2 - 60, HEIGHT // 2 + 10))

        # Малювання кнопки
        pygame.draw.rect(screen, (255, 255, 255), button_rect)  # білий прямокутник
        restart_text = font.render("Restart", True, (0, 0, 0))  # чорний текст
        screen.blit(restart_text, (button_rect.x + 20, button_rect.y + 10))

    pygame.display.update()
    pygame.time.delay(100)
