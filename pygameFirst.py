import pygame
import random
import math
from pygame import mixer

'''
This is my first experience in learning how to make a game with python.
this is the video used: https://www.youtube.com/watch?v=FfWpgLFMI7w&ab_channel=freeCodeCamp.org
this was done using the pygame framework.

Crruent time stamp: 1:27:00
Great page fro icons flaticon.com
'''


#Initializes pygame
pygame.init()

#Create window (width,height)
screen = pygame.display.set_mode((800,600))

#Setting title and icon (appears in task bar)
pygame.display.set_caption("David's Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('ufo.png')
playerX = 355 #Pixel 0,0 is in the top left
playerY = 450 #This would be our starting values.
playerX_change = 0
playerY_change = 0

#Enemy
#To make multiple enemies, you have to make a list, specify its length, and then iterate through it adding everything. 
enemyImg = []
enemyX = [] 
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 15

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(5,730)) #Random int between bounds (min max)
    enemyY.append(random.randint(50,150))
    enemyX_change.append(3)
    enemyY_change.append(0.3)

#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 450
bulletY_change = -10
bullet_state = 'ready' #Ready means it isn't visible, fire means it is moving

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32) #32 is size

textX = 10
textY = 10

def show_score(x,y):
    score = font.render('Score: ' + str(score_value), True, (255,255,255) )
    screen.blit(score, (x,y))

#Game over
game_over = False
game_over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    game_over = True
    text = game_over_font.render('GAME OVER', True, (255,255,255))
    text_rect = text.get_rect(center=(800/2, 600/2)) #To center. 800 and 600 are sizes. Normally set these numbers as constants, like SCREEN_WIDTH/2, SCREEN_HEIGHT/2-
    screen.blit(text, text_rect)
    #screen.blit(text, (x,y))

#Scales image. First sets a default size, then sets it to the player img
#It is just way easire to resize file. Skips a lot of work. Since they are PNG, they are lossless
DEFAULT_IMAGE_SIZE = (64,64)
playerImg = pygame.transform.scale(playerImg, DEFAULT_IMAGE_SIZE)
bulletImg = pygame.transform.scale(bulletImg, (30,30))


#Player method that is declared in the running window loop.
#Parameters x andy are used to determine the position of the player in the screen
def player(x,y):
    if game_over == False:
        screen.blit(playerImg, (x,y))

def enemy(x,y, i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x +16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY,gap):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < gap:
        return True
    else:
        return False

#Colors and setting background color.
backgroundImg = pygame.image.load('background.png')
backgroundImg = pygame.transform.scale(backgroundImg,(800,600)) #Sizing the background. 
green = (150,200,8)
blue = (0,0,200)
red = (245,0,0)
black = (0,0,0)
beige = (195, 148, 99)
white = (255,255,255)

#Background sound
mixer.music.load('backgroundMusic.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)


#Game Loop
running = True
while running:

    screen.fill(white) #Color of the screen/Setting background color
    screen.blit(backgroundImg,(0,0)) #Adding the background will slow down the iterations of the while loop, which is why it was necessary to increase speeds for all elements.

    for event in pygame.event.get(): #Closing the game
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN: #KEYDOWN means a key is pressed. KEYUP means it was released
            if event.key == pygame.K_DOWN:
                playerY_change = 4
            if event.key ==pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key ==pygame.K_UP:
                playerY_change = -4
            
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_Sound = mixer.Sound('shoot.wav')
                    bullet_Sound.set_volume(10)
                    bullet_Sound.play()
                    #Gets the current coordinates and fires on these ones.
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(playerX,playerY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
        

    '''
    this constantly moves the player. This is because everytime the while loop is run, the count increases, constantly changing the position of the player. 
    playerX += 1 Moves right -= moves left
    playerY -= 1 Moves up += 1 Moves down
    '''
    playerX += playerX_change
    playerY += playerY_change

    


    #Creates bounds, if it reaches certain x position, it stops moving
    if game_over == False:
        if playerX <= 5:
            playerX = 5
        elif playerX >= 731:
            playerX = 731

        if playerY <= -6:
            playerY = -6
        elif playerY >= 540:
            playerY = 540
    

    #Enemy movement, iteration through lists so then it affects all enemies.

    for i in range(num_of_enemies):
        enemyX[i] +=enemyX_change[i]
        enemyY[i] += enemyY_change[i]
        if enemyX[i] <= 5:
            enemyX[i] = 5 #stops
            enemyX_change[i] = 3 #changes direction of movement
            enemyX[i] += enemyX_change[i]
        elif enemyX[i] >= 731:
            enemyX[i] = 731
            enemyX_change[i] = -3
        
        #Collision for bullet
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY,27)
        if collision:
            collision_Sound = mixer.Sound('explosion.wav')
            collision_Sound.set_volume(0.2)
            collision_Sound.play()
            bulletY = playerY
            bulletX = playerX
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(5,730) #Respawn
            enemyY[i] = random.randint(50,150)

        #Collision for player
        collision = isCollision(enemyX[i],enemyY[i],playerX,playerY,45)
        if collision:
            for j in range (num_of_enemies):
                enemyY[j] = 2000
            #playerX = 2000
            #playerY = 2000
            game_over_text()
            break
            #These comments would be useful, but since moving the enemies out of range, it automatically triggers next if statement. 
        
        enemy(enemyX[i],enemyY[i],i)

        #Game over
        
        if enemyY[i] >= 530:
            '''enemyY[i] = 530
            enemyX_change[i] = 0
            enemyY[i] += enemyY_change[i]
            '''
             #This code was to stop the enemy when it arrived at the end of the screen.
            for j in range (num_of_enemies):
                enemyY[j] = 2000
            
            game_over_text()
            break


    #Bullet movement
    if bullet_state is 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY += bulletY_change

    if bulletY <= 0:
        bullet_state = 'ready'
        bulletY = playerY


    #bullet(playerX,playerY)
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update() #Adds everything to the display.
