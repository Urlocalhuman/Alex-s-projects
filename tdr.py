from os import remove
import pygame
import time
print("Alex's tower defence")
time.sleep(1)
gamemode = "normal"
    
speed = 10

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
PURPLE = (160, 32, 240)
BROWN = (150, 75, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)
DARKGRAY = (100, 100, 100)
BORANGE = (219, 161, 94)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Alex's tower defense")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Define tower class
class Tower:
    def __init__(self, x, y, range, damage, cost, color):
        self.x = x
        self.y = y
        self.range = range
        self.damage = damage
        self.cost = cost
        self.level = 1
        self.selected = False
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.range, 1)
        pygame.draw.rect(screen, self.color, (self.x - 10, self.y - 10, 20, 20))
        if self.selected:
            pygame.draw.rect(screen, RED, (self.x - 15, self.y - 15, 30, 30), 2)

    def attack(self, enemies, bullets):
        pass

    def upgrade(self):
        self.level += 1
        self.range += 20
        self.damage += 5
        self.cost += 50


class Rifleman(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 2, 70, DARKGRAY)
        self.shoot_interval = 15
        self.last_shot = 0

    def attack(self, enemies, bullets):
        self.last_shot += 1
        if self.last_shot >= self.shoot_interval:
            self.last_shot = 0
            for enemy in enemies:
                    if (enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2 <= self.range ** 2:
                        bullets.append(GeneralBullet(self.x, self.y, enemy, self.damage))
                        break    

# Define enemy class
class Enemy:
    def __init__(self, path, max_health, speed, color, cash, name):
        self.path = path
        self.health = self.max_health = max_health
        self.speed = speed
        self.color = color
        self.cash = cash
        self.path_index = 0
        self.speed2 = self.speed
        self.x, self.y = self.path[self.path_index]
        self.name = name

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
        health_bar_width = 60
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.x - 10, self.y - 20, health_bar_width, 5))
        pygame.draw.rect(screen, GREEN, (self.x - 10, self.y - 20, health_bar_width * health_ratio, 5))
        font = pygame.font.Font(None, 18)
        text = font.render(f"{int(self.health)}/{self.max_health} {self.name}", True, BLACK)
        screen.blit(text, (self.x - 10, self.y - 35))

# Define bullet class
class Bullet:
    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = speed

    def move(self):
        dx, dy = self.target.x - self.x, self.target.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance != 0:
            dx, dy = dx / distance, dy / distance
            self.x += dx * self.speed
            self.y += dy * self.speed

        if abs(self.x - self.target.x) < self.speed and abs(self.y - self.target.y) < self.speed:
            self.target.health -= self.damage  
            return True
        return False

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 3)

class GeneralBullet(Bullet):
    def __init__(self, x, y, target, damage):
        super().__init__(x, y, target, damage)
        self.speed = speed + 5

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 3)

# Define paths for maps
map_paths = [
    [(0, 300), (200, 300), (200, 200), (300, 200), (300, 400), (200, 400), (200, 300), (600, 300), (600, 200), (700, 200), (700, 400), (600, 400), (600, 300), (800, 300)],
    [(0, 100), (400, 100), (400, 400), (100, 400), (100, 600), (800, 600)]
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

# Wave definitions
def newwaves():
    global gamemode, waves
    if gamemode == "normal":
        waves = [
            {"normal": 5}, #1
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

# Draw the path on the map
def draw_path(map_index):
    screen.fill(GRAY)
    path = map_paths[map_index]
    for i in range(len(path) - 1):
        pygame.draw.line(screen, BLACK, path[i], path[i + 1], 5)

# Start a new wave
def start_wave():
    global wave_started, enemy_spawn_timer, current_wave
    wave_started = True
    enemy_spawn_timer = 0
    current_wave += 1

def spawn_enemies():
    global wave_started, cash
    if current_wave > len(waves):
        wave_started = False
        return

    wave = waves[current_wave - 1]       
    if gamemode == "normal":
        if wave["normal"] > 0:
            enemies.append(Enemy(map_paths[selected_map], 4, 4, GREEN, 10, "Normal"))
            wave["normal"] -= 1

    if len(enemies) == 0:
        wave_started = False
        cash += (200 + round((current_wave * 5) / 2))




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
                    elif 300 <= x <= 500 and 450 <= y <= 500:
                        current_screen = "shop"
                else:
                    for tower in towers:
                        if tower.x - 15 <= x <= tower.x + 15 and tower.y - 15 <= y <= tower.y + 15:
                            tower.selected = not tower.selected
                            selected_tower = tower if tower.selected else None
                            break
                    else:
                        if tower_selection == 1 and cash >= 120:
                            towers.append(Rifleman(x, y))
                            cash -= 120


            elif current_screen == "shop":
                if 700 <= x <= 780 and 10 <= y <= 50:  # Back button
                    current_screen = "main"

        elif event.type == pygame.KEYDOWN:
            if current_screen == "main":
                if event.key == pygame.K_u and selected_tower and cash >= selected_tower.cost:
                    selected_tower.upgrade()
                    cash -= selected_tower.cost
                elif event.key == pygame.K_1:
                    tower_selection = 1

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
                if enemy_spawn_timer > 30:
                    spawn_enemies()
                    enemy_spawn_timer = 0

            # Update enemies
            for enemy in enemies[:]:
                if enemy.move():
                    base_health -= enemy.health
                    enemies.remove(enemy)
                elif enemy.health <= 0:
                    cash += enemy.cash
                    enemies.remove(enemy)

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
                text = font.render("Selected Tower: Rifleman (120 cash)", True, BLACK)
            screen.blit(text, (10, 130))

            # Check for game over
            if base_health <= 0:
                selected_map = None
                towers.clear()
                enemies.clear()
                bullets.clear()
                current_wave = 0
                wave_started = False
                newwaves()

    elif current_screen == "shop":
        shop_screen()  # Ensure shop screen is redrawn each frame

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
