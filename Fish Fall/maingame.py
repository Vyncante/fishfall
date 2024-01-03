#FishFall
import pygame
import random

pygame.init()
pygame.mixer.init()
WIDTH = 500
HEIGHT = 800
fps = 60
timer = pygame.time.Clock()
huge_font = pygame.font.SysFont('Arial', 42)
font = pygame.font.SysFont('Arial', 24)
pygame.display.set_caption('Fish Fall')
screen = pygame.display.set_mode([WIDTH, HEIGHT])
bg = (135, 206, 235)
game_over = False
corals = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 670, 1]]
coral_images = []
for i in range(1, 4):
    img = pygame.image.load(f'assets/coral/coral{i}.png')
    coral_images.append(img)

player_x = 240
player_y = 40
fish = pygame.transform.scale(pygame.image.load('assets/fish.png'), (50, 50))
direction = -1
y_speed = 0
gravity = 0.2
x_speed = 3
x_direction = 0

score = 0
total_distance = 0
file = open('high_scores.txt', 'r')
read = file.readlines()
first_high = int(read[0])
high_score = first_high

shark = pygame.transform.scale(pygame.image.load('assets/shark.png'), (300, 200))
enemies = [[-234, random.randint(400, HEIGHT - 100), 1]]

def draw_corals(coral_list, images):
    platforms = []
    for j in range(len(coral_list)):
        image = images[coral_list[j][2] - 1]
        platform = pygame.rect.Rect((coral_list[j][0] + 5, coral_list[j][1] + 40), (120, 10))
        screen.blit(image, (coral_list[j][0], coral_list[j][1]))
        pygame.draw.rect(screen, 'gray', [coral_list[j][0] + 5, coral_list[j][1] + 40, 120, 3])
        platforms.append(platform)
    return platforms


def draw_player(x_pos, y_pos, player_img, direc):
    if direc == -1:
        player_img = pygame.transform.flip(player_img, False, True)
    screen.blit(player_img, (x_pos, y_pos))
    player_rect = pygame.rect.Rect((x_pos + 7, y_pos + 40), (36, 10))
    return player_rect


def draw_enemies(enemy_list, shark_img):
    enemy_rects = []
    for j in range(len(enemy_list)):
        enemy_rect = pygame.rect.Rect((enemy_list[j][0] + 40, enemy_list[j][1] + 50), (215, 70))
        enemy_rects.append(enemy_rect)
        if enemy_list[j][2] == 1:
            screen.blit(shark_img, (enemy_list[j][0], enemy_list[j][1]))
        elif enemy_list[j][2] == -1:
            screen.blit(pygame.transform.flip(shark_img, 1, 0), (enemy_list[j][0], enemy_list[j][1]))
    return enemy_rects


def move_enemies(enemy_list, current_score):
    enemy_speed = 2 + current_score//15
    for j in range(len(enemy_list)):
        if enemy_list[j][2] == 1:
            if enemy_list[j][0] < WIDTH:
                enemy_list[j][0] += enemy_speed
            else:
                enemy_list[j][2] = -1
        elif enemy_list[j][2] == -1:
            if enemy_list[j][0] > -235:
                enemy_list[j][0] -= enemy_speed
            else:
                enemy_list[j][2] = 1
        if enemy_list[j][1] < -100:
            enemy_list[j][1] = random.randint(HEIGHT, HEIGHT + 500)
    return enemy_list


def update_objects(coral_list, play_y, enemy_list):
    lowest_coral = 0
    update_speed = 10
    if play_y > 200:
        play_y -= update_speed
        for q in range(len(enemy_list)):
            enemy_list[q][1] -= update_speed
        for j in range(len(coral_list)):
            coral_list[j][1] -= update_speed
            if coral_list[j][1] > lowest_coral:
                lowest_coral = coral_list[j][1]
        if lowest_coral < 750:
            num_corals = random.randint(1, 2)
            if num_corals == 1:
                x_pos = random.randint(0, WIDTH - 70)
                y_pos = random.randint(HEIGHT + 100, HEIGHT + 300)
                coral_type = random.randint(1, 3)
                coral_list.append([x_pos, y_pos, coral_type])
            else:
                x_pos = random.randint(0, WIDTH / 2 - 70)
                y_pos = random.randint(HEIGHT + 100, HEIGHT + 300)
                coral_type = random.randint(1, 3)
                x_pos2 = random.randint(WIDTH / 2 + 70, WIDTH - 70)
                y_pos2 = random.randint(HEIGHT + 100, HEIGHT + 300)
                coral_type2 = random.randint(1, 3)
                coral_list.append([x_pos, y_pos, coral_type])
                coral_list.append([x_pos2, y_pos2, coral_type2])
    return play_y, coral_list, enemy_list


run = True
while run:
    screen.fill(bg)
    timer.tick(fps)
    coral_platforms = draw_corals(corals, coral_images)
    player = draw_player(player_x, player_y, fish, direction)
    enemy_boxes = draw_enemies(enemies, shark)
    enemies = move_enemies(enemies, score)
    player_y, corals, enemies = update_objects(corals, player_y, enemies)
    if game_over:
        end_text = huge_font.render('Fish Fall', True, 'black')
        end_text2 = font.render('Game Over: Press Enter to Restart', True, 'black')
        screen.blit(end_text, (70, 20))
        screen.blit(end_text2, (60, 80))
        player_y = - 300
        y_speed = 0

    for i in range(len(coral_platforms)):
        if direction == -1 and player.colliderect(coral_platforms[i]):
            y_speed *= -1
            if y_speed > -2:
                y_speed = -2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_direction = -1
            elif event.key == pygame.K_RIGHT:
                x_direction = 1
            if event.key == pygame.K_RETURN and game_over:
                game_over = False
                player_x = 240
                player_y = 40
                direction = -1
                y_speed = 0
                x_direction = 0
                score = 0
                total_distance = 0
                enemies = [[-234, random.randint(400, HEIGHT - 100), 1]]
                corals = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 670, 1]]

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                x_direction = 0
            elif event.key == pygame.K_RIGHT:
                x_direction = 0

    if y_speed < 10 and not game_over:
        y_speed += gravity
    player_y += y_speed
    if y_speed < 0:
        direction = 1
    else:
        direction = -1
    player_x += x_speed * x_direction
    if player_x > WIDTH:
        player_x = -30
    elif player_x < -50:
        player_x = WIDTH - 20

    for i in range(len(enemy_boxes)):
        if player.colliderect(enemy_boxes[i]) and not game_over:
            game_over = True
            if score > first_high:
                file = open('high_scores.txt', 'w')
                write_score = str(score)
                file.write(write_score)
                file.close()
                first_high = score

    total_distance += y_speed
    score = round(total_distance / 100)
    score_text = font.render(f'Score: {score}', True, 'black')
    screen.blit(score_text, (10, HEIGHT - 70))
    if score > high_score:
        high_score = score
    score_text2 = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text2, (10, HEIGHT - 40))

    pygame.display.flip()
pygame.quit()