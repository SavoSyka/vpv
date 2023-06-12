import random
import time

import pygame
import sys
from math import sqrt
from matplotlib import pyplot as plt
# Pygame инициализация
pygame.init()
WIDTH, HEIGHT = 1600, 800
FPS = 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def simulate_knudsen_effect(num_particles, hole_size, temperature_difference):
    # Скорость синих частиц
    blue_speed = (temperature_difference / 10000)
    # Скорость красных частиц
    red_speed = (temperature_difference / 1000)
    bkr = blue_speed/red_speed
    rkb = red_speed/blue_speed
    #print(bkr,rkb)


    particles_high_temp = num_particles // int((1+(red_speed/blue_speed)**2))
    particles_low_temp = num_particles - particles_high_temp

    # Цвета
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Создание списков для хранения позиций и скоростей частиц
    low_temp_particles = []
    high_temp_particles = []
    watches = []
    en_red = []
    en_blue = []


    for _ in range(particles_low_temp):
        x = random.uniform(-1, 0)
        y = random.uniform(-1, 1)

        # Симуляция частиц с низкой температурой
        if x < 0:
            vx = random.gauss(-blue_speed, blue_speed)
            vy = random.gauss(-blue_speed, blue_speed)
        else:
            vx = random.gauss(-red_speed, red_speed)
            vy = random.gauss(-red_speed, red_speed)

        # Частица движется к отверстию
        if vy < 0:
            vy *= -1

        # Добавление частицы в список
        low_temp_particles.append([x, y, vx, vy])

    for _ in range(particles_high_temp):
        x = random.uniform(0, 1)
        y = random.uniform(-1, 1)

        # Симуляция частиц с высокой температурой
        if x > 0:
            vx = random.uniform(red_speed/10, red_speed)
            vy = sqrt(red_speed**2 - vx**2)
        else:
            vx = random.uniform(blue_speed / 10, blue_speed)
            vy = sqrt(blue_speed ** 2 - vx ** 2)

        # Частица движется от отверстия
        if vy > 0:
            vy *= -1

        # Добавление частицы в список
        high_temp_particles.append([x, y, vx, vy])
    for particle in low_temp_particles:
        x, y, vx, vy = particle

        if x >= hole_size / 2:
            color = RED
        else:
            color = BLUE

        pygame.draw.circle(screen, color, (int((x + 1) * WIDTH / 2), int((y + 1) * HEIGHT / 2)), 2)

    for particle in high_temp_particles:
        x, y, vx, vy = particle

        if x <= -hole_size / 2:
            color = BLUE
        else:
            color = RED

        pygame.draw.circle(screen, color, (int((x + 1) * WIDTH / 2), int((y + 1) * HEIGHT / 2)), 2)
    # Основной цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #print(watches, en_red)
                plt.ylabel('Количество частиц')
                plt.xlabel('Время')
                plt.plot(watches, en_red, 'r')
                #plt.plot(watches, en_blue, 'b')

                plt.show()
                sys.exit()

        # Обновление позиций частиц
        for particle in low_temp_particles:
            particle[0] += particle[2]
            particle[1] += particle[3]

            # Обработка отражения от стенок
            if particle[0] < -1 or particle[0] > 1:
                particle[2] *= -1
            if particle[1] < -1 or particle[1] > 1:
                particle[3] *= -1
            if 0.01*temperature_difference > particle[0] > -0.001*temperature_difference and abs(particle[1]) > hole_size/(HEIGHT):
                particle[2] *= -1

        for particle in high_temp_particles:
            particle[0] += particle[2]
            particle[1] += particle[3]

            # Обработка отражения от стенок
            if particle[0] < -1 or particle[0] > 1:
                particle[2] *= -1
            if particle[1] < -1 or particle[1] > 1:
                particle[3] *= -1
            if -0.01*temperature_difference<particle[0] < 0.001*temperature_difference and abs(particle[1]) > hole_size/(HEIGHT):
                particle[2] *= -1

        for particle in low_temp_particles:
            particle[0] += particle[2]
            particle[1] += particle[3]

            # Проверка, прошла ли частица через отверстие
            if 1 > particle[0] > -0.001 and abs(particle[1]) <= hole_size / (HEIGHT):
                # Удаление частицы из списка холодных
                low_temp_particles.remove(particle)

                # Изменение скорости частицы
                particle[2] *= rkb
                particle[3] *= rkb
                # Добавление частицы в список горячих
                high_temp_particles.append(particle)

        for particle in high_temp_particles:
            particle[0] += particle[2]
            particle[1] += particle[3]

            # Проверка, прошла ли частица через отверстие
            if -1 < particle[0] < 0.001 and abs(particle[1]) <= hole_size / (HEIGHT):
                # Удаление частицы из списка холодных
                high_temp_particles.remove(particle)

                # Изменение скорости частицы
                particle[2] *= bkr
                particle[3] *= bkr

                # Добавление частицы в список горячих
                low_temp_particles.append(particle)

        # Отрисовка частиц на экране
        screen.fill(WHITE)

        # Отрисовка стенок
        pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, WIDTH, 2))  # Верхняя стенка
        pygame.draw.rect(screen, BLACK, pygame.Rect(0, HEIGHT - 2, WIDTH, 2))  # Нижняя стенка
        pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, 2, HEIGHT))  # Левая стенка
        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH - 2, 0, 2, HEIGHT))  # Правая стенка

        # Отрисовка перегородки
        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH/2, 0, 5, (HEIGHT-hole_size)/2))
        pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH / 2, (HEIGHT+hole_size)/2, 5, (HEIGHT-hole_size) / 2))

        for particle in low_temp_particles:
            x, y, _, _ = particle
            pygame.draw.circle(screen, BLUE, (int((x + 1) * WIDTH / 2), int((y + 1) * HEIGHT / 2)), 2)

        for particle in high_temp_particles:
            x, y, _, _ = particle
            pygame.draw.circle(screen, RED, (int((x + 1) * WIDTH / 2), int((y + 1) * HEIGHT / 2)), 2)

        pygame.display.flip()
        clock.tick(FPS)

        watches.append(time.perf_counter())
        en_red.append(len(high_temp_particles))
        en_blue.append(len(low_temp_particles))




simulate_knudsen_effect(num_particles = 5000, hole_size = 5, temperature_difference = 2)