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
PLASMA_BOLT_SIZE = (15, 15) # New constant for plasma bolt size
PLASMA_BOLT_COLOR = (255, 100, 0) # Orange-red for plasma
MAX_PLAYER_SPEED = 5
MAX_ASTEROID_SPEED = 2
MAX_ENEMY_SPEED = 2
MAX_MISSILE_VELOCITY = 2
MAX_PLASMA_BOLT_VELOCITY = 8 # Plasma bolts are fast
LASER_COLOR = (255, 0, 0)
LASER_WIDTH = 3

# Define your weapon types with their properties and costs
WEAPON_TYPES = {
    "Missile Launcher": {"type": "MissileLauncher", "cost": 0, "description": "Homing missiles, free."},
    "Laser Cannon": {"type": "LaserCannon", "cost": 500, "description": "Continuous beam, drains score."},
    "Plasma Blaster": {"type": "PlasmaBlaster", "cost": 1000, "description": "Fires powerful plasma bolts."}
}
PLAYER_WEAPON_TYPE_INIT = "Missile Launcher" # Default starting weapon

# --- Helper Functions ---

def calculate_distance(pos1, pos2):
    """Calculates the Euclidean distance between two points."""
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def generate_random_position(width_range, height_range):
    """Generates a random position within specified ranges."""
    x = random.randrange(*width_range)
    y = random.randrange(*height_range)
    return x, y

def limit_position(position, max_width, max_height):
    """Limits a position to stay within screen boundaries."""
    x, y = position
    x = max(0, min(x, max_width))
    y = max(0, min(y, max_height))
    return x, y

def split_asteroid(original_asteroid):
    """Splits an asteroid into smaller asteroids or resources upon destruction."""
    new_items = []
    original_center_x = original_asteroid.rect.centerx
    original_center_y = original_asteroid.rect.centery

    if original_asteroid.size_index < len(ASTEROID_SIZES) - 1:
        # Split into smaller asteroids if not the smallest size
        for _ in range(2):
            new_size_index = original_asteroid.size_index + 1
            
            # Add slight offset to prevent instant re-collision
            # Push them away from the center of the original asteroid
            angle = random.uniform(0, 2 * math.pi)
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
        # Split into resources if it's the smallest size
        for _ in range(random.randint(1, 3)):
            resource = Resource(original_center_x, original_center_y,
                               random.randint(0, len(RESOURCE_COLORS) - 1))
            new_items.append(resource)
    return new_items

def generate_asteroid_position(player_position, screen_width, screen_height):
    """Generates an asteroid position far enough from the player."""
    while True:
        x = random.randrange(screen_width)
        y = random.randrange(screen_height)
        if calculate_distance((x, y), player_position) > 150: # Ensure asteroids don't spawn too close
            return x, y

def draw_button(surface, rect, color, text, text_color, font_obj):
    """Helper function to draw a button with text."""
    pygame.draw.rect(surface, color, rect, border_radius=5)
    text_surface = font_obj.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

# --- Game Classes ---

class Spaceship(pygame.sprite.Sprite):
    """Player controlled spaceship."""
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
        self.weapon = Weapon(PLAYER_WEAPON_TYPE_INIT) # Initialize with default weapon
        self.firing_weapon = False # True when Shift is pressed (for discrete shots)
        self.shooting_laser = False # True when Left Mouse is pressed (for continuous laser)
        self.active_laser = None # Reference to the active Laser sprite

    def update(self):
        """Updates spaceship position and limits it to screen."""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

        self.weapon.update() # Update weapon's internal cooldown

    def accelerate(self, direction):
        """Changes spaceship's speed based on direction."""
        if direction == "up": self.speed_y = -MAX_PLAYER_SPEED
        elif direction == "down": self.speed_y = MAX_PLAYER_SPEED
        elif direction == "left": self.speed_x = -MAX_PLAYER_SPEED
        elif direction == "right": self.speed_x = MAX_PLAYER_SPEED
        elif direction == "stop_x": self.speed_x = 0
        elif direction == "stop_y": self.speed_y = 0

class Asteroid(pygame.sprite.Sprite):
    """Asteroid objects that the player mines or avoids."""
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
        self.health = self.size[0] * 2 # Health based on size

    def update(self):
        """Updates asteroid position with a slight drag and wraps around screen edges."""
        self.speed_x -= self.speed_x * 0.01 # Apply slight drag
        self.speed_y -= self.speed_y * 0.01
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Wrap around screen edges
        if self.rect.left > SCREEN_WIDTH: self.rect.right = 0
        if self.rect.right < 0: self.rect.left = SCREEN_WIDTH
        if self.rect.top > SCREEN_HEIGHT: self.rect.bottom = 0
        if self.rect.bottom < 0: self.rect.top = SCREEN_HEIGHT

    def damage(self, amount):
        """Applies damage to the asteroid. Returns True if destroyed."""
        self.health -= amount
        return self.health <= 0

class Resource(pygame.sprite.Sprite):
    """Resources dropped by destroyed asteroids."""
    def __init__(self, x, y, resource_type):
        super().__init__()
        self.resource_type = resource_type
        self.color = RESOURCE_COLORS[resource_type]
        self.image = pygame.Surface((10, 10))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.value = (resource_type + 1) * 10 # Value based on type
        self.lifetime = 600 # Lifetime in frames (10 seconds at 60 FPS)

    def update(self):
        """Decrements lifetime and kills the resource if expired."""
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    """Enemy spaceship that moves randomly and shoots missiles."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface(ENEMY_SIZE, pygame.SRCALPHA)
        pygame.draw.polygon(self.image, ENEMY_COLOR, [(0, 0), (ENEMY_SIZE[0], ENEMY_SIZE[1]/2), (0, ENEMY_SIZE[1])])
        self.original_image = self.image # Store original for rotation
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = random.uniform(-MAX_ENEMY_SPEED, MAX_ENEMY_SPEED)
        self.speed_y = random.uniform(-MAX_ENEMY_SPEED, MAX_ENEMY_SPEED)
        self.health = 50
        self.target_player = None # Will be set to the player instance
        self.next_shot = time.time() + random.randint(0, 2) # Initial random delay
        self.shoot_delay = 5 # Time between shots

    def update(self):
        """Updates enemy position, changes direction randomly, and rotates image."""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Rotate image to face direction of movement
        self.angle = math.degrees(math.atan2(self.speed_x, self.speed_y))
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        # Randomly change direction
        if random.random() < 0.01: # Less frequent direction change
            self.speed_x = random.uniform(-MAX_ENEMY_SPEED, MAX_ENEMY_SPEED)
            self.speed_y = random.uniform(-MAX_ENEMY_SPEED, MAX_ENEMY_SPEED)
        
        # Bounce off screen edges
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH: self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT: self.speed_y *= -1
        
    def shoot_missile(self):
        """Fires a missile if target is available and cooldown is ready."""
        if time.time() >= self.next_shot and self.target_player:
            missile = Missile(self.rect.centerx, self.rect.centery, self.target_player, MISSILE_COLOR)
            self.next_shot = time.time() + self.shoot_delay
            return missile
        return None

class Missile(pygame.sprite.Sprite):
    """Homing missile projectile."""
    def __init__(self, x, y, target, color):
        super().__init__()
        self.image = pygame.Surface(MISSILE_SIZE, pygame.SRCALPHA)
        pygame.draw.polygon(self.image, color, [(0, MISSILE_SIZE[1]/2), (MISSILE_SIZE[0], 0), (MISSILE_SIZE[0], MISSILE_SIZE[1])])
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target = target
        self.damage = 20
        self.speed = MAX_MISSILE_VELOCITY
        self.angle = 0
        self.life_time = 5 # seconds
        self.deathtime = time.time() + self.life_time
        
        # Initial velocity towards target
        dx = target.rect.centerx - x
        dy = target.rect.centery - y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.vx = self.speed * (dx / dist)
            self.vy = self.speed * (dy / dist)
        else:
            self.vx = 0
            self.vy = 0

    def update(self):
        """Updates missile position, tracks target, and self-destructs after lifetime."""
        if self.target and self.deathtime > time.time():
            # Predict target position based on its speed
            target_pos = self.target.rect.center
            target_speed = [getattr(self.target, 'speed_x', 0), getattr(self.target, 'speed_y', 0)] # Get speed if available
            distance = math.dist(self.rect.center, target_pos)
            
            pred_target_pos = target_pos
            if distance > 0:
                time_intercept = distance / self.speed
                pred_target_pos = [
                    target_pos[0] + target_speed[0] * time_intercept,
                    target_pos[1] + target_speed[1] * time_intercept
                ]

            # Calculate desired direction
            dx = pred_target_pos[0] - self.rect.centerx
            dy = pred_target_pos[1] - self.rect.centery
            dist_to_pred = math.hypot(dx, dy)
            if dist_to_pred > 0:
                desired_dir = [dx / dist_to_pred, dy / dist_to_pred]
            else:
                desired_dir = [0, 0]

            # Current direction from velocity
            current_speed = math.hypot(self.vx, self.vy)
            current_dir = [self.vx / current_speed, self.vy / current_speed] if current_speed > 0 else [0, 0]

            # Adjust direction with turning limit for smooth homing
            if current_speed > 0 and dist_to_pred > 0:
                dot_product = current_dir[0] * desired_dir[0] + current_dir[1] * desired_dir[1]
                cross_product = current_dir[0] * desired_dir[1] - current_dir[1] * desired_dir[0]
                angle_diff = math.atan2(cross_product, dot_product)
                max_turn = math.radians(3)  # 3 degrees per frame for smooth turning
                turn_angle = max(-max_turn, min(max_turn, angle_diff))
                
                # Rotate velocity vector
                cos_theta = math.cos(turn_angle)
                sin_theta = math.sin(turn_angle)
                new_vx = self.vx * cos_theta - self.vy * sin_theta
                new_vy = self.vx * sin_theta + self.vy * cos_theta
                self.vx = new_vx
                self.vy = new_vy
                
                # Normalize and scale to maintain constant speed
                current_speed = math.hypot(self.vx, self.vy)
                if current_speed > 0:
                    self.vx = self.speed * (self.vx / current_speed)
                    self.vy = self.speed * (self.vy / current_speed)

            # Update position
            self.rect.x += self.vx
            self.rect.y += self.vy

            # Update visual rotation
            self.angle = math.degrees(math.atan2(self.vy, self.vx)) # Angle based on current velocity
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            # If target is gone or lifetime expired, create explosion and kill self
            expl = Explosion(self.rect.center, 'small')
            all_sprites.add(expl)
            self.kill()

class PlasmaBolt(pygame.sprite.Sprite):
    """Straight-moving, high-damage plasma projectile."""
    def __init__(self, x, y, target_pos):
        super().__init__()
        self.image = pygame.Surface(PLASMA_BOLT_SIZE, pygame.SRCALPHA)
        pygame.draw.circle(self.image, PLASMA_BOLT_COLOR, (PLASMA_BOLT_SIZE[0]//2, PLASMA_BOLT_SIZE[1]//2), PLASMA_BOLT_SIZE[0]//2)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.damage = 50 # High damage
        self.speed = MAX_PLASMA_BOLT_VELOCITY
        self.life_time = 3 # seconds
        self.deathtime = time.time() + self.life_time

        # Calculate initial velocity towards target_pos (straight line)
        dx = target_pos[0] - x
        dy = target_pos[1] - y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.vx = self.speed * (dx / dist)
            self.vy = self.speed * (dy / dist)
        else:
            self.vx = 0
            self.vy = 0

    def update(self):
        """Updates plasma bolt position and self-destructs after lifetime or off screen."""
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Kill if off screen or lifetime expired
        if not screen.get_rect().colliderect(self.rect) or time.time() > self.deathtime:
            expl = Explosion(self.rect.center, 'small')
            all_sprites.add(expl)
            self.kill()

class Laser(pygame.sprite.Sprite):
    """Visual representation of the player's laser beam."""
    def __init__(self, start_pos, end_pos):
        super().__init__()
        # Create a surface large enough for the whole screen to draw the line on
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.update_beam(start_pos, end_pos)

    def update_beam(self, start_pos, end_pos):
        """Updates the laser beam's start and end points."""
        self.image.fill((0, 0, 0, 0))  # Clear previous beam
        pygame.draw.line(self.image, LASER_COLOR, start_pos, end_pos, LASER_WIDTH)
    
    def update(self):
        """Update method for sprite group compatibility. Beam is updated externally."""
        pass # The beam's position is updated directly by the player in the main loop

class Weapon():
    """Manages the player's current weapon and its firing logic."""
    def __init__(self, type_name):
        self.set_weapon_type(type_name) # Set initial weapon type
        self.missiles = pygame.sprite.Group() # Group for player's missiles
        self.plasma_bolts = pygame.sprite.Group() # Group for player's plasma bolts
        self.next_fire = time.time() # Cooldown timer
        self.ready = True # Is weapon ready to fire?

    def set_weapon_type(self, type_name):
        """Changes the weapon type and updates its properties."""
        self.type_name = type_name # Store the name for display/selection
        self.type = WEAPON_TYPES[type_name]["type"] # Store the internal type identifier
        
        if self.type == "MissileLauncher":
            self.shoot_delay = 0.4
            self.damage = 20 # Damage per missile
        elif self.type == "LaserCannon":
            self.shoot_delay = 0.05 # Fast "fire rate" for continuous laser (not actual shots)
            self.damage = 0.5 # Damage per frame for laser
        elif self.type == "PlasmaBlaster":
            self.shoot_delay = 0.7 # Slower fire rate
            self.damage = 50 # High damage per bolt
        
        self.ready = True # Reset readiness when changing weapon

    def update(self):
        """Updates weapon's internal cooldown."""
        if time.time() > self.next_fire:
            self.ready = True

    def fire(self, x, y, target = None, target_pos = None):
        """Fires a projectile based on the current weapon type."""
        if self.ready:
            if self.type == "MissileLauncher" and target:
                missile = Missile(x, y, target, (255, 0, 0)) # Player missiles are red
                self.next_fire = time.time() + self.shoot_delay
                self.ready = False
                self.missiles.add(missile)
                return missile
            elif self.type == "PlasmaBlaster" and target_pos:
                plasma_bolt = PlasmaBolt(x, y, target_pos)
                self.next_fire = time.time() + self.shoot_delay
                self.ready = False
                self.plasma_bolts.add(plasma_bolt)
                return plasma_bolt
        return None # Return None if not ready or no valid target/weapon type

class Explosion(pygame.sprite.Sprite):
    """Visual explosion effect."""
    def __init__(self, center, size_category='medium'): # e.g., 'small', 'medium', 'large'
        super().__init__()
        self.center = center
        self.animation_speed = 4  # Lower is faster animation (frames per stage)
        self.frame_count = 0
        
        # Define radii and colors for different explosion sizes
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
        self._draw_frame() # Draw initial frame

    def _draw_frame(self):
        """Draws the current stage of the explosion animation."""
        self.image.fill((0, 0, 0, 0)) # Clear surface with transparent black
        radius = self.radii[self.current_stage]
        color = self.colors[self.current_stage]
        # Draw circle in the center of the explosion's own surface
        pygame.draw.circle(self.image, color, (self.image.get_width() // 2, self.image.get_height() // 2), radius)

    def update(self):
        """Updates the explosion animation frame."""
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_stage += 1
            if self.current_stage >= self.max_stages:
                self.kill()  # Animation finished, remove sprite
            else:
                self._draw_frame() # Draw next frame

# --- Game Setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Mining Game")
clock = pygame.time.Clock()

# Fonts for UI
font = pygame.font.Font(None, 36)
menu_font = pygame.font.Font(None, 48) # Larger font for menu titles
small_font = pygame.font.Font(None, 24) # Smaller font for descriptions

# Sprite Groups
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
resources = pygame.sprite.Group()
enemies = pygame.sprite.Group()
missiles = pygame.sprite.Group() # Enemy and player missiles
plasma_bolts = pygame.sprite.Group() # Player's plasma bolts
explosions = pygame.sprite.Group() # Group for explosion animations

# Player initialization
player = Spaceship(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
all_sprites.add(player)

# Global variable to store weapon button rectangles for click detection in pause menu
weapon_buttons_rects = {}

def spawn_initial_entities():
    """Spawns initial asteroids and enemies, clearing existing ones."""
    # Clear existing dynamic sprites before spawning new ones (except player)
    for sprite in all_sprites:
        if sprite != player:
            sprite.kill()
    asteroids.empty()
    resources.empty()
    enemies.empty()
    missiles.empty()
    plasma_bolts.empty()
    explosions.empty()

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

spawn_initial_entities() # Initial spawn when game starts

def display_game_over_screen(screen, final_score):
    """Displays the game over screen with final score and restart prompt."""
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Final Score: {final_score}", True, WHITE)
    play_again_text = font.render("Press SPACE to Play Again", True, GREEN)
    screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)))
    screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
    screen.blit(play_again_text, play_again_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2/3)))
    pygame.display.flip()

def draw_pause_menu(screen):
    """Draws the pause menu with weapon selector."""
    global weapon_buttons_rects # Access the global dictionary

    # Darken the background
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) # Semi-transparent black
    screen.blit(overlay, (0, 0))

    # Title
    title_text = menu_font.render("PAUSED", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
    screen.blit(title_text, title_rect)

    # Weapon Selector Title
    weapon_selector_title = font.render("Weapon Selector:", True, YELLOW)
    screen.blit(weapon_selector_title, (SCREEN_WIDTH / 2 - weapon_selector_title.get_width() / 2, SCREEN_HEIGHT / 4 + 70))

    y_offset = SCREEN_HEIGHT / 4 + 120
    button_height = 50
    button_width = 250
    button_spacing = 10
    
    weapon_buttons_rects.clear() # Clear previous rects before redrawing

    # Draw weapon buttons
    for i, (weapon_name, weapon_info) in enumerate(WEAPON_TYPES.items()):
        button_y = y_offset + i * (button_height + button_spacing)
        button_rect = pygame.Rect(
            SCREEN_WIDTH / 2 - button_width / 2,
            button_y,
            button_width,
            button_height
        )
        weapon_buttons_rects[weapon_name] = button_rect # Store rect for click detection

        # Highlight current weapon
        button_color = BLUE if player.weapon.type_name == weapon_name else (50, 50, 50)
        text_color = WHITE

        draw_button(screen, button_rect, button_color, weapon_name, text_color, font)
        
        # Display description and cost
        desc_text = small_font.render(weapon_info["description"], True, (200, 200, 200))
        cost_text = small_font.render(f"Cost: {weapon_info['cost']}", True, YELLOW)
        
        screen.blit(desc_text, (button_rect.right + 10, button_rect.centery - 15))
        screen.blit(cost_text, (button_rect.right + 10, button_rect.centery + 5))

# --- Game Loop ---
running = True
game_over = False
game_paused = False # New flag for pause state

while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: # 'P' for Pause
                game_paused = not game_paused # Toggle pause state
                # If pausing, ensure laser is off
                if game_paused and player.active_laser:
                    player.active_laser.kill()
                    player.active_laser = None
                player.shooting_laser = False
                player.firing_weapon = False
            
            if not game_paused: # Only process game input if game is not paused
                if event.key == pygame.K_w: player.accelerate("up")
                elif event.key == pygame.K_s: player.accelerate("down")
                elif event.key == pygame.K_a: player.accelerate("left")
                elif event.key == pygame.K_d: player.accelerate("right")
                elif event.key == pygame.K_LSHIFT: player.firing_weapon = True # For Missile/Plasma
            # No specific KEYDOWN handling for menu, as it's mouse-driven
        elif event.type == pygame.KEYUP:
            if not game_paused: # Only process game input if game is not paused
                if event.key == pygame.K_w and player.speed_y < 0: player.accelerate("stop_y")
                elif event.key == pygame.K_s and player.speed_y > 0: player.accelerate("stop_y")
                elif event.key == pygame.K_a and player.speed_x < 0: player.accelerate("stop_x")
                elif event.key == pygame.K_d and player.speed_x > 0: player.accelerate("stop_x")
                elif event.key == pygame.K_LSHIFT: player.firing_weapon = False # Stop firing discrete weapons
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left mouse button
            if not game_paused:
                # This handles the Laser Cannon activation
                if player.weapon.type == "LaserCannon":
                    player.shooting_laser = True
                    if player.active_laser is None: # Create laser only if one isn't active
                        mouse_pos = pygame.mouse.get_pos()
                        player.active_laser = Laser(player.rect.center, mouse_pos)
                        all_sprites.add(player.active_laser)
                # For other weapons, mouse click might not be the primary fire, or it could be secondary
                # For now, only Laser uses continuous mouse down.
            else: # If paused, handle mouse clicks in the pause menu
                mouse_pos = event.pos
                for weapon_name, rect in weapon_buttons_rects.items():
                    if rect.collidepoint(mouse_pos):
                        weapon_info = WEAPON_TYPES[weapon_name]
                        # Check if player can afford or already has the weapon
                        if player.score >= weapon_info["cost"] or player.weapon.type_name == weapon_name:
                            if player.weapon.type_name != weapon_name: # Only deduct score if changing weapon
                                player.score -= weapon_info["cost"]
                                print(f"Purchased {weapon_name}. Score: {player.score}")
                            player.weapon.set_weapon_type(weapon_name)
                            print(f"Weapon changed to: {weapon_name}")
                            # Optionally unpause after selection: game_paused = False
                        else:
                            print(f"Not enough score to buy {weapon_name} (needs {weapon_info['cost']}). Current score: {player.score}")
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if not game_paused:
                # Deactivate Laser Cannon
                if player.weapon.type == "LaserCannon":
                    player.shooting_laser = False
                    if player.active_laser:
                        player.active_laser.kill()
                        player.active_laser = None

    if not game_over:
        if not game_paused: # Only update game elements if not paused
            # --- Update ---
            all_sprites.update() # This updates player, asteroids, enemies, missiles, plasma_bolts, explosions, active_laser

            # Player Firing Logic (based on selected weapon)
            if player.weapon.type == "MissileLauncher":
                if player.firing_weapon: # Fired with Shift key
                    # Find closest asteroid to target
                    target_asteroid = None
                    min_dist = float('inf')
                    for ast in asteroids:
                        dist = calculate_distance(player.rect.center, ast.rect.center)
                        if dist < min_dist:
                            min_dist = dist
                            target_asteroid = ast
                    
                    if target_asteroid:
                        missile_fired = player.weapon.fire(player.rect.centerx, player.rect.centery, target_asteroid)
                        if missile_fired:
                            missiles.add(missile_fired)
                            all_sprites.add(missile_fired)
            
            elif player.weapon.type == "LaserCannon":
                if player.shooting_laser and player.score > 0: # Fired with Left Mouse, drains score
                    # Update laser beam position
                    if player.active_laser:
                        player.active_laser.update_beam(player.rect.center, pygame.mouse.get_pos())
                    
                    player.score -= 0.5 # Continuous score drain
                    if player.score < 0: player.score = 0 # Prevent negative score
                    
                    # Apply continuous damage to asteroids under the mouse cursor
                    mouse_pos = pygame.mouse.get_pos()
                    for asteroid_target in list(asteroids): # Iterate over a copy for safe removal
                        if asteroid_target.rect.collidepoint(mouse_pos):
                            if asteroid_target.damage(player.weapon.damage): # Use weapon's damage
                                player.score += 5 # Score for laser destruction
                                expl = Explosion(asteroid_target.rect.center, 'small')
                                all_sprites.add(expl)
                                new_items = split_asteroid(asteroid_target)
                                asteroid_target.kill()
                                for item in new_items:
                                    all_sprites.add(item)
                                    if isinstance(item, Asteroid): asteroids.add(item)
                                    elif isinstance(item, Resource): resources.add(item)
                                break # Process one asteroid per frame for the laser
                else: # If score is zero or mouse released, stop laser
                    if player.active_laser:
                        player.active_laser.kill()
                        player.active_laser = None
                    player.shooting_laser = False # Ensure flag is off

            elif player.weapon.type == "PlasmaBlaster":
                if player.firing_weapon: # Fired with Shift key
                    mouse_pos = pygame.mouse.get_pos() # Target mouse cursor
                    plasma_bolt_fired = player.weapon.fire(player.rect.centerx, player.rect.centery, target_pos=mouse_pos)
                    if plasma_bolt_fired:
                        plasma_bolts.add(plasma_bolt_fired)
                        all_sprites.add(plasma_bolt_fired)


            # Asteroid and player collision
            collided_asteroids = pygame.sprite.spritecollide(player, asteroids, False) # False: don't kill asteroid yet
            for asteroid_hit in collided_asteroids:
                player.health -= asteroid_hit.size[0] * 2 # Damage based on size
                
                expl = Explosion(asteroid_hit.rect.center, 'medium')
                all_sprites.add(expl)

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

            # Missile and player collision (only enemy missiles target player)
            for missile in missiles:
                if missile.target == player: # Check if this missile targets the player
                    if pygame.sprite.collide_rect(missile, player):
                        player.health -= missile.damage
                        expl = Explosion(missile.rect.center, 'small') # Missile explosion on player
                        missile.kill()
                        all_sprites.add(expl)
                        if player.health <= 0:
                            game_over = True
                            break
            if game_over: continue

            # Missile and asteroid collision (player missiles and enemy missiles)
            missile_asteroid_hits = pygame.sprite.groupcollide(missiles, asteroids, True, False) # Missile killed, asteroid not (yet)
            for missile_obj, asteroids_hit_list in missile_asteroid_hits.items():
                for asteroid_obj in asteroids_hit_list:
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

            # Plasma Bolt and asteroid collision
            plasma_asteroid_hits = pygame.sprite.groupcollide(plasma_bolts, asteroids, True, False)
            for plasma_bolt_obj, asteroids_hit_list in plasma_asteroid_hits.items():
                for asteroid_obj in asteroids_hit_list:
                    if asteroid_obj.damage(plasma_bolt_obj.damage): # Plasma bolts do high damage
                        player.score += 20 # More score for plasma destruction
                        expl = Explosion(asteroid_obj.rect.center, 'large') # Larger explosion for plasma
                        all_sprites.add(expl)
                        new_items = split_asteroid(asteroid_obj)
                        asteroid_obj.kill()
                        for item in new_items:
                            all_sprites.add(item)
                            if isinstance(item, Asteroid): asteroids.add(item)
                            elif isinstance(item, Resource): resources.add(item)
                    else:
                        expl = Explosion(plasma_bolt_obj.rect.center, 'medium') # Medium impact explosion
                        all_sprites.add(expl)

            # Respawn asteroids if too few
            if len(asteroids) < 3: # Maintain a minimum number of asteroids
                for _ in range(3 - len(asteroids)):
                    x, y = generate_asteroid_position(player.rect.center, SCREEN_WIDTH, SCREEN_HEIGHT)
                    # Spawn a mix of sizes
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

        # Draw UI elements (Health, Score)
        health_text = font.render(f"Health: {max(0, int(player.health))}", True, GREEN if player.health > 30 else RED)
        score_text = font.render(f"Score: {int(player.score)}", True, BLUE)
        weapon_text = font.render(f"Weapon: {player.weapon.type_name}", True, YELLOW)
        screen.blit(health_text, (10, 10))
        screen.blit(score_text, (10, 40))
        screen.blit(weapon_text, (10, 70))

        if game_paused: # Draw pause menu on top if paused
            draw_pause_menu(screen)

        pygame.display.flip()
        clock.tick(FPS)
    else: # Game Over state
        display_game_over_screen(screen, player.score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.K_SPACE: # Restart game on SPACE
                game_over = False
                player.health = 100
                player.score = 0
                player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                player.speed_x, player.speed_y = 0,0
                player.weapon.set_weapon_type(PLAYER_WEAPON_TYPE_INIT) # Reset weapon
                if player.active_laser: # Ensure laser is cleared on restart
                    player.active_laser.kill()
                    player.active_laser = None
                player.shooting_laser = False
                player.firing_weapon = False
                
                spawn_initial_entities() # Respawn all game elements

pygame.quit()
