import pygame
import random
import math


class Enemy:
    def __init__(self, enemy_image, enemyx, enemyy):
        self.enemy_image = enemy_image
        self.enemyx = enemyx
        self.enemyy = enemyy
        self.enemy_move = random.randint(2, 4)
        self.enemy_bullet_image = pygame.image.load("enemy bullet.png")
        self.enemy_bulletx = self.enemyx
        self.enemy_bullety = 0
        self.enemy_bullet_move = random.randint(2, 4)
        self.fire = random.choice([True, False])

    @staticmethod
    def draw_enemy(x, y):
        screen.blit(enemy_image, (x, y))

    def enemy_bullet_fire(self, x, y):
        screen.blit(self.enemy_bullet_image, (x + 16, y + 50))


class Player:
    def __init__(self):
        self.playerimage = pygame.image.load("Spaceship.png")
        self.playerx = 400
        self.playery = 500
        self.player_move = 0
        self.bullet_img = pygame.image.load("bullet.png")
        self.bulletX = 0
        self.bulletY = 500
        self.bullet_move = -4
        self.bullet_fire = False


    def draw_player(self, x, y):
        screen.blit(self.playerimage, (x, y))


    def draw_bullet(self, x, y):
        screen.blit(self.bullet_img, (x+16, y))


def colision_func(enemyx, enemyy, bulletX, bulletY):
    distance=math.sqrt(math.pow(enemyx-bulletX, 2) + (math.pow(enemyy-bulletY, 2)))
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


def draw_game_over():
    game_over = game_over_font.render(f"GAME OVER!", True, (255, 255, 255))
    screen.blit(game_over, (200, 200))


def draw_game_over_score():
    game_over_score = game_over_score_font.render(f'Your score is: {score_value}', True, (255, 255, 255))
    screen.blit(game_over_score, (200, 300))


def draw_score():
    score = score_font.render("Score is : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (10, 10))


def play_again_draw():
    play_again = play_again_font.render("Press 'q' to play again ", True, (255, 255, 255))
    screen.blit(play_again, (200, 500))


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    background = pygame.image.load("background.png")
    pygame.display.set_caption("Space invaders")
    icon = pygame.image.load("game_icon.png")
    pygame.display.set_icon(icon)
    program = True

    while program:

        enemy_image = pygame.image.load("enemy.png")
        enemy_list = []
        n = 0
        number_of_enemies = 3
        while n < number_of_enemies:
            enemyx = random.randint(0, 736)
            enemyy = 10
            enemy_bulletx = 0
            enemy_bullety = 0
            e = Enemy(enemy_image, enemyx, enemyy)
            enemy_list.append(e)
            n += 1

        p = Player()

        game_over_font = pygame.font.Font("CHICKEN PIE.ttf", 60)
        game_over_score_font = pygame.font.Font("CHICKEN PIE.ttf", 40)
        score_font = pygame.font.Font("CHICKEN PIE.ttf", 20)
        play_again_font = pygame.font.Font("CHICKEN PIE.ttf", 20)
        score_value = 0

        over = False
        running = True

        while running:
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    program = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        p.player_move = -2
                    elif event.key == pygame.K_d:
                        p.player_move = 2
                    if event.key == pygame.K_SPACE and p.bullet_fire is False:
                        p.bulletX = p.playerx
                        p.draw_bullet(p.bulletX, p.bulletY)
                        p.bullet_fire = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        p.player_move = 0
            p.playerx += p.player_move
            p.draw_player(p.playerx, p.playery)
            if p.playerx <= 0:
                p.player_move = 0
            elif p.playerx >= 736:
                p.player_move = 0
            if p.bullet_fire:
                p.bulletY += p.bullet_move
                p.draw_bullet(p.bulletX, p.bulletY)
            if p.bulletY <= 0:
                p.bulletY = 500
                p.bullet_fire = False

            for enemy in enemy_list:
                Enemy.draw_enemy(enemy.enemyx, enemy.enemyy)
                enemy.enemyx += enemy.enemy_move
                if enemy.enemyx >= 736:
                    enemy.enemy_move = -enemy.enemy_move
                elif enemy.enemyx <= 0:
                    enemy.enemy_move = -enemy.enemy_move
                if not enemy.fire:
                    enemy.enemy_bulletx = enemy.enemyx
                    enemy.enemy_bullety = enemy.enemy_bullety
                    enemy.enemy_bullet_fire(enemy.enemy_bulletx, enemy.enemy_bullety)
                    enemy.fire = True
                if enemy.fire:
                    enemy.enemy_bullet_fire(enemy.enemy_bulletx, enemy.enemy_bullety)
                    enemy.enemy_bullety += enemy.enemy_bullet_move
                if enemy.enemy_bullety >= 800:
                    enemy.enemy_bullety = 0
                    enemy.fire = False
                colision=colision_func(enemy.enemyx, enemy.enemyy, p.bulletX, p.bulletY)
                if colision:
                    enemy.enemyx = random.randint(0, 730)
                    score_value += 1
                    if enemy.enemy_move < 0:
                        enemy.enemy_move -= 1
                    elif enemy.enemy_move > 0:
                        enemy.enemy_move +=1
                    enemy.enemy_bullet_move += 1
                    p.bulletY = 500
                    p.bullet_fire = False
                enemy_colision=enemy_colision_func(p.playerx, p.playery, enemy.enemy_bulletx, enemy.enemy_bullety)
                if enemy_colision:
                    running = False
                    over = True
            draw_score()
            pygame.display.update()

        while over:
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))
            draw_game_over()
            draw_game_over_score()
            play_again_draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    over = False
                    program = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        over = False
                        running = True
            pygame.display.update()
