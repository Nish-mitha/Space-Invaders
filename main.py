import pygame
import random
import math
from pygame import mixer


# initializing pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((1600, 850))

# backgroud
background = pygame.image.load('assets/images/game_background.png')

# Background Music
mixer.music.load('assets/music/background_music.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('assets/images/alien.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('assets/images/space_ship.png')
playerX = 80
playerY = 650
playerX_change = 0

# UFO
ufoImg = pygame.image.load('assets/images/ufo.png')
ufoX = 0
ufoY = 5
ufoX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 3
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('assets/images/alien.png'))
    enemyX.append(random.randint(0, 1550))
    enemyY.append(random.randint(200, 250))
    enemyX_change.append(1.5)
    enemyY_change.append(60)

# Bullet
# Ready-bullet cannot be seen on the screen
# Fire-bullet is currently moving
BulletImg = pygame.image.load('assets/images/bullet.png')
BulletX = 0
BulletY = 650
BulletX_change = 0
BulletY_change = 4
Bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('assets/images/HorrorType.TTF',60)
font1 = pygame.font.Font('freesansbold.ttf',40)
textX = 10
textY = 10

#Game Over text
game_font = pygame.font.Font('assets/images/HorrorType.TTF',300)

#function to display game over
def game_over_text():
    game_text = game_font.render("GAME OVER!!!", True, (255, 0, 0))
    screen.blit(game_text, (100, 120))


# function to display score
def show_score(x, y):
    score = font.render("Score", True, (255, 0, 0))
    score1 = font1.render(": "+str(score_value), True, (255,0, 0))
    screen.blit(score, (x, y))
    screen.blit(score1, (65, 30))

# function to display ufo
def ufo(x, y):
    screen.blit(ufoImg, (x, y))


# function to display player
def player(x, y):
    screen.blit(playerImg, (x, y))


# function to display enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# function to display bullet
def fire_bullet(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))


# function to check collision
def isCollision(enemyX, enemyY, BulletX, BulletY):
    distance = math.sqrt((math.pow(enemyX - BulletX, 2)) + (math.pow(enemyY - BulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# for closing the game screen
running = True
while running:
    # Background Color-RGB
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # close game window
            running = False

        # If keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if Bullet_state is "ready":
                    Bullet_sound = mixer.Sound('assets/music/laser.wav')  # Bullet sound
                    Bullet_sound.play()
                    BulletX = playerX  # get current x coordinate of player
                    fire_bullet(BulletX, BulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player boundary
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1400:  # 1400 because x coordinate is 1600 and image width is 200px so 1600-200->1400
        playerX = 1400

    # ufo boundary
    ufoX += ufoX_change
    if ufoX <= 0:
        ufoX_change = 1.5
        ufoX += ufoX_change
    elif ufoX >= 1350:  # 1350 because x coordinate is 1600 and image width is 250px so 1600-250->1350
        ufoX_change = -1.5
        ufoX += ufoX_change

    # enemy movement
    for i in range(num_of_enemies):
        #Game Over
        if enemyY[i]>600:
            playerX=2000
            Bullet_sound = mixer.Sound('assets/music/gameover.wav')  # Bullet sound
            Bullet_sound.play()
        if playerX>2000:
            game_over_text()
            pygame.mixer.music.stop()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 1536:  # 736 because x coordinate is 800 and image width is 64px so 800-64->736
            enemyX_change[i] = -1.5
            enemyY[i] += enemyY_change[i]

        # Collision
        Collision = isCollision(enemyX[i], enemyY[i], BulletX, BulletY)
        if Collision:
            Collision_sound = mixer.Sound('assets/music/explosion.wav')  #Collision sound
            Collision_sound.play()
            BulletY = 650
            Bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        # function call for player and enemy
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if BulletY <= 0:
        BulletY = 650
        Bullet_state = "ready"

    if Bullet_state is "fire":
        fire_bullet(BulletX, BulletY)  # function call
        BulletY -= BulletY_change

    # function call
    player(playerX, playerY)
    ufo(ufoX, ufoY)
    show_score(textX, textY)
    pygame.display.update()
