import pygame
from collisionCheck import *

#Powerup Class
class Powerup:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.powerup_img = img
        self.mask = pygame.mask.from_surface(self.powerup_img)

    def draw(self, window):
        window.blit(self.powerup_img, (self.x, self.y))

    def get_width(self):
        return self.powerup_img.get_width()

    def get_height(self):
        return self.powerup_img.get_height()

    def move(self, vel):
        self.y -= vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision (self, obj):
        return collide(obj, self)