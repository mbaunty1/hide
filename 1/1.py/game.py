import pygame
import sys
import random
import math

class HideAndSeekGame:
    def __init__(self):
        pygame.init()

        # Налаштування екрану
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Хованки: Знайди фігуру")

        # Ініціалізація шрифта
        self.font = pygame.font.Font(None, 36)

        # Налаштування рівнів
        self.level = 1
        self.objects_per_level = 5  # Кількість об'єктів на рівень
        # Список кольорів, з яких будуть вибиратися кольори для фігур
        self.colors = [(196, 98, 193), (199, 26, 78), (115, 217, 184), (183, 217, 115)]

        # Випадковий вибір мети (фігури, яку треба знайти)
        self.target_shape = random.choice(["square", "circle", "triangle", "star", "diamond"])

        # Показати гравцю фігуру
        self.show_target_shape()

        # Генерація об'єктів
        self.objects = []
        self.generate_objects()

        # Таймер і рахунок
        self.start_time = pygame.time.get_ticks()

        # Основні змінні гри
        self.running = True
        self.clock = pygame.time.Clock()

    def show_target_shape(self):
        """Показати фігуру, яку потрібно знайти, і дочекатися натискання кнопки ОК"""
        waiting_for_ok = True
        while waiting_for_ok:
            self.screen.fill((255, 255, 255))

            # Вивести текст і фігуру
            target_color = random.choice(self.colors)
            x, y = self.screen_width // 2 - 50, self.screen_height // 2 - 50

            if self.target_shape == "square":
                pygame.draw.rect(self.screen, target_color, (x, y, 100, 100))
            elif self.target_shape == "circle":
                pygame.draw.circle(self.screen, target_color, (x + 50, y + 50), 50)
            elif self.target_shape == "triangle":
                points = [(x, y + 100), (x + 50, y), (x + 100, y + 100)]
                pygame.draw.polygon(self.screen, target_color, points)
            elif self.target_shape == "star":
                self.draw_star(x, y, target_color)
            elif self.target_shape == "diamond":
                points = [(x, y + 50), (x + 50, y), (x + 100, y + 50), (x + 50, y + 100)]
                pygame.draw.polygon(self.screen, target_color, points)

            # Показати текст
            instruction_text = self.font.render("Натисніть ОК, щоб почати", True, (0, 0, 0))
            self.screen.blit(instruction_text, (self.screen_width // 2 - instruction_text.get_width() // 2, self.screen_height // 2 + 120))

            pygame.display.flip()

            # Перевірка на натискання ОК
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting_for_ok = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Ліва кнопка миші
                    waiting_for_ok = False

    def generate_objects(self):
        """Генерація об'єктів для рівня"""
        self.objects = []

        for _ in range(self.objects_per_level):
            x = random.randint(0, self.screen_width - 50)
            y = random.randint(0, self.screen_height - 50)

            random_shape = random.choice(["square", "circle", "triangle", "star", "diamond"])  # Додано нові фігури
            random_color = random.choice(self.colors)

            self.objects.append((random_shape, random_color, (x, y)))

        # Додаємо обрану фігуру як мету (ціль)
        x = random.randint(0, self.screen_width - 50)
        y = random.randint(0, self.screen_height - 50)
        random_color = random.choice(self.colors)
        self.objects.append((self.target_shape, random_color, (x, y), True))

    def run_game(self):
        """Основний цикл гри"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Ліва кнопка миші
                    self.check_click(event.pos)

            self.draw_objects()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def check_click(self, position):
        """Перевірка на клік по фігурі"""
        for obj in self.objects:
            shape, color, pos, *rest = obj
            x, y = pos

            if shape == "square":
                rect = pygame.Rect(x, y, 50, 50)
                if rect.collidepoint(position):
                    self.next_level()
                    return

            elif shape == "circle":
                center = (x + 25, y + 25)
                if ((position[0] - center[0]) ** 2 + (position[1] - center[1]) ** 2) <= 25 ** 2:
                    self.next_level()
                    return

            elif shape == "triangle":
                points = [(x, y + 50), (x + 25, y), (x + 50, y + 50)]
                if self.point_in_triangle(position, points):
                    self.next_level()
                    return

            elif shape == "star":
                if self.is_point_in_star(position, x, y):
                    self.next_level()
                    return

            elif shape == "diamond":
                points = [(x, y + 25), (x + 25, y), (x + 50, y + 25), (x + 25, y + 50)]
                if self.point_in_polygon(position, points):
                    self.next_level()
                    return

        # Якщо клікаєш не на правильну фігуру
        self.game_over()

    def next_level(self):
        """Перехід до наступного рівня"""
        self.level += 1
        self.objects_per_level += 5  # Ускладнюємо, додаючи більше об'єктів
        self.generate_objects()
        self.start_time = pygame.time.get_ticks()  # Скидаємо таймер

        if self.level == 50:  # Якщо досягнуто 50 рівня
            self.win()

    def game_over(self):
        """Кінець гри"""
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(game_over_text, (self.screen_width // 2 - game_over_text.get_width() // 2, self.screen_height // 2))

        pygame.display.flip()
        pygame.time.wait(2000)  # Затримка 2 секунди, щоб гравець побачив результат
        self.running = False  # Завершення гри

    def win(self):
        """Перемога"""
        win_text = self.font.render("YOU WIN!", True, (0, 255, 0))
        self.screen.blit(win_text, (self.screen_width // 2 - win_text.get_width() // 2, self.screen_height // 2))

        pygame.display.flip()
        pygame.time.wait(2000)  # Затримка 2 секунди, щоб гравець побачив результат
        self.running = False  # Завершення гри

    def draw_objects(self):
        """Малювання всіх об'єктів на екрані"""
        self.screen.fill((255, 255, 255))

        for obj in self.objects:
            shape, color, pos, *rest = obj
            x, y = pos

            if shape == "square":
                pygame.draw.rect(self.screen, color, (x, y, 50, 50))
            elif shape == "circle":
                pygame.draw.circle(self.screen, color, (x + 25, y + 25), 25)
            elif shape == "triangle":
                points = [(x, y + 50), (x + 25, y), (x + 50, y + 50)]
                pygame.draw.polygon(self.screen, color, points)
            elif shape == "star":
                self.draw_star(x, y, color)
            elif shape == "diamond":
                points = [(x, y + 25), (x + 25, y), (x + 50, y + 25), (x + 25, y + 50)]
                pygame.draw.polygon(self.screen, color, points)

        # Відображення часу
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        time_text = self.font.render(f"Час: {elapsed_time} сек", True, (0, 0, 0))
        level_text = self.font.render(f"Рівень: {self.level}", True, (0, 0, 0))
        self.screen.blit(time_text, (10, 10))
        self.screen.blit(level_text, (10, 50))

    @staticmethod
    def point_in_triangle(point, triangle):
        """Перевірка, чи точка знаходиться всередині трикутника"""
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        b1 = sign(point, triangle[0], triangle[1]) < 0.0
        b2 = sign(point, triangle[1], triangle[2]) < 0.0
        b3 = sign(point, triangle[2], triangle[0]) < 0.0

        return b1 == b2 == b3

    @staticmethod
    def point_in_polygon(point, polygon):
        """Перевірка, чи точка знаходиться всередині багатокутника"""
        x, y = point
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def draw_star(self, x, y, color):
        """Малювання зірки"""
        points = [
            (x + 25, y), (x + 31, y + 15), (x + 47, y + 15),
            (x + 34, y + 25), (x + 39, y + 40), (x + 25, y + 30),
            (x + 11, y + 40), (x + 16, y + 25), (x + 3, y + 15),
            (x + 19, y + 15)
        ]
        pygame.draw.polygon(self.screen, color, points)

    def is_point_in_star(self, point, x, y):
        """Перевірка, чи точка знаходиться всередині зірки"""
        points = [
            (x + 25, y), (x + 31, y + 15), (x + 47, y + 15),
            (x + 34, y + 25), (x + 39, y + 40), (x + 25, y + 30),
            (x + 11, y + 40), (x + 16, y + 25), (x + 3, y + 15),
            (x + 19, y + 15)
        ]
        return self.point_in_polygon(point, points)

if __name__ == "__main__":
    game = HideAndSeekGame()
    game.run_game()
