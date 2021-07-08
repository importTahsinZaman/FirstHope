from prerequisites import *
from lasers import *

#Parent class for all ships
class Ship:

    def __init__(self, x, y, health= 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        self.cooldownTimer = 30 #THIS VALUE SHOULD BE THE SAME AS COOLDOWNTIMER VARIABLE IN DEF MAIN FUNCTION

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown (self):
        if self.cool_down_counter >= self.cooldownTimer:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser_sound.play()
            laser = Laser(self.x + 32, self.y, self.laser_img) # !IMPORTANT! The 32 is used to center the laser to the ship
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width (self):
        return self.ship_img.get_width()

    def get_height (self):
        return self.ship_img.get_height()


#Class for player ship
class Player (Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x,y,health)
        self.ship_img = PLAYER_SPACE_SHIP
        self.laser_img = PLAYER_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.points = 0

        self.speed_powerup_timer = 900 #900 = 15 seconds, multiply the desired number of seconds by the frame rate (Usually 60)
        self.speed_powerup_timer_counter = 0

        self.cooldown_powerup_timer = 900 #900 = 15 seconds, multiply the desired number of seconds by the frame rate (Usually 60)
        self.cooldown_powerup_timer_counter = 0

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.points += 1
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 1, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 1, self.ship_img.get_width() * (self.health/self.max_health), 10))

#Class for enemy ships
class Enemy (Ship):
    COLOR_MAP = {
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "pink": (PINK_SPACE_SHIP, PINK_LASER),
                "red": (RED_SPACE_SHIP, RED_LASER)
    }

    def __init__(self, x, y, color, health = 100):
        super().__init__(x,y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move (self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            if self.ship_img == GREEN_SPACE_SHIP:
                laser = Laser(self.x+35, self.y + 125, self.laser_img) #The 35 and 125 are used for laser centering
            elif self.ship_img == PINK_SPACE_SHIP:
                laser = Laser(self.x+49, self.y + 100, self.laser_img) #The 49 and 100 are used for laser centering
            elif self.ship_img == RED_SPACE_SHIP:
                laser = Laser(self.x+69, self.y + 100, self.laser_img) #The 69 and 100 are used for laser centering
            self.lasers.append(laser)
            self.cool_down_counter = 1