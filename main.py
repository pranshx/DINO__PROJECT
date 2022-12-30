# ***IMPORTANT
# THE QUIT BUTTON DO NOT WORK PROPERLY STOP THE EXECUTION FOR EXITING

import pygame
import os
import random
import math
from pygame import mixer

# Starting the mixer
mixer.init()

# Loading the song
mixer.music.load("sounds/backgroundmusic.mp3")

# Setting the volume
mixer.music.set_volume(0.7)

# Start playing the song

pos_x = 0
funccount=0

# Initialising and Creating window
pygame.init()
win = pygame.display.set_mode((1080, 700))
pygame.display.set_caption("Dino Run")

# Load images bg, sprites and obstacle
bg_img = pygame.image.load('sprites\BG\desertBG.jpg')

stationary = pygame.image.load(os.path.join("sprites\dino still", 'idle (1).png'))
dinoRun = [pygame.image.load(os.path.join("sprites\dino run", 'Run (2).png')),
           pygame.image.load(os.path.join("sprites\dino run", 'Run (5).png')),
           pygame.image.load(os.path.join("sprites\dino run", 'Run (6).png'))]

dinoJump = [pygame.image.load(os.path.join("sprites\dino jump", 'Jump (3).png')),
            pygame.image.load(os.path.join("sprites\dino jump", 'Jump (12).png')),
            pygame.image.load(os.path.join("sprites\dino jump", 'Run (1).png'))]

smallcacta = [pygame.image.load('sprites\obstacle\obstacleCactus.png'),
            pygame.image.load('sprites\obstacle\cactus2obstacle2.png'),]

largecacta = [pygame.image.load('sprites\obstacle\largecacta1.png'),
            pygame.image.load('sprites\obstacle\largecacta2.png'),]

# Transforming the images

# transforming background
background = pygame.transform.scale(bg_img, (1080, 700))

# tranforming image when dino run jum and still
stationary = pygame.transform.scale(stationary,(125,110))

for j in range(0, 3):
    dinoRun[j] = pygame.transform.scale(dinoRun[j], (125, 110))
    dinoJump[j] = pygame.transform.scale(dinoJump[j], (125, 90))


for j in range(0, 2):
    smallcacta[j] = pygame.transform.scale(smallcacta[j], (130, 110))
    largecacta[j] = pygame.transform.scale(largecacta[j], (130, 120))




class dino:
    X_POS = 50
    Y_POS = 500
    JUMP_VEL = 12
# initializing images
    def __init__(self):
        self.run_img = dinoRun
        self.jump_img = dinoJump

# UPDATING VALUE OF DINORUN TO FALSE
        self.dino_run = False
        self.dino_jump = False

        self.stepIndex = 0
        self.image = self.run_img[0]

        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.jump_vel = self.JUMP_VEL

    def update(self, userInput):
        if self.dino_run:
            self.run()
            # UPDATING IF TO ELIF
        elif self.dino_jump:
            self.jump()

        if self.stepIndex >= 30:
            self.stepIndex = 0

# taking user input to see if user pressed space
        if userInput[pygame.K_SPACE] and not self.dino_jump:
            self.dino_run = False
            self.dino_jump = True
        elif not (self.dino_jump or userInput[pygame.K_SPACE]):
            self.dino_run = True
            self.dino_jump = False

    def run(self):
        self.image = self.run_img[self.stepIndex//10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.stepIndex += 1


    def jump(self):
        self.dino_run = False
        self.image = self.jump_img[self.stepIndex//10]
        if self.dino_jump:
                self.dino_rect.y -= self.jump_vel * 4
                self.jump_vel -= 1

        if self.jump_vel <= - self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL

        self.stepIndex += 1

    def draw(self,SCREEN):
        SCREEN.blit(self.image,(self.dino_rect.x,self.dino_rect.y))



class obstacle:
# initializing obtacle iamges
    def __init__(self,image,type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = 1800

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -1080:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type],self.rect)


class SmallCactus(obstacle):
    def __init__(self,image):
        self.type = random.randint(0,1)
        super().__init__(image,self.type)
        self.rect.y = 480


class LargeCactus(obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = 500


def main():
    global game_speed, width, obstacles,scores,death_count
    obstacles = []
    width = 1080
    game_speed = 15
    font = pygame.font.Font('freesansbold.ttf', 30)
    scores =0
    death_count=0
# defining score fuc to keep track of score
    def score():
        global scores,game_speed
        scores += 1
        text = font.render("Points: "+str(scores), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center= (900,40)
        win.blit(text, textRect)


    def backGround():
        global pos_x
        win.blit(background, (pos_x, 0))
        win.blit(background, (width + pos_x, 0))
        # adding a background if it exceeded width
        if pos_x == -width:
            win.blit(background, (width + pos_x, 0))
            pos_x = 0
        pos_x -= game_speed

    run = True
    clock = pygame.time.Clock()
    dinosaur = dino()
    mixer.music.play(10)
    a = 0


    while run:

        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                run = False
                mixer.music.stop()
                a = 1
        if a == 0:

        # Input
            userInput = pygame.key.get_pressed()

            backGround()
            dinosaur.draw(win)
            dinosaur.update(userInput)
            score()
            pygame.draw.rect(win,(255,0,0),dinosaur.dino_rect,2)

            if len(obstacles) == 0:
                if random.randint(0,1)==0:
                    obstacles.append(SmallCactus(smallcacta))
                elif random.randint(0,1)==1:
                    obstacles.append(LargeCactus(largecacta))


            for obstacle in obstacles:
                obstacle.draw(win)
                obstacle.update()
                if dinosaur.dino_rect.colliderect(obstacle.rect):
                    pygame.draw.rect(win,(255,0,0),obstacle.rect,2)
                    mixer.music.stop()
                    print("collide")
                    death_count += 1
                    startend(death_count)

            # Movement
# slowing the runtime
            clock.tick(32)
            pygame.display.update()
# making a theme for begining and ending of game
def startend(death_count):
    global scores,pos_x
    start = True
    while start:
        win.blit(background,(0,0))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count==0:
            text = font.render("Press spacebar to start",True,(0,0,0))
        elif death_count>0:
            text = font.render("Press spacebar to start", True, (0, 0, 0))
            score = font.render("Points: " + str(scores), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center=(1080//2,700//2+50)
            win.blit(score,scoreRect)
        textRect = text.get_rect()
        textRect.center = (1080//2,700//2)
        win.blit(text,textRect)
        win.blit(stationary,(1080//2 -110,700//2+80))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                funccount=1
            if event.type == pygame.KEYDOWN:
                main()
if funccount==0:
    startend(death_count=0)

