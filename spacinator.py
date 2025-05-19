import pygame
import time
import random
import math
# import time # Not explicitly used, can be removed if not needed for other debugging

# Initialize Pygame
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0) # For explosions
ASTEROID_SIZES = [(40, 40), (30, 30), (25, 25)]
ASTEROID_COLORS = [(100, 100, 100), (150, 150, 150), (200, 200, 200)]
RESOURCE_COLORS = [YELLOW, GREEN, BLUE]
PLAYER_SIZE = (30, 30)
PLAYER_COLOR = GREEN
ENEMY_SIZE = (35, 35)
ENEMY_COLOR = RED
MISSILE_SIZE = (10, 10)
MISSILE_COLOR = YELLOW
MAX_PLAYER_SPEED = 5
MAX_ASTEROID_SPEED = 2
MAX_ENEMY_SPEED = 2
MAX_MISSILE_SPEED = 2
LASER_COLOR = (255, 0, 0)
LASER_WIDTH = 3

# --- Helper Functions ---

def calculate_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def generate_random_position(width_range, height_range):
    x = random.randrange(*width_range)
    y = random.randrange(*height_range)
    return x, y

def limit_position(position, max_width, max_height):
    x, y = position
    x = max(0, min(x, max_width))
    y = max(0, min(y, max_height))
    return x, y

def split_asteroid(original_asteroid):
    """Splits an asteroid into smaller asteroids or resources."""
    new_items = []
    original_center_x = original_asteroid.rect.centerx
    original_center_y = original_asteroid.rect.centery

    if original_asteroid.size_index < len(ASTEROID_SIZES) - 1:
        # Split into smaller asteroids
        for _ in range(2):
            new_size_index = original_asteroid.size_index + 1
            
            # Add slight offset to prevent instant re-collision
            # Push them away from the center of the original asteroid
            angle = random.uniform(0, 2 * math.pi)
            # Ensure a minimum displacement, especially if player is involved
            # Increased displacement distance
            displacement_distance = ASTEROID_SIZES[new_size_index][0] + 5 # Based on new asteroid size + a bit

            disp_x = math.cos(angle) * displacement_distance
            disp_y = math.sin(angle) * displacement_distance
            
            # Inherit some velocity from parent, with some randomness
            parent_speed_x = getattr(original_asteroid, 'speed_x', 0)
            parent_speed_y = getattr(original_asteroid, 'speed_y', 0)

            new_speed_x = parent_speed_x * 0.5 + random.uniform(-MAX_ASTEROID_SPEED, MAX_ASTEROID_SPEED) / (new_size_index + 1.5)
            new_speed_y = parent_speed_y * 0.5 + random.uniform(-MAX_ASTEROID_SPEED, MAX_ASTEROID_SPEED) / (new_size_index + 1.5)


            new_asteroid_obj = Asteroid(
                original_center_x + disp_x,
                original_center_y + disp_y,
                new_size_index,
                new_speed_x,
                new_speed_y
            )
            new_items.append(new_asteroid_obj)
    else:
        # Split into resources
        for _ in range(random.randint(1, 3)):
            resource = Resource(original_center_x, original_center_y,
                               random.randint(0, len(RESOURCE_COLORS) - 1))
            new_items.append(resource)
    return new_items


def generate_asteroid_position(player_position, screen_width, screen_height):
    while True:
        x = random.randrange(screen_width)
        y = random.randrange(screen_height)
        if calculate_distance((x, y), player_position) > 150:
            return x, y

# --- Game Classes ---

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
        pygame.draw.polygon(self.image, PLAYER_COLOR, [(0, PLAYER_SIZE[1]), (PLAYER_SIZE[0] / 2, 0), (PLAYER_SIZE[0], PLAYER_SIZE[1])])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = 0
        self.speed_y = 0
        self.health = 100
        self.score = 0
        self.weapon = Weapon()
        self.firing_weapon = False
        self.shooting_laser = False
        self.active_laser = None

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

        self.weapon.update()

    def accelerate(self, direction):
        if direction == "up": self.speed_y = -MAX_PLAYER_SPEED
        elif direction == "down": self.speed_y = MAX_PLAYER_SPEED
        elif direction == "left": self.speed_x = -MAX_PLAYER_SPEED
        elif direction == "right": self.speed_x = MAX_PLAYER_SPEED
        elif direction == "stop_x": self.speed_x = 0
        elif direction == "stop_y": self.speed_y = 0

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, size_index, speed_x, speed_y):
        super().__init__()
        self.size_index = size_index
        self.size = ASTEROID_SIZES[size_index]
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, ASTEROID_COLORS[size_index], (0, 0, self.size[0], self.size[1]))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.health = self.size[0] # Adjusted health

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left > SCREEN_WIDTH: self.rect.right = 0
        if self.rect.right < 0: self.rect.left = SCREEN_WIDTH
        if self.rect.top > SCREEN_HEIGHT: self.rect.bottom = 0
        if self.rect.bottom < 0: self.rect.top = SCREEN_HEIGHT

    def damage(self, amount):
        self.health -= amount
        return self.health <= 0

class Resource(pygame.sprite.Sprite):
    def __init__(self, x, y, resource_type):
        super().__init__()
        self.resource_type = resource_type
        self.color = RESOURCE_COLORS[resource_type]
        self.image = pygame.Surface((10, 10))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.value = (resource_type + 1) * 10
        self.lifetime = 600 # Increased lifetime (10 seconds at 60 FPS)

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface(ENEMY_SIZE, pygame.SRCALPHA)
        pygame.draw.polygon(self.image, ENEMY_COLOR, [(0, 0), (ENEMY_SIZE[0], ENEMY_SIZE[1]/2), (0, ENEMY_SIZE[1])])
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = random.uniform(-MAX_ENEMY_SPEED, MAX_ENEMY_SPEED)
        self.speed_y = random.uniform(-MAX_ENEMY_SPEED, MAX_ENEMY_SPEED)
        self.health = 50
        self.target_player = None
        self.next_shot = time.time() + random.randint(0, 2)
        self.shoot_delay = 5

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        self.angle = math.degrees(math.atan2(self.speed_x, self.speed_y))
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        if random.random() < 0.01: # Less frequent direction change
            self.speed_x = random.uniform(-MAX_ENEMY_SPEED, MAX_ENEMY_SPEED)
            self.speed_y = random.uniform(-MAX_ENEMY_SPEED, MAX_ENEMY_SPEED)
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH: self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT: self.speed_y *= -1
        


    def shoot_missile(self):
        if time.time() >= self.next_shot and self.target_player:
            missile = Missile(self.rect.centerx, self.rect.centery, self.target_player)
            self.next_shot = time.time() + self.shoot_delay
            return missile
        return None

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, target, color = None):
        super().__init__()
        self.image = pygame.Surface(MISSILE_SIZE, pygame.SRCALPHA)
        self.speed = MAX_MISSILE_SPEED
        if(color):
            pygame.draw.polygon(self.image, color, [(0, MISSILE_SIZE[1]/2), (MISSILE_SIZE[0], 0), (MISSILE_SIZE[0], MISSILE_SIZE[1])])
            self.speed = MAX_MISSILE_SPEED + 2
        else:
            pygame.draw.polygon(self.image, MISSILE_COLOR, [(0, MISSILE_SIZE[1]/2), (MISSILE_SIZE[0], 0), (MISSILE_SIZE[0], MISSILE_SIZE[1])])
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target = target
        self.damage = 20 # Increased missile damage
        self.angle = 0
        self.life_time = 5
        self.deathtime = time.time() + self.life_time 

    def update(self):
        if self.target and self.target.alive() and self.deathtime > time.time(): # Check if target is still alive
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist == 0: dist = 1 # Avoid division by zero
            
            self.angle = math.degrees(math.atan2(dy, dx))
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            
            self.rect.x += self.speed * dx / dist
            self.rect.y += self.speed * dy / dist   
        else:
            expl = Explosion(self.rect.center, 'small')
            all_sprites.add(expl)
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, start_pos, end_pos):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.update_beam(start_pos, end_pos)

    def update_beam(self, start_pos, end_pos):
        self.image.fill((0, 0, 0, 0))  # Clear previous beam
        pygame.draw.line(self.image, LASER_COLOR, start_pos, end_pos, LASER_WIDTH)
    
    # update() is not strictly needed if all changes are driven by update_beam
    # but all_sprites group calls update, so it should exist.
    def update(self):
        pass

class Weapon():
    def __init__(self, type = "MissileLauncher"):
        self.type = type
        self.shoot_delay = 1.5
        self.next_fire = time.time()
        self.ready = True

    def update(self):
        if time.time() > self.next_fire:
            self.ready = True

    def fire(self, x, y, target = None):
        if self.type == "MissileLauncher" and target:
            if self.ready and target:
                missile = Missile(x, y, target, (255, 0, 0))
                self.next_fire = time.time() + self.shoot_delay
                self.ready = False
                return missile
            return None

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size_category='medium'): # e.g., 'small', 'medium', 'large'
        super().__init__()
        self.center = center
        self.animation_speed = 4  # Lower is faster animation
        self.frame_count = 0
        
        if size_category == 'small':
            self.radii = [5, 10, 15, 12, 8] # Expand then shrink
            self.colors = [YELLOW, ORANGE, RED, ORANGE, YELLOW]
        elif size_category == 'large':
            self.radii = [20, 35, 50, 40, 25]
            self.colors = [YELLOW, ORANGE, RED, ORANGE, YELLOW]
        else: # medium
            self.radii = [10, 20, 30, 25, 15]
            self.colors = [YELLOW, ORANGE, RED, ORANGE, YELLOW]

        self.current_stage = 0
        self.max_stages = len(self.radii)
        
        # Ensure surface is large enough for the biggest radius
        max_r = max(self.radii)
        self.image = pygame.Surface((max_r * 2, max_r * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.center)
        self._draw_frame()

    def _draw_frame(self):
        self.image.fill((0, 0, 0, 0)) # Clear surface
        radius = self.radii[self.current_stage]
        color = self.colors[self.current_stage]
        # Draw circle in the center of the explosion's own surface
        pygame.draw.circle(self.image, color, (self.image.get_width() // 2, self.image.get_height() // 2), radius)

    def update(self):
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_stage += 1
            if self.current_stage >= self.max_stages:
                self.kill()  # Animation finished
            else:
                self._draw_frame()

# --- Game Setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Mining Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
resources = pygame.sprite.Group()
enemies = pygame.sprite.Group()
missiles = pygame.sprite.Group()
explosions = pygame.sprite.Group() # New group for explosions

player = Spaceship(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
all_sprites.add(player)

def spawn_initial_entities():
    # Clear existing dynamic sprites before spawning new ones (except player)
    for sprite in all_sprites:
        if sprite != player:
            sprite.kill()
    asteroids.empty()
    resources.empty()
    enemies.empty()
    missiles.empty()
    explosions.empty() # Clear explosions too

    for _ in range(5): # Initial asteroids
        x, y = generate_asteroid_position(player.rect.center, SCREEN_WIDTH, SCREEN_HEIGHT)
        asteroid = Asteroid(x, y, 0, random.uniform(-MAX_ASTEROID_SPEED, MAX_ASTEROID_SPEED),
                            random.uniform(-MAX_ASTEROID_SPEED, MAX_ASTEROID_SPEED))
        asteroids.add(asteroid)
        all_sprites.add(asteroid)

    for _ in range(2): # Initial enemies
        x, y = generate_asteroid_position(player.rect.center, SCREEN_WIDTH, SCREEN_HEIGHT)
        enemy = Enemy(x,y)
        enemy.target_player = player
        enemies.add(enemy)
        all_sprites.add(enemy)

spawn_initial_entities() # Initial spawn

# --- Game Loop ---
running = True
game_over = False
font = pygame.font.Font(None, 36)

def display_game_over_screen(screen, final_score):
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Final Score: {final_score}", True, WHITE)
    play_again_text = font.render("Press SPACE to Play Again", True, GREEN)
    screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)))
    screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
    screen.blit(play_again_text, play_again_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2/3)))
    pygame.display.flip()

while running:
    if not game_over:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w: player.accelerate("up")
                elif event.key == pygame.K_s: player.accelerate("down")
                elif event.key == pygame.K_a: player.accelerate("left")
                elif event.key == pygame.K_d: player.accelerate("right")
                elif event.key == pygame.K_LSHIFT: player.firing_weapon = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w and player.speed_y < 0: player.accelerate("stop_y")
                elif event.key == pygame.K_s and player.speed_y > 0: player.accelerate("stop_y")
                elif event.key == pygame.K_a and player.speed_x < 0: player.accelerate("stop_x")
                elif event.key == pygame.K_d and player.speed_x > 0: player.accelerate("stop_x")
                elif event.key == pygame.K_LSHIFT: player.firing_weapon = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left mouse
                player.shooting_laser = True
                if player.active_laser is None: # Create laser only if one isn't active
                    mouse_pos = pygame.mouse.get_pos()
                    player.active_laser = Laser(player.rect.center, mouse_pos)
                    all_sprites.add(player.active_laser)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                player.shooting_laser = False
                if player.active_laser:
                    player.active_laser.kill()
                    player.active_laser = None

        # --- Update ---
        all_sprites.update() # This now also updates player.active_laser if it exists
        # explosions.update() # Already part of all_sprites update if added there

        if player.shooting_laser and player.active_laser:
            player.active_laser.update_beam(player.rect.center, pygame.mouse.get_pos())
        elif not player.shooting_laser and player.active_laser: # Ensure laser is removed if shooting stops unexpectedly
             player.active_laser.kill()
             player.active_laser = None


        # Asteroid and player collision
        collided_asteroids = pygame.sprite.spritecollide(player, asteroids, False) # False: don't kill asteroid yet
        for asteroid_hit in collided_asteroids:
            player.health -= asteroid_hit.size[0] * 2 # Damage based on size
            
            expl = Explosion(asteroid_hit.rect.center, 'medium')
            all_sprites.add(expl)
            # explosions.add(expl) # No need if added to all_sprites

            new_items = split_asteroid(asteroid_hit)
            asteroid_hit.kill() # Kill the original asteroid now

            for item in new_items:
                all_sprites.add(item)
                if isinstance(item, Asteroid): asteroids.add(item)
                elif isinstance(item, Resource): resources.add(item)
            if player.health <= 0:
                game_over = True
                break 
        if game_over: continue # Skip rest of updates if game over from this collision
            
            

        # Resource and player collision
        collected_resources = pygame.sprite.spritecollide(player, resources, True) # True: kill resource on collide
        for resource_collected in collected_resources:
            player.score += resource_collected.value
            # No damage from resources

        # Enemy and player collision
        collided_enemies = pygame.sprite.spritecollide(player, enemies, True) # True: kill enemy on collide
        for enemy_hit in collided_enemies:
            player.health -= 30 # Damage from enemy collision
            expl = Explosion(enemy_hit.rect.center, 'medium') # Enemy explodes too
            all_sprites.add(expl)
            if player.health <= 0:
                game_over = True
                break
        if game_over: continue

        # Enemy shooting missiles
        for enemy_unit in enemies:
            missile_fired = enemy_unit.shoot_missile()
            if missile_fired:
                missiles.add(missile_fired)
                all_sprites.add(missile_fired)

        # Missile and player collision
        for missile in missiles:
            if missile.target == player:
                missile_hit = pygame.sprite.collide_rect(missile, player) # True: kill missile
                
                if missile_hit:
                    player.health -= missile.damage
                    expl = Explosion(missile.rect.center, 'small') # Missile explosion on player
                    missile.kill()
                    all_sprites.add(expl)
                    if player.health <= 0:
                        game_over = True
                        break
        if game_over: continue
        
        # Missile and asteroid collision
        # groupcollide returns a dict: {missile_collided: [list_of_asteroids_hit_by_it]}
        missile_asteroid_hits = pygame.sprite.groupcollide(missiles, asteroids, True, False) # Missile killed, asteroid not (yet)
        for missile_obj, asteroids_hit_list in missile_asteroid_hits.items():
            for asteroid_obj in asteroids_hit_list:
                # Asteroid takes damage from missile, e.g. missile.damage or a fixed amount
                if asteroid_obj.damage(missile_obj.damage * 2): # Missiles do more damage to asteroids
                    player.score += 10 # Score for destroying asteroid with missile
                    
                    expl = Explosion(asteroid_obj.rect.center, 'medium') # Asteroid explosion
                    all_sprites.add(expl)

                    new_items = split_asteroid(asteroid_obj)
                    asteroid_obj.kill() # Kill asteroid if damage destroyed it
                    for item in new_items:
                        all_sprites.add(item)
                        if isinstance(item, Asteroid): asteroids.add(item)
                        elif isinstance(item, Resource): resources.add(item)
                else: # Asteroid damaged but not destroyed
                    expl = Explosion(missile_obj.rect.center, 'small') # Smaller impact explosion
                    all_sprites.add(expl)


        # Laser and asteroid collision
        if player.shooting_laser and player.active_laser:
            mouse_pos = pygame.mouse.get_pos()
            # Iterate over a copy of asteroids list for safe removal
            for asteroid_target in list(asteroids): 
                if asteroid_target.rect.collidepoint(mouse_pos):
                    # Check if the point is actually on the laser line (optional, for precision)
                    # For simplicity, direct collidepoint is used for "tip of the laser" damage
                    if asteroid_target.damage(0.5):  # Continuous damage, adjust rate (e.g. 0.5 per frame)
                        player.score += 5 # Score for laser destruction
                        
                        expl = Explosion(asteroid_target.rect.center, 'small') # Laser hit explosion
                        all_sprites.add(expl)

                        new_items = split_asteroid(asteroid_target)
                        asteroid_target.kill()
                        for item in new_items:
                            all_sprites.add(item)
                            if isinstance(item, Asteroid): asteroids.add(item)
                            elif isinstance(item, Resource): resources.add(item)
                        break # Process one asteroid per frame for the laser
        
        # Weapon firing at asteroid
        if player.firing_weapon:
            mouse_pos = pygame.mouse.get_pos()
            if player.weapon.type == "MissileLauncher":
                for asteroid_target in list(asteroids): 
                    if asteroid_target.rect.collidepoint(mouse_pos):
                        missile_fired = player.weapon.fire(player.rect.x, player.rect.y, asteroid_target)
                        if missile_fired:
                            missile_fired
                            missiles.add(missile_fired)
                            all_sprites.add(missile_fired)
                    
        
        # Respawn asteroids if too few
        if len(asteroids) < 3: # Maintain a minimum number of asteroids
            for _ in range(3 - len(asteroids)):
                x, y = generate_asteroid_position(player.rect.center, SCREEN_WIDTH, SCREEN_HEIGHT)
                # Spawn a mix of sizes, or just large ones
                size_idx = random.choices([0, 1, 2], weights=[0.6, 0.3, 0.1], k=1)[0]
                new_ast = Asteroid(x, y, size_idx, 
                                   random.uniform(-MAX_ASTEROID_SPEED, MAX_ASTEROID_SPEED),
                                   random.uniform(-MAX_ASTEROID_SPEED, MAX_ASTEROID_SPEED))
                asteroids.add(new_ast)
                all_sprites.add(new_ast)
        
        # Respawn enemies if too few
        if len(enemies) < 1: # Maintain a minimum number of enemies
            for _ in range(2 - len(enemies)): # Spawn up to 2
                x, y = generate_asteroid_position(player.rect.center, SCREEN_WIDTH, SCREEN_HEIGHT)
                new_enemy = Enemy(x,y)
                new_enemy.target_player = player
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)


        # --- Draw ---
        screen.fill(BLACK)
        all_sprites.draw(screen) # Draws all sprites, including player, asteroids, enemies, missiles, active_laser, explosions

        health_text = font.render(f"Health: {max(0, int(player.health))}", True, GREEN if player.health > 30 else RED)
        score_text = font.render(f"Score: {player.score}", True, BLUE)
        screen.blit(health_text, (10, 10))
        screen.blit(score_text, (10, 40))

        pygame.display.flip()
        clock.tick(FPS)
    else: # Game Over
        display_game_over_screen(screen, player.score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    player.health = 100
                    player.score = 0
                    player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.speed_x, player.speed_y = 0,0
                    if player.active_laser: # Ensure laser is cleared on restart
                        player.active_laser.kill()
                        player.active_laser = None
                    player.shooting_laser = False
                    
                    spawn_initial_entities() # Respawn game elements
                    # No break needed here, loop will continue to game state

pygame.quit()
