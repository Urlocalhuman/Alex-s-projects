import time
import random
import subprocess
import sys
import threading

def checkmodules():
    required_modules = ['pygame']
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])
checkmodules()
import pygame



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
STINKYBROWN = (173, 38, 0)





# Define tower class
class Tower:
    def __init__(self, x, y, range, damage, color, cost, sell, canstun=True, charge=False, special="n", slot=0):
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
        self.slot = slot
        if charge == True:
            self.charge = 1200
        self.special = special

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x - 10, self.y - 10, 20, 20))
        if self.selected:
            pygame.draw.rect(screen, RED, (self.x - 15, self.y - 15, 30, 30), 2)
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.range, 1)
    def attack(self, enemies, bullets, extra=""):
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

    def attack(self, enemies, bullets, extra=""):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(GeneralBullet(self.x, self.y, enemy, self.damage, "normal"))
                        break   
    
    def getupgrades(self, gui_x, gui_y, screen):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Shooter (level {self.level})", True, BLACK)
        screen.blit(self.towername, (gui_x+5, gui_y+5))

        if self.level == 0:
            self.text = ["Cost: 100", "+ 1 firerate", "Sell: 58"]
        if self.level == 1:
            self.text = ["Cost: 250", "+ 1 damage", "+ 10 range", "Sell: 91"]
        if self.level == 2:
            self.text = ["Cost: 400", "+ 1 firerate", "+ 2 damage", "+ 15 range", "Sell: 175"]
        if self.level == 3:
            self.text = ["MAX LEVEL", "Sell: 308"]

        for i in range(len(self.text)):
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (gui_x+5, (gui_y+25)+(20*i)))
    
    def upgrade(self, cash):
        if self.level == 0:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 250
                self.shoot_interval -= 1
                self.sell = 91

        elif self.level == 1:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 400
                self.damage += 1
                self.range += 10
                self.sell = 175

        elif self.level == 2:
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

    def attack(self, enemies, bullets, extra=""):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(GeneralBullet(self.x, self.y, enemy, self.damage, "normal"))
                        break     
    def getupgrades(self, gui_x, gui_y, screen):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Archer (level {self.level})", True, BLACK)
        screen.blit(self.towername, (gui_x+5, gui_y+5))

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
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (gui_x+5, (gui_y+25)+(20*i)))
    
    def upgrade(self, cash):
        if self.level == 0:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 400
                self.shoot_interval -= 2
                self.damage += 20
                self.sell = 266

        elif self.level == 1:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1200
                self.damage += 20
                self.range += 30
                self.sell = 400

        elif self.level == 2:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 800
                self.range += 30
                self.shoot_interval -= 6
                self.damage += 30
                self.sell = 308

        elif self.level == 3:
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

    def attack(self, enemies, bullets, extra=""):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(GeneralBullet(self.x, self.y, enemy, self.damage, "normal"))
                        break

    def getupgrades(self, gui_x, gui_y, screen):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Rifleman (level {self.level})", True, BLACK)
        screen.blit(self.towername, (gui_x+5, gui_y+5))

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
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (gui_x+5, (gui_y+25)+(20*i)))
    
    def upgrade(self, cash):
        if self.level == 0:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 650
                self.range += 10
                self.sell = 433

        elif self.level == 1:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1000
                self.damage += 4
                self.range += 20
                self.sell = 650

        elif self.level == 2:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1100
                self.range += 10
                self.shoot_interval -= 1
                self.sell = 983

        elif self.level == 3:
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

    def attack(self, enemies, bullets, extra=""):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(MeleeAttack(self.x, self.y, enemy, self.damage, "normal"))
                        break

    def getupgrades(self, gui_x, gui_y, screen):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Swordsman (level {self.level})", True, BLACK)
        screen.blit(self.towername, (gui_x+5, gui_y+5))

        if self.level == 0:
            self.text = ["Cost: 1000", "+ 5 range", "+ 4 damage" , "Sell: 366"]
        if self.level == 1:
            self.text = ["Cost: 1400", "+ 4 damage", "+ 1 firerate", "Sell: 700"]
        if self.level == 2:
            self.text = ["Cost: 2500", "+ 2 firerate", "+ 10 range", "+ 6 damage", "Sell: 1166"]
        if self.level == 3:
            self.text = ["MAX LEVEL", "Sell: 2000"]

        for i in range(len(self.text)):
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (gui_x+5, (gui_y+25)+(20*i)))
    
    def upgrade(self, cash):
        if self.level == 0:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1400
                self.range += 5
                self.damage + 4
                self.sell = 700

        elif self.level == 1:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 2500
                self.damage += 4
                self.shoot_interval -= 1
                self.sell = 1166

        elif self.level == 2:
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

    def attack(self, enemies, bullets, extra=""):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(GeneralBullet(self.x, self.y, enemy, self.damage, "normal"))
                        break

    def getupgrades(self, gui_x, gui_y, screen):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Turret (level {self.level})", True, BLACK)
        screen.blit(self.towername, (gui_x+5, gui_y+5))

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
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (gui_x+5, (gui_y+25)+(20*i)))
    
    def upgrade(self, cash):
        if self.level == 0:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1000
                self.range += 20
                self.sell = 1766

        elif self.level == 1:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 2500
                self.damage += 3
                self.sell = 2100

        elif self.level == 2:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 4000
                self.range += 10
                self.damage += 7
                self.canstun = False
                self.sell = 2933
        
        elif self.level == 3:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 12000
                self.range += 20
                self.damage += 5
                self.sell = 4266

        elif self.level == 4:
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

    def attack(self, enemies, bullets, extra=""):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(GeneralBullet(self.x, self.y, enemy, self.damage, "ice", self.power))
                        break

    def getupgrades(self, gui_x, gui_y, screen):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Ice Blaster (level {self.level})", True, BLACK)
        screen.blit(self.towername, (gui_x+5, gui_y+5))

        if self.level == 0:
            self.text = ["Cost: 200", "+ 2 firerate", "Sell: 500"]
        if self.level == 1:
            self.text = ["Cost: 400", "+ 4 damage", "+ 10 range", "Sell: 566"]
        if self.level == 2:
            self.text = ["Cost: 1000", "+ 2 firerate", "+ Stronger slowing", "+ 15 range", "Sell: 700"]
        if self.level == 3:
            self.text = ["MAX LEVEL", "Sell: 1033"]

        for i in range(len(self.text)):
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (gui_x+5, (gui_y+25)+(20*i)))
    
    def upgrade(self, cash):
        if self.level == 0:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 400
                self.shoot_interval -= 2
                self.sell = 566

        elif self.level == 1:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1000
                self.damage += 4
                self.range += 10
                self.sell = 700

        elif self.level == 2:
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

    def getupgrades(self, gui_x, gui_y, screen):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Confusion bomber (level {self.level})", True, BLACK)
        screen.blit(self.towername, (gui_x+5, gui_y+5))

        if self.level == 0:
            self.text = ["Cost: 800", "+ 5 firerate", "+ 10 range", "Sell: 833"]
        if self.level == 1:
            self.text = ["Cost: 1000", "+ 4 damage", "+ 15 range", "Sell: 1100"]
        if self.level == 2:
            self.text = ["Cost: 1400", "+ 5 firerate", "+ Stronger confusion", "+ 15 range", "Sell: 1433"]
        if self.level == 3:
            self.text = ["MAX LEVEL", "Sell: 1900"]

        for i in range(len(self.text)):
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (gui_x+5, (gui_y+25)+(20*i)))
    
    def upgrade(self, cash):
        if self.level == 0:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1000
                self.shoot_interval -= 5
                self.range += 10
                self.sell = 1100

        elif self.level == 1:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1400
                self.damage += 4
                self.range += 15
                self.sell = 1433

        elif self.level == 2:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 0
                self.range += 15
                self.power += 1
                self.shoot_interval -= 5
                self.sell = 1900
        return cash
  
class Sentry(Tower):
    def __init__(self, x, y, lv, slot):
        super().__init__(x, y, 0, 0, DARKGRAY, 0, 0, canstun=False, special="s")
        self.lv = lv
        self.slot = slot
        if self.lv == 0:
            self.shoot_interval = 10
            self.damage = 3
            self.range = 80
            self.hp = 30
            self.max_time = 300
        elif self.lv == 1:
            self.shoot_interval = 10
            self.damage = 5
            self.range = 90
            self.hp = 40
            self.max_time = 600
        elif self.lv == 2:
            self.shoot_interval = 4
            self.damage = 6
            self.range = 110
            self.hp = 120
            self.max_time = 1000
        elif self.lv == 3:
            self.shoot_interval = 5
            self.damage = 25
            self.range = 140
            self.hp = 300
            self.max_time = 1300
        elif self.lv == 4:
            self.shoot_interval = 2
            self.damage = 18
            self.range = 190
            self.max_time = 2000
            self.hp = 350
        self.last_shot = 0
        self.time = 0

    def tick(self):
        self.time += 1

    def attack(self, enemies, bullets):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(GeneralBullet(self.x, self.y, enemy, self.damage, "normal"))
                        break   
    
    def getupgrades(self, gui_x, gui_y, screen):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Sentry (level {self.lv}) from id {self.slot}", True, BLACK)
        screen.blit(self.towername, (gui_x+5, gui_y+5))

        self.text = ["No upgrades", f"Time left: {(self.max_time-self.time)}", f"HP: {self.hp}"]

        for i in range(len(self.text)):
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (gui_x+5, (gui_y+25)+(20*i)))
    
    def upgrade(self, cash):
        pass


class Engineer(Tower):
    def __init__(self, x, y, slot):
        super().__init__(x, y, 120, 16, RED, 600, 266, special="e", slot=slot)
        self.shoot_interval = 14
        self.last_shot = 0
        self.scrap = 0
        self.maxscrap = 64
        self.sentries = 0
        self.maxsentries = 1
        self.sentrylv = 0

    def attack(self, enemies, bullets):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(GeneralBullet(self.x, self.y, enemy, self.damage, "normal"))
                        self.scrap += (self.damage/2)
                        if self.scrap >= self.maxscrap:
                            self.scrap = self.maxscrap
                        break
                    

    def getupgrades(self, gui_x, gui_y, screen):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Engineer {self.slot} (level {self.level})", True, BLACK)
        screen.blit(self.towername, (gui_x+5, gui_y+5))

        if self.level == 0:
            self.text = ["Cost: 600", "+ 4 damage", "2 max sentries", "Sell: 266", f"Current scrap: {self.scrap}/{self.maxscrap}"]
        if self.level == 1:
            self.text = ["Cost: 1000", "+ 5 damage", "+ 10 range", "96 max scrap", "better sentries", "Sell: 466", f"Current scrap: {self.scrap}/{self.maxscrap}"]
        if self.level == 2:
            self.text = ["Cost: 4000", "+ 1 firerate", "+ 10 range", "+ 5 damage", "4 max sentries", "minigun sentry", "120 max scrap", "Sell: 800", f"Current scrap: {self.scrap}/{self.maxscrap}"]
        if self.level == 3:
            self.text = ["Cost: 8000", "+10 damage", "+ 20 range", "powerhouse sentry", "240 max scrap", "6 max sentries", "Sell: 2133", f"Current scrap: {self.scrap}/{self.maxscrap}"]
        if self.level == 4:
            self.text = ["Cost: 16000", "+1 firerate", "+ 25 damage", "+ 20 range", "460 max scrap", "max level sentry", "8 max sentries", "Sell: 4800", f"Current scrap: {self.scrap}/{self.maxscrap}"]
        if self.level == 5:
            self.text = ["MAX LEVEL", "Sell: 10133", f"Current scrap: {self.scrap}/{self.maxscrap}"]

        for i in range(len(self.text)):
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (gui_x+5, (gui_y+25)+(20*i)))
    
    def upgrade(self, cash):
        if self.level == 0:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 1000
                self.damage += 4
                self.maxsentries = 2
                self.sell = 466

        elif self.level == 1:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 4000
                self.range += 10
                self.damage += 5
                self.maxscrap = 96
                self.sentrylv += 1
                self.sell = 800

        elif self.level == 2:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 8000
                self.range += 10
                self.shoot_interval += 1
                self.damage += 5
                self.maxsentries = 4
                self.maxscrap = 120
                self.sentrylv = 2
                self.sell = 2133
        
        elif self.level == 3:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 16000
                self.range += 20
                self.damage += 10
                self.maxsentries = 6
                self.maxscrap = 240
                self.sentrylv = 3
                self.sell = 4800

        elif self.level == 4:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 0
                self.range += 20
                self.damage += 25
                self.shoot_interval -= 1
                self.maxscrap= 460
                self.maxsentries = 8
                self.sentrylv = 4
                self.sell = 10133
        return cash

class MilBase(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 0, BROWN, 100, 1100, canstun=False, special="u")
        self.lastsummon = 0
        self.summontime = 800
        self.unitlevel = 0
        self.secondsummontime = 0
        self.doublesummon = False
        self.ondoublesummon = False

    def attack(self, enemies, bullets, extra=[]):
        units=extra[0]
        map_paths = extra[1]
        selected_map = [extra[2]]
        if self.lastsummon >= self.summontime:
            if self.unitlevel == 0:
                units.append(Unit(map_paths[selected_map], 20, 3, DARKGRAY, "Jeep lv0", 0, 20, 100))
            elif self.unitlevel == 1:
                units.append(Unit(map_paths[selected_map], 80, 3, DARKGRAY, "Jeep lv1", 0, 20, 100))
            elif self.unitlevel == 2:
                units.append(Unit(map_paths[selected_map], 120, 3, DARKGRAY, "Jeep lv2", 5, 200, 11))
            elif self.unitlevel == 3:
                units.append(Unit(map_paths[selected_map], 1400, 2, STINKYBROWN, "Tank", 60, 220, 14))
            elif self.unitlevel == 4:
                units.append(Unit(map_paths[selected_map], 1600, 1, GRAY, "War machine tank", 7, 220, 3))               
            self.lastsummon = 0
            if self.doublesummon:
                self.ondoublesummon = True
        else:
            self.lastsummon += 1

        if self.ondoublesummon and self.secondsummontime == 30:
            if self.unitlevel == 3:
                units.append(Unit(map_paths[selected_map], 1400, 2, STINKYBROWN, "Tank", 60, 220, 14))
            elif self.unitlevel == 4:
                units.append(Unit(map_paths[selected_map], 1600, 1, GRAY, "War machine tank", 7, 220, 3)) 
            self.ondoublesummon = False
            self.secondsummontime = 0
        elif self.ondoublesummon:
            self.secondsummontime += 1

        return units           
    
    def getupgrades(self, gui_x, gui_y, screen):
        self.font = pygame.font.Font(None, 25)
        self.towername = self.font.render(f"Military Base (level {self.level})", True, BLACK)
        screen.blit(self.towername, (gui_x+5, gui_y+5))

        if self.level == 0:
            self.text = ["Cost: 100", "Shorter summoning time", f"Summoning time: {self.lastsummon}/{self.summontime}"]
        elif self.level == 1:
            self.text = ["Cost: 400", "Stronger jeeps", f"Summoning time: {self.lastsummon}/{self.summontime}"]
        elif self.level == 2:
            self.text = ["Cost: 1200", "Stronger jeeps", "Shorter summoning time", f"Summoning time: {self.lastsummon}/{self.summontime}"] 
        elif self.level == 3:
            self.text = ["Cost: 4000", "Unlocks tanks", f"Summoning time: {self.lastsummon}/{self.summontime}"]
        elif self.level == 4:
            self.text = ["Cost: 2000", "Double summons", f"Summoning time: {self.lastsummon}/{self.summontime}"]           
        elif self.level == 5:
            self.text = ["Cost: 9000", "Unlocks war machine tanks", f"Summoning time: {self.lastsummon}/{self.summontime}"]
        elif self.level == 6:        
            self.text = ["MAX LEVEL", "Sell: 3000", f"Summoning time: {self.lastsummon}/{self.summontime}"]
        for i in range(len(self.text)):
            screen.blit(self.font.render(self.text[i] ,True, BLACK), (gui_x+5, (gui_y+25)+(20*i)))
    
    def upgrade(self, cash):
        if self.level == 0:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.cost = 400
                self.summontime = 730
                self.sell = 1133
        
        elif self.level == 1:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.unitlevel = 1
                self.cost = 1200
                self.sell = 1266

        elif self.level == 2:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.unitlevel = 2
                self.summontime = 660
                self.cost = 4000
                self.sell = 1666

        elif self.level == 3:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.unitlevel = 3
                self.cost = 0
                self.summontime = 2600
                self.sell = 3000 

        elif self.level == 4:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.doublesummon = True
                self.cost = 9000
                self.sell = 3000 

        elif self.level == 5:
            if cash >= self.cost:
                cash -= self.cost
                self.level += 1
                self.unitlevel = 4
                self.cost = 0
                self.sell = 3000 
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
        self.direction = "f"
        self.backtime = 0   

    def move(self):
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            dx, dy = target_x - self.x, target_y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance != 0:
                dx, dy = dx / distance, dy / distance
                if self.direction == "b":
                    self.x -= dx * self.speed
                    self.y -= dy * self.speed
                    self.backtime -= 1
                    if self.backtime == 0:
                        self.direction = "f"
                else:
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
        self.speed = 5
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
                self.target.backtime += (self.power*80 + round((35*self.power)/self.target.speed))
                self.target.direction = "b"
                if self.target.path_index <= -1:
                    self.target.path_index = 0
                        
            elif self.type == "ice":
                if self.target.speed > 0 and self.target.speed > self.power:
                    self.target.speed -= self.power

            return True
        return False


    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 3)





class Unit(Tower):
    def __init__(self, path, max_health, speed, color, name, damage, range, firerate):
        super().__init__(0, 0, range, damage, color, 0, 0)
        self.shoot_interval = firerate
        self.last_shot = 0
        self.path = path
        self.health = self.max_health = max_health
        self.speed = speed
        self.color = color
        self.path_index = len(self.path) - 1
        self.x, self.y = self.path[self.path_index]
        self.name = name
  

    def move(self):
        if self.path_index != 0:
            target_x, target_y = self.path[self.path_index - 1]
            dx, dy = target_x - self.x, target_y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance != 0:
                dx, dy = dx / distance, dy / distance
                self.x += dx * self.speed
                self.y += dy * self.speed                   

                if abs(self.x - target_x) < self.speed and abs(self.y - target_y) < self.speed:
                    self.path_index -= 1
            else:
                self.path_index -= 1
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
        pygame.draw.circle(screen, self.color, (self.x + 10, self.y + 10), self.range, 1)

    def attack(self, enemies, bullets, extra=""):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            shotfired = False
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(GeneralBullet(self.x, self.y, enemy, self.damage, "normal"))
                        shotfired = True
                        break
            return shotfired
                    


class GeneralBullet(Bullet):
    def __init__(self, x, y, target, damage, type, power=1):
        super().__init__(x, y, target, damage, type, power)
        self.speed = 5 + 5

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 3)

class MeleeAttack(Bullet):
    def __init__(self, x, y, target, damage, type):
        super().__init__(x, y, target, damage, type)
        self.speed = 5 + 10

    def draw(self, screen):
        pygame.draw.circle(screen, BROWN, (int(self.x), int(self.y)), 5)







def main_screen(screen):
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


def shop_screen(screen):
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

class main:
    def __init__(self):
        print("Alex's tower defence")
        time.sleep(1)
        print("version v0.8rBROKEN")
        self.gamemode = "normal"
        self.speed = 10
        self.enemy_spawn_time = 20
        self.heal_time = 0
        self.spawn_time = 0
        self.buff_time = 0
        self.lastupgradetime = 0
        self.towerselected = False
        self.moving_ui = False
        self.gui_x = 50
        self.gui_y = 120
        self.devmode = False



        while True:
            do = input("start or help? (s/h)").lower()
            if do == "s":
                break
            elif do == "h":
                print("Use keys 1-9 to switch between towers. ")
                print("Click to place a tower. ")
                print("Click on a tower to select it and view its upgrades. ")
                print("Use 'u' to upgrade a selected tower, and use 'x' to sell it. ")
                print("Use 'd' to deselect a tower. ")
                print("Use 'm' to move the upgrade gui")
            elif do == "d":
                print("Devmode enabled. IMPORTANT: PROGRESS WILL NOT BE SAVED IN DEVMODE! ")
                self.devmode = True
        # Initialize screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Alex's tower defense")

        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()
        self.placelimits = {"1": 25, "2": 5, "3": 5, "4": 12, "5": 8, "6": 20, "7": 2, "8": 5, "9": 3}
        self.placed = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0}
        # Game variables
        self.cash = 400
        self.towers = []
        self.enemies = []
        self.bullets = []
        self.units = []
        self.enemy_spawn_timer = 0
        self.selected_map = None
        self.selected_tower = None
        self.base_health = 200
        self.current_wave = 0
        self.wave_started = False
        self.wave_timer = 0
        self.tower_selection = 1
        self.running = True
        self.waves = []
        # Define paths for maps
        self.map_paths = [
            [(0, 300), (200, 300), (200, 100), (700, 100), (700, 500), (200, 500), (200, 300), (400, 300), (750, 200), (750, 400), (700, 400), (400, 400), (400, 150), (800, 150)],
            [(0, 300), (800, 400)]
        ]



    def draw_path(self, map_index):
        self.screen.fill(GRAY)
        path = self.map_paths[map_index]
        for i in range(len(path) - 1):
            pygame.draw.line(self.screen, BLACK, path[i], path[i + 1], 5)

    def start_wave(self):
        self.wave_started = True
        self.enemy_spawn_timer = 0
        self.current_wave += 1

    #units.append(Unit(map_paths[selected_map], 500, 1, RED, "Unit", 5, 250, 9))

    #            {"normal": 0, "fast": 0, "heavy": 0, "boss": 0, "electro": 0, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 0, "jester": 0},
    #blank wave template
    # Wave definitions
    def newwaves(self):
        if self.gamemode == "normal":
            self.waves = [
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
                {"normal": 0, "fast": 0, "heavy": 0, "boss": 0, "electro": 0, "giant": 0, "rusher": 0, "healer": 0, "shielded": 0, "necro": 0, "titan": 1, "jester": 1}, #24
                {"normal": 0, "fast": 0, "heavy": 0, "boss": 0, "electro": 0, "giant": 0, "rusher": 20, "healer": 3, "shielded": 8, "necro": 3, "titan": 1, "jester": 2}, #25
                {"normal": 0, "fast": 0, "heavy": 0, "boss": 0, "electro": 0, "giant": 3, "rusher": 20, "healer": 6, "shielded": 6, "necro": 1, "titan": 2, "jester": 2}, #26
                {"normal": 5, "fast": 6, "heavy": 7, "boss": 3, "electro": 8, "giant": 4, "rusher": 9, "healer": 4, "shielded": 10, "necro": 2, "titan": 2, "jester": 2}, #27   


                # More waves can be added here
            ]


    def spawn_enemies(self):
        if self.current_wave > len(self.waves):
            self.wave_started = False
            return

        self.wave = self.waves[self.current_wave - 1]       
        if self.gamemode == "normal":
            if self.wave["normal"] > 0:
                self.enemies.append(Enemy(self.map_paths[self.selected_map], 4, 4, GREEN, 2, "Normal", 0, "n"))
                self.wave["normal"] -= 1
            if self.wave["normal"] == 0:
                if self.wave["fast"] > 0:
                    self.enemies.append(Enemy(self.map_paths[self.selected_map], 3, 6, LIGHTBLUE, 5, "Fast", 0, "n"))
                    self.wave["fast"] -= 1

                if self.wave["fast"] == 0:
                    if self.wave["heavy"] > 0:
                        self.enemies.append(Enemy(self.map_paths[self.selected_map], 12, 3, GBROWN, 15, "Heavy", 10, "n"))
                        self.wave["heavy"] -= 1

                    if self.wave["heavy"] == 0:
                        if self.wave["boss"] > 0:
                            self.enemies.append(Enemy(self.map_paths[self.selected_map], 140, 2, DGREEN, 60, "Easy Boss", 0, "n"))
                            self.wave["boss"] -= 1

                        if self.wave["boss"] == 0:
                            if self.wave["electro"] > 0:
                                self.enemies.append(Enemy(self.map_paths[self.selected_map], 60, 8, YELLOW, 40, "Electro", 0, "n"))
                                self.wave["electro"] -= 1

                            if self.wave["electro"] == 0:
                                if self.wave["giant"] > 0:
                                    self.enemies.append(Enemy(self.map_paths[self.selected_map], 1750, 1, DARKGRAY, 250, "Giant Boss", 20, "n"))
                                    self.wave["giant"] -= 1
                                            
                                if self.wave["giant"] == 0:
                                    if self.wave["rusher"] > 0:
                                        self.enemies.append(Enemy(self.map_paths[self.selected_map], 250, 7, RED, 80, "Rusher", 0, "n"))
                                        self.wave["rusher"] -= 1
                                    
                                    if self.wave["giant"] == 0:
                                        if self.wave["healer"] > 0:
                                            self.enemies.append(Enemy(self.map_paths[self.selected_map], 850, 2, PINK, 100, "Healer", 15, "h"))
                                            self.wave["healer"] -= 1

                                        if self.wave["healer"] == 0:
                                            if self.wave["shielded"] > 0:
                                                self.enemies.append(Enemy(self.map_paths[self.selected_map], 400, 3, GRAY, 120, "Shielded", 60, "n"))
                                                self.wave["shielded"] -= 1

                                            if self.wave["shielded"] == 0:
                                                if self.wave["necro"] > 0:
                                                    self.enemies.append(Enemy(self.map_paths[self.selected_map], 1500, 3, VERYDARKGRAY, 125, "Necromancer", 25, "s"))
                                                    self.wave["necro"] -= 1

                                                if self.wave["necro"] == 0:
                                                    if self.wave["titan"] > 0:
                                                        self.enemies.append(Enemy(self.map_paths[self.selected_map], 17500, 2, BURPLE, 500, "Titan Boss", 50, "n"))
                                                        self.wave["titan"] -= 1

                                                    if self.wave["titan"] == 0:
                                                        if self.wave["jester"] > 0:
                                                            self.enemies.append(Enemy(self.map_paths[self.selected_map], 4000, 3, PURPLE, 225, "Jester", 20, "j"))
                                                            self.wave["jester"] -= 1                                                 
        if len(self.enemies) == 0:
            self.wave_started = False
            self.cash += (50 + (self.current_wave * 25))
            if self.current_wave <= 8:
                self.enemy_spawn_timer = 20
            elif self.current_wave == 9:
                self.enemy_spawn_timer = 10
            elif self.current_wave >= 14:
                self.enemy_spawn_timer = 5

    def unit_and_enemies_thread_oh_god_help(self):
        while self.running:
            # Update enemies
            for enemy in self.enemies[:]:
                if enemy.move():
                    self.base_health -= enemy.health
                    self.cash += round(enemy.cash/2)
                    self.enemies.remove(enemy)
                elif enemy.health <= 0:
                    self.cash += enemy.cash
                    self.enemies.remove(enemy)
                elif enemy.type == "h":
                    if self.heal_time >= 150:                        
                        for enemy in self.enemies:
                            enemy.health += round(enemy.max_health/7)
                            if enemy.health > enemy.max_health:
                                enemy.health = enemy.max_health
                        self.heal_time = 0
                    else:
                        self.heal_time += 1

                elif enemy.type == "s":
                    if self.spawn_time >= 200:
                        self.wave = self.waves[self.current_wave - 1]   
                        for i in range(random.randint(6, 10)):
                            spawn_enemy = random.choice(list(self.wave.keys())[:6])
                            self.wave[spawn_enemy] += 1
                            self.spawn_time = 0
                    else:
                        self.spawn_time += 1

                elif enemy.type == "j":
                    if self.buff_time >= 175:
                        buffed_enem = random.randint(0, (len(self.enemies)-1))
                        buff = random.choice(["s", "h", "d"])
                        if buff == "s":
                            self.enemies[buffed_enem].speed += random.randint(1, 2)
                        elif buff == "h":
                            self.enemies[buffed_enem].health += round(self.enemies[buffed_enem].max_health/10)
                        elif buff == "d":
                            self.enemies[buffed_enem].shield += 0.2
                            if self.enemies[buffed_enem].shield >= 1:
                                self.enemies[buffed_enem].shield = 0.8
                        self.buff_time = 0
                    else:
                        self.buff_time += 1

            # Update units
            for unit in self.units:
                unit.attack(self.enemies, self.bullets)
                if unit.move():
                    self.units.remove(unit)
                if unit.health <= 0:
                    self.units.remove(unit)

                for enemy in self.enemies:
                    if abs(enemy.x - unit.x) <= 8 and abs(enemy.y - unit.y) <= 8:
                        if enemy.health >= unit.health:
                            enemy.health -= unit.health
                            self.units.remove(unit)
                            break
                        else:
                            ehp = enemy.health
                            enemy.health -= unit.health
                            unit.health -= ehp


    def towers_and_bullets_thread_oh_god_two_threads_its_going_to_break(self):
        # Update towers
        while self.running:
            for tower in self.towers:
                
                if tower.special == "u":
                    self.units = tower.attack(self.enemies, self.bullets, extra=[self.map_paths, self.selected_map, self.units])
                else:
                    tower.attack(self.enemies, self.bullets, extra=[])

                if tower.special == "s":
                    tower.tick()
                    if tower.time >= tower.max_time:
                        for engineer in self.towers:
                            if engineer.special == "e":
                                if engineer.slot == tower.slot:
                                    engineer.sentries -= 1
                        self.towers.remove(tower)

                if tower.special == "e":
                    if tower.scrap >= tower.maxscrap:
                        if tower.maxsentries > tower.sentries:
                            if random.randint(1, 2) == 1:
                                xpos = random.randint(-30, -10)
                            else:
                                xpos = random.randint(10, 30)

                            if random.randint(1, 2) == 1:
                                ypos = random.randint(-30, -10)
                            else:
                                ypos = random.randint(10, 30)

                            self.towers.append(Sentry(tower.x+xpos, tower.y+ypos, tower.sentrylv, tower.slot))
                            tower.sentries += 1
                            tower.scrap = 0   

            # Update bullets
            for bullet in self.bullets[:]:
                if bullet.move():
                    self.bullets.remove(bullet)



    def start(self):
        self.newwaves()
        self.current_screen = "main"
        
        # new addition that will break everything
        self.unit_enemy_thread = threading.Thread(target=self.unit_and_enemies_thread_oh_god_help, daemon=True)
        self.tower_bullet_thread = threading.Thread(target=self.towers_and_bullets_thread_oh_god_two_threads_its_going_to_break, daemon=True)
        self.unit_enemy_thread.start()
        self.tower_bullet_thread.start()


        # Main game loop
        self.running = True
        while self.running:
            self.screen.fill(WHITE)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    if self.current_screen == "main":
                        if self.selected_map is None:
                            if 150 <= x <= 350 and 200 <= y <= 400:
                                self.selected_map = 0
                            elif 450 <= x <= 650 and 200 <= y <= 400:
                                self.selected_map = 1
                                self.cash = 800
                                self.enemy_spawn_timer = 15
                            elif 300 <= x <= 500 and 450 <= y <= 500:
                                self.current_screen = "shop"
                        else:
                            if not self.moving_ui:
                                for tower in self.towers:
                                    if tower.x - 15 <= x <= tower.x + 15 and tower.y - 15 <= y <= tower.y + 15:
                                        for thing in self.towers:
                                            if thing.selected:
                                                thing.selected = False
                                        tower.selected = True
                                        self.towerselected = True
                                        break

                                if self.placed[f"{self.tower_selection}"] < self.placelimits[f"{self.tower_selection}"] and self.towerselected == False:
                                    if self.tower_selection == 1 and self.cash >= 175:
                                        self.towers.append(Shooter(x, y))
                                        self.placed["1"] += 1
                                        self.cash -= 175
                                    if self.tower_selection == 2 and self.cash >= 2500:
                                        self.towers.append(CBomber(x, y))
                                        self.placed["2"] += 1
                                        self.cash -= 2500    
                                    elif self.tower_selection == 3 and self.cash >= 1500:
                                        self.towers.append(IceBlaster(x, y))
                                        self.placed["3"] += 1
                                        self.cash -= 1500    
                                    elif self.tower_selection == 4 and self.cash >= 500:
                                        self.towers.append(Archer(x, y))
                                        self.placed["4"] += 1
                                        self.cash -= 500
                                    elif self.tower_selection == 5 and self.cash >= 1100:
                                        self.towers.append(Rifleman(x, y))
                                        self.placed["5"] += 1
                                        self.cash -= 1100
                                    elif self.tower_selection == 6 and self.cash >= 1100:
                                        self.towers.append(Swordsman(x, y))
                                        self.placed["6"] += 1
                                        self.cash -= 1100
                                    elif self.tower_selection == 7 and self.cash >= 4800:
                                        self.towers.append(Turret(x, y))
                                        self.placed["7"] += 1
                                        self.cash -= 4800
                                    elif self.tower_selection == 8 and self.cash >= 1200:
                                        self.towers.append(Engineer(x, y, self.placed["8"]))
                                        self.placed["8"] += 1
                                        self.cash -= 1200
                                    elif self.tower_selection == 9 and self.cash >= 3300:
                                        self.towers.append(MilBase(x, y))
                                        self.placed["9"] += 1
                                        self.cash -= 3300
                            else:
                                self.gui_x, self.gui_y = x, y
                                self.moving_ui = False
                    elif self.current_screen == "shop":
                        if 700 <= x <= 780 and 10 <= y <= 50:  # Back button
                            self.current_screen = "main"

                elif event.type == pygame.KEYDOWN:
                    if self.current_screen == "main":
                        if event.key == pygame.K_1:
                            self.tower_selection = 1
                        elif event.key == pygame.K_2:
                            self.tower_selection = 2
                        elif event.key == pygame.K_3:
                            self.tower_selection = 3
                        elif event.key == pygame.K_4:
                            self.tower_selection = 4
                        elif event.key == pygame.K_5:
                            self.tower_selection = 5
                        elif event.key == pygame.K_6:
                            self.tower_selection = 6
                        elif event.key == pygame.K_7:
                            self.tower_selection = 7
                        elif event.key == pygame.K_8:
                            self.tower_selection = 8
                        elif event.key == pygame.K_9:
                            self.tower_selection = 9
                        elif event.key == pygame.K_d:
                            for tower in self.towers:
                                tower.selected = False
                            self.towerselected = False
                        elif event.key == pygame.K_e:
                            if self.lastupgradetime >= 5:
                                for tower in self.towers:
                                    if tower.selected:
                                        self.cash = tower.upgrade(self.cash)
                                self.lastupgradetime = 0
                        elif event.key == pygame.K_x:
                            for tower in self.towers:
                                if tower.selected and tower.special != "s":
                                    self.cash += tower.sell
                                    self.towers.remove(tower)
                                    self.towerselected = False
                        elif event.key == pygame.K_m:
                            self.moving_ui = not self.moving_ui 

                        elif event.key == pygame.K_END:
                            self.base_health = 0

                        elif event.key == pygame.K_F10 and self.devmode:
                            self.cash += 1000
                        elif event.key == pygame.K_F9 and self.devmode:
                            try:
                                exec(input("Waiting for command... >"))
                            except Exception as e:
                                print(f"Error running: {e}")        

            if self.current_screen == "main":
                if self.selected_map is None:
                    self.save_button_rect = main_screen(self.screen)
                else:
                    self.draw_path(self.selected_map)

                    # Manage waves
                    if not self.wave_started:
                        self.wave_timer += 1
                        if self.wave_timer > 120:
                            self.start_wave()
                            self.wave_timer = 0
                    else:
                        self.enemy_spawn_timer += 1
                        if self.enemy_spawn_timer > self.enemy_spawn_time:
                            self.spawn_enemies()
                            self.enemy_spawn_timer = 0

                    # Update enemies
                    for enemy in self.enemies[:]:
                        if enemy.move():
                            self.base_health -= enemy.health
                            self.cash += round(enemy.cash/2)
                            self.enemies.remove(enemy)
                        elif enemy.health <= 0:
                            self.cash += enemy.cash
                            self.enemies.remove(enemy)
                        elif enemy.type == "h":
                            if self.heal_time >= 150:                        
                                for enemy in self.enemies:
                                    enemy.health += round(enemy.max_health/7)
                                    if enemy.health > enemy.max_health:
                                        enemy.health = enemy.max_health
                                self.heal_time = 0
                            else:
                                self.heal_time += 1

                        elif enemy.type == "s":
                            if self.spawn_time >= 200:
                                self.wave = self.waves[self.current_wave - 1]   
                                for i in range(random.randint(6, 10)):
                                    spawn_enemy = random.choice(list(self.wave.keys())[:6])
                                    self.wave[spawn_enemy] += 1
                                    self.spawn_time = 0
                            else:
                                self.spawn_time += 1

                        elif enemy.type == "j":
                            if self.buff_time >= 175:
                                buffed_enem = random.randint(0, (len(self.enemies)-1))
                                buff = random.choice(["s", "h", "d"])
                                if buff == "s":
                                    self.enemies[buffed_enem].speed += random.randint(1, 2)
                                elif buff == "h":
                                    self.enemies[buffed_enem].health += round(self.enemies[buffed_enem].max_health/10)
                                elif buff == "d":
                                    self.enemies[buffed_enem].shield += 0.2
                                    if self.enemies[buffed_enem].shield >= 1:
                                        self.enemies[buffed_enem].shield = 0.8
                                self.buff_time = 0
                            else:
                                self.buff_time += 1

                    # Update units
                    for unit in self.units:
                        unit.attack(self.enemies, self.bullets)
                        if unit.move():
                            self.units.remove(unit)
                        if unit.health <= 0:
                            self.units.remove(unit)

                        for enemy in self.enemies:
                            if abs(enemy.x - unit.x) <= 8 and abs(enemy.y - unit.y) <= 8:
                                if enemy.health >= unit.health:
                                    enemy.health -= unit.health
                                    self.units.remove(unit)
                                    break
                                else:
                                    ehp = enemy.health
                                    enemy.health -= unit.health
                                    unit.health -= ehp
                                        


                    

                    # Draw towers
                    for tower in self.towers:
                        tower.draw(self.screen)

                    # Draw units
                    for unit in self.units:
                        unit.draw(self.screen)

                    # Draw enemies
                    for enemy in self.enemies:
                        enemy.draw(self.screen)

                    # Draw bullets
                    for bullet in self.bullets:
                        bullet.draw(self.screen)

                    # Draw UI
                    font = pygame.font.Font(None, 36)
                    text = font.render(f"Cash: ${self.cash}", True, BLACK)
                    self.screen.blit(text, (10, 10))
                    text = font.render(f"Base Health: {self.base_health}", True, BLACK)
                    self.screen.blit(text, (10, 50))
                    text = font.render(f"Wave: {self.current_wave}", True, BLACK)
                    self.screen.blit(text, (10, 90))

                    # Draw selected tower type
                    if self.tower_selection == 1:
                        text = font.render("Selected Tower: Shooter (175 cash)", True, BLACK)
                    elif self.tower_selection == 2:
                        text = font.render("Selected Tower: Confusion Bomber (2500 cash)", True, BLACK)
                    elif self.tower_selection == 3:
                        text = font.render("Selected Tower: Ice Blaster (1500 cash)", True, BLACK)
                    elif self.tower_selection == 4:
                        text = font.render("Selected Tower: Archer (500 cash)", True, BLACK)
                    elif self.tower_selection == 5:
                        text = font.render("Selected Tower: Rifleman (1100 cash)", True, BLACK)
                    elif self.tower_selection == 6:
                        text = font.render("Selected Tower: Swordsman (1100 cash)", True, BLACK)
                    elif self.tower_selection == 7:
                        text = font.render("Selected Tower: Turret (4800 cash)", True, BLACK)
                    elif self.tower_selection == 8:
                        text = font.render("Selected Tower: Engineer (1200 cash)", True, BLACK)
                    elif self.tower_selection == 9:
                        text = font.render("Selected Tower: Military Base (3300 cash)", True, BLACK)
                    self.screen.blit(text, (200, 10))

                    # upgrades
                    if self.towerselected:
                        pygame.draw.rect(self.screen, DARKGRAY if not self.moving_ui else GRAY, (self.gui_x, self.gui_y, 200, 300))
                        pygame.draw.rect(self.screen, BLACK, (self.gui_x, self.gui_y, 200, 300), 2)
                        pygame.draw.rect(self.screen, GREEN, (self.gui_x, self.gui_y+250, 100, 50))
                        pygame.draw.rect(self.screen, RED, (self.gui_x+100, self.gui_y+250, 100, 50))
                        font2 = pygame.font.Font(None, 25)
                        selldiag = font2.render("Sell (x)", True, BLACK)
                        upgdiag = font2.render("Upgrade (e)", True, BLACK)
                        self.screen.blit(upgdiag, (self.gui_x, self.gui_y+250))
                        self.screen.blit(selldiag, (self.gui_x+100, self.gui_y+250))
                        for tower in self.towers:
                            if tower.selected:
                                tower.getupgrades(self.gui_x, self.gui_y, self.screen)

                    # Check for game over
                    if self.base_health <= 0:
                        self.selected_map = None
                        self.towers.clear()
                        self.enemies.clear()
                        self.bullets.clear()
                        self.current_wave = 0
                        self.base_health = 200
                        self.cash = 400
                        self.wave_started = False
                        self.newwaves()

            elif self.current_screen == "shop":
                shop_screen()  # Ensure shop screen is redrawn each frame


            self.lastupgradetime += 1
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()        


if __name__ == "__main__":
    game = main() # making the main game loop object oriented was a pain in the ass and i will probably regret it in the future
    game.start()
