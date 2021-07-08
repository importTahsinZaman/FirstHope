#import needed modules
import pygame
import os
import random
import button
from fileReaderWriter import *

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
        health_label = gameFont3.render(f"Health:{player.health}", 1, (white_color))  #Renders health label
        level_label = gameFont3.render(f"Level:{level}", 1, (white_color))            #Renders level label
        points_label = gameFont3.render(f"Points:{player.points}", 1, (white_color))  #Renders points label

        WIN.blit(health_label, (10, 10))                                    #Displays player health
        WIN.blit(level_label, (WIDTH - level_label.get_width()-10, 10))     #Displays game level
        WIN.blit(points_label, (WIDTH/2 - points_label.get_width()/2, 10))  #Diplays the points

        for enemy in enemies:                   #Draws/creates enemies
            enemy.draw(WIN)

        for powerup in powerups:                #Draws/creates powerups
            powerup.draw(WIN)

        player.draw(WIN)                        #Creates/draws the player

        if lost:                                #Loss message
            lost_label = gameFont4.render ("SHIP DESTROYED", 1, (white_color))
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


        if lost:                                #goes back to main menu when player loses
            if lost_count > FPS * 1.5:
                writeFile ('gameData.txt', 'enemiesKilled', readFile('gameData.txt', 'enemiesKilled') + player.points)
                if player.points > readFile('gameData.txt', 'highscore'):
                    writeFile('gameData.txt', 'highscore', player.points)
                run = False
                main_menu()
            else:
                continue

        if len(enemies) == 0:                   #Spawns new enemies when all enemies are gone
            level += 1
            wave_length += 5

            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1200, -100), random.choice(["green", "red", "pink"]))
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

        player.move_lasers(-laser_vel, enemies)   #Moves player's laser

def instructionsScreen ():
    run = True
    while run:
        WIN.blit(BG, (0, 0))
                                             # Writes this text:
        information_label1 = gameFont3.render("Press W,A,S,D to move up, left, down, and right.", 1, (white_color))
        WIN.blit(information_label1, (30, 30))

                                              #Writes this text:
        information_label2 = gameFont3.render("Press spacebar to fire your weapon and destroy alien ships", 1, (white_color))
        WIN.blit(information_label2, (30, information_label1.get_height() + 30))

        #Main Menu Label
        main_menu_label = gameFont3.render("Main Menu", 1, (white_color))
        WIN.blit (main_menu_label, (WIDTH/2-main_menu_label.get_width()/2, HEIGHT- 55))

        #Main Menu Button
        main_menu_picture = pygame.transform.scale(pygame.image.load('buttonPicture.png').convert_alpha(), (main_menu_label.get_width(), main_menu_label.get_height() - 10))
        main_menu_button = button.Button(WIDTH/2-main_menu_label.get_width()/2, HEIGHT- 55, main_menu_picture, 1)
        if main_menu_button.draw(WIN): main_menu()

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

def space_logs_screen ():
    run = True
    while run:
        WIN.blit(BG, (0, 0))
                                              #Prints this text:
        information_label1 = gameFont5.render("Logs encrypted, must collect data from alien spacecrafts", 1, (white_color))
        WIN.blit(information_label1, (30, 30))

                                              #Writes this text:
        information_label2 = gameFont5.render("Year 2321. Earth Population: 12.1 billion:", 1, (white_color))
        WIN.blit(information_label2, (30, information_label1.get_height() + 60))

        if readFile('gameData.txt', 'enemiesKilled') < 150:
                                                #Writes this text:
            information_label3 = gameFont5.render(f"--------------   [{150 - readFile('gameData.txt', 'enemiesKilled')} Data samples required to decrypt]", 1, (white_color))
            WIN.blit(information_label3, (30, information_label1.get_height() + information_label2.get_height() +90))
        else:
            information_label3 = gameFont5.render("Initial Alien Contact", 1, (white_color))
            WIN.blit(information_label3, (30, information_label1.get_height() + information_label2.get_height() +90))

        information_label4 = gameFont5.render("Year 2331. Earth population: 12.2 billion:", 1, (white_color))
        WIN.blit(information_label4, (30, information_label1.get_height() + information_label2.get_height()+ information_label3.get_height() + 130))

        if readFile('gameData.txt', 'enemiesKilled') < 300:
                                                #Writes this text:
            information_label5 = gameFont5.render(f"--------------   [{300 - readFile('gameData.txt', 'enemiesKilled')} Data samples required to decrypt]", 1, (white_color))
            WIN.blit(information_label5, (30, information_label1.get_height() + information_label2.get_height()+ information_label3.get_height() + information_label4.get_height() + 170))
        else:
            information_label5 = gameFont5.render("Alien Trade",1, (white_color))
            WIN.blit(information_label5, (30, information_label1.get_height() + information_label2.get_height() + information_label3.get_height() + information_label4.get_height() + 170))

                                              #Writes this text:
        information_label6 = gameFont5.render("Year 2345. Earth population: 12.5 billion:", 1, (white_color))
        WIN.blit(information_label6, (30, information_label1.get_height() + information_label2.get_height()+ information_label3.get_height() + information_label4.get_height() + information_label5.get_height() + 210))

        if readFile('gameData.txt', 'enemiesKilled') < 450:
                                              #Writes this text:
            information_label7 = gameFont5.render(f"--------------   [{450 - readFile('gameData.txt', 'enemiesKilled')} Data samples required to decrypt]", 1, (white_color))
            WIN.blit(information_label7, (30, information_label1.get_height() + information_label2.get_height() + information_label3.get_height()+ information_label4.get_height() + information_label5.get_height() + information_label6 .get_height() + 250))
        else:
                                              #Writes this text:
            information_label7 = gameFont5.render("Human Intergalactic Travel", 1, (white_color))
            WIN.blit(information_label7, (30, information_label1.get_height() + information_label2.get_height() + information_label3.get_height()+ information_label4.get_height() + information_label5.get_height() + information_label6 .get_height() + 250))

        information_label8 = gameFont5.render("Year 2351. Earth population 1 million:", 1, (white_color))
        WIN.blit(information_label8, (30, information_label1.get_height() + information_label2.get_height()+ information_label3.get_height() + information_label4.get_height() + information_label5.get_height() + information_label6.get_height() + information_label7.get_height() + 290))

        if readFile('gameData.txt', 'enemiesKilled') < 600:
                                                #Writes this text:
            information_label9 = gameFont5.render(f"--------------   [{600 - readFile('gameData.txt', 'enemiesKilled')} Data samples required to decrypt]", 1, (white_color))
            WIN.blit(information_label9, (30, information_label1.get_height() + information_label2.get_height()+ information_label3.get_height() + information_label4.get_height() + information_label5.get_height() + information_label6.get_height() + information_label7.get_height() + information_label8.get_height() + 330))
        else:
            information_label9 = gameFont5.render("Alien Queen Killed by Humans", 1, (white_color))
            WIN.blit(information_label9, (30, information_label1.get_height() + information_label2.get_height()+ information_label3.get_height() + information_label4.get_height() + information_label5.get_height() + information_label6.get_height() + information_label7.get_height() + information_label8.get_height() + 330))

        information_label10 = gameFont5.render("Year 2354. Earth population 300 Thousand:", 1, (white_color))
        WIN.blit(information_label10, (30, information_label1.get_height() + information_label2.get_height()+ information_label3.get_height() + information_label4.get_height() + information_label5.get_height() + information_label6.get_height() + information_label7.get_height() + information_label8.get_height() + information_label9.get_height() + 370))

        if readFile('gameData.txt', 'enemiesKilled') < 750:
                                                #Writes this text:
            information_label11 = gameFont5.render(f"--------------   [{750 - readFile('gameData.txt', 'enemiesKilled')} Data samples required to decrypt]", 1, (white_color))
            WIN.blit(information_label11, (30, information_label1.get_height() + information_label2.get_height()+ information_label3.get_height() + information_label4.get_height() + information_label5.get_height() + information_label6.get_height() + information_label7.get_height() + information_label8.get_height() + information_label9.get_height() + information_label10.get_height() + 410))
        else:
            information_label11 = gameFont5.render("Aliens Massacre Humans", 1, (white_color))
            WIN.blit(information_label11, (30, information_label1.get_height() + information_label2.get_height()+ information_label3.get_height() + information_label4.get_height() + information_label5.get_height() + information_label6.get_height() + information_label7.get_height() + information_label8.get_height() + information_label9.get_height() + information_label10.get_height() + 410))

        information_label12 = gameFont5.render (f"Enemies Killed: {readFile('gameData.txt', 'enemiesKilled')}", 1, (white_color))
        WIN.blit(information_label12, (WIDTH - information_label12.get_width(), HEIGHT - 40))


        #Main Menu Label
        main_menu_label = gameFont3.render("Main Menu", 1, (white_color))
        WIN.blit (main_menu_label, (WIDTH/2-main_menu_label.get_width()/2, HEIGHT- 55))

        #Main Menu Button
        main_menu_picture = pygame.transform.scale(pygame.image.load('buttonPicture.png').convert_alpha(), (main_menu_label.get_width(), main_menu_label.get_height() - 10))
        main_menu_button = button.Button(WIDTH/2-main_menu_label.get_width()/2, HEIGHT- 55, main_menu_picture, 1)
        if main_menu_button.draw(WIN): main_menu()

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


#Function for main menu:
def main_menu():
    run = True
    while run:
        WIN.blit(BG, (0,0))

        #Title Label
        mainTitle_label = gameFont1.render("FIRST HOPE", 1, (white_color))
        WIN.blit(mainTitle_label, (WIDTH / 2 - mainTitle_label.get_width() / 2, HEIGHT / 2 - mainTitle_label.get_height() / 2))

        #Highscore Label
        highscore_label = gameFont3.render(f"HIGHSCORE: {readFile('gameData.txt', 'highscore')} ", 1, (white_color))
        WIN.blit (highscore_label, (WIDTH/2-highscore_label.get_width()/2, (HEIGHT/2-highscore_label.get_height()/2)+mainTitle_label.get_height() - 30))

        #Play Label
        play_label = gameFont3.render("PLAY", 1, (white_color))
        WIN.blit (play_label, (WIDTH/2-play_label.get_width()/2, (HEIGHT/2-play_label.get_height()/2)+mainTitle_label.get_height()+highscore_label.get_height()))

        #Play Button
        play_button_picture = pygame.transform.scale(pygame.image.load('buttonPicture.png').convert_alpha(), (play_label.get_width(), play_label.get_height() - 10))
        play_button = button.Button((WIDTH/2-play_label.get_width()/2), ((HEIGHT/2-play_label.get_height()/2)+mainTitle_label.get_height()+highscore_label.get_height()), play_button_picture, 1)
        if play_button.draw(WIN): main()

        #Instructions Label
        instructions_label = gameFont3.render("Instructions", 1, (white_color))
        WIN.blit (instructions_label, (WIDTH/2-instructions_label.get_width()/2, (HEIGHT/2-instructions_label.get_height()/2)+mainTitle_label.get_height()+highscore_label.get_height() + play_label.get_height() + 10))

        #Instructions Button
        instructions_picture = pygame.transform.scale(pygame.image.load('buttonPicture.png').convert_alpha(), (instructions_label.get_width(), instructions_label.get_height() - 10))
        instructions_button = button.Button ((WIDTH/2 - instructions_label.get_width()/2), ((HEIGHT/2- instructions_label.get_height()/2)+ mainTitle_label.get_height()+highscore_label.get_height() + play_label.get_height()+ 10), instructions_picture, 1)
        if instructions_button.draw (WIN): instructionsScreen()

        #Space Logs Label
        space_logs_label = gameFont3.render("Space Logs", 1, (white_color))
        WIN.blit (space_logs_label, (WIDTH/2-space_logs_label.get_width()/2, (HEIGHT/2-space_logs_label.get_height()/2)+mainTitle_label.get_height()+highscore_label.get_height() + play_label.get_height() + instructions_label.get_height() + 15))

        #Space Logs button
        space_logs_picture = pygame.transform.scale(pygame.image.load('buttonPicture.png').convert_alpha(), (space_logs_label.get_width(), space_logs_label.get_height() - 10))
        space_logs_button = button.Button ((WIDTH/2 - space_logs_label.get_width()/2), ((HEIGHT/2 - space_logs_label.get_height()/2) + mainTitle_label.get_height()+highscore_label.get_height() + play_label.get_height() + instructions_label.get_height()+ 18), space_logs_picture, 1)
        if space_logs_button.draw (WIN): space_logs_screen() #main () is a place holder for now

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()
main_menu() #Runs game