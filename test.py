import pygame
import time
import random
import math

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
YELLOW = (255, 255, 0) # Player Missile/Explosion
ORANGE = (255, 165, 0) # Explosion
GRAY = (150, 150, 150)

ASTEROID_SIZES = [(40, 40), (30, 30), (25, 25)]
ASTEROID_COLORS = [(100, 100, 100), (150, 150, 150), (200, 200, 200)]
RESOURCE_COLORS = [YELLOW, GREEN, BLUE]
PLAYER_SIZE = (30, 30)
PLAYER_COLOR = GREEN
ENEMY_SIZE = (35, 35)
ENEMY_COLOR = RED # Enemy Missile
MISSILE_SIZE = (10, 10)

# Adjusted speeds and acceleration for smoother, less frantic movement
MAX_PLAYER_SPEED = 4
PLAYER_ACCELERATION = 0.3
PLAYER_DECELERATION = 0.96 # Slower deceleration
MAX_ASTEROID_SPEED = 1 # Slower asteroids
MAX_ENEMY_SPEED = 1.2 # Slower enemies
ENEMY_ACCELERATION_FACTOR = 0.03 # Slower enemy turning
MAX_MISSILE_SPEED = 6 # Player missiles slightly faster
ENEMY_MISSILE_SPEED = 3 # Enemy missiles

LASER_COLOR = (0, 255, 255) # Cyan for laser
LASER_WIDTH = 4
LASER_DAMAGE_PER_FRAME = 0.7 # Increased laser damage

# Game States
GAME_STATE_PLAYING = 1
GAME_STATE_PAUSED = 2
GAME_STATE_GAME_OVER = 3

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

            angle = random.uniform(0, 2 * math.pi)
            displacement_distance = ASTEROID_SIZES[new_size_index][0] + 10 # Increased displacement

            disp_x = math.cos(angle) * displacement_distance
            disp_y = math.sin(angle) * displacement_distance

            parent_speed_x = getattr(original_asteroid, 'speed_x', 0)
            parent_speed_y = getattr(original_asteroid, 'speed_y', 0)

            # New asteroids inherit some parent speed and get a random push
            new_speed_x = parent_speed_x * 0.4 + random.uniform(-MAX_ASTEROID_SPEED * 1.5, MAX_ASTEROID_SPEED * 1.5)
            new_speed_y = parent_speed_y * 0.4 + random.uniform(-MAX_ASTEROID_SPEED * 1.5, MAX_ASTEROID_SPEED * 1.5)

            # Ensure new speeds are within reasonable bounds
            new_speed_x = max(-MAX_ASTEROID_SPEED, min(new_speed_x, MAX_ASTEROID_SPEED))
            new_speed_y = max(-MAX_ASTEROID_SPEED, min(new_speed_y, MAX_ASTEROID_SPEED))


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
        for _ in range(random.randint(2, 4)): # More resources from smallest asteroids
            resource = Resource(original_center_x, original_center_y,
                               random.randint(0, len(RESOURCE_COLORS) - 1))
            new_items.append(resource)
    return new_items


def generate_asteroid_position(player_position, screen_width, screen_height):
    while True:
        x = random.randrange(screen_width)
        y = random.randrange(screen_height)
        if calculate_distance((x, y), player_position) > 200: # Ensure asteroids don't spawn too close to player
            return x, y

# --- Game Classes ---

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
        # Draw a simple triangle spaceship
        pygame.draw.polygon(self.original_image, PLAYER_COLOR, [(0, PLAYER_SIZE[1]), (PLAYER_SIZE[0] / 2, 0), (PLAYER_SIZE[0], PLAYER_SIZE[1])])
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = 0
        self.speed_y = 0
        self.accel_x = 0
        self.accel_y = 0
        self.deceleration = PLAYER_DECELERATION
        self.health = 200 # Increased player health
        self.score = 0
        self.weapon = Weapon() # Default weapon is Missile Launcher
        self.firing_primary_weapon = False # For Shift key weapon
        self.shooting_laser = False # For mouse laser
        self.active_laser = None # The active Laser sprite

    def update(self):
        # Apply acceleration
        self.speed_x += self.accel_x
        self.speed_y += self.accel_y

        # Apply deceleration if no acceleration is applied in a direction
        if self.accel_x == 0:
            self.speed_x *= self.deceleration
        if self.accel_y == 0:
            self.speed_y *= self.deceleration

        # Limit speed
        self.speed_x = max(-MAX_PLAYER_SPEED, min(self.speed_x, MAX_PLAYER_SPEED))
        self.speed_y = max(-MAX_PLAYER_SPEED, min(self.speed_y, MAX_PLAYER_SPEED))

        # Update position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Keep player within screen bounds
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

        # Rotate image based on movement direction
        angle = 0
        if self.speed_x != 0 or self.speed_y != 0:
             angle = math.degrees(math.atan2(-self.speed_y, self.speed_x))
        self.image = pygame.transform.rotate(self.original_image, angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.weapon.update() # Update weapon cooldown

    def set_acceleration(self, dir_x, dir_y):
        """Sets the acceleration based on directional input (-1, 0, 1)."""
        self.accel_x = dir_x * PLAYER_ACCELERATION
        self.accel_y = dir_y * PLAYER_ACCELERATION

    def fire_primary_weapon(self, target=None):
        """Fires the currently equipped primary weapon (Shift key)."""
        # Currently only Missile Launcher is the primary weapon
        if self.weapon.ready and self.weapon.type == "MissileLauncher" and target:
             missile = self.weapon.fire(self.rect.centerx, self.rect.centery, target)
             return missile
        return None


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
        self.health = (self.size[0] * 2) * (size_index + 1) # Health based on size index
        self.max_health = self.health # Store max health for potential health bars later

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Wrap around screen
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
        self.image = pygame.Surface((12, 12)) # Slightly larger resources
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.value = (resource_type + 1) * 20 # Increased resource value
        self.lifetime = 900 # Increased lifetime (15 seconds)

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.Surface(ENEMY_SIZE, pygame.SRCALPHA)
        # Draw a simple triangle enemy
        pygame.draw.polygon(self.original_image, ENEMY_COLOR, [(0, 0), (ENEMY_SIZE[0], ENEMY_SIZE[1]/2), (0, ENEMY_SIZE[1])])
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = random.uniform(-MAX_ENEMY_SPEED, MAX_ENEMY_SPEED)
        self.speed_y = random.uniform(-MAX_ENEMY_SPEED, MAX_ENEMY_SPEED)
        self.health = 75 # Increased enemy health
        self.max_health = self.health
        self.target_player = None
        self.next_shot = time.time() + random.randint(1, 3) # Longer initial delay
        self.shoot_delay = 4 # Longer shoot delay

    def update(self):
        # Simple AI: Move towards player gradually
        if self.target_player:
            target_x, target_y = self.target_player.rect.center
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            dist = math.hypot(dx, dy)

            if dist > 0:
                target_speed_x = (dx / dist) * MAX_ENEMY_SPEED
                target_speed_y = (dy / dist) * MAX_ENEMY_SPEED

                self.speed_x += (target_speed_x - self.speed_x) * ENEMY_ACCELERATION_FACTOR
                self.speed_y += (target_speed_y - self.speed_y) * ENEMY_ACCELERATION_FACTOR

        # Limit enemy speed
        self.speed_x = max(-MAX_ENEMY_SPEED, min(self.speed_x, MAX_ENEMY_SPEED))
        self.speed_y = max(-MAX_ENEMY_SPEED, min(self.speed_y, MAX_ENEMY_SPEED))

        # Update position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Keep enemy within screen bounds
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH: self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT: self.speed_y *= -1

        # Rotate image to face direction of movement
        angle = 0
        if self.speed_x != 0 or self.speed_y != 0:
             angle = math.degrees(math.atan2(-self.speed_y, self.speed_x))
        self.image = pygame.transform.rotate(self.original_image, angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)


    def shoot_missile(self):
        if time.time() >= self.next_shot and self.target_player:
            # Enemy missiles target the player
            missile = Missile(self.rect.centerx, self.rect.centery, self.target_player, color=RED, speed=ENEMY_MISSILE_SPEED)
            self.next_shot = time.time() + self.shoot_delay + random.uniform(-1, 1) # Add some randomness to delay
            return missile
        return None

    def damage(self, amount):
        self.health -= amount
        return self.health <= 0


class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, target, color=YELLOW, speed=MAX_MISSILE_SPEED, damage=25): # Default color is player's
        super().__init__()
        self.image = pygame.Surface(MISSILE_SIZE, pygame.SRCALPHA)
        self.speed = speed
        self.color = color
        # Draw a simple triangle missile
        pygame.draw.polygon(self.image, self.color, [(0, MISSILE_SIZE[1]/2), (MISSILE_SIZE[0], 0), (MISSILE_SIZE[0], MISSILE_SIZE[1])])
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target = target # The sprite target
        self.damage = damage # Missile damage
        self.life_time = 6 # seconds
        self.deathtime = time.time() + self.life_time

    def update(self):
        # Missile homing behavior
        if self.target and self.target.alive() and time.time() < self.deathtime:
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)

            if dist > 0:
                # Calculate unit vector towards target
                dir_x = dx / dist
                dir_y = dy / dist

                # Update position based on direction and speed
                self.rect.x += self.speed * dir_x
                self.rect.y += self.speed * dir_y

                # Rotate image to face direction of movement
                angle = math.degrees(math.atan2(dy, dx))
                self.image = pygame.transform.rotate(self.original_image, angle - 90)
                self.rect = self.image.get_rect(center=self.rect.center)
        else:
            # Explode if target is gone or lifetime expired
            expl = Explosion(self.rect.center, 'small')
            all_sprites.add(expl)
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, start_pos, end_pos):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.update_beam(start_pos, end_pos) # Initial drawing

    def update_beam(self, start_pos, end_pos):
        """Redraws the laser beam."""
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.image.fill((0, 0, 0, 0))  # Clear previous beam
        pygame.draw.line(self.image, LASER_COLOR, (start_pos[0] - self.rect.x, start_pos[1] - self.rect.y), (end_pos[0] - self.rect.x, end_pos[1] - self.rect.y), LASER_WIDTH)

    def update(self):
        pass # Laser sprite position is fixed, appearance updated by update_beam

class Weapon():
    def __init__(self, type = "MissileLauncher"):
        self.type = type
        self.shoot_delay = 0.5 # Faster missile firing
        self.next_fire = time.time()
        self.ready = True

    def update(self):
        """Updates the weapon's cooldown."""
        if time.time() >= self.next_fire:
            self.ready = True

    def fire(self, x, y, target = None):
        """Attempts to fire the weapon."""
        if self.ready:
            if self.type == "MissileLauncher" and target:
                # Create a missile instance
                missile = Missile(x, y, target, color=YELLOW, damage=50) # Player missiles are yellow
                self.next_fire = time.time() + self.shoot_delay
                self.ready = False
                return missile
            # Add logic for other primary weapon types here if implemented later
        return None # Return None if not ready or no valid target/type

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size_category='medium'):
        super().__init__()
        self.center = center
        self.animation_speed = 4
        self.frame_count = 0

        if size_category == 'small':
            self.radii = [5, 10, 15, 12, 8]
            self.colors = [YELLOW, ORANGE, RED, ORANGE, YELLOW]
        elif size_category == 'large':
            self.radii = [20, 35, 50, 40, 25]
            self.colors = [YELLOW, ORANGE, RED, ORANGE, YELLOW]
        else: # medium
            self.radii = [10, 20, 30, 25, 15]
            self.colors = [YELLOW, ORANGE, RED, ORANGE, YELLOW]

        self.current_stage = 0
        self.max_stages = len(self.radii)

        max_r = max(self.radii)
        self.image = pygame.Surface((max_r * 2, max_r * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.center)
        self._draw_frame() # Draw the initial frame

    def _draw_frame(self):
        """Draws the current stage of the explosion animation."""
        self.image.fill((0, 0, 0, 0)) # Clear surface
        if self.current_stage < self.max_stages:
            radius = self.radii[self.current_stage]
            color = self.colors[self.current_stage]
            pygame.draw.circle(self.image, color, (self.image.get_width() // 2, self.image.get_height() // 2), radius)

    def update(self):
        """Updates the explosion animation frame."""
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_stage += 1
            if self.current_stage >= self.max_stages:
                self.kill()  # Animation finished
            else:
                self._draw_frame() # Draw the next frame

# --- Game Setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Mining Game")
clock = pygame.time.Clock()

# Sprite Groups
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
resources = pygame.sprite.Group()
enemies = pygame.sprite.Group()
missiles = pygame.sprite.Group()
explosions = pygame.sprite.Group()

# Player setup
player = Spaceship(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
all_sprites.add(player)

# Font setup
font = pygame.font.Font(None, 36)

# Game State
game_state = GAME_STATE_PLAYING

# Pause Menu Setup
pause_menu_font = pygame.font.Font(None, 50)
# Updated menu items to clarify controls
pause_menu_items = ["Resume", "Primary Weapon: Missile Launcher (Shift Key)", "Mining Tool: Laser (Left Mouse)"]
pause_menu_rects = []

def setup_pause_menu():
    """Calculates the positions and sizes of pause menu items."""
    pause_menu_rects.clear()
    total_height = len(pause_menu_items) * 60
    start_y = SCREEN_HEIGHT // 2 - total_height // 2
    for i, item in enumerate(pause_menu_items):
        text_surface = pause_menu_font.render(item, True, WHITE)
        rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * 60))
        pause_menu_rects.append(rect)

setup_pause_menu() # Initial setup

def draw_pause_menu(screen):
    """Draws the pause menu overlay."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) # Semi-transparent black
    screen.blit(overlay, (0, 0))

    title_text = pause_menu_font.render("Paused", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
    screen.blit(title_text, title_rect)

    for i, item in enumerate(pause_menu_items):
        color = WHITE
        # Highlight selected primary weapon
        if "Missile Launcher" in item and player.weapon.type == "MissileLauncher":
             color = YELLOW

        text_surface = pause_menu_font.render(item, True, color)
        rect = pause_menu_rects[i]
        screen.blit(text_surface, rect)

def handle_pause_menu_click(mouse_pos):
    """Handles clicks on the pause menu."""
    for i, rect in enumerate(pause_menu_rects):
        if rect.collidepoint(mouse_pos):
            selected_item = pause_menu_items[i]
            if selected_item == "Resume":
                return GAME_STATE_PLAYING
            elif "Missile Launcher" in selected_item:
                player.weapon.type = "MissileLauncher"
                print("Primary Weapon set to Missile Launcher")
                # return GAME_STATE_PLAYING # Option to return to game after selection
            elif "Laser (Left Mouse)" in selected_item:
                 print("Laser is the mining tool controlled by the left mouse button.")
                 # return GAME_STATE_PLAYING # Option to return to game after selection
    return GAME_STATE_PAUSED # Stay in paused state if no valid click

def spawn_initial_entities():
    """Spawns the initial asteroids and enemies."""
    for sprite in all_sprites:
        if sprite != player:
            sprite.kill()
    asteroids.empty()
    resources.empty()
    enemies.empty()
    missiles.empty()
    explosions.empty()

    # More initial asteroids for mining
    for _ in range(8):
        x, y = generate_asteroid_position(player.rect.center, SCREEN_WIDTH, SCREEN_HEIGHT)
        size_idx = random.choices([0, 1, 2], weights=[0.5, 0.3, 0.2], k=1)[0] # More large/medium asteroids initially
        asteroid = Asteroid(x, y, size_idx, random.uniform(-MAX_ASTEROID_SPEED, MAX_ASTEROID_SPEED),
                            random.uniform(-MAX_ASTEROID_SPEED, MAX_ASTEROID_SPEED))
        asteroids.add(asteroid)
        all_sprites.add(asteroid)

    # Fewer initial enemies
    for _ in range(1):
        x, y = generate_asteroid_position(player.rect.center, SCREEN_WIDTH, SCREEN_HEIGHT)
        enemy = Enemy(x,y)
        enemy.target_player = player
        enemies.add(enemy)
        all_sprites.add(enemy)

spawn_initial_entities() # Initial spawn

def display_game_over_screen(screen, final_score):
    """Draws the game over screen."""
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Final Score: {final_score}", True, WHITE)
    play_again_text = font.render("Press SPACE to Play Again", True, GREEN)
    screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)))
    screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
    screen.blit(play_again_text, play_again_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2/3)))
    pygame.display.flip()

# --- Game Loop ---
running = True

while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: # Pause key
                if game_state == GAME_STATE_PLAYING:
                    game_state = GAME_STATE_PAUSED
                elif game_state == GAME_STATE_PAUSED:
                    game_state = GAME_STATE_PLAYING

            if game_state == GAME_STATE_PLAYING:
                if event.key == pygame.K_w: player.set_acceleration(player.accel_x, -1)
                elif event.key == pygame.K_s: player.set_acceleration(player.accel_x, 1)
                elif event.key == pygame.K_a: player.set_acceleration(-1, player.accel_y)
                elif event.key == pygame.K_d: player.set_acceleration(1, player.accel_y)
                elif event.key == pygame.K_LSHIFT: player.firing_primary_weapon = True # Start firing primary weapon

            elif game_state == GAME_STATE_GAME_OVER:
                if event.key == pygame.K_SPACE:
                    game_state = GAME_STATE_PLAYING
                    player.health = 200 # Reset player health
                    player.score = 0
                    player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.speed_x, player.speed_y = 0, 0
                    player.accel_x, player.accel_y = 0, 0
                    if player.active_laser:
                        player.active_laser.kill()
                        player.active_laser = None
                    player.shooting_laser = False
                    spawn_initial_entities()

        elif event.type == pygame.KEYUP:
            if game_state == GAME_STATE_PLAYING:
                if event.key == pygame.K_w and player.accel_y < 0: player.set_acceleration(player.accel_x, 0)
                elif event.key == pygame.K_s and player.accel_y > 0: player.set_acceleration(player.accel_x, 0)
                elif event.key == pygame.K_a and player.accel_x < 0: player.set_acceleration(0, player.accel_y)
                elif event.key == pygame.K_d and player.accel_x > 0: player.set_acceleration(0, player.accel_y)
                elif event.key == pygame.K_LSHIFT: player.firing_primary_weapon = False # Stop firing primary weapon

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == GAME_STATE_PLAYING:
                if event.button == 1: # Left mouse button for laser
                    player.shooting_laser = True
                    if player.active_laser is None:
                        mouse_pos = pygame.mouse.get_pos()
                        player.active_laser = Laser(player.rect.center, mouse_pos)
                        all_sprites.add(player.active_laser)
            elif game_state == GAME_STATE_PAUSED:
                 new_state = handle_pause_menu_click(event.pos)
                 if new_state:
                     game_state = new_state

        elif event.type == pygame.MOUSEBUTTONUP:
            if game_state == GAME_STATE_PLAYING:
                if event.button == 1: # Left mouse button for laser
                    player.shooting_laser = False
                    if player.active_laser:
                        player.active_laser.kill()
                        player.active_laser = None


    # --- Update ---
    if game_state == GAME_STATE_PLAYING:
        all_sprites.update()

        # Update laser position if active (must be after player update)
        if player.shooting_laser and player.active_laser:
            player.active_laser.update_beam(player.rect.center, pygame.mouse.get_pos())
        elif not player.shooting_laser and player.active_laser:
             player.active_laser.kill()
             player.active_laser = None


        # --- Collision Detection ---

        # Asteroid and player collision
        collided_asteroids = pygame.sprite.spritecollide(player, asteroids, False)
        for asteroid_hit in collided_asteroids:
            player.health -= asteroid_hit.size[0] # Reduced damage from collision
            expl = Explosion(asteroid_hit.rect.center, 'medium')
            all_sprites.add(expl)
            new_items = split_asteroid(asteroid_hit)
            asteroid_hit.kill()
            for item in new_items:
                all_sprites.add(item)
                if isinstance(item, Asteroid): asteroids.add(item)
                elif isinstance(item, Resource): resources.add(item)
            if player.health <= 0:
                game_state = GAME_STATE_GAME_OVER
                break
        if game_state == GAME_STATE_GAME_OVER: continue

        # Resource and player collision
        collected_resources = pygame.sprite.spritecollide(player, resources, True)
        for resource_collected in collected_resources:
            player.score += resource_collected.value

        # Enemy and player collision
        collided_enemies = pygame.sprite.spritecollide(player, enemies, False) # Don't kill enemy immediately
        for enemy_hit in collided_enemies:
            player.health -= 15 # Reduced damage from enemy collision
            # Enemy doesn't die from collision, just takes damage
            if player.health <= 0:
                game_state = GAME_STATE_GAME_OVER
                break
        if game_state == GAME_STATE_GAME_OVER: continue


        # Enemy shooting missiles
        for enemy_unit in enemies:
            missile_fired = enemy_unit.shoot_missile()
            if missile_fired:
                missiles.add(missile_fired)
                all_sprites.add(missile_fired)

        # Missile and player collision (only enemy missiles)
        for missile in list(missiles):
            if missile.target == player and missile.color == RED: # Check if it's an enemy missile targeting player
                if pygame.sprite.collide_rect(missile, player):
                    player.health -= missile.damage
                    expl = Explosion(missile.rect.center, 'small')
                    missile.kill()
                    all_sprites.add(expl)
                    if player.health <= 0:
                        game_state = GAME_STATE_GAME_OVER
                        break
        if game_state == GAME_STATE_GAME_OVER: continue

        # Missile and asteroid collision (player missiles only)
        # Create a temporary group of player missiles
        
        missiles_hitting_asteroids = pygame.sprite.groupcollide(missiles, asteroids, True, False)
        for missile_obj, asteroids_hit_list in missiles_hitting_asteroids.items():
            for asteroid_obj in asteroids_hit_list:
                if asteroid_obj.damage(missile_obj.damage * 1.5): # Player missiles do good damage to asteroids
                    player.score += 10
                    expl = Explosion(asteroid_obj.rect.center, 'medium')
                    all_sprites.add(expl)
                    new_items = split_asteroid(asteroid_obj)
                    asteroid_obj.kill()
                    for item in new_items:
                        all_sprites.add(item)
                        if isinstance(item, Asteroid): asteroids.add(item)
                        elif isinstance(item, Resource): resources.add(item)
                else:
                    expl = Explosion(missile_obj.rect.center, 'small')
                    all_sprites.add(expl)

        # Missile and enemy collision (player missiles only)
        # Create a temporary group of player missiles
        player_missiles = pygame.sprite.Group([m for m in missiles if m.color == YELLOW])
        player_missiles_hitting_enemies = pygame.sprite.groupcollide(player_missiles, enemies, True, False)
        for missile_obj, enemies_hit_list in player_missiles_hitting_enemies.items():
            for enemy_obj in enemies_hit_list:
                 if enemy_obj.damage(missile_obj.damage * 2): # Player missiles do more damage to enemies
                      player.score += 20 # Score for destroying enemy
                      expl = Explosion(enemy_obj.rect.center, 'large') # Bigger explosion for enemy
                      all_sprites.add(expl)
                      enemy_obj.kill() # Kill enemy if damage destroyed it
                 else:
                      expl = Explosion(missile_obj.rect.center, 'small') # Smaller impact explosion
                      all_sprites.add(expl)


        # Laser and asteroid collision (only if laser is active)
        if player.shooting_laser and player.active_laser:
            mouse_pos = pygame.mouse.get_pos()
            # Iterate over a copy of asteroids list for safe removal
            for asteroid_target in list(asteroids):
                # Check if the asteroid's rect collides with the mouse position
                if asteroid_target.rect.collidepoint(mouse_pos):
                    # Apply continuous damage with the laser
                    if asteroid_target.damage(LASER_DAMAGE_PER_FRAME):
                        player.score += 5
                        expl = Explosion(asteroid_target.rect.center, 'small')
                        all_sprites.add(expl)
                        new_items = split_asteroid(asteroid_target)
                        asteroid_target.kill()
                        for item in new_items:
                            all_sprites.add(item)
                            if isinstance(item, Asteroid): asteroids.add(item)
                            elif isinstance(item, Resource): resources.add(item)
                        # No break here, allow laser to hit multiple asteroids if they are close enough

        # Laser and enemy collision (Laser does NOT damage enemies)
        # This collision is intentionally not handled here.

        # Player primary weapon firing (Shift key)
        if player.firing_primary_weapon:
             mouse_pos = pygame.mouse.get_pos()
             # Find a target (asteroid or enemy) under the mouse cursor
             target_under_mouse = None
             # Prioritize enemies if under the mouse
             for enemy_target in enemies:
                 if enemy_target.rect.collidepoint(mouse_pos):
                     target_under_mouse = enemy_target
                     break # Target the first enemy found

             if target_under_mouse is None: # If no enemy, check for asteroids
                 for asteroid_target in asteroids:
                     if asteroid_target.rect.collidepoint(mouse_pos):
                         target_under_mouse = asteroid_target
                         break # Target the first asteroid found

             if target_under_mouse:
                 missile_fired = player.fire_primary_weapon(target_under_mouse)
                 if missile_fired:
                     missiles.add(missile_fired)
                     all_sprites.add(missile_fired)


        # Respawn entities if too few for progression
        # Gradually increase spawn rates or max counts as score increases?
        min_asteroids = 5 + player.score // 200 # More asteroids as score increases
        min_enemies = 1 + player.score // 500 # More enemies as score increases (slower increase)

        if len(asteroids) < min_asteroids:
            for _ in range(min_asteroids - len(asteroids)):
                x, y = generate_asteroid_position(player.rect.center, SCREEN_WIDTH, SCREEN_HEIGHT)
                size_idx = random.choices([0, 1, 2], weights=[0.4, 0.3, 0.3], k=1)[0] # More variety
                new_ast = Asteroid(x, y, size_idx,
                                   random.uniform(-MAX_ASTEROID_SPEED, MAX_ASTEROID_SPEED),
                                   random.uniform(-MAX_ASTEROID_SPEED, MAX_ASTEROID_SPEED))
                asteroids.add(new_ast)
                all_sprites.add(new_ast)

        if len(enemies) < min_enemies:
            for _ in range(min_enemies - len(enemies)):
                x, y = generate_asteroid_position(player.rect.center, SCREEN_WIDTH, SCREEN_HEIGHT)
                new_enemy = Enemy(x,y)
                new_enemy.target_player = player
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)


    # --- Draw ---
    screen.fill(BLACK)

    # Draw all sprites
    all_sprites.draw(screen)

    # Draw UI elements (Health, Score)
    if game_state != GAME_STATE_GAME_OVER:
        health_text = font.render(f"Health: {max(0, int(player.health))}", True, GREEN if player.health > 50 else YELLOW if player.health > 20 else RED)
        score_text = font.render(f"Score: {player.score}", True, BLUE)
        screen.blit(health_text, (10, 10))
        screen.blit(score_text, (10, 40))

    # Draw pause menu if game is paused
    if game_state == GAME_STATE_PAUSED:
        draw_pause_menu(screen)

    # Draw game over screen if game is over
    if game_state == GAME_STATE_GAME_OVER:
        display_game_over_screen(screen, player.score)


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
