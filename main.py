#import needed modules
import pygame
import os
import random
import button

#Game Icon:
pygame.display.set_icon(pygame.image.load(os.path.join("assets", "playerShip.png")))

#import font initializer
pygame.font.init()

#create fonts (font name is press start 2p)
gameFont1 = pygame.font.Font('gameFont.ttf', 150)
gameFont2 = pygame.font.Font('gameFont.ttf', 60)
gameFont3 = pygame.font.Font('gameFont.ttf', 50)
gameFont4 = pygame.font.Font('gameFont.ttf', 90)

#Setting app width/height and title
WIDTH, HEIGHT = 1600, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survivor")

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

#Sound effects
laser_sound = pygame.mixer.Sound('laserSound.mp3')

#Buttons
testButton_img = pygame.image.load(os.path.join("assets", "testButton.png")).convert_alpha()

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
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision (self, obj):
        return collide(obj, self)



#Class for lasers
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw (self, window):
        window.blit(self.img, (self.x, self.y))

    def move (self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision (self, obj):
        return collide(obj, self)

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


def check_highscore():
    with open('highscore.txt', 'r') as file:
        highscore = file.read().strip()
    return int(highscore)

#Collision function
def collide (obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

#main function
def main ():
    run = True
    FPS = 60
    level = 0

    enemies = []
    wave_length = 5
    enemy_vel = 1

    COOLDOWNTIMER = 30 #THIS VALUE SHOULD BE SAME AS player.cooldownTimer!!!!!!!! (IN CLASS PLAYER)

    powerups = []

    if level < 3:
        powerups_max = 3
    elif level >= 3 and level < 6:
        powerups_max = 4
    elif level >= 6 and level < 9:
        powerups_max = 5
    elif level >= 9:
        powerups_max = 6

    powerup_vel = 1

    healAmount = 10 #How much the health powerup heals for
    speedAmount = 2 #How much speed the speed powerup gives
    cooldownAmount = 15 #How much cooldown reduction the cooldown powerup gives

    PLAYER_VEL = 9  #Non changing player velocity

    player_vel = PLAYER_VEL  #Changing player velocity
    laser_vel = 5

    player = Player(int(WIDTH/2-PLAYER_SPACE_SHIP.get_width()/2), 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    i = 0

    pygame.mixer.music.load('gameMusic.mp3')
    pygame.mixer.music.play(-1)

#Function for refreshing window
    def redraw_window (i):
        WIN.blit (BG, [0, i])
        WIN.blit (BG, [0,-HEIGHT +i])

        #draw text
        health_label = gameFont3.render(f"Health:{player.health}", 1, (255, 255, 255))  #Renders health label
        level_label = gameFont3.render(f"Level:{level}", 1, (255, 255, 255))            #Renders level label
        points_label = gameFont3.render(f"Points:{player.points}", 1, (255, 255, 255))  #Renders points label

        WIN.blit(health_label, (10, 10))                                    #Displays player health
        WIN.blit(level_label, (WIDTH - level_label.get_width()-10, 10))     #Displays game level
        WIN.blit(points_label, (WIDTH/2 - points_label.get_width()/2, 10))  #Diplays the points

        for enemy in enemies:                   #Draws/creates enemies
            enemy.draw(WIN)

        for powerup in powerups:                #Draws/creates powerups
            powerup.draw(WIN)

        player.draw(WIN)                        #Creates/draws the player

        if lost:                                #Loss message
            lost_label = gameFont4.render ("SHIP DESTROYED", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))


        pygame.display.update()                  #Updates display

#Main loop
    while run:                                  #FPS clock speed
        clock.tick(FPS)
        redraw_window(i)
        if i == 0:
            i= HEIGHT
        i -= 1

        if player.health <=0:                   #Closes game when player loses
            lost = True
            lost_count += 1

        if lost:                                #Closes game when the player loses
            if lost_count > FPS * 3:
                if player.points > check_highscore():
                    with open ('highscore.txt', 'r+') as file:
                        file.write (str(player.points))
                run = False
                main_menu()
            else:
                continue

        if len(enemies) == 0:                   #Spawns new enemies when all enemies are gone
            level += 1
            wave_length += 5

            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["green", "red", "pink"]))
                enemies.append(enemy)

        if len(powerups) == 0:                  #Spawns new powerups when all powerups are gone

            for j in range(powerups_max):
                powerup = Powerup(random.randrange(50, WIDTH-100), random.randrange(-1700, -1000), random.choice([HEALTHPOWERUP, SPEEDPOWERUP, COOLDOWNPOWERUP]))
                powerups.append (powerup)

        for event in pygame.event.get():        #Closes the game when the x is pressed
            if event.type == pygame.QUIT:
                quit()

#Checks for key presses and moves player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  #left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:   #right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:   #up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 10 < HEIGHT: #down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

#Enemy movement and lasers
        for enemy in enemies[:]:                                           #Enemy Loop
            enemy.move (enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 3*60) == 1:                             #Enemy random shoot
                enemy.shoot()

            if collide(enemy, player):                                      #Checks for collision between enemy and player
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:                      #Checks if enemy has gone off screen
                player.health -= 10
                enemies.remove(enemy)

        for powerup in powerups[:]:                                           #Powerup loop
            powerup.move (powerup_vel)

            if collide(powerup, player):                                        #Checks for collision between powerups and player
                if powerup.powerup_img == HEALTHPOWERUP:
                    if player.health <= player.max_health - healAmount:
                        player.health += healAmount

                    elif player.health > player.max_health - healAmount:
                        player.health = player.max_health

                    powerups.remove (powerup)

                elif powerup.powerup_img == SPEEDPOWERUP:                       #Gives player speed powerup
                    if player_vel == PLAYER_VEL:
                        player_vel = player_vel + speedAmount
                        player.speed_powerup_timer_counter = 1
                    powerups.remove(powerup)

                elif powerup.powerup_img == COOLDOWNPOWERUP:                     #Gives player cooldown powerup
                    if player.cooldownTimer == COOLDOWNTIMER:
                        player.cooldownTimer = player.cooldownTimer - cooldownAmount
                        player.cooldown_powerup_timer_counter = 1
                        powerups.remove(powerup)
                    elif player.cooldownTimer == COOLDOWNTIMER - cooldownAmount:
                        powerups.remove(powerup)

            elif powerup.y + powerup.get_height() > HEIGHT:                       #Checks if the powerup is going offscreen
                powerups.remove(powerup)

        if player.speed_powerup_timer_counter >= player.speed_powerup_timer:      #Timer for speed powerup
            player_vel = PLAYER_VEL
        elif player.speed_powerup_timer_counter > 0:
            player.speed_powerup_timer_counter += 1

        if player.cooldown_powerup_timer_counter >= player.cooldown_powerup_timer: #Timer for cooldown powerup
            player.cooldownTimer = 30
        elif player.cooldown_powerup_timer_counter > 0:
            player.cooldown_powerup_timer_counter += 1

        #Temporary Print statement to bug test game:
        print (f"Player Speed:{player_vel}  Speed Cooldown: {player.speed_powerup_timer_counter}/{player.speed_powerup_timer}  Player cooldown: {player.cooldownTimer} Cooldown Powerup Cooldown: {player.cooldown_powerup_timer_counter}/{player.cooldown_powerup_timer}")

        player.move_lasers(-laser_vel, enemies)   #Moves player's laser

#Function for main menu:
def main_menu():
    pygame.mixer.music.load('menuMusic.mp3')
    pygame.mixer.music.play(-1)

    run = True
    while run:
        WIN.blit(BG, (0,0))

        mainTitle_label = gameFont1.render("LAST HOPE", 1, (255,255,255))
        WIN.blit(mainTitle_label, (WIDTH / 2 - mainTitle_label.get_width() / 2, HEIGHT / 2 - mainTitle_label.get_height() / 2))

        highscore_label = gameFont3.render(f"HIGHSCORE: {check_highscore()} ", 1, (255, 255, 255))
        WIN.blit (highscore_label, (WIDTH/2-highscore_label.get_width()/2, (HEIGHT/2-highscore_label.get_height()/2)+mainTitle_label.get_height() - 30))

        play_label = gameFont3.render("PLAY", 1, (255, 255, 255))
        WIN.blit (play_label, (WIDTH/2-play_label.get_width()/2, (HEIGHT/2-play_label.get_height()/2)+mainTitle_label.get_height()+highscore_label.get_height()))

        play_button_picture = pygame.transform.scale(pygame.image.load('buttonPicture.png').convert_alpha(), (play_label.get_width(), play_label.get_height() - 10))
        play_button = button.Button((WIDTH/2-play_label.get_width()/2), ((HEIGHT/2-play_label.get_height()/2)+mainTitle_label.get_height()+highscore_label.get_height()), play_button_picture, 1)

        if play_button.draw(WIN):
            main()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()
main_menu() #Runs game