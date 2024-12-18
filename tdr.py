import time
import random
import os

try:
    import pygame
except ModuleNotFoundError:
    print("Required module missing (pygame), auto installing required module.")
    os.system("py -m pip install pygame")
    import pygame


print("Alex's tower defence")
time.sleep(1)
print("version v0.5.0.1r")
gamemode = "normal"
speed = 10
enemy_spawn_time = 20
heal_time = 0
spawn_time = 0
buff_time = 0
towerselected = False
# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARKGRAY = (100, 100, 100)
LIGHTBLUE = (0, 186, 255)
GBROWN = (77, 57, 23)
DGREEN = (0, 115, 6)
YELLOW = (255, 255, 0)
BROWN = (120, 72, 0)
PINK = (255, 0, 255)
PURPLE = (154, 0, 255)
ICE = (165, 255, 251)
VERYDARKGRAY = (64, 64, 64)
BURPLE = (82, 0, 163)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alex's tower defense")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Define tower class
class Tower:
    def __init__(self, x, y, range, damage, color, cost, sell, canstun=True, charge=False):
        self.x = x
        self.y = y
        self.range = range
        self.damage = damage
        self.level = 0
        self.color = color
        self.selected = False
        self.cost = cost
        self.sell = sell
        self.canstun = canstun
        if charge == True:
            self.charge = 1200

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.range, 1)
        pygame.draw.rect(screen, self.color, (self.x - 10, self.y - 10, 20, 20))
        if self.selected:
            pygame.draw.rect(screen, RED, (self.x - 15, self.y - 15, 30, 30), 2)

    def attack(self, enemies, bullets):
        pass

    def getupgrades(self):
        pass

    def upgrade(self):
        pass
 




class Shooter(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 75, 2, DARKGRAY, 100, 58)
        self.shoot_interval = 10
        self.last_shot = 0

    def attack(self, enemies, bullets):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(GeneralBullet(self.x, self.y, enemy, self.damage, "normal"))
                        break   
    
    def getupgrades(self):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Shooter (level {self.level})", True, BLACK)
        screen.blit(self.towername, (55, 130))

        if self.level == 0:
            self.text = ["Cost: 100", "+ 1 firerate", "Sell: 58"]
        if self.level == 1:
            self.text = ["Cost: 250", "+ 1 damage", "+ 10 range", "Sell: 91"]
        if self.level == 2:
            self.text = ["Cost: 400", "+ 1 firerate", "+ 2 damage", "+ 15 range", "Sell: 175"]
        if self.level == 3:
            self.text = ["MAX LEVEL", "Sell: 308"]

        for i in range(len(self.text)):
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (55, 150+(20*i)))
    
    def upgrade(self, cash):
        if self.level == 0:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 250
                self.shoot_interval -= 1
                self.sell = 91

        if self.level == 1:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 400
                self.damage += 1
                self.range += 10
                self.sell = 175

        if self.level == 2:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 0
                self.range += 15
                self.shoot_interval -= 1
                self.damage += 2
                self.sell = 308
        return cash

    
                


        

class Archer(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 350, 120, BROWN, 300, 166)
        self.shoot_interval = 100
        self.last_shot = 0

    def attack(self, enemies, bullets):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(GeneralBullet(self.x, self.y, enemy, self.damage, "normal"))
                        break     
    def getupgrades(self):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Archer (level {self.level})", True, BLACK)
        screen.blit(self.towername, (55, 130))

        if self.level == 0:
            self.text = ["Cost: 300", "+ 2 firerate", "+ 20 damage", "Sell: 166"]
        if self.level == 1:
            self.text = ["Cost: 400", "+ 20 damage", "+ 30 range", "Sell: 266"]
        if self.level == 2:
            self.text = ["Cost: 1200", "+ 6 firerate", "+ 30 damage", "+ 30 range", "Sell: 400"]
        if self.level == 3:
            self.text = ["Cost: 1300", "+ 12 firerate", "+ 20 range", "Sell: 800"]
        if self.level == 4:
            self.text = ["MAX LEVEL", "Sell: 1233"]

        for i in range(len(self.text)):
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (55, 150+(20*i)))
    
    def upgrade(self, cash):
        if self.level == 0:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 400
                self.shoot_interval -= 2
                self.damage += 20
                self.sell = 266

        if self.level == 1:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1200
                self.damage += 20
                self.range += 30
                self.sell = 400

        if self.level == 2:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 800
                self.range += 30
                self.shoot_interval -= 6
                self.damage += 30
                self.sell = 308

        if self.level == 3:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 0
                self.shoot_interval -= 12
                self.range += 20
                self.sell = 1233
        return cash



class Rifleman(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 125, 12, BLUE, 200, 366)
        self.shoot_interval = 4
        self.last_shot = 0

    def attack(self, enemies, bullets):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(GeneralBullet(self.x, self.y, enemy, self.damage, "normal"))
                        break

    def getupgrades(self):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Rifleman (level {self.level})", True, BLACK)
        screen.blit(self.towername, (55, 130))

        if self.level == 0:
            self.text = ["Cost: 200", "+ 10 range", "Sell: 366"]
        if self.level == 1:
            self.text = ["Cost: 650", "+ 4 damage", "+ 20 range", "Sell: 433"]
        if self.level == 2:
            self.text = ["Cost: 1000", "+ 1 firerate", "+ 10 range", "Sell: 650"]
        if self.level == 3:
            self.text = ["Cost: 1100", "+ 6 damage", "+ 20 range", "Sell: 983"]
        if self.level == 4:
            self.text = ["MAX LEVEL", "Sell: 1350"]

        for i in range(len(self.text)):
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (55, 150+(20*i)))
    
    def upgrade(self, cash):
        if self.level == 0:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 650
                self.range += 10
                self.sell = 433

        if self.level == 1:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1000
                self.damage += 4
                self.range += 20
                self.sell = 650

        if self.level == 2:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1100
                self.range += 10
                self.shoot_interval -= 1
                self.sell = 983

        if self.level == 3:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 0
                self.damage += 6
                self.range += 20
                self.sell = 1350
        return cash


class Swordsman(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 60, WHITE, 1000, 366)
        self.shoot_interval = 10
        self.last_shot = 0

    def attack(self, enemies, bullets):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(MeleeAttack(self.x, self.y, enemy, self.damage, "normal"))
                        break

    def getupgrades(self):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Swordsman (level {self.level})", True, BLACK)
        screen.blit(self.towername, (55, 130))

        if self.level == 0:
            self.text = ["Cost: 1000", "+ 5 range", "+ 4 damage" , "Sell: 366"]
        if self.level == 1:
            self.text = ["Cost: 1400", "+ 4 damage", "+ 1 firerate", "Sell: 700"]
        if self.level == 2:
            self.text = ["Cost: 2500", "+ 2 firerate", "+ 10 range", "+ 6 damage", "Sell: 1166"]
        if self.level == 3:
            self.text = ["MAX LEVEL", "Sell: 2000"]

        for i in range(len(self.text)):
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (55, 150+(20*i)))
    
    def upgrade(self, cash):
        if self.level == 0:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1400
                self.range += 5
                self.damage + 4
                self.sell = 700

        if self.level == 1:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 2500
                self.damage += 4
                self.shoot_interval -= 1
                self.sell = 1166

        if self.level == 2:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 0
                self.range += 10
                self.damage += 6
                self.shoot_interval -= 2
                self.sell = 2000
        return cash



class Turret(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 275, 45, BLACK, 500, 1600)
        self.shoot_interval = 2
        self.last_shot = 0

    def attack(self, enemies, bullets):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(GeneralBullet(self.x, self.y, enemy, self.damage, "normal"))
                        break

    def getupgrades(self):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Turret (level {self.level})", True, BLACK)
        screen.blit(self.towername, (55, 130))

        if self.level == 0:
            self.text = ["Cost: 500", "+ 20 range", "Sell: 1600"]
        if self.level == 1:
            self.text = ["Cost: 1000", "+ 3 damage", "+ 10 range", "Sell: 1766"]
        if self.level == 2:
            self.text = ["Cost: 2500", "Stun immunity", "+ 10 range", "+ 7 damage", "Sell: 2100"]
        if self.level == 3:
            self.text = ["Cost: 4000", "+5 damage", "+ 20 range", "Sell: 2933"]
        if self.level == 4:
            self.text = ["Cost: 12000", "+1 firerate", "+ 10 damage", "+ 20 range", "Sell: 4266"]
        if self.level == 5:
            self.text = ["MAX LEVEL", "Sell: 8266"]

        for i in range(len(self.text)):
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (55, 150+(20*i)))
    
    def upgrade(self, cash):
        if self.level == 0:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1000
                self.range += 20
                self.sell = 1766

        if self.level == 1:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 2500
                self.damage += 3
                self.sell = 2100

        if self.level == 2:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 4000
                self.range += 10
                self.damage += 7
                self.canstun = False
                self.sell = 2933
        
        if self.level == 3:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 12000
                self.range += 20
                self.damage += 5
                self.sell = 4266

        if self.level == 4:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 0
                self.range += 20
                self.damage += 10
                self.shoot_interval -= 1
                self.sell = 8266
        return cash


class IceBlaster(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 4, ICE, 200, 500)
        self.shoot_interval = 30
        self.last_shot = 0
        self.power = 1

    def attack(self, enemies, bullets):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(GeneralBullet(self.x, self.y, enemy, self.damage, "ice", self.power))
                        break

    def getupgrades(self):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Ice Blaster (level {self.level})", True, BLACK)
        screen.blit(self.towername, (55, 130))

        if self.level == 0:
            self.text = ["Cost: 200", "+ 2 firerate", "Sell: 500"]
        if self.level == 1:
            self.text = ["Cost: 400", "+ 4 damage", "+ 10 range", "Sell: 566"]
        if self.level == 2:
            self.text = ["Cost: 1000", "+ 2 firerate", "+ Stronger slowing", "+ 15 range", "Sell: 700"]
        if self.level == 3:
            self.text = ["MAX LEVEL", "Sell: 1033"]

        for i in range(len(self.text)):
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (55, 150+(20*i)))
    
    def upgrade(self, cash):
        if self.level == 0:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 400
                self.shoot_interval -= 2
                self.sell = 566

        if self.level == 1:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1000
                self.damage += 4
                self.range += 10
                self.sell = 700

        if self.level == 2:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 0
                self.range += 15
                self.power += 1
                self.shoot_interval -= 2
                self.sell = 1033
        return cash
                
class CBomber(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 0, PURPLE, 800, 833)
        self.shoot_interval = 40
        self.last_shot = 0
        self.power = 1

    def attack(self, enemies, bullets):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(GeneralBullet(self.x, self.y, enemy, self.damage, "confusion", self.power))
                        break

    def getupgrades(self):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Confusion bomber (level {self.level})", True, BLACK)
        screen.blit(self.towername, (55, 130))

        if self.level == 0:
            self.text = ["Cost: 800", "+ 5 firerate", "+ 10 range", "Sell: 833"]
        if self.level == 1:
            self.text = ["Cost: 1000", "+ 4 damage", "+ 15 range", "Sell: 1100"]
        if self.level == 2:
            self.text = ["Cost: 1400", "+ 5 firerate", "+ Stronger confusion", "+ 15 range", "Sell: 1433"]
        if self.level == 3:
            self.text = ["MAX LEVEL", "Sell: 1900"]

        for i in range(len(self.text)):
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (55, 150+(20*i)))
    
    def upgrade(self, cash):
        if self.level == 0:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1000
                self.shoot_interval -= 5
                self.range += 10
                self.sell = 1100

        if self.level == 1:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1400
                self.damage += 4
                self.range += 15
                self.sell = 1433

        if self.level == 2:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 0
                self.range += 15
                self.power += 1
                self.shoot_interval -= 5
                self.sell = 1900
        return cash
  
# Define enemy class
class Enemy:
    def __init__(self, path, max_health, speed, color, cash, name, shield, type):
        self.path = path
        self.health = self.max_health = max_health
        self.speed = speed
        self.color = color
        self.cash = cash
        self.path_index = 0
        self.speed2 = self.speed
        self.x, self.y = self.path[self.path_index]
        self.name = name
        self.shield = shield/100
        self.type = type   

    def move(self):
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            dx, dy = target_x - self.x, target_y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance != 0:
                dx, dy = dx / distance, dy / distance
                self.x += dx * self.speed
                self.y += dy * self.speed

                if abs(self.x - target_x) < self.speed and abs(self.y - target_y) < self.speed:
                    self.path_index += 1
            else:
                self.path_index += 1
        else:
            return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 20, 20))
        pygame.draw.rect(screen, BLACK, (self.x , self.y , 21, 21), 2)
        health_bar_width = 60
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.x - 10, self.y - 20, health_bar_width, 5))
        pygame.draw.rect(screen, GREEN, (self.x - 10, self.y - 20, health_bar_width * health_ratio, 5))
        font = pygame.font.Font(None, 18)
        text = font.render(f"{int(self.health)}/{self.max_health} {self.name}", True, BLACK)
        screen.blit(text, (self.x - 10, self.y - 35))

# Define bullet class
class Bullet:
    def __init__(self, x, y, target, damage, type, power=1):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = speed
        self.type = type
        self.power = power

    def move(self):
        dx, dy = self.target.x - self.x, self.target.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance != 0:
            dx, dy = dx / distance, dy / distance
            self.x += dx * self.speed
            self.y += dy * self.speed

        if abs(self.x - self.target.x) < self.speed and abs(self.y - self.target.y) < self.speed:
            self.target.health -= round(self.damage - (self.damage * self.target.shield))
            if self.type == "confusion":
                if self.target.path_index >= 0 and self.path_index >= self.power:
                    self.target.path_index -= self.power
            elif self.type == "ice":
                self.target.speed -= 2
                if self.target.speed >= 0 and self.target.speed >= self.power:
                    self.target.speed -= self.power

            return True
        return False


    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 3)



class GeneralBullet(Bullet):
    def __init__(self, x, y, target, damage, type, power=1):
        super().__init__(x, y, target, damage, type, power)
        self.speed = speed + 5

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 3)

class MeleeAttack(Bullet):
    def __init__(self, x, y, target, damage, type):
        super().__init__(x, y, target, damage, type)
        self.speed = speed + 10

    def draw(self, screen):
        pygame.draw.circle(screen, BROWN, (int(self.x), int(self.y)), 5)

# Define paths for maps
map_paths = [
    [(0, 300), (200, 300), (200, 100), (700, 100), (700, 500), (200, 500), (200, 300), (400, 300), (750, 200), (750, 400), (700, 400), (400, 400), (400, 150), (800, 150)],
    [(0, 300), (800, 400)]
]

# Game variables
cash = 400
towers = []
enemies = []
bullets = []
enemy_spawn_timer = 0
selected_map = None
selected_tower = None
base_health = 200
current_wave = 0
wave_started = False
wave_timer = 0
tower_selection = 1
waves = []

#            {"normal": 0, "fast": 0, "heavy": 0, "boss": 0, "electro": 0, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0},
#blank wave template
# Wave definitions
def newwaves():
    global gamemode, waves
    if gamemode == "normal":
        waves = [
            {"normal": 3, "fast": 0, "heavy": 0, "boss": 0, "electro": 0, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #1
            {"normal": 5, "fast": 0, "heavy": 0, "boss": 0, "electro": 0, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #2
            {"normal": 6, "fast": 2, "heavy": 0, "boss": 0, "electro": 0, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #3
            {"normal": 12, "fast": 8, "heavy": 0, "boss": 0, "electro": 0, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #4
            {"normal": 3, "fast": 0, "heavy": 6, "boss": 0, "electro": 0, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #5
            {"normal": 8, "fast": 5, "heavy": 3, "boss": 0, "electro": 0, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #6
            {"normal": 4, "fast": 3, "heavy": 6, "boss": 1, "electro": 0, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #7
            {"normal": 0, "fast": 22, "heavy": 8, "boss": 0, "electro": 0, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #8
            {"normal": 0, "fast": 10, "heavy": 0, "boss": 2, "electro": 0, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #9
            {"normal": 16, "fast": 12, "heavy": 20, "boss": 1, "electro": 0, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #10
            {"normal": 0, "fast": 40, "heavy": 0, "boss": 4, "electro": 0, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #11
            {"normal": 12, "fast": 8, "heavy": 18, "boss": 1, "electro": 4, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #12
            {"normal": 0, "fast": 10, "heavy": 0, "boss": 12, "electro": 8, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #13
            {"normal": 0, "fast": 0, "heavy": 0, "boss": 2, "electro": 4, "giant": 1, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #14
            {"normal": 0, "fast": 10, "heavy": 0, "boss": 0, "electro": 20, "giant": 0, "rusher": 5, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #15
            {"normal": 0, "fast": 0, "heavy": 15, "boss": 20, "electro": 0, "giant": 2, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #16
            {"normal": 0, "fast": 0, "heavy": 0, "boss": 0, "electro": 0, "giant": 3, "rusher": 7, "healer": 1, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #17
            {"normal": 0, "fast": 0, "heavy": 0, "boss": 0, "electro": 10, "giant": 4, "rusher": 0, "healer": 1, "shielded": 2, "necro": 0, "titan": 0, "jester": 0}, #18   
            {"normal": 0, "fast": 0, "heavy": 0, "boss": 0, "electro": 0, "giant": 10, "rusher": 0, "healer": 1, "shielded": 8, "necro": 0, "titan": 0, "jester": 0}, #19
            {"normal": 0, "fast": 0, "heavy": 0, "boss": 0, "electro": 10, "giant": 0, "rusher": 10, "healer": 1, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #20
            {"normal": 8, "fast": 4, "heavy": 10, "boss": 2, "electro": 6, "giant": 2, "rusher": 12, "healer": 0, "shielded": 4, "necro": 0, "titan": 0, "jester": 0}, #21
            {"normal": 0, "fast": 0, "heavy": 0, "boss": 0, "electro": 0, "giant": 0, "rusher": 22, "healer": 2, "shielded": 0, "necro": 0, "titan": 0, "jester": 0}, #22
            {"normal": 0, "fast": 0, "heavy": 0, "boss": 0, "electro": 0, "giant": 4, "rusher": 0, "healer": 1, "shielded": 0, "necro": 1, "titan": 0, "jester": 0}, #23
            {"normal": 0, "fast": 0, "heavy": 0, "boss": 0, "electro": 0, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 2, "jester": 1}, #24
            {"normal": 0, "fast": 0, "heavy": 0, "boss": 0, "electro": 0, "giant": 0, "rusher": 20, "healer": 3, "shielded": 8, "necro": 3, "titan": 1, "jester": 2}, #25
            # More waves can be added here
        ]

#i nearly forgot to call the newwaves function lol
newwaves()


def main_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Select a Map", True, BLACK)
    screen.blit(text, (250, 50))

    font = pygame.font.Font(None, 36)
    
    # Map 1 button
    text1 = font.render("1", True, BLACK)
    pygame.draw.rect(screen, GREEN, (150, 200, 200, 200))
    screen.blit(text1, (250, 300))
    
    # Map 2 button
    text2 = font.render("2", True, BLACK)
    pygame.draw.rect(screen, BLUE, (450, 200, 200, 200))
    screen.blit(text2, (550, 300))

    # Shop button
    text_shop = font.render("Shop", True, BLACK)
    pygame.draw.rect(screen, RED, (300, 450, 200, 50))
    screen.blit(text_shop, (370, 460))

    #Save button
    text_save = font.render("Save", True, BLACK)
    pygame.draw.rect(screen, GRAY, (100, 100, 100, 100))
    screen.blit(text_save, (370, 460))

    pygame.display.flip()

def draw_path(map_index):
    screen.fill(GRAY)
    path = map_paths[map_index]
    for i in range(len(path) - 1):
        pygame.draw.line(screen, BLACK, path[i], path[i + 1], 5)

def start_wave():
    global wave_started, enemy_spawn_timer, current_wave
    wave_started = True
    enemy_spawn_timer = 0
    current_wave += 1

def spawn_enemies():
    global wave_started, cash, enemy_spawn_timer
    if current_wave > len(waves):
        wave_started = False
        return

    wave = waves[current_wave - 1]       
    if gamemode == "normal":
        if wave["normal"] > 0:
            enemies.append(Enemy(map_paths[selected_map], 4, 4, GREEN, 2, "Normal", 0, "n"))
            wave["normal"] -= 1
        if wave["normal"] == 0:
            if wave["fast"] > 0:
                enemies.append(Enemy(map_paths[selected_map], 3, 6, LIGHTBLUE, 5, "Fast", 0, "n"))
                wave["fast"] -= 1

            if wave["fast"] == 0:
                if wave["heavy"] > 0:
                    enemies.append(Enemy(map_paths[selected_map], 12, 3, GBROWN, 15, "Heavy", 10, "n"))
                    wave["heavy"] -= 1

                if wave["heavy"] == 0:
                    if wave["boss"] > 0:
                        enemies.append(Enemy(map_paths[selected_map], 140, 2, DGREEN, 60, "Easy Boss", 0, "n"))
                        wave["boss"] -= 1

                    if wave["boss"] == 0:
                        if wave["electro"] > 0:
                            enemies.append(Enemy(map_paths[selected_map], 60, 8, YELLOW, 40, "Electro", 0, "n"))
                            wave["electro"] -= 1

                        if wave["electro"] == 0:
                            if wave["giant"] > 0:
                                enemies.append(Enemy(map_paths[selected_map], 1750, 1, DARKGRAY, 250, "Giant Boss", 20, "n"))
                                wave["giant"] -= 1
                                        
                            if wave["giant"] == 0:
                                if wave["rusher"] > 0:
                                    enemies.append(Enemy(map_paths[selected_map], 250, 7, RED, 80, "Rusher", 0, "n"))
                                    wave["rusher"] -= 1
                                
                                if wave["giant"] == 0:
                                    if wave["healer"] > 0:
                                        enemies.append(Enemy(map_paths[selected_map], 850, 2, PINK, 100, "Healer", 15, "h"))
                                        wave["healer"] -= 1

                                    if wave["healer"] == 0:
                                        if wave["shielded"] > 0:
                                            enemies.append(Enemy(map_paths[selected_map], 400, 3, GRAY, 120, "Shielded", 60, "n"))
                                            wave["shielded"] -= 1

                                        if wave["shielded"] == 0:
                                            if wave["necro"] > 0:
                                                enemies.append(Enemy(map_paths[selected_map], 1500, 3, VERYDARKGRAY, 125, "Necromancer", 25, "s"))
                                                wave["necro"] -= 1

                                            if wave["necro"] == 0:
                                                if wave["titan"] > 0:
                                                    enemies.append(Enemy(map_paths[selected_map], 17500, 2, BURPLE, 500, "Titan Boss", 50, "n"))
                                                    wave["titan"] -= 1

                                                if wave["titan"] == 0:
                                                    if wave["jester"] > 0:
                                                        enemies.append(Enemy(map_paths[selected_map], 4000, 3, PURPLE, 225, "Jester", 20, "j"))
                                                        wave["jester"] -= 1                                                 
    if len(enemies) == 0:
        wave_started = False
        cash += (50 + (current_wave * 25))
        if current_wave <= 8:
            enemy_spawn_timer = 20
        elif current_wave == 9:
            enemy_spawn_timer = 10
        elif current_wave >= 14:
            enemy_spawn_timer = 5




def main_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Select a Map", True, BLACK)
    screen.blit(text, (250, 50))

    font = pygame.font.Font(None, 36)
    
    # Map 1 button
    text1 = font.render("1", True, BLACK)
    pygame.draw.rect(screen, GREEN, (150, 200, 200, 200))
    screen.blit(text1, (250, 300))
    
    # Map 2 button
    text2 = font.render("2", True, BLACK)
    pygame.draw.rect(screen, BLUE, (450, 200, 200, 200))
    screen.blit(text2, (550, 300))

    # Shop button
    text_shop = font.render("Shop", True, BLACK)
    pygame.draw.rect(screen, RED, (300, 450, 200, 50))
    screen.blit(text_shop, (370, 460))
    
    # Save button
    save_button_rect = pygame.Rect(10, 10, 100, 50)
    pygame.draw.rect(screen, GRAY, save_button_rect)
    save_text = font.render("Save", True, BLACK)
    screen.blit(save_text, (20, 20))
    
    pygame.display.flip()
    return save_button_rect


def shop_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Shop", True, BLACK)
    screen.blit(text, (350, 50))

    # Display coins
    font = pygame.font.Font(None, 36)
    text_coins = font.render(f"Coins: not implemented", True, BLACK)
    screen.blit(text_coins, (350, 150))
    
    # Back button
    text_back = font.render("Back", True, BLACK)
    pygame.draw.rect(screen, RED, (700, 10, 80, 40))
    screen.blit(text_back, (710, 20))

    pygame.display.flip()

placelimits = {"1": 25, "2": 5, "3": 5, "4": 12, "5": 8, "6": 20, "7": 2}
placed = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0}

current_screen = "main"
# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if current_screen == "main":
                if selected_map is None:
                    if 150 <= x <= 350 and 200 <= y <= 400:
                        selected_map = 0
                    elif 450 <= x <= 650 and 200 <= y <= 400:
                        selected_map = 1
                        cash = 800
                        enemy_spawn_timer = 15
                    elif 300 <= x <= 500 and 450 <= y <= 500:
                        current_screen = "shop"
                else:

                    for tower in towers:
                        if tower.x - 15 <= x <= tower.x + 15 and tower.y - 15 <= y <= tower.y + 15:
                            for thing in towers:
                                if thing.selected:
                                    thing.selected = False
                            tower.selected = True
                            towerselected = True
                            break

                    if placed[f"{tower_selection}"] < placelimits[f"{tower_selection}"] and towerselected == False:
                        if tower_selection == 1 and cash >= 175:
                            towers.append(Shooter(x, y))
                            cash -= 175
                        if tower_selection == 2 and cash >= 2500:
                            towers.append(CBomber(x, y))
                            cash -= 2500    
                        elif tower_selection == 3 and cash >= 1500:
                            towers.append(IceBlaster(x, y))
                            cash -= 1500    
                        elif tower_selection == 4 and cash >= 500:
                            towers.append(Archer(x, y))
                            cash -= 500
                        elif tower_selection == 5 and cash >= 1100:
                            towers.append(Rifleman(x, y))
                            cash -= 1100
                        elif tower_selection == 6 and cash >= 1100:
                            towers.append(Swordsman(x, y))
                            cash -= 1100
                        elif tower_selection == 7 and cash >= 4800:
                            towers.append(Turret(x, y))
                            cash -= 4800


            elif current_screen == "shop":
                if 700 <= x <= 780 and 10 <= y <= 50:  # Back button
                    current_screen = "main"

        elif event.type == pygame.KEYDOWN:
            if current_screen == "main":
                if event.key == pygame.K_1:
                    tower_selection = 1
                elif event.key == pygame.K_2:
                    tower_selection = 2
                elif event.key == pygame.K_3:
                    tower_selection = 3
                elif event.key == pygame.K_4:
                    tower_selection = 4
                elif event.key == pygame.K_5:
                    tower_selection = 5
                elif event.key == pygame.K_6:
                    tower_selection = 6
                elif event.key == pygame.K_7:
                    tower_selection = 7
                elif event.key == pygame.K_d:
                    for tower in towers:
                        tower.selected = False
                    towerselected = False
                elif event.key == pygame.K_e:
                    for tower in towers:
                        if tower.selected:
                            cash = tower.upgrade(cash)
                elif event.key == pygame.K_x:
                    for tower in towers:
                        if tower.selected:
                            cash += tower.sell
                            towers.remove(tower)
                            towerselected = False

                                

    if current_screen == "main":
        if selected_map is None:
            save_button_rect = main_screen()
        else:
            draw_path(selected_map)

            # Manage waves
            if not wave_started:
                wave_timer += 1
                if wave_timer > 120:
                    start_wave()
                    wave_timer = 0
            else:
                enemy_spawn_timer += 1
                if enemy_spawn_timer > enemy_spawn_time:
                    spawn_enemies()
                    enemy_spawn_timer = 0

            # Update enemies
            for enemy in enemies[:]:
                if enemy.move():
                    base_health -= enemy.health
                    cash += round(enemy.cash/2)
                    enemies.remove(enemy)
                elif enemy.health <= 0:
                    cash += enemy.cash
                    enemies.remove(enemy)
                elif enemy.type == "h":
                    if heal_time >= 150:                        
                        for enemy in enemies:
                            enemy.health += round(enemy.max_health/7)
                            if enemy.health > enemy.max_health:
                                enemy.health = enemy.max_health
                        heal_time = 0
                    else:
                        heal_time += 1

                elif enemy.type == "s":
                    if spawn_time >= 200:
                        wave = waves[current_wave - 1]   
                        for i in range(random.randint(6, 10)):
                            spawn_enemy = random.choice(list(wave.keys())[:6])
                            wave[spawn_enemy] += 1
                            spawn_time = 0
                    else:
                        spawn_time += 1

                elif enemy.type == "j":
                    if buff_time >= 175:
                        buffed_enem = random.randint(0, (len(enemies)-1))
                        buff = random.choice(["s", "h", "d"])
                        if buff == "s":
                            enemies[buffed_enem].speed += random.randint(1, 2)
                        elif buff == "h":
                            enemies[buffed_enem].health += round(enemies[buffed_enem].max_health/10)
                        elif buff == "d":
                            enemies[buffed_enem].shield += 0.2
                            if enemies[buffed_enem].shield >= 1:
                                enemies[buffed_enem].shield = 0.8
                        buff_time = 0
                    else:
                        buff_time += 1


            # Update towers
            for tower in towers:
                tower.attack(enemies, bullets, )

            # Update bullets
            for bullet in bullets[:]:
                if bullet.move():
                    bullets.remove(bullet)

            # Draw towers
            for tower in towers:
                tower.draw(screen)

            # Draw enemies
            for enemy in enemies:
                enemy.draw(screen)

            # Draw bullets
            for bullet in bullets:
                bullet.draw(screen)

            # Draw UI
            font = pygame.font.Font(None, 36)
            text = font.render(f"Cash: ${cash}", True, BLACK)
            screen.blit(text, (10, 10))
            text = font.render(f"Base Health: {base_health}", True, BLACK)
            screen.blit(text, (10, 50))
            text = font.render(f"Wave: {current_wave}", True, BLACK)
            screen.blit(text, (10, 90))

            # Draw selected tower type
            if tower_selection == 1:
                text = font.render("Selected Tower: Shooter (175 cash)", True, BLACK)
            elif tower_selection == 2:
                text = font.render("Selected Tower: Confusion Bomber (2500 cash)", True, BLACK)
            elif tower_selection == 3:
                text = font.render("Selected Tower: Ice Blaster (1500 cash)", True, BLACK)
            elif tower_selection == 4:
                text = font.render("Selected Tower: Archer (500 cash)", True, BLACK)
            elif tower_selection == 5:
                text = font.render("Selected Tower: Rifleman (1100 cash)", True, BLACK)
            elif tower_selection == 6:
                text = font.render("Selected Tower: Swordsman (1100 cash)", True, BLACK)
            elif tower_selection == 7:
                text = font.render("Selected Tower: Turret (4800 cash)", True, BLACK)
            screen.blit(text, (200, 10))

            # upgrades
            if towerselected:
                pygame.draw.rect(screen, DARKGRAY, (50, 120, 200, 300))
                pygame.draw.rect(screen, BLACK, (50, 120, 200, 300), 2)
                pygame.draw.rect(screen, GREEN, (50, 370, 100, 50))
                pygame.draw.rect(screen, RED, (150, 370, 100, 50))
                font2 = pygame.font.Font(None, 25)
                selldiag = font2.render("Sell (x)", True, BLACK)
                upgdiag = font2.render("Upgrade (e)", True, BLACK)
                screen.blit(upgdiag, (50, 370))
                screen.blit(selldiag, (150, 370))
                for tower in towers:
                    if tower.selected:
                        tower.getupgrades()

            # Check for game over
            if base_health <= 0:
                selected_map = None
                towers.clear()
                enemies.clear()
                bullets.clear()
                current_wave = 0
                base_health = 200
                cash = 400
                wave_started = False
                newwaves()

    elif current_screen == "shop":
        shop_screen()  # Ensure shop screen is redrawn each frame

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
