
import pygame
import random
import math
from pygame import mixer

#Initialize pygame.
pygame.init()

#creating the screen
screen = pygame.display.set_mode((800,800))

#CHANGING TITLE AND ICON
pygame.display.set_caption("Space InvaderZ")
icon = pygame.image.load("greenspaceship.png")
pygame.display.set_icon(icon)

#BACKGROUND 
bg = pygame.image.load("background.jpg")

#BACKGROUND MUSIC 
mixer.music.load("background.mp3")
mixer.music.play(-1)

#PLAYER 
players = pygame.image.load("spacefighter.png")
playerX = 360
playerY = 700
X_change = 0
# Y_change = 0

#ENEMY 
enemy = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numenemy = 6
for i in range (numenemy):
    enemy.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0,730))
    enemyY.append(random.randint(32,150))
    enemyX_change.append(2)
    enemyY_change.append(35) #Enemy moves down by 50 pixels

#BULLET 
bullet = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 700
bulletX_change = 0
bulletY_change = 25
#ready state is the bullet is not in the screen yet
# fire state is when the bullet is in the screen
bullet_state = "ready"

#SCORE 
score_value = 0
font = pygame.font.Font("freesansbold.ttf",34)
textX = 12 
textY = 12 
#GAME OVER TEXT
over_font = pygame.font.Font("freesansbold.ttf", 80)

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (0,0,0))
    screen.blit(score, (x,y))    

def game_over_text():
    over_text = over_font.render("Game Over", True,(0,255,0))
    screen.blit(over_text, (200,350))
    
def player(x,y):
    screen.blit(players,(x,y))
    
def enemyy(x,y,i):
    screen.blit(enemy[i], (x, y))
    
def bullet_fire(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet,(x + 15, y + 12))  
      
def Iscollision(enemyX,enemyY,bulletX,bulletY):   
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False  

#GAME LOOP
running = True
while running:
#SCREEN 
    screen.fill((0,0,9)) #RGB    
#BACKGROUND
    screen.blit(bg,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
#FOR CONTROLS
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                X_change -= 3.75
            if event.key == pygame.K_RIGHT:
                X_change += 3.75
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("lazer.mp3")
                    bullet_sound.play()
                    bulletX = playerX
                    bullet_fire(bulletX,bulletY)                        
#PLAYER MOVEMENT     
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                X_change = 0
        # if event.type == pygame.KEYDOWN:        
        #     if event.key == pygame.K_UP:
        #         Y_change -= 2.75
        #     if event.key == pygame.K_DOWN:
        #         Y_change += 2.75  
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
        #         Y_change = 0    

    playerX += X_change   
    # playerY += Y_change
    if playerX <= 0:
        playerX = 736 
    elif playerX >= 736:
        playerX = 736 
    # if playerY <= 0:
    #     playerY = 736 
    # elif playerY >= 736:
    #     playerY = 736      
#ENEMY MOVEMENT 
    for i in range(numenemy):
        #GAME OVER 
        if enemyY[i] > 600:
            for j in range(numenemy):
                enemyY[j] = 2000
            game_over_text()
            break
            
        enemyX[i] += enemyX_change[i]  
        # enemyY[i] += enemyY_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] -= 1.2 
            enemyY[i] += enemyY_change[i]
    
        #COLLISION
        collision = Iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.mp3")
            explosion_sound.play()
            bulletY = 750 
            bullet_state = "ready" 
            score_value += 1
            enemyX[i] = random.randint(0,730)
            enemyY[i] = random.randint(32,150)   
        enemyy(enemyX[i], enemyY[i],i)  
              
    #BULLET MOVEMENT 
    if bulletY <=0:
        bulletY = 750
        bullet_state = "ready"
            
    if bullet_state == "fire":
        bullet_fire (bulletX,bulletY)
        bulletY -= bulletY_change
            # bulletY = playerY  
                    
    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()        
        