import pygame
import random
import math
from pygame import mixer

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Priyanshi Sahu")

icon = pygame.image.load("launch.png")
pygame.display.set_icon(icon)

bg = pygame.image.load("background.jpg")

image = pygame.image.load("space.png")
imageX = 400
imageY = 480
imageX_ch = 0


def image_func(x, y):
    screen.blit(image, (x, y))


enemyimg = []
enemyX = []
enemyY = []
enemyY_ch = []
enemyX_ch = []
no_enemies = 7

for i in range(no_enemies):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(20, 150))
    enemyY_ch.append(50)
    enemyX_ch.append(1.90)


def enemy_func(x, y):
    screen.blit(enemyimg[i], (x, y))


bulletX = 0
bullet = pygame.image.load("bullet.png")
bulletY = 480
bullet_ch = 5
bullet_st = "ready"


def bullet_func(x, y):
    global bullet_st
    bullet_st = "fire"
    screen.blit(bullet, (x + 16, y - 4))


score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
fontX = 10
fontY = 10


def score_func(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def collision(enemyX, enemyY, bulletX, bulletY):
    if bullet_st == "fire":
        d = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
        if d < 27:
            return True
        else:
            return False


mixer.music.load("background.wav")
mixer.music.play(-1)

game_over_text = pygame.font.Font("freesansbold.ttf", 64)


def game_over_func(x, y):
    over_text = game_over_text.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (x, y))


high_score_img = pygame.image.load("high score.png")


def high_score_func():
    screen.blit(high_score_img, (700, 490))


a = ""


def prints_high_score():
    if a == "high score":
        high_score_func()


alert = pygame.image.load("alert.png")


def alert_func(x, y):
    screen.blit(alert, (x, y))


sound_test = "yes"
bullet_over = "no"  # bullet will not disappear

running = True
while running:
    screen.fill((0, 0, 0))

    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                imageX_ch = -2
            if event.key == pygame.K_RIGHT:
                imageX_ch = 2
            if event.key == pygame.K_SPACE:
                if bullet_st == "ready":
                    bullet_sound = mixer.Sound("bullet.wav")
                    bullet_sound.play()
                    bulletX = imageX
                    bullet_func(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                imageX_ch = 0
            if event.key == pygame.K_LEFT:
                imageX_ch = 0

    if imageX <= 0:
        imageX = 0
    elif imageX >= 736:
        imageX = 736
    imageX += imageX_ch
    image_func(imageX, imageY)
    alert_sound = mixer.Sound("alert-sound.mp3")

    for i in range(no_enemies):

        if enemyY[i] > 365:

            alert_sound.play()
            if enemyX[i] <= -1.90:
                enemyX[i] += 25
            elif enemyX[i] >= 736:
                enemyX[i] -= 25
            alert_func(enemyX[i], enemyY[i])

        if enemyY[i] > 445:
            alert_sound.stop()
            bullet_over = "yes"  # if the game will be over  the the bullet has to be disappear
            for j in range(no_enemies):
                enemyY[j] = 2000
                imageY = 2000
            game_over_func(210, 250)
            break

        enemyX[i] += enemyX_ch[i]
        if enemyX[i] <= -1:
            enemyY[i] += enemyY_ch[i]
            enemyX_ch[i] = 1.90
        elif enemyX[i] >= 736:
            enemyY[i] += enemyY_ch[i]
            enemyX_ch[i] = -1.90
        collisions = collision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collisions:
            explose_sound = mixer.Sound("explosion.mp3")
            explose_sound.play()

            bulletY = 480
            bullet_st = "ready"
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(20, 150)
            score_value += 1
            with open("high score.txt") as f:
                high_score = f.read()
                if int(high_score) < score_value:
                    with open("high score.txt", "w") as w:
                        w.write(str(score_value))
                    a = "high score"

        enemy_func(enemyX[i], enemyY[i])

    if bullet_over == "no":
        if bullet_st == "fire":
            bulletY -= bullet_ch
            bullet_func(bulletX, bulletY)
        if bulletY <= 0:
            bulletY = 480
            bullet_st = "ready"

    score_func(fontX, fontY)
    prints_high_score()

    pygame.display.update()
