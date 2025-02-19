from random import randint
from typing import Optional
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Базовый класс игрового объекта"""

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)) -> None:
        """Инициализация игрового объекта"""
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Базовый метод отрисовки для переопределения"""
        pass


class Apple(GameObject):
    """Класс объекта Яблоко"""

    def __init__(self) -> None:
        """Инициализация объекта яблока"""
        super().__init__(body_color=APPLE_COLOR)
        self.position = self.randomize_position()
        self.draw()

    def randomize_position(self) -> None:
        """Рандомизация позиции яблока"""
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self) -> None:
        """Отрисовка яблока на поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс объекта Змейка"""

    def __init__(self):
        """Инициализация змейки"""
        super().__init__(
            position=(
                GRID_WIDTH // 2 * GRID_SIZE,
                GRID_HEIGHT // 2 * GRID_SIZE
            ),
            body_color=SNAKE_COLOR
        )
        self.length: int = 1
        self.positions: list[tuple[int, int]] = [self.position]
        self.next_direction: Optional[tuple[int, int]] = None
        self.direction: tuple[int, int] = RIGHT

    def update_direction(self):
        """Обновление направления движения"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовка змейки"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last() != self.get_head_position():
            last_rect = pygame.Rect(self.last(), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self) -> None:
        """Перемещение змейки"""
        dx, dy = self.direction
        new_head: tuple[int, int] = (
            (self.positions[0][0] + dx * GRID_SIZE) % SCREEN_WIDTH,
            (self.positions[0][1] + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.update_direction()
        self.positions.insert(0, new_head)
        self.draw()
        self.positions.pop()

    def get_head_position(self):
        """Получить координаты головы змейки"""
        return self.positions[0]

    def last(self):
        """Получить координаты хвоста змейки"""
        return self.positions[-1]

    def grow(self):
        """Увеличение размера змейки"""
        self.length += 1
        self.positions.append(self.last())
        self.move()

    def reset(self):
        """Сброс размера змейки до 1"""
        self.positions = [self.position]
        self.length = 1


def handle_keys(game_object):
    """Функция обработки нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция игры"""
    # Инициализация PyGame:
    pygame.init()
    apple: Apple = Apple()
    snake: Snake = Snake()

    # Избегаем того, чтобы яблоко спавнилось на змейке
    while apple.position == snake.get_head_position():
        apple.position = apple.randomize_position()

    apple.draw()
    snake.draw()

    pygame.display.update()

    # Основной игровой цикл
    while True:
        clock.tick(SPEED)

        # Обработка нажатий клавиш
        handle_keys(snake)

        # Проверка на съеденное яблоко
        if snake.get_head_position() == apple.position:
            snake.grow()
            while apple.position in snake.positions:
                apple.position = apple.randomize_position()
            apple.draw()
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.draw()
            apple.draw()
            snake.move()
        else:
            snake.move()

        # Обновление экрана
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()