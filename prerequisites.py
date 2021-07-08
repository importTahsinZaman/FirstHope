import pygame
import os

#Game Icon:
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "playerShip.png")))

#import font initializer
pygame.font.init()

#Font Color
white_color = (255,255,255)

#create fonts (font name is "press start 2p")
gameFont1 = pygame.font.Font('gameFont.ttf', 150)
gameFont2 = pygame.font.Font('gameFont.ttf', 60)
gameFont3 = pygame.font.Font('gameFont.ttf', 50)
gameFont4 = pygame.font.Font('gameFont.ttf', 90)
gameFont5 = pygame.font.Font ('gameFont.ttf', 40)


#Setting app width/height and title
WIDTH, HEIGHT = 1600, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Hope")

#Enemy Ships
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "greenEnemy.png"))
PINK_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pinkEnemy.png"))
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "redEnemy.png"))

#Player image
PLAYER_SPACE_SHIP = pygame.image.load(os.path.join("assets", "playerShip.png"))

#Lasers (35,45 is my determined ideal size for the lasers)
RED_LASER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "redLaser.png")), (35, 45))
PINK_LASER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pinkLaser.png")), (35, 45))
GREEN_LASER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "greenLaser.png")), (35, 45))
PLAYER_LASER = pygame.image.load(os.path.join("assets", "playerLaser.png"))

#Powerups
HEALTHPOWERUP = pygame.image.load(os.path.join("assets", "healthPowerup.png"))
SPEEDPOWERUP = pygame.image.load(os.path.join("assets", "speedPowerup.png"))
COOLDOWNPOWERUP = pygame.image.load(os.path.join("assets", "cooldownPowerup.png"))

#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "mainBackground.png")), (WIDTH, HEIGHT))

#Music Initialization
pygame.mixer.init()
pygame.mixer.music.load('menuMusic.mp3')
pygame.mixer.music.play(-1)

#Sound effects
laser_sound = pygame.mixer.Sound('laserSound.mp3')