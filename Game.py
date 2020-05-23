import pygame
import random
import math


pygame.init()
screen = pygame.display.set_mode((800, 600))


background = pygame.image.load("background.png")
pygame.display.set_caption("Space invaders")
icon=pygame.image.load("game_icon.png")
pygame.display.set_icon(icon)

player_img = pygame.image.load("Spaceship.png")
PlayerX = 400
PlayerY = 500
Player_move = 0

bullet_img = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 0
bullet_move = 3
bullet_fire = False

enemy_bullet_img = pygame.image.load("enemy bullet.png")
enemy_bulletX = 0
enemy_bulletY = 20
enemy_bullet_move = 5
# enemy_bullet_fire = False


enemy_img = pygame.image.load("enemy.png")
enemyX = []
enemyY = []
enemies = 3
enemy_move = []


game_over_font=pygame.font.Font("CHICKEN PIE.ttf", 60)


font=pygame.font.Font("CHICKEN PIE.ttf", 20)
x=10
y=10
score_value = 0

def draw_game_over():
    game_over=font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(game_over, (400, 300))


def draw_score (x,y):
    score=font.render("Score is : " + str(score_value), False, (255, 255, 255))
    screen.blit(score, (x, y))

def draw_player(x, y):
    screen.blit(player_img, (x, y))


def draw_enemy(x, y):
    screen.blit(enemy_img, (x, y))


def draw_bullet(x, y):
    screen.blit(bullet_img, (x+16, y-16))
    global bullet_fire
    bullet_fire = True

def enemy_draw_bullet(x, y):
    screen.blit(bullet_img, (x+16, y+50))
    global enemy_bullet_fire
    enemy_bullet_fire = True

def colision_func(enemyX, enemyY, bulletX, bulletY):
    distance=math.sqrt(math.pow(enemyX-bulletX, 2) + (math.pow(enemyY-bulletY, 2)))
    if distance < 35:
        return True
    else:
        return False

def enemy_colision_func(PlayerX, PlayerY, enemy_bulletX, enemy_bulletY):
    distance = math.sqrt(math.pow(PlayerX-enemy_bulletX, 2) + (math.pow(PlayerY - enemy_bulletY, 2)))
    if distance < 25:
        return True
    else:
        return False


for i in range(enemies):
    enemyX.append(random.randint(0, 200))
    enemyY.append(20)
    enemy_move.append(3)

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                Player_move = -2
            elif event.key == pygame.K_d:
                Player_move = 2
            if event.key == pygame.K_SPACE and bullet_fire is False:
                bulletX = PlayerX
                draw_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                Player_move = 0

    PlayerX += Player_move
    if PlayerX <= 0:
        PlayerX=0
    elif PlayerX >= 736:
        PlayerX = 736
    draw_player(PlayerX, PlayerY)

    for i in range(enemies):
        draw_enemy(enemyX[i], enemyY[i])
        enemy_bullet_fire = False
        if not enemy_bullet_fire:
            enemy_bulletX = enemyX[i]
            enemy_draw_bullet(enemy_bulletX, enemy_bulletY)

        enemyX[i] += enemy_move[i]
        if enemyX[i] >= 736:
            enemy_move[i] = -2
        elif enemyX[i] <= 0:
            enemy_move[i] = 2
        colision = colision_func(enemyX[i], enemyY[i], bulletX, bulletY)
        if colision:
            score_value += 1
            bulletY = 500
            bullet_fire = False
            enemyX[i] = random.randint(0, 736)
    enemy_colision = enemy_colision_func(PlayerX, PlayerY, enemy_bulletX, enemy_bulletY)
    if enemy_colision:
        enemy_bullet_fire = False
        draw_game_over()
        score_value = 0
        break
        # if enemy_bullet_fire:
        #     enemy_draw_bullet(enemy_bulletX, enemy_bulletY)
        #     enemy_bulletY += enemy_bullet_move

    if enemy_bulletY >= 800:
        enemy_bulletY = 0
        enemy_bullet_fire = False

    if bullet_fire:
        draw_bullet(bulletX, bulletY)
        bulletY -= bullet_move
    if bulletY <= 0:
        bulletY = 500
        bullet_fire = False

    if enemy_bullet_fire:
        enemy_draw_bullet(enemy_bulletX, enemy_bulletY)
        enemy_bulletY += enemy_bullet_move

    # draw_enemy(enemyX, enemyY)
    draw_score(x, y)
    pygame.display.update()

