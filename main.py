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
RED = (255, 0, 0) # Enemy Missile
GREEN = (0, 255, 0) # Player Ship
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0) # Player Missile/Explosion/Resource
ORANGE = (255, 165, 0) # Explosion
CYAN = (0, 255, 255) # Laser Color
GRAY = (150, 150, 150) # Asteroid Color

ASTEROID_SIZES = [(40, 40), (30, 30), (25, 25)]
ASTEROID_COLORS = [(100, 100, 100), (150, 150, 150), (200, 200, 200)]
RESOURCE_COLORS = [YELLOW, GREEN, BLUE] # Yellow, Green, Blue resources
PLAYER_SIZE = (30, 30)
PLAYER_COLOR = GREEN
ENEMY_SIZE = (35, 35)
ENEMY_COLOR = RED
MISSILE_SIZE = (10, 10)

# Adjusted speeds and acceleration for smoother, less frantic movement
MAX_PLAYER_SPEED = 0.2 # Player speed now affects map movement rate
PLAYER_ACCELERATION = 0.005 # Slower acceleration for finer control
PLAYER_DECELERATION = 0.98 # Slower deceleration for smoother stop

MAX_ASTEROID_SPEED = 1.5
MAX_ENEMY_SPEED = 1.8
ENEMY_ACCELERATION_FACTOR = 0.03
MAX_MISSILE_SPEED = 5 # Player missiles slightly faster
ENEMY_MISSILE_SPEED = 4 # Enemy missiles

LASER_COLOR = CYAN
LASER_WIDTH = 4
LASER_DAMAGE_PER_FRAME = 0.7 # Increased laser damage

# Camera Dampening
CAMERA_DAMPENING = 0.95 # Closer to 1 for smoother, slower camera

# Enemy Sight Range
ENEMY_SIGHT_RANGE = 300 # Pixels

# Weapon Costs (Score points)
WEAPON_COSTS = {
    "MissileLauncher": 0, # Starting weapon is free
    # Add costs for future weapons here
}

# Game States
GAME_STATE_PLAYING = 1
GAME_STATE_PAUSED = 2
GAME_STATE_GAME_OVER = 3

# --- Helper Functions ---

def calculate_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def generate_random_map_position(center_x, center_y, min_distance, max_distance):
    """Generates a random position within a distance range from a center point in map coordinates."""
    while True:
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(min_distance, max_distance)
        x = center_x + math.cos(angle) * distance
        y = center_y + math.sin(angle) * distance
        return x, y

def split_asteroid(original_asteroid):
    """Splits an asteroid into smaller asteroids or resources."""
    new_items = []
    original_map_x = original_asteroid.map_x
    original_map_y = original_asteroid.map_y

    if original_asteroid.size_index < len(ASTEROID_SIZES) - 1:
        # Split into smaller asteroids
        for _ in range(2):
            new_size_index = original_asteroid.size_index + 1

            angle = random.uniform(0, 2 * math.pi)
            displacement_distance = ASTEROID_SIZES[new_size_index][0] + 15 # Increased displacement

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
                original_map_x + disp_x,
                original_map_y + disp_y,
                new_size_index,
                new_speed_x,
                new_speed_y
            )
            new_items.append(new_asteroid_obj)
    else:
        # Split into resources
        for _ in range(random.randint(2, 4)): # More resources from smallest asteroids
            resource = Resource(original_map_x, original_map_y,
                               random.randint(0, len(RESOURCE_COLORS) - 1))
            new_items.append(resource)
    return new_items

# --- Game Classes ---

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, map_x, map_y):
        super().__init__()
        self.original_image = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, PLAYER_COLOR, [(0, PLAYER_SIZE[1]), (PLAYER_SIZE[0] / 2, 0), (PLAYER_SIZE[0], PLAYER_SIZE[1])])
        self.image = self.original_image
        self.rect = self.image.get_rect()
        # Player's screen position is fixed at the center
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.map_x = map_x # Player's position in the game world
        self.map_y = map_y

        self.speed_x = 0
        self.speed_y = 0
        self.accel_x = 0
        self.accel_y = 0
        self.deceleration = PLAYER_DECELERATION
        self.health = 200
        self.score = 0
        self.weapon = Weapon() # Default weapon is Missile Launcher
        self.firing_primary_weapon = False # For Shift key weapon
        self.shooting_laser = False # For mouse laser
        self.active_laser = None # The active Laser sprite

        self.owned_weapons = ["MissileLauncher"] # Player starts with Missile Launcher

    def update(self):
        # Apply acceleration to speed
        self.speed_x += self.accel_x
        self.speed_y += self.accel_y

        # Apply deceleration if no acceleration is applied
        if self.accel_x == 0:
            self.speed_x *= self.deceleration
        if self.accel_y == 0:
            self.speed_y *= self.deceleration

        # Limit speed
        self.speed_x = max(-MAX_PLAYER_SPEED, min(self.speed_x, MAX_PLAYER_SPEED))
        self.speed_y = max(-MAX_PLAYER_SPEED, min(self.speed_y, MAX_PLAYER_SPEED))

        # Update player's map position based on speed
        self.map_x += self.speed_x
        self.map_y += self.speed_y

        # Rotate image based on movement direction
        angle = 0
        if self.speed_x != 0 or self.speed_y != 0:
             angle = math.degrees(math.atan2(-self.speed_y, self.speed_x))
        self.image = pygame.transform.rotate(self.original_image, angle - 90)
        # The rect's center is fixed on the screen, so we just update the image
        self.rect = self.image.get_rect(center=self.rect.center)


        self.weapon.update() # Update weapon cooldown

    def set_acceleration(self, dir_x, dir_y):
        """Sets the acceleration based on directional input (-1, 0, 1)."""
        self.accel_x = dir_x * PLAYER_ACCELERATION
        self.accel_y = dir_y * PLAYER_ACCELERATION

    def fire_primary_weapon(self, target=None):
        """Fires the currently equipped primary weapon (Shift key)."""
        if self.weapon.ready and target: # Check if weapon is ready and there's a target
             # Missile Launcher logic (only primary weapon for now)
             if self.weapon.type == "MissileLauncher":
                 missile = self.weapon.fire(self.rect.centerx, self.rect.centery, target)
                 return missile
        return None

    def buy_weapon(self, weapon_type):
        """Attempts to buy a weapon."""
        if weapon_type in WEAPON_COSTS:
            cost = WEAPON_COSTS[weapon_type]
            if self.score >= cost and weapon_type not in self.owned_weapons:
                self.score -= cost
                self.owned_weapons.append(weapon_type)
                print(f"Bought {weapon_type} for {cost} points.")
                return True
            elif weapon_type in self.owned_weapons:
                print(f"Already own {weapon_type}.")
                return False
            else:
                print(f"Not enough score to buy {weapon_type}. Need {cost}, have {self.score}.")
                return False
        else:
            print(f"Weapon type {weapon_type} not found.")
            return False

    def switch_weapon(self, weapon_type):
        """Switches to an owned weapon."""
        if weapon_type in self.owned_weapons:
            self.weapon.type = weapon_type
            print(f"Switched to {weapon_type}.")
            return True
        else:
            print(f"Do not own {weapon_type}.")
            return False


class GameEntity(pygame.sprite.Sprite):
    """Base class for entities that exist in the game world (map coordinates)."""
    def __init__(self, map_x, map_y, image, size):
        super().__init__()
        self.original_image = image
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.map_x = map_x
        self.map_y = map_y
        self.speed_x = 0
        self.speed_y = 0

    def update_screen_position(self, camera_offset_x, camera_offset_y):
        """Updates the sprite's screen position based on its map position and camera offset."""
        self.rect.center = (self.map_x - camera_offset_x + SCREEN_WIDTH // 2,
                            self.map_y - camera_offset_y + SCREEN_HEIGHT // 2)

    def update(self):
        # Update map position based on speed
        self.map_x += self.speed_x
        self.map_y += self.speed_y
        # Update screen position will be handled by the main game loop using camera offset

class Asteroid(GameEntity):
    def __init__(self, map_x, map_y, size_index, speed_x, speed_y):
        self.size_index = size_index
        self.size = ASTEROID_SIZES[size_index]
        image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.ellipse(image, ASTEROID_COLORS[size_index], (0, 0, self.size[0], self.size[1]))
        super().__init__(map_x, map_y, image, self.size)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.health = (self.size[0] * 2) * (size_index + 1)
        self.max_health = self.health

    def update(self):
        super().update() # Update map position

    def damage(self, amount):
        self.health -= amount
        return self.health <= 0

class Resource(GameEntity):
    def __init__(self, map_x, map_y, resource_type):
        self.resource_type = resource_type
        self.color = RESOURCE_COLORS[resource_type]
        image = pygame.Surface((12, 12))
        image.fill(self.color)
        super().__init__(map_x, map_y, image, (12, 12))
        self.value = (resource_type + 1) * 20
        self.lifetime = 900

    def update(self):
        super().update() # Update map position
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class Enemy(GameEntity):
    def __init__(self, map_x, map_y):
        image = pygame.Surface(ENEMY_SIZE, pygame.SRCALPHA)
        pygame.draw.polygon(image, ENEMY_COLOR, [(0, 0), (ENEMY_SIZE[0], ENEMY_SIZE[1]/2), (0, ENEMY_SIZE[1])])
        super().__init__(map_x, map_y, image, ENEMY_SIZE)
        self.speed_x = random.uniform(-MAX_ENEMY_SPEED, MAX_ENEMY_SPEED)
        self.speed_y = random.uniform(-MAX_ENEMY_SPEED, MAX_ENEMY_SPEED)
        self.health = 75
        self.max_health = self.health
        self.target_player = None # Will be set to the player sprite
        self.next_shot = time.time() + random.randint(1, 3)
        self.shoot_delay = 4

    def update(self):
        # Simple AI: Move towards player gradually
        if self.target_player:
            target_x, target_y = self.target_player.map_x, self.target_player.map_y
            dx = target_x - self.map_x
            dy = target_y - self.map_y
            dist = math.hypot(dx, dy)

            if dist > 0:
                target_speed_x = (dx / dist) * MAX_ENEMY_SPEED
                target_speed_y = (dy / dist) * MAX_ENEMY_SPEED

                self.speed_x += (target_speed_x - self.speed_x) * ENEMY_ACCELERATION_FACTOR
                self.speed_y += (target_speed_y - self.speed_y) * ENEMY_ACCELERATION_FACTOR

        # Limit enemy speed
        self.speed_x = max(-MAX_ENEMY_SPEED, min(self.speed_x, MAX_ENEMY_SPEED))
        self.speed_y = max(-MAX_ENEMY_SPEED, min(self.speed_y, MAX_ENEMY_SPEED))

        super().update() # Update map position

        # Rotate image to face direction of movement
        angle = 0
        if self.speed_x != 0 or self.speed_y != 0:
             angle = math.degrees(math.atan2(-self.speed_y, self.speed_x))
        self.image = pygame.transform.rotate(self.original_image, angle - 90)
        # Update rect center relative to its *current* screen position before rotation
        current_screen_center = self.rect.center
        self.rect = self.image.get_rect(center=current_screen_center)


    def shoot_missile(self):
        # Only shoot if player is within sight range and weapon is ready
        if self.target_player and time.time() >= self.next_shot:
            dist_to_player = calculate_distance((self.map_x, self.map_y), (self.target_player.map_x, self.target_player.map_y))
            if dist_to_player <= ENEMY_SIGHT_RANGE:
                missile = Missile(self.map_x, self.map_y, self.target_player, color=RED, speed=ENEMY_MISSILE_SPEED)
                self.next_shot = time.time() + self.shoot_delay + random.uniform(-1, 1)
                return missile
        return None

    def damage(self, amount):
        self.health -= amount
        return self.health <= 0


class Missile(GameEntity):
    def __init__(self, map_x, map_y, target, color=YELLOW, speed=MAX_MISSILE_SPEED):
        image = pygame.Surface(MISSILE_SIZE, pygame.SRCALPHA)
        pygame.draw.polygon(image, color, [(0, MISSILE_SIZE[1]/2), (MISSILE_SIZE[0], 0), (MISSILE_SIZE[0], MISSILE_SIZE[1])])
        super().__init__(map_x, map_y, image, MISSILE_SIZE)
        self.speed = speed
        self.color = color
        self.target = target
        self.damage = 25
        self.life_time = 6
        self.deathtime = time.time() + self.life_time

    def update(self):
        # Missile homing behavior in map coordinates
        if self.target and self.target.alive() and time.time() < self.deathtime:
            dx = self.target.map_x - self.map_x
            dy = self.target.map_y - self.map_y
            dist = math.hypot(dx, dy)

            if dist > 0:
                dir_x = dx / dist
                dir_y = dy / dist

                self.map_x += self.speed * dir_x
                self.map_y += self.speed * dir_y

                # Rotate image to face direction of movement
                angle = math.degrees(math.atan2(dy, dx))
                self.image = pygame.transform.rotate(self.original_image, angle - 90)
                # Update rect center relative to its *current* screen position before rotation
                current_screen_center = self.rect.center
                self.rect = self.image.get_rect(center=current_screen_center)

        else:
            expl = Explosion(self.map_x, self.map_y, 'small') # Explosion uses map coords
            all_sprites.add(expl)
            self.kill()


class Laser(pygame.sprite.Sprite): # Laser is a screen-space effect, not a game entity
    def __init__(self, start_screen_pos, end_screen_pos):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.start_screen_pos = start_screen_pos
        self.end_screen_pos = end_screen_pos
        self.update_beam(start_screen_pos, end_screen_pos)

    def update_beam(self, start_screen_pos, end_screen_pos):
        self.start_screen_pos = start_screen_pos
        self.end_screen_pos = end_screen_pos
        self.image.fill((0, 0, 0, 0))
        pygame.draw.line(self.image, LASER_COLOR, self.start_screen_pos, self.end_screen_pos, LASER_WIDTH)

    def update(self):
        pass

class Weapon():
    def __init__(self, type = "MissileLauncher"):
        self.type = type
        self.shoot_delay = 1.0
        self.next_fire = time.time()
        self.ready = True

    def update(self):
        if time.time() >= self.next_fire:
            self.ready = True

    def fire(self, player_screen_x, player_screen_y, target_entity):
        """Fires a projectile from the player's screen position towards a target entity's map position."""
        if self.ready:
            if self.type == "MissileLauncher" and target_entity:
                # Missile needs the target's map coordinates
                missile = Missile(player_screen_x, player_screen_y, target_entity, color=YELLOW)
                self.next_fire = time.time() + self.shoot_delay
                self.ready = False
                return missile
        return None

class Explosion(GameEntity): # Explosions also exist in map space
    def __init__(self, map_x, map_y, size_category='medium'):
        self.center_map = (map_x, map_y) # Store center in map coords
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
        # Create a surface large enough for the largest frame
        image = pygame.Surface((max_r * 2, max_r * 2), pygame.SRCALPHA)
        super().__init__(map_x, map_y, image, (max_r * 2, max_r * 2)) # Initialize with map coords
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)) # Initial screen position (will be updated)
        self._draw_frame()

    def _draw_frame(self):
        self.image.fill((0, 0, 0, 0))
        if self.current_stage < self.max_stages:
            radius = self.radii[self.current_stage]
            color = self.colors[self.current_stage]
            # Draw circle in the center of the explosion's own surface
            pygame.draw.circle(self.image, color, (self.image.get_width() // 2, self.image.get_height() // 2), radius)

    def update(self):
        # No map position update needed for explosions, they are static in the world
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_stage += 1
            if self.current_stage >= self.max_stages:
                self.kill()
            else:
                self._draw_frame()

# --- Game Setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Mining Game")
clock = pygame.time.Clock()

# Sprite Groups
all_sprites = pygame.sprite.Group()
game_entities = pygame.sprite.Group() # Group for all entities in map space
asteroids = pygame.sprite.Group()
resources = pygame.sprite.Group()
enemies = pygame.sprite.Group()
missiles = pygame.sprite.Group()
explosions = pygame.sprite.Group() # Explosions are also GameEntities now

# Player setup
player = Spaceship(0, 0) # Start at map origin
all_sprites.add(player) # Player is in all_sprites for drawing
# Player is NOT in game_entities because its screen position is fixed

# Camera/Offset
camera_offset_x = 0
camera_offset_y = 0

# Font setup
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Game State
game_state = GAME_STATE_PLAYING

# Pause Menu Setup
pause_menu_font = pygame.font.Font(None, 50)
# Updated menu items to include Buy/Equip options
pause_menu_items = ["Resume", "Weapons:"]
# Dynamically add weapon options
for weapon_type in WEAPON_COSTS:
    pause_menu_items.append(f"{weapon_type} - Cost: {WEAPON_COSTS[weapon_type]}")

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
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
    screen.blit(title_text, title_rect)

    # Draw player score in the pause menu
    score_text = font.render(f"Score: {player.score}", True, BLUE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
    screen.blit(score_text, score_rect)


    for i, item in enumerate(pause_menu_items):
        color = WHITE
        # Highlight equipped weapon
        if player.weapon.type in item and "Weapon:" not in item:
             color = YELLOW
        # Indicate owned weapons
        if any(owned_weapon in item for owned_weapon in player.owned_weapons) and "Weapon:" not in item:
             color = GREEN if color == WHITE else color # Green if owned, keep yellow if equipped

        text_surface = pause_menu_font.render(item, True, color)
        rect = pause_menu_rects[i]
        screen.blit(text_surface, rect)

def handle_pause_menu_click(mouse_pos):
    """Handles clicks on the pause menu."""
    global game_state
    for i, rect in enumerate(pause_menu_rects):
        if rect.collidepoint(mouse_pos):
            selected_item = pause_menu_items[i]
            if selected_item == "Resume":
                game_state = GAME_STATE_PLAYING
                return
            elif "Weapon:" in selected_item:
                pass # Just a title, not clickable
            else:
                # Extract weapon type from the menu item string
                weapon_type_str = selected_item.split(" - ")[0]
                if weapon_type_str in WEAPON_COSTS:
                    if weapon_type_str in player.owned_weapons:
                        player.switch_weapon(weapon_type_str)
                    else:
                        player.buy_weapon(weapon_type_str)


def spawn_initial_entities():
    """Spawns the initial asteroids and enemies around the origin."""
    # Clear existing dynamic sprites before spawning new ones (except player)
    for sprite in all_sprites:
        if sprite != player:
            sprite.kill()
    game_entities.empty()
    asteroids.empty()
    resources.empty()
    enemies.empty()
    missiles.empty()
    explosions.empty()

    # Spawn initial asteroids around the origin
    for _ in range(15): # More initial asteroids
        x, y = generate_random_map_position(0, 0, 100, 500) # Spawn within a range around origin
        size_idx = random.choices([0, 1, 2], weights=[0.5, 0.3, 0.2], k=1)[0]
        asteroid = Asteroid(x, y, size_idx, random.uniform(-MAX_ASTEROID_SPEED, MAX_ASTEROID_SPEED),
                            random.uniform(-MAX_ASTEROID_SPEED, MAX_ASTEROID_SPEED))
        asteroids.add(asteroid)
        all_sprites.add(asteroid)
        game_entities.add(asteroid)

    # Spawn initial enemies around the origin
    for _ in range(2): # Fewer initial enemies
        x, y = generate_random_map_position(0, 0, 300, 600) # Spawn further out
        enemy = Enemy(x,y)
        enemy.target_player = player
        enemies.add(enemy)
        all_sprites.add(enemy)
        game_entities.add(enemy)


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

def draw_center_pointer(screen, player_map_x, player_map_y):
    """Draws an arrow pointing towards the map origin and displays coordinates/distance."""
    origin_x, origin_y = 0, 0
    dx = origin_x - player_map_x
    dy = origin_y - player_map_y
    distance_to_origin = math.hypot(dx, dy)

    # Calculate angle to origin
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)

    # Position the pointer near the edge of the screen, pointing inwards
    pointer_distance_from_center = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 2 - 20 # Adjust as needed
    pointer_x = SCREEN_WIDTH // 2 + math.cos(angle_rad) * pointer_distance_from_center
    pointer_y = SCREEN_HEIGHT // 2 + math.sin(angle_rad) * pointer_distance_from_center

    # Draw a simple triangle arrow
    arrow_size = 15
    points = [
        (pointer_x + math.cos(angle_rad) * arrow_size, pointer_y + math.sin(angle_rad) * arrow_size),
        (pointer_x + math.cos(angle_rad - math.pi / 2) * arrow_size * 0.6, pointer_y + math.sin(angle_rad - math.pi / 2) * arrow_size * 0.6),
        (pointer_x + math.cos(angle_rad + math.pi / 2) * arrow_size * 0.6, pointer_y + math.sin(angle_rad + math.pi / 2) * arrow_size * 0.6)
    ]
    pygame.draw.polygon(screen, WHITE, points)

    # Display coordinates and distance
    coords_text = small_font.render(f"Coords: ({int(player_map_x)}, {int(player_map_y)})", True, WHITE)
    distance_text = small_font.render(f"Dist: {int(distance_to_origin)}", True, WHITE)

    screen.blit(coords_text, (10, SCREEN_HEIGHT - 50))
    screen.blit(distance_text, (10, SCREEN_HEIGHT - 30))


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
                    player.health = 200
                    player.score = 0
                    player.map_x, player.map_y = 0, 0 # Reset player map position
                    player.speed_x, player.speed_y = 0, 0
                    player.accel_x, player.accel_y = 0, 0
                    if player.active_laser:
                        player.active_laser.kill()
                        player.active_laser = None
                    player.shooting_laser = False
                    spawn_initial_entities() # Respawn game elements around new origin

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
                 handle_pause_menu_click(event.pos) # Handle clicks in the pause menu

        elif event.type == pygame.MOUSEBUTTONUP:
            if game_state == GAME_STATE_PLAYING:
                if event.button == 1: # Left mouse button for laser
                    player.shooting_laser = False
                    if player.active_laser:
                        player.active_laser.kill()
                        player.active_laser = None


    # --- Update ---
    if game_state == GAME_STATE_PLAYING:
        player.update() # Update player's map position

        # Calculate camera offset with dampening
        target_offset_x = player.map_x
        target_offset_y = player.map_y
        camera_offset_x += (target_offset_x - camera_offset_x) * (1 - CAMERA_DAMPENING)
        camera_offset_y += (target_offset_y - camera_offset_y) * (1 - CAMERA_DAMPENING)

        # Update all game entities based on map position and camera offset
        for entity in game_entities:
            entity.update() # Update entity's map position
            entity.update_screen_position(camera_offset_x, camera_offset_y) # Update screen position

        # Update laser screen position if active (must be after player update)
        if player.shooting_laser and player.active_laser:
            player.active_laser.update_beam(player.rect.center, pygame.mouse.get_pos())
        elif not player.shooting_laser and player.active_laser:
             player.active_laser.kill()
             player.active_laser = None


        # --- Collision Detection ---

        # Asteroid and player collision (using screen positions for collision)
        # We need temporary groups for entities currently visible on screen for accurate collision
        visible_asteroids = pygame.sprite.Group([a for a in asteroids if screen.get_rect().colliderect(a.rect)])
        collided_asteroids = pygame.sprite.spritecollide(player, visible_asteroids, False)
        for asteroid_hit in collided_asteroids:
            player.health -= asteroid_hit.size[0] # Reduced damage from collision
            expl = Explosion(asteroid_hit.map_x, asteroid_hit.map_y, 'medium') # Explosion at map coords
            all_sprites.add(expl)
            game_entities.add(expl)
            new_items = split_asteroid(asteroid_hit)
            asteroid_hit.kill()
            game_entities.remove(asteroid_hit)
            for item in new_items:
                all_sprites.add(item)
                game_entities.add(item)
                if isinstance(item, Asteroid): asteroids.add(item)
                elif isinstance(item, Resource): resources.add(item)
            if player.health <= 0:
                game_state = GAME_STATE_GAME_OVER
                break
        if game_state == GAME_STATE_GAME_OVER: continue

        # Resource and player collision (using screen positions)
        visible_resources = pygame.sprite.Group([r for r in resources if screen.get_rect().colliderect(r.rect)])
        collected_resources = pygame.sprite.spritecollide(player, visible_resources, True)
        for resource_collected in collected_resources:
            player.score += resource_collected.value
            game_entities.remove(resource_collected)


        # Enemy and player collision (using screen positions)
        visible_enemies = pygame.sprite.Group([e for e in enemies if screen.get_rect().colliderect(e.rect)])
        collided_enemies = pygame.sprite.spritecollide(player, visible_enemies, False)
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
                game_entities.add(missile_fired)

        # Missile and player collision (only enemy missiles, using screen positions)
        visible_enemy_missiles = pygame.sprite.Group([m for m in missiles if m.color == RED and screen.get_rect().colliderect(m.rect)])
        for missile in list(visible_enemy_missiles):
            if missile.target == player: # Ensure it's an enemy missile targeting the player
                if pygame.sprite.collide_rect(missile, player):
                    player.health -= missile.damage
                    expl = Explosion(missile.map_x, missile.map_y, 'small') # Explosion at map coords
                    missile.kill()
                    game_entities.remove(missile)
                    all_sprites.add(expl)
                    game_entities.add(expl)
                    if player.health <= 0:
                        game_state = GAME_STATE_GAME_OVER
                        break
        if game_state == GAME_STATE_GAME_OVER: continue

        # Missile and asteroid collision (player missiles only, using screen positions)
        visible_asteroids = pygame.sprite.Group([a for a in asteroids if screen.get_rect().colliderect(a.rect)])
        player_missiles = pygame.sprite.Group([m for m in missiles if m.color == YELLOW and screen.get_rect().colliderect(m.rect)])
        player_missiles_hitting_asteroids = pygame.sprite.groupcollide(player_missiles, visible_asteroids, True, False)
        for missile_obj, asteroids_hit_list in player_missiles_hitting_asteroids.items():
            game_entities.remove(missile_obj)
            for asteroid_obj in asteroids_hit_list:
                if asteroid_obj.damage(missile_obj.damage * 1.5):
                    player.score += 10
                    expl = Explosion(asteroid_obj.map_x, asteroid_obj.map_y, 'medium') # Explosion at map coords
                    all_sprites.add(expl)
                    game_entities.add(expl)
                    new_items = split_asteroid(asteroid_obj)
                    asteroid_obj.kill()
                    game_entities.remove(asteroid_obj)
                    for item in new_items:
                        all_sprites.add(item)
                        game_entities.add(item)
                        if isinstance(item, Asteroid): asteroids.add(item)
                        elif isinstance(item, Resource): resources.add(item)
                else:
                    expl = Explosion(missile_obj.map_x, missile_obj.map_y, 'small') # Explosion at map coords
                    all_sprites.add(expl)
                    game_entities.add(expl)


        # Missile and enemy collision (player missiles only, using screen positions)
        visible_enemies = pygame.sprite.Group([e for e in enemies if screen.get_rect().colliderect(e.rect)])
        player_missiles = pygame.sprite.Group([m for m in missiles if m.color == YELLOW and screen.get_rect().colliderect(m.rect)])
        player_missiles_hitting_enemies = pygame.sprite.groupcollide(player_missiles, visible_enemies, True, False)
        for missile_obj, enemies_hit_list in player_missiles_hitting_enemies.items():
            game_entities.remove(missile_obj)
            for enemy_obj in enemies_hit_list:
                 if enemy_obj.damage(missile_obj.damage * 2):
                      player.score += 20
                      expl = Explosion(enemy_obj.map_x, enemy_obj.map_y, 'large') # Explosion at map coords
                      all_sprites.add(expl)
                      game_entities.add(expl)
                      enemy_obj.kill()
                      game_entities.remove(enemy_obj)
                 else:
                      expl = Explosion(missile_obj.map_x, missile_obj.map_y, 'small') # Explosion at map coords
                      all_sprites.add(expl)
                      game_entities.add(expl)


        # Laser and asteroid collision (only if laser is active, using screen positions)
        if player.shooting_laser and player.active_laser:
            mouse_pos = pygame.mouse.get_pos()
            visible_asteroids = pygame.sprite.Group([a for a in asteroids if screen.get_rect().colliderect(a.rect)])
            for asteroid_target in list(visible_asteroids):
                # Check if the asteroid's rect collides with the mouse position
                if asteroid_target.rect.collidepoint(mouse_pos):
                    if asteroid_target.damage(LASER_DAMAGE_PER_FRAME):
                        player.score += 5
                        expl = Explosion(asteroid_target.map_x, asteroid_target.map_y, 'small') # Explosion at map coords
                        all_sprites.add(expl)
                        game_entities.add(expl)
                        new_items = split_asteroid(asteroid_target)
                        asteroid_target.kill()
                        game_entities.remove(asteroid_target)
                        for item in new_items:
                            all_sprites.add(item)
                            game_entities.add(item)
                            if isinstance(item, Asteroid): asteroids.add(item)
                            elif isinstance(item, Resource): resources.add(item)


        # Player primary weapon firing (Shift key)
        if player.firing_primary_weapon:
             mouse_pos = pygame.mouse.get_pos()
             # Find a target (asteroid or enemy) under the mouse cursor (using screen positions)
             target_under_mouse = None
             visible_enemies = pygame.sprite.Group([e for e in enemies if screen.get_rect().colliderect(e.rect)])
             visible_asteroids = pygame.sprite.Group([a for a in asteroids if screen.get_rect().colliderect(a.rect)])

             # Prioritize enemies if under the mouse
             for enemy_target in visible_enemies:
                 if enemy_target.rect.collidepoint(mouse_pos):
                     target_under_mouse = enemy_target
                     break

             if target_under_mouse is None: # If no enemy, check for asteroids
                 for asteroid_target in visible_asteroids:
                     if asteroid_target.rect.collidepoint(mouse_pos):
                         target_under_mouse = asteroid_target
                         break

             if target_under_mouse:
                 # Fire missile from player's screen center towards the target entity's map position
                 missile_fired = player.fire_primary_weapon(target_under_mouse)
                 if missile_fired:
                     missiles.add(missile_fired)
                     all_sprites.add(missile_fired)
                     game_entities.add(missile_fired)


        # Procedural Generation and Difficulty Scaling
        distance_from_origin = calculate_distance((player.map_x, player.map_y), (0, 0))
        difficulty_factor = 1 + distance_from_origin / 1000 # Increase difficulty every 1000 units from origin

        min_asteroids = int(10 * difficulty_factor) # More asteroids further out
        min_enemies = int(2 * difficulty_factor) # More enemies further out

        # Define spawn area relative to player's map position
        spawn_area_center_x = player.map_x
        spawn_area_center_y = player.map_y
        spawn_min_dist = 600 # Spawn entities at least this far from player
        spawn_max_dist = 1000 # Spawn entities within this max distance

        # Spawn asteroids if too few
        if len(asteroids) < min_asteroids:
            for _ in range(min_asteroids - len(asteroids)):
                x, y = generate_random_map_position(spawn_area_center_x, spawn_area_center_y, spawn_min_dist, spawn_max_dist)
                size_idx = random.choices([0, 1, 2], weights=[0.4, 0.3, 0.3], k=1)[0]
                new_ast = Asteroid(x, y, size_idx,
                                   random.uniform(-MAX_ASTEROID_SPEED * difficulty_factor * 0.5, MAX_ASTEROID_SPEED * difficulty_factor * 0.5),
                                   random.uniform(-MAX_ASTEROID_SPEED * difficulty_factor * 0.5, MAX_ASTEROID_SPEED * difficulty_factor * 0.5))
                asteroids.add(new_ast)
                all_sprites.add(new_ast)
                game_entities.add(new_ast)


        # Spawn enemies if too few
        if len(enemies) < min_enemies:
            for _ in range(min_enemies - len(enemies)):
                x, y = generate_random_map_position(spawn_area_center_x, spawn_area_center_y, spawn_min_dist, spawn_max_dist)
                new_enemy = Enemy(x,y)
                new_enemy.target_player = player
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
                game_entities.add(new_enemy)


    # --- Draw ---
    screen.fill(BLACK)

    # Draw all game entities (asteroids, enemies, missiles, resources, explosions)
    # Their screen positions are updated based on the camera offset
    for entity in game_entities:
        screen.blit(entity.image, entity.rect)

    # Draw the player (always centered)
    screen.blit(player.image, player.rect)

    # Draw UI elements (Health, Score, Center Pointer)
    if game_state != GAME_STATE_GAME_OVER:
        health_text = font.render(f"Health: {max(0, int(player.health))}", True, GREEN if player.health > 100 else YELLOW if player.health > 50 else RED)
        score_text = font.render(f"Score: {player.score}", True, BLUE)
        screen.blit(health_text, (10, 10))
        screen.blit(score_text, (10, 40))

        draw_center_pointer(screen, player.map_x, player.map_y)


    # Draw pause menu if game is paused
    if game_state == GAME_STATE_PAUSED:
        draw_pause_menu(screen)

    # Draw game over screen if game is over
    if game_state == GAME_STATE_GAME_OVER:
        display_game_over_screen(screen, player.score)


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
