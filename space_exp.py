import pygame
import math
import random

# --- Pygame Initialization ---
pygame.init()

# --- Screen Dimensions ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Star Citizen Lite")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)
ORANGE = (255, 165, 0)
MINING_LASER_COLOR = (0, 255, 50) # Bright green for mining laser
STATION_COLOR = (200, 200, 255) # Light blue for space station
SHIP_PART_COLOR = (0, 150, 0) # Dark green for ship parts
CARBON_COLOR = (50, 50, 50) # Dark gray/black for Carbon
SILICON_COLOR = (150, 150, 150) # Lighter gray for Silicon
GOLD_COLOR = (255, 215, 0) # Gold
PING_COLOR = (0, 255, 100) # Bright green for ping
BUTTON_COLOR = (50, 50, 100) # Dark blue for buttons
BUTTON_HOVER_COLOR = (70, 70, 120) # Slightly lighter blue on hover
ACTIVE_BUTTON_COLOR = (100, 100, 150) # Color for active/selected button
AUTO_MINE_BEAM_COLOR = (0, 200, 255) # Cyan-like color for auto-mining beams
CHARGE_BAR_COLOR = (0, 150, 255) # Blue for charge bar
COOLDOWN_BAR_COLOR = (255, 0, 255) # Magenta for cooldown bar
BROWN = (139, 69, 19) # For Rocky Planet
CYAN = (0, 255, 255) # For Ice Planet
PURPLE = (128, 0, 128) # For Gas Giant
ELITE_ENEMY_COLOR = (150, 0, 0) # Dark red for elite enemies
SAFEZONE_COLOR = (0, 255, 255, 50) # Cyan with transparency for safezone
MINING_ZONE_COLOR = (0, 200, 0, 50) # Green with transparency for mining zones
NPC_COLOR = (0, 150, 0) # Dark green for mining NPCs
ENEMY_BASE_COLOR = (100, 0, 0) # Dark red for enemy base
TURRET_COLOR = (200, 50, 50) # Red for turrets
MISSILE_LAUNCHER_COLOR = (255, 100, 0) # Orange for missile launchers
PROXIMITY_GREEN = (0, 255, 0, 50) # Green for far proximity
PROXIMITY_YELLOW = (255, 255, 0, 100) # Yellow for medium proximity
PROXIMITY_RED = (255, 0, 0, 150) # Red for close proximity
FAST_ENEMY_COLOR = (0, 100, 150) # Dark blue for fast enemies

# --- Game Constants ---
FPS = 60
PLAYER_BASE_SPEED = 3 # Base speed for player movement
PLAYER_ROTATION_SPEED = 3
PLAYER_LASER_SPEED = 8
ENEMY_SPEED = 1.5
ENEMY_LASER_SPEED = 5
ASTEROID_MIN_SIZE = 20
ASTEROID_MAX_SIZE = 50
ASTEROID_MIN_RESOURCES = 10
ASTEROID_MAX_RESOURCES = 50
MAX_ASTEROIDS = 15 # Increased for a larger world
MAX_ENEMIES = 5 # Increased for a larger world
ENEMY_SPAWN_TIMER = 2000 # milliseconds, increased spawn rate slightly
PLAYER_SHOOT_COOLDOWN = 250 # milliseconds
ENEMY_SHOOT_COOLDOWN = 1000 # milliseconds

# Elite Enemy Constants
ELITE_ENEMY_HEALTH = 150 # Much more health
ELITE_ENEMY_DAMAGE = 20 # More damage
ELITE_ENEMY_SPEED = 2.0 # Slightly faster
ELITE_ENEMY_XP_VALUE = 300 # More XP
ELITE_ENEMY_DROP_CHANCE = 0.8 # Higher chance to drop parts
ELITE_ENEMY_SHIP_PART_AMOUNT = 3 # Drops more ship parts
ELITE_ENEMY_SPAWN_CHANCE = 0.2 # 20% chance for an enemy to be elite

# Fast Enemy Constants
FAST_ENEMY_HEALTH = 30 # Less health
FAST_ENEMY_DAMAGE = 10 # Same damage as regular enemy
FAST_ENEMY_SPEED = 3.0 # Much faster
FAST_ENEMY_XP_VALUE = 75 # Slightly less XP than regular
FAST_ENEMY_DROP_CHANCE = 0.3 # Lower chance to drop parts
FAST_ENEMY_SHIP_PART_AMOUNT = 1 # Drops less ship parts
FAST_ENEMY_SPAWN_CHANCE = 0.3 # 30% chance for an enemy to be fast

# Safezone Constants
SAFEZONE_RADIUS = 500 # Radius around the space station where enemies are culled/not spawned

# Mining Safezone Constants
NUM_MINING_ZONES = 3 # Number of mining safezones
MINING_ZONE_RADIUS = 300 # Radius of each mining safezone
MINING_ZONE_SPAWN_RANGE = 4000 # Max distance from world origin for mining zone spawn
MINING_ZONE_MAX_ASTEROIDS = 20 # More asteroids in mining zones
MINING_ZONE_MAX_NPCS = 3 # Number of mining NPCs per zone
NPC_MINING_SPEED = 1.5 # Speed of mining NPCs
NPC_MINING_DAMAGE_PER_TICK = 0.5 # Damage NPCs deal to asteroids per frame

# Enemy Base Constants
ENEMY_BASE_SIZE = 200
ENEMY_BASE_HEALTH = 1000
ENEMY_BASE_SPAWN_RANGE = 5000 # Max distance from world origin for base spawn
ENEMY_BASE_PROXIMITY_RADIUS = 1200 # Radius for proximity effects
ENEMY_BASE_TURRET_COUNT = 4
ENEMY_BASE_MISSILE_LAUNCHER_COUNT = 2
ENEMY_BASE_TURRET_FIRE_RATE = 500 # ms
ENEMY_BASE_TURRET_DAMAGE = 15
ENEMY_BASE_MISSILE_FIRE_RATE = 3000 # ms
ENEMY_BASE_MISSILE_DAMAGE = 40
ENEMY_BASE_TURRET_ACCURACY_MAX_OFFSET = 30 # Max angle offset for inaccuracy (degrees)
ENEMY_BASE_TURRET_ACCURACY_MIN_OFFSET = 0 # Min angle offset (perfect accuracy)

# Camera constants for damped movement
CAMERA_DEADZONE_WIDTH = SCREEN_WIDTH // 4
CAMERA_DEADZONE_HEIGHT = SCREEN_HEIGHT // 4
CAMERA_SPEED = 5 # How fast the camera catches up to the player

# World spawning and culling constants
WORLD_SPAWN_OFFSET = 700 # Objects will spawn within this distance from the player's current position (increased)
WORLD_CULL_DISTANCE = 1000 # Objects beyond this distance from player are removed

# Mining Tool Constants
MINING_LASER_DAMAGE_PER_TICK = 1 # Damage applied to asteroid per frame if focused (for Drill, ShortRangeLaser, LongRangeLaser, AutoMiningLaser)
DEFAULT_LASER_RANGE = 300 # Original default laser range (now for 'Laser' if it were selectable)
SHORT_RANGE_LASER_RANGE = min(SCREEN_WIDTH, SCREEN_HEIGHT) / 4 # One-fourth of screen's smaller dimension as radius
LONG_RANGE_LASER_RANGE = DEFAULT_LASER_RANGE * 2 # Double the default laser range

# Auto-Mining Laser Constants
AUTO_MINE_TARGET_COUNT = 3 # Number of asteroids to mine per burst
AUTO_MINE_RANGE = 400 # Radius around player for auto-mining targeting
RESOURCE_MAGNET_SPEED = 5 # Speed at which resources are pulled towards the player
AUTO_MINE_MAX_CHARGE = 100 # Maximum charge level for auto-mining
AUTO_MINE_CHARGE_DECREASE_RATE = 0.5 # Charge decrease per frame while active
AUTO_MINE_CHARGE_REFILL_RATE = 0.2 # Charge refill per frame while inactive/cooldown

# Space Station Constants
SPACESTATION_SIZE = 100
SPACESTATION_SPAWN_RANGE = 2000 # Max distance from world origin for station spawn
SPACESTATION_INTERACT_DISTANCE = 100 # Distance player needs to be to interact with station
HEALTH_REGEN_RATE_PER_SEC = 5 # Total health regenerated per second
HEALTH_REGEN_INCREMENT = 1 # Health regenerated per interval
HEALTH_REGEN_INTERVAL = 1000 * HEALTH_REGEN_INCREMENT / HEALTH_REGEN_RATE_PER_SEC # Milliseconds per increment


# XP and Leveling Constants
INITIAL_XP_THRESHOLD = 500
XP_THRESHOLD_MULTIPLIER = 1.5 # XP needed for next level = current_threshold * multiplier
ENEMY_XP_VALUE = 100 # XP gained per enemy destroyed

# Ship Part Constants
ENEMY_DROP_CHANCE = 0.5 # 50% chance for an enemy to drop a part
SHIP_PART_AMOUNT = 1 # Amount of parts dropped per enemy
SHIP_PART_SIZE = 10 # Visual size of the ship part

# Material Drop Constants
MATERIAL_DROP_SIZE = 8 # Visual size of dropped materials
MATERIAL_DROP_CHANCES = {
    "Carbon": 0.70,  # 70% chance (most common)
    "Silicon": 0.25, # 25% chance (uncommon)
    "Gold": 0.05     # 5% chance (rare)
}
MATERIAL_COLORS = {
    "Carbon": CARBON_COLOR,
    "Silicon": SILICON_COLOR,
    "Gold": GOLD_COLOR
}
MATERIAL_AMOUNTS = { # Amount of material dropped per successful drop
    "Carbon": 1,
    "Silicon": 1,
    "Gold": 1
}

# New Special Resource Constants
ROCKY_ORE_COLOR = (160, 82, 45) # Sienna-like color for Rocky Ore
ROCKY_ORE_DROP_CHANCE = 0.3 # 30% chance for Rocky Ore if near Rocky Planet
ROCKY_ORE_AMOUNT = 1
NEAR_PLANET_DISTANCE = 200 # Distance for an asteroid to be considered "near" a planet

GAS_GIANT_CRYSTAL_COLOR = (200, 0, 200) # Distinct purple/magenta for Gas Giant Crystal
GAS_GIANT_CRYSTAL_TRADE_COST = {"Gold": 5, "Silicon": 10, "Ship Parts": 3}
GAS_GIANT_CRYSTAL_TRADE_AMOUNT = 1

# Ping Constants
PING_COOLDOWN = 5000 # milliseconds between pings
PING_OUTGOING_SPEED = 200 # pixels per second
PING_OUTGOING_MAX_RADIUS = 1500 # Max radius for the outgoing ring
PING_OUTGOING_LIFETIME = 3 # seconds for the outgoing ring to fade
PING_INCOMING_DURATION = 1.5 # seconds for the incoming beam to be visible
PING_BEAM_LENGTH = 70 # Length of the incoming directional beam

# Planet Constants
MAX_PLANETS = 5
PLANET_SPAWN_RANGE = 3000

PLANET_TYPES = {
    "Rocky Planet": {
        "color": BROWN,
        "min_size": 100,
        "max_size": 150,
        "gravity_strength": 0.5, # How strong the pull is at max
        "gravity_radius": 300 # Radius within which gravity applies
    },
    "Ice Planet": {
        "color": CYAN,
        "min_size": 80,
        "max_size": 120,
        "gravity_strength": 0.3,
        "gravity_radius": 250
    },
    "Gas Giant": {
        "color": PURPLE,
        "min_size": 180,
        "max_size": 250,
        "gravity_strength": 0.8,
        "gravity_radius": 400
    }
}

# New Outpost Type
OUTPOST_TYPES = {
    "Trading Outpost": {
        "color": (100, 100, 200), # Blue-ish for trading outpost
        "size": 70
    }
}

# New Antenna Constants
ANTENNA_TYPES = {
    "Basic Antenna": {
        "range_multiplier": 1.0,
        "reveals_stealth": False
    },
    "Standard Antenna": {
        "range_multiplier": 1.5,
        "reveals_stealth": False
    },
    "Advanced Antenna": {
        "range_multiplier": 2.5,
        "reveals_stealth": True
    }
}

STEALTH_ASTEROID_COLOR = (10, 10, 10) # Almost black, for invisible state
STEALTH_ASTEROID_REVEAL_COLOR = (255, 100, 0) # Orange/red when revealed
STEALTH_ASTEROID_SPAWN_CHANCE = 0.1 # 10% chance for an asteroid to be stealth


# --- Fonts ---
FONT = pygame.font.Font(None, 24)
LARGE_FONT = pygame.font.Font(None, 48)
MENU_FONT = pygame.font.Font(None, 36)
INVENTORY_FONT = pygame.font.Font(None, 30)
BUTTON_FONT = pygame.font.Font(None, 30)

# --- UI Constants ---
BUTTON_PRESS_COOLDOWN = 200 # Milliseconds to prevent double-clicking

# --- Engine Constants ---
ENGINE_TYPES = {
    "Standard Thruster": {
        "top_speed_multiplier": 1.0,
        "acceleration_multiplier": 1.0,
        "gravity_resistance_multiplier": 1.0
    },
    "Ion Engine": {
        "top_speed_multiplier": 1.5, # High top speed
        "acceleration_multiplier": 0.7, # Low acceleration
        "gravity_resistance_multiplier": 0.01 # Very weak against gravity (effectively stuck)
    },
    "Space Thruster": {
        "top_speed_multiplier": 0.8, # Lower top speed
        "acceleration_multiplier": 1.3, # Fast acceleration
        "gravity_resistance_multiplier": 1.5 # Strong against gravity
    },
    "Hyper Drive": { # New engine
        "top_speed_multiplier": 5.0, # Very high top speed
        "acceleration_multiplier": 1.0, # Normal acceleration
        "gravity_resistance_multiplier": 2.0 # Very strong against gravity
    }
}

# Jump Drive Constants
JUMP_DRIVE_COOLDOWN = 10000 # milliseconds between jumps
JUMP_DRIVE_ALIGNMENT_DURATION = 1500 # milliseconds for ship to align
JUMP_DRIVE_WARP_DURATION = 2000 # milliseconds for warp animation
JUMP_DRIVE_ZOOM_FACTOR = 0.2 # How much to zoom out (e.g., 0.2 means 5x zoom out)
JUMP_DRIVE_RING_SPEED = 150 # pixels per second for rings
JUMP_DRIVE_MAX_RING_RADIUS = 500 # Max radius for the rings
JUMP_DRIVE_RING_INITIAL_OFFSET = 30 # Initial distance of rings from ship's rear
JUMP_DRIVE_RING_TRAIL_SPEED = 5 # Speed at which rings move away from ship

# --- Weapon Constants ---
WEAPON_TYPES = {
    "Laser": {
        "damage": 20,
        "speed": PLAYER_LASER_SPEED,
        "cooldown": PLAYER_SHOOT_COOLDOWN,
        "color": YELLOW,
        "projectile_type": "Projectile"
    },
    "Homing Missile": {
        "damage": 50,
        "speed": 6,
        "cooldown": 2000,
        "color": RED,
        "turn_rate": 15, # Increased for better responsiveness
        "projectile_type": "HomingMissile"
    },
    "Swarm Rocket": {
        "damage": 35, # Slightly less damage per rocket
        "speed": 5,
        "cooldown": 4000,
        "color": ORANGE,
        "turn_rate": 20, # Increased for better responsiveness
        "count": 7,
        "spread_angle": 30, # Degrees of initial spread - INCREASED FROM 15 TO 30
        "projectile_type": "SwarmRocketProjectile"
    }
}

# Homing Missile Constants
HOMING_MISSILE_LIFETIME = 5000 # milliseconds
SWARM_ROCKET_LIFETIME = 4000 # milliseconds (slightly shorter for swarm)


# --- Game Classes ---

class Player(pygame.sprite.Sprite):
    """
    Represents the player's spaceship.
    Handles movement, rotation, shooting, and resource management.
    Coordinates (self.x, self.y) are now world coordinates.
    Now includes XP, Level, Ship Parts, and various materials.
    """
    def __init__(self):
        super().__init__()
        self.original_image = pygame.Surface((30, 40), pygame.SRCALPHA)
        # Draw a simple triangle for the player ship, pointing UP (0 degrees visual angle)
        pygame.draw.polygon(self.original_image, BLUE, [(15, 0), (0, 40), (30, 40)])
        self.image = self.original_image
        # Initial rect is just for internal collision tracking, not screen position
        self.rect = self.image.get_rect(center=(0, 0)) # Start at world origin

        self.x = 0.0 # Player's world X coordinate
        self.y = 0.0 # Player's world Y coordinate
        self.base_speed = PLAYER_BASE_SPEED # Base speed constant
        self.current_speed = self.base_speed # Actual speed, adjusted by engine
        self.angle = 0 # Degrees, 0 means pointing up, positive is counter-clockwise for pygame.transform.rotate
        self.rotation_speed = PLAYER_ROTATION_SPEED
        self.health = 100
        self.max_health = 100
        self.resources = 0 # Generic resources from asteroids (old system, but kept for now)
        
        # Weapon slots and cooldowns
        self.weapon_slot_1 = "Laser"
        self.weapon_slot_2 = "None"
        self.last_shot_time_slot1 = 0
        self.last_shot_time_slot2 = 0


        # New attributes for progression
        self.level = 1
        self.current_xp = 0
        self.xp_threshold = INITIAL_XP_THRESHOLD
        self.ship_parts = 0

        # New attributes for materials
        self.carbon_ore = 0
        self.silicon_ore = 0
        self.gold_ore = 0
        self.rocky_ore = 0 # New special resource
        self.gas_giant_crystal = 0 # New special resource

        # Mining tool - Default is now Drill
        self.current_mining_tool = "Drill" # "Drill", "ShortRangeLaser", "LongRangeLaser", "AutoMiningLaser"

        # Energy Core attributes
        self.recharge_rate_multiplier = 1.0
        self.power_output_multiplier = 1.0

        # Propulsion attributes
        self.current_engine_type = "Standard Thruster"
        self.engine_top_speed_multiplier = ENGINE_TYPES[self.current_engine_type]["top_speed_multiplier"]
        self.engine_acceleration_multiplier = ENGINE_TYPES[self.current_engine_type]["acceleration_multiplier"]
        self.engine_gravity_resistance_multiplier = ENGINE_TYPES[self.current_engine_type]["gravity_resistance_multiplier"]
        
        # Antenna attributes
        self.current_antenna_type = "Basic Antenna"
        self.radar_range_multiplier = ANTENNA_TYPES[self.current_antenna_type]["range_multiplier"]

    def update(self, keys, current_time, game_state, target_angle=None):
        """
        Updates the player's position and rotation based on input.
        Player's (x, y) are world coordinates and are not clamped to screen.
        If in JUMP_DRIVE_ALIGNING state, rotates towards target_angle.
        """
        if game_state == "JUMP_DRIVE_ALIGNING" and target_angle is not None:
            # Calculate the shortest path to rotate
            diff_angle = (target_angle - self.angle + 180) % 360 - 180

            if abs(diff_angle) > 1: # Only rotate if difference is significant
                rotation_amount = self.rotation_speed * (diff_angle / abs(diff_angle)) # Rotate in correct direction
                self.angle += rotation_amount
                self.angle %= 360
            else:
                self.angle = target_angle # Snap to target if very close
        else:
            # Normal Rotation
            if keys[pygame.K_a]: # Rotate Left
                self.angle += self.rotation_speed
            if keys[pygame.K_d]: # Rotate Right
                self.angle -= self.rotation_speed
            self.angle %= 360 # Keep angle within 0-360 degrees

            # Movement (only apply if not in jump sequence)
            # Calculate movement vector based on current angle.
            rad_angle_for_movement = math.radians((270 - self.angle) % 360) # 0=up, 90=left, etc.

            effective_speed = self.base_speed * self.engine_top_speed_multiplier * self.engine_acceleration_multiplier

            if keys[pygame.K_w]: # Forward
                self.x += effective_speed * math.cos(rad_angle_for_movement)
                self.y += effective_speed * math.sin(rad_angle_for_movement)
            if keys[pygame.K_s]: # Backward
                self.x -= effective_speed * 0.5 * math.cos(rad_angle_for_movement) # Slower backward speed
                self.y -= effective_speed * 0.5 * math.sin(rad_angle_for_movement)


        # Update the rect for collision detection (using world coordinates)
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        # Rotate the image for drawing
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def set_engine(self, engine_type_name):
        """Sets the player's current engine and updates related stats."""
        if engine_type_name in ENGINE_TYPES:
            self.current_engine_type = engine_type_name
            engine_data = ENGINE_TYPES[engine_type_name]
            self.engine_top_speed_multiplier = engine_data["top_speed_multiplier"]
            self.engine_acceleration_multiplier = engine_data["acceleration_multiplier"]
            self.engine_gravity_resistance_multiplier = engine_data["gravity_resistance_multiplier"]
            print(f"Engine set to: {self.current_engine_type}")
        else:
            print(f"Error: Unknown engine type '{engine_type_name}'")

    def set_antenna(self, antenna_type_name):
        """Sets the player's current antenna and updates related stats."""
        if antenna_type_name in ANTENNA_TYPES:
            self.current_antenna_type = antenna_type_name
            antenna_data = ANTENNA_TYPES[antenna_type_name]
            self.radar_range_multiplier = antenna_data["range_multiplier"]
            print(f"Antenna set to: {self.current_antenna_type}")
        else:
            print(f"Error: Unknown antenna type '{antenna_type_name}'")

    def set_weapon(self, weapon_type_name, slot_number):
        """Sets the weapon in the specified slot."""
        if weapon_type_name in WEAPON_TYPES or weapon_type_name == "None":
            if slot_number == 1:
                self.weapon_slot_1 = weapon_type_name
                print(f"Weapon Slot 1 set to: {self.weapon_slot_1}")
            elif slot_number == 2:
                self.weapon_slot_2 = weapon_type_name
                print(f"Weapon Slot 2 set to: {self.weapon_slot_2}")
            else:
                print(f"Error: Invalid weapon slot number '{slot_number}'")
        else:
            print(f"Error: Unknown weapon type '{weapon_type_name}'")


    def shoot(self, current_time, weapon_slot_number, target_sprite=None): # Renamed target_enemy to target_sprite
        """
        Creates a new projectile based on the equipped weapon in the specified slot.
        Projectile's initial position is in world coordinates.
        target_sprite is used for homing missiles (can be enemy or base).
        """
        weapon_type = None
        last_shot_time_ref = None
        if weapon_slot_number == 1:
            weapon_type = self.weapon_slot_1
            last_shot_time_ref = self.last_shot_time_slot1
        elif weapon_slot_number == 2:
            weapon_type = self.weapon_slot_2
            last_shot_time_ref = self.last_shot_time_slot2
        
        if weapon_type == "None":
            return None # No weapon equipped in this slot

        weapon_data = WEAPON_TYPES.get(weapon_type)
        if not weapon_data:
            return None # Should not happen if weapon_type is valid

        # Apply energy core power output multiplier to cooldown
        effective_cooldown = weapon_data["cooldown"] / self.power_output_multiplier

        if current_time - last_shot_time_ref > effective_cooldown:
            # Update the correct last shot time
            if weapon_slot_number == 1:
                self.last_shot_time_slot1 = current_time
            elif weapon_slot_number == 2:
                self.last_shot_time_slot2 = current_time

            # Projectile starts from the front of the ship, using the same angle conversion for direction
            rad_angle_for_projectile = math.radians((270 - self.angle) % 360) # Player's current heading
            offset_x = 25 * math.cos(rad_angle_for_projectile) # Offset from center to front
            offset_y = 25 * math.sin(rad_angle_for_projectile)
            start_x = self.x + offset_x
            start_y = self.y + offset_y

            if weapon_data["projectile_type"] == "Projectile":
                return Projectile(start_x, start_y, self.angle, weapon_data["speed"], weapon_data["color"], weapon_data["damage"])
            elif weapon_data["projectile_type"] == "HomingMissile":
                if target_sprite: # Homing missiles need a target
                    print(f"Player.shoot: Firing Homing Missile at target_sprite at ({target_sprite.x:.2f}, {target_sprite.y:.2f})")
                    return HomingMissile(start_x, start_y, self.angle, weapon_data["speed"], weapon_data["color"], target_sprite, weapon_data["damage"], weapon_data["turn_rate"])
                else:
                    print(f"Player.shoot: No valid target found for Homing Missile in slot {weapon_slot_number}.") # Debug print
                    return None
            elif weapon_data["projectile_type"] == "SwarmRocketProjectile":
                if target_sprite: # Swarm rockets also need a target
                    print(f"Player.shoot: Firing Swarm Rocket at target_sprite at ({target_sprite.x:.2f}, {target_sprite.y:.2f})")
                    projectiles = []
                    base_angle = self.angle # Player's current angle
                    for i in range(weapon_data["count"]):
                        # Calculate spread angle for each rocket
                        spread_offset = (i - (weapon_data["count"] - 1) / 2) * weapon_data["spread_angle"]
                        rocket_angle = (base_angle + spread_offset) % 360
                        projectiles.append(SwarmRocketProjectile(start_x, start_y, rocket_angle, weapon_data["speed"], weapon_data["color"], target_sprite, weapon_data["damage"], weapon_data["turn_rate"]))
                    return projectiles
                else:
                    print(f"Player.shoot: No valid target found for Swarm Rocket in slot {weapon_slot_number}.") # Debug print
                    return None
        return None

    def take_damage(self, amount):
        """Reduces player health."""
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def add_resources(self, amount):
        """Adds resources to the player's inventory (old system)."""
        self.resources += amount

    def add_xp(self, amount):
        """Adds XP to the player and handles leveling up."""
        self.current_xp += amount
        while self.current_xp >= self.xp_threshold:
            self.current_xp -= self.xp_threshold # Carry over excess XP
            self.level += 1
            self.xp_threshold = int(self.xp_threshold * XP_THRESHOLD_MULTIPLIER)
            print(f"Player Leveled Up! New Level: {self.level}, Next XP Threshold: {self.xp_threshold}")

    def add_ship_parts(self, amount):
        """Adds ship parts to the player's inventory."""
        self.ship_parts += amount
        # print(f"Collected {amount} ship parts! Total: {self.ship_parts}") # Removed for inventory display

    def add_material(self, material_type, amount):
        """Adds specific materials to the player's inventory."""
        if material_type == "Carbon":
            self.carbon_ore += amount
        elif material_type == "Silicon":
            self.silicon_ore += amount
        elif material_type == "Gold":
            self.gold_ore += amount
        elif material_type == "RockyOre": # Handle new resource
            self.rocky_ore += amount
        elif material_type == "GasGiantCrystal": # Handle new resource
            self.gas_giant_crystal += amount
        # print(f"Collected {amount} {material_type}! Total: Carbon: {self.carbon_ore}, Silicon: {self.silicon_ore}, Gold: {self.gold_ore}") # Removed for inventory display

    def draw(self, screen, camera_x, camera_y):
        """
        Draws the player ship on the screen relative to the camera.
        """
        # Calculate screen position from world position and camera offset
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        # Get the rect for drawing, centered at the screen position
        draw_rect = self.image.get_rect(center=(screen_x, screen_y))
        screen.blit(self.image, draw_rect)

class Asteroid(pygame.sprite.Sprite):
    """
    Represents an asteroid that can be mined for resources.
    Coordinates (self.x, self.y) are world coordinates.
    Now includes health for mining and drops specific materials.
    """
    def __init__(self, x, y, size, resources, is_stealth=False):
        super().__init__()
        self.size = size
        self.resources = resources
        self.max_health = size * 2 # Larger asteroids have more health
        self.health = self.max_health
        self.is_stealth = is_stealth
        self.is_revealed = False # Only for stealth asteroids, becomes True when advanced antenna is active

        if self.is_stealth:
            self.original_color = STEALTH_ASTEROID_COLOR # This is its base hidden color
            self.image = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, self.original_color, (size, size), size)
        else:
            self.original_color = GRAY # Regular asteroid color
            self.image = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, self.original_color, (size, size), size)

        self.rect = self.image.get_rect(center=(x, y)) # Rect uses world coordinates
        self.x = float(x)
        self.y = float(y)

    def take_damage(self, amount):
        """Reduces asteroid health."""
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def get_material_drop(self):
        """
        Determines which material to drop based on defined chances.
        Returns the material type and amount, or None if no drop.
        """
        roll = random.random() # 0.0 to 1.0
        cumulative_chance = 0.0
        material_to_drop = None

        # Create a list of (material_type, chance) tuples to iterate in a specific order
        ordered_materials = [
            ("Carbon", MATERIAL_DROP_CHANCES["Carbon"]),
            ("Silicon", MATERIAL_DROP_CHANCES["Silicon"]),
            ("Gold", MATERIAL_DROP_CHANCES["Gold"])
        ]

        for material_type, chance in ordered_materials:
            cumulative_chance += chance
            if roll < cumulative_chance: # Use < for exclusive upper bound
                material_to_drop = material_type
                break
        
        if material_to_drop:
            return material_type, MATERIAL_AMOUNTS[material_to_drop]
        return None, 0


    def draw(self, screen, camera_x, camera_y):
        """
        Draws the asteroid on the screen relative to the camera.
        Also draws a health bar for the asteroid.
        """
        # Only draw if not stealth or if revealed
        if not self.is_stealth or self.is_revealed:
            screen_x = self.x - camera_x
            screen_y = self.y - camera_y
            draw_rect = self.image.get_rect(center=(screen_x, screen_y))
            SCREEN.blit(self.image, draw_rect)

            # Draw health bar
            if self.health < self.max_health: # Only show if damaged
                bar_width = self.size * 2
                bar_height = 5
                health_percentage = self.health / self.max_health
                current_health_width = int(bar_width * health_percentage)

                health_bar_bg_rect = pygame.Rect(screen_x - self.size, screen_y + self.size + 5, bar_width, bar_height)
                health_bar_rect = pygame.Rect(screen_x - self.size, screen_y + self.size + 5, current_health_width, bar_height)

                pygame.draw.rect(screen, RED, health_bar_bg_rect)
                pygame.draw.rect(screen, GREEN, health_bar_rect)


class Enemy(pygame.sprite.Sprite):
    """
    Represents an enemy spaceship.
    Moves towards the player and shoots.
    Coordinates (self.x, self.y) are world coordinates.
    """
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.Surface((30, 30), pygame.SRCALPHA)
        # Draw a simple square for the enemy ship
        pygame.draw.rect(self.original_image, RED, (0, 0, 30, 30))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y)) # Rect uses world coordinates

        self.x = float(x)
        self.y = float(y)
        self.base_speed = ENEMY_SPEED # Store base speed
        self.speed = ENEMY_SPEED
        self.health = 50
        self.max_health = 50
        self.last_shot_time = 0
        self.angle = 0 # Initialize angle
        self.vx = 0.0 # Add vx
        self.vy = 0.0 # Add vy
        self.xp_value = ENEMY_XP_VALUE
        self.drop_chance = ENEMY_DROP_CHANCE
        self.ship_part_amount = SHIP_PART_AMOUNT
        self.base_damage = 10 # Base damage for enemy projectiles
        self.current_damage = self.base_damage
        self.base_cooldown = ENEMY_SHOOT_COOLDOWN
        self.current_cooldown = self.base_cooldown
        self.accuracy_offset = 0 # No accuracy offset by default

    def update(self, player_pos, current_time, proximity_multiplier=1.0):
        """
        Updates the enemy's position to move towards the player.
        Applies proximity_multiplier to speed, damage, and accuracy.
        All positions are in world coordinates.
        """
        # Apply proximity buffs
        self.speed = self.base_speed * proximity_multiplier
        self.current_damage = int(self.base_damage * proximity_multiplier)
        self.current_cooldown = self.base_cooldown / proximity_multiplier # Faster cooldown
        # Accuracy: higher multiplier means less offset (more accurate)
        # The 2.0 in the denominator assumes a max multiplier of 2.0. If multiplier goes higher, adjust this.
        self.accuracy_offset = ENEMY_BASE_TURRET_ACCURACY_MAX_OFFSET * (1 - (proximity_multiplier - 1) / (2.0 - 1.0))
        self.accuracy_offset = max(ENEMY_BASE_TURRET_ACCURACY_MIN_OFFSET, min(ENEMY_BASE_TURRET_ACCURACY_MAX_OFFSET, self.accuracy_offset))


        # Calculate angle to player using atan2, which gives angle relative to positive x-axis.
        # Add 90 degrees to convert to our visual angle convention (0=up, 90=left, etc.)
        dx = player_pos[0] - self.x
        dy = player_pos[1] - self.y
        self.angle = math.degrees(math.atan2(dy, dx)) + 90
        self.angle %= 360 # Keep angle within 0-360 degrees

        # Calculate movement vector based on current angle.
        rad_angle_for_movement = math.radians((270 - self.angle) % 360)
        self.vx = self.speed * math.cos(rad_angle_for_movement) # Store vx
        self.vy = self.speed * math.sin(rad_angle_for_movement) # Store vy

        self.x += self.vx # Apply movement
        self.y += self.vy # Apply movement

        # Update the rect for collision detection (using world coordinates)
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        # Rotate image to face player
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        # The rect for drawing will be calculated in the draw method based on camera offset
        self.rect = self.image.get_rect(center=(self.x, self.y))


    def shoot(self, current_time):
        """
        Creates a new projectile if cooldown allows.
        Projectile's initial position is in world coordinates.
        Applies accuracy offset.
        """
        if current_time - self.last_shot_time > self.current_cooldown:
            self.last_shot_time = current_time
            # Projectile starts from the front of the ship, using the same angle conversion for direction
            rad_angle_for_projectile = math.radians((270 - self.angle) % 360)
            offset_x = 20 * math.cos(rad_angle_for_projectile) # Offset from center to front
            offset_y = 20 * math.sin(rad_angle_for_projectile)
            start_x = self.x + offset_x
            start_y = self.y + offset_y

            # Apply accuracy offset
            actual_angle = self.angle + random.uniform(-self.accuracy_offset, self.accuracy_offset)

            return Projectile(start_x, start_y, actual_angle, ENEMY_LASER_SPEED, ORANGE, self.current_damage)
        return None

    def take_damage(self, amount):
        """Reduces enemy health."""
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def draw(self, screen, camera_x, camera_y):
        """
        Draws the enemy ship on the screen relative to the camera.
        """
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        draw_rect = self.image.get_rect(center=(screen_x, screen_y))
        SCREEN.blit(self.image, draw_rect)

class EliteEnemy(Enemy):
    """
    A stronger version of the regular enemy.
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.original_image = pygame.Surface((40, 40), pygame.SRCALPHA) # Slightly larger
        pygame.draw.rect(self.original_image, ELITE_ENEMY_COLOR, (0, 0, 40, 40), border_radius=5) # Dark red, rounded
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        self.base_speed = ELITE_ENEMY_SPEED
        self.speed = ELITE_ENEMY_SPEED
        self.health = ELITE_ENEMY_HEALTH
        self.max_health = ELITE_ENEMY_HEALTH
        self.xp_value = ELITE_ENEMY_XP_VALUE
        self.drop_chance = ELITE_ENEMY_DROP_CHANCE
        self.ship_part_amount = ELITE_ENEMY_SHIP_PART_AMOUNT
        self.base_damage = ELITE_ENEMY_DAMAGE
        self.current_damage = self.base_damage
        self.base_cooldown = ENEMY_SHOOT_COOLDOWN / 2 # Elite enemies shoot faster
        self.current_cooldown = self.base_cooldown

class FastEnemy(Enemy):
    """
    A faster but weaker version of the regular enemy.
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.original_image = pygame.Surface((25, 25), pygame.SRCALPHA) # Slightly smaller
        pygame.draw.circle(self.original_image, FAST_ENEMY_COLOR, (12, 12), 12) # Blue circle
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        self.base_speed = FAST_ENEMY_SPEED
        self.speed = FAST_ENEMY_SPEED
        self.health = FAST_ENEMY_HEALTH
        self.max_health = FAST_ENEMY_HEALTH
        self.xp_value = FAST_ENEMY_XP_VALUE
        self.drop_chance = FAST_ENEMY_DROP_CHANCE
        self.ship_part_amount = FAST_ENEMY_SHIP_PART_AMOUNT
        self.base_damage = FAST_ENEMY_DAMAGE
        self.current_damage = self.base_damage
        self.base_cooldown = ENEMY_SHOOT_COOLDOWN * 0.75 # Slightly faster cooldown
        self.current_cooldown = self.base_cooldown


class Projectile(pygame.sprite.Sprite):
    """
    Represents a laser projectile fired by player or enemy.
    Coordinates (self.x, self.y) are world coordinates.
    """
    def __init__(self, x, y, angle, speed, color, damage):
        super().__init__()
        self.image = pygame.Surface((5, 10), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, 5, 10))
        self.rect = self.image.get_rect(center=(x, y)) # Rect uses world coordinates

        self.x = float(x)
        self.y = float(y)
        self.angle = angle # This angle is the visual angle (0=up, 90=left, etc.)
        self.speed = speed
        self.color = color
        self.damage = damage

        # Calculate velocity components using the corrected angle conversion
        rad_angle_for_movement = math.radians((270 - self.angle) % 360)
        self.vx = self.speed * math.cos(rad_angle_for_movement)
        self.vy = self.speed * math.sin(rad_angle_for_movement)

    def update(self, camera_x, camera_y, current_time=None, game_manager=None): # Added game_manager for HomingMissile
        """
        Updates the projectile's position in world coordinates.
        Removes projectile if it goes far off the visible screen.
        """
        self.x += self.vx
        self.y += self.vy
        # Update the rect for collision detection (using world coordinates)
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        # Remove projectile if it goes off screen (with a margin for camera movement)
        # Check if the projectile is outside the camera's view plus a buffer
        if not (self.x > camera_x - 100 and self.x < camera_x + SCREEN_WIDTH + 100 and \
                self.y > camera_y - 100 and self.y < camera_y + SCREEN_HEIGHT + 100):
            self.kill() # Removes the sprite from all groups it belongs to

    def draw(self, screen, camera_x, camera_y):
        """
        Draws the projectile on the screen relative to the camera.
        """
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        draw_rect = self.image.get_rect(center=(screen_x, screen_y))
        SCREEN.blit(self.image, draw_rect)

class HomingMissile(Projectile):
    """
    A projectile that homes in on a target enemy or base.
    """
    def __init__(self, x, y, angle, speed, color, target_sprite, damage, turn_rate):
        # Pass a dummy angle to Projectile as its vx/vy will be re-calculated
        super().__init__(x, y, angle, speed, color, damage) 
        self.target = target_sprite # Can be player, enemy, or enemy base
        self.turn_rate = turn_rate
        self.image = pygame.Surface((8, 15), pygame.SRCALPHA) # Slightly larger missile image
        pygame.draw.rect(self.image, self.color, (0, 0, 8, 15), border_radius=2) # Rounded rectangle
        self.original_image = self.image.copy() # Store original for rotation

        # Calculate initial velocity directly towards target
        if self.target: # Ensure target exists
            target_x, target_y = self.target.x, self.target.y # Use target's world coordinates
            dx = target_x - x
            dy = target_y - y
            dist = math.hypot(dx, dy)
            if dist > 0:
                self.vx = self.speed * (dx / dist)
                self.vy = self.speed * (dy / dist)
                # Set initial visual angle based on this initial velocity
                self.angle = (math.degrees(math.atan2(self.vy, self.vx)) + 90) % 360
            else:
                self.vx = 0
                self.vy = 0
                self.angle = angle # Fallback to player's angle if no distance
        else: # If no target, use initial angle
            rad_angle_for_movement = math.radians((270 - angle) % 360) # Use the initial angle passed in
            self.vx = self.speed * math.cos(rad_angle_for_movement)
            self.vy = self.speed * math.sin(rad_angle_for_movement)
            self.angle = angle # Keep the initial angle

        self.lifetime = HOMING_MISSILE_LIFETIME # milliseconds
        self.deathtime = pygame.time.get_ticks() + self.lifetime

    def update(self, camera_x, camera_y, current_time, game_manager=None):
        """
        Updates the missile's position, homing towards its target.
        """
        # Check for lifetime
        if current_time > self.deathtime:
            self.kill()
            return # Stop updating if dead

        # If current target is invalid, try to find a new one (only for player missiles)
        if not self.target or not self.target.alive():
            if game_manager and (isinstance(self.target, Enemy) or isinstance(self.target, EnemyBase)): # Only player missiles re-target enemies/base
                # Search for a new target within a reasonable range from the missile's current position
                self.target = game_manager.find_nearest_enemy_or_base_to_point(self.x, self.y, max_range=500) # Updated method
                if not self.target:
                    pass # Keep existing vx, vy
            elif game_manager and isinstance(self.target, Player): # Enemy missiles target player
                if not game_manager.player.alive(): # If player is dead, stop homing
                    self.target = None
                    pass
                else: # Player is still alive, keep targeting
                    pass

        # If target is valid and alive, home in
        if self.target and self.target.alive():
            target_x, target_y = self.target.x, self.target.y
            
            dx = target_x - self.x
            dy = target_y - self.y
            
            desired_angle_rad = math.atan2(dy, dx) # Angle from positive x-axis

            current_speed_magnitude = math.hypot(self.vx, self.vy)
            if current_speed_magnitude == 0:
                self.vx = self.speed * math.cos(desired_angle_rad)
                self.vy = self.speed * math.sin(desired_angle_rad)
                current_speed_magnitude = self.speed

            current_angle_rad = math.atan2(self.vy, self.vx)

            angle_diff_rad = (desired_angle_rad - current_angle_rad + math.pi + 2*math.pi) % (2*math.pi) - math.pi

            max_turn_rad = math.radians(self.turn_rate)
            turn_amount_rad = max(-max_turn_rad, min(max_turn_rad, angle_diff_rad))

            new_vx = self.vx * math.cos(turn_amount_rad) - self.vy * math.sin(turn_amount_rad)
            new_vy = self.vx * math.sin(turn_amount_rad) + self.vy * math.cos(turn_amount_rad)

            new_speed_magnitude = math.hypot(new_vx, new_vy)
            if new_speed_magnitude > 0:
                self.vx = self.speed * (new_vx / new_speed_magnitude)
                self.vy = self.speed * (new_vy / new_speed_magnitude)
            else:
                self.vx = self.speed * math.cos(desired_angle_rad)
                self.vy = self.speed * math.sin(desired_angle_rad)

            self.angle = (math.degrees(math.atan2(self.vy, self.vx)) + 90) % 360

        else:
            pass # If target is lost or dead, continue in last known direction

        super().update(camera_x, camera_y, current_time, game_manager)

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))


class SwarmRocketProjectile(HomingMissile):
    """
    A smaller homing missile used in swarm rockets.
    Initializes with a specific angle (for spread) then homes.
    """
    def __init__(self, x, y, angle, speed, color, target_sprite, damage, turn_rate): # Renamed target_enemy to target_sprite
        super().__init__(x, y, angle, speed, color, target_sprite, damage, turn_rate)
        
        # Override the initial velocity set by HomingMissile's __init__
        # to use the spread angle provided. Homing will then take over in update.
        rad_angle_for_initial_spread = math.radians((270 - angle) % 360)
        self.vx = self.speed * math.cos(rad_angle_for_initial_spread)
        self.vy = self.speed * math.sin(rad_angle_for_initial_spread)
        self.angle = angle # Ensure visual angle matches initial direction

        self.image = pygame.Surface((6, 12), pygame.SRCALPHA) # Even smaller missile image
        pygame.draw.rect(self.image, self.color, (0, 0, 6, 12), border_radius=1)
        self.original_image = self.image.copy()
        
        self.lifetime = SWARM_ROCKET_LIFETIME # Use a different constant
        self.deathtime = pygame.time.get_ticks() + self.lifetime


class SpaceStation(pygame.sprite.Sprite):
    """
    Represents a space station where the player can pause and be safe.
    """
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        # Draw a simple station shape: a square outline with a central circle
        pygame.draw.rect(self.image, STATION_COLOR, (0, 0, size, size), 3) # Outline
        pygame.draw.circle(self.image, STATION_COLOR, (size // 2, size // 2), size // 4, 0) # Filled inner circle
        self.rect = self.image.get_rect(center=(x, y))
        self.x = float(x)
        self.y = float(y)
        self.size = size

    def draw(self, screen, camera_x, camera_y):
        """
        Draws the space station on the screen relative to the camera.
        """
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        draw_rect = self.image.get_rect(center=(screen_x, screen_y))
        SCREEN.blit(self.image, draw_rect)

class TradingOutpost(pygame.sprite.Sprite):
    """
    Represents a trading outpost, specifically for the Gas Giant.
    """
    def __init__(self, x, y, size, color):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        # Draw a simple outpost shape: a hexagon
        points = []
        for i in range(6):
            angle = math.pi * 2 / 6 * i
            px = size // 2 + (size // 2 - 5) * math.cos(angle)
            py = size // 2 + (size // 2 - 5) * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(self.image, color, points, 3) # Outline
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 4, 0) # Central circle
        self.rect = self.image.get_rect(center=(x, y))
        self.x = float(x)
        self.y = float(y)
        self.size = size
        self.color = color

    def draw(self, screen, camera_x, camera_y):
        """
        Draws the trading outpost on the screen relative to the camera.
        """
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        draw_rect = self.image.get_rect(center=(screen_x, screen_y))
        SCREEN.blit(self.image, draw_rect)


class ShipPart(pygame.sprite.Sprite):
    """
    Represents a collectible ship part dropped by enemies.
    """
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(self.image, SHIP_PART_COLOR, (0, 0, size, size)) # Small green square
        self.rect = self.image.get_rect(center=(x, y))
        self.x = float(x)
        self.y = float(y)
        self.size = size

    def draw(self, screen, camera_x, camera_y):
        """
        Draws the ship part on the screen relative to the camera.
        """
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        draw_rect = self.image.get_rect(center=(screen_x, screen_y))
        SCREEN.blit(self.image, draw_rect)

class MaterialDrop(pygame.sprite.Sprite):
    """
    Represents a collectible material dropped by asteroids.
    """
    def __init__(self, x, y, material_type, amount, size):
        super().__init__()
        self.material_type = material_type
        self.amount = amount
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Update MATERIAL_COLORS to include new resources
        updated_material_colors = MATERIAL_COLORS.copy()
        updated_material_colors["RockyOre"] = ROCKY_ORE_COLOR
        updated_material_colors["GasGiantCrystal"] = GAS_GIANT_CRYSTAL_COLOR

        pygame.draw.circle(self.image, updated_material_colors[material_type], (size // 2, size // 2), size // 2) # Small colored circle
        self.rect = self.image.get_rect(center=(x, y))
        self.x = float(x)
        self.y = float(y)
        self.size = size

    def draw(self, screen, camera_x, camera_y):
        """
        Draws the material drop on the screen relative to the camera.
        """
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        draw_rect = self.image.get_rect(center=(screen_x, screen_y))
        SCREEN.blit(self.image, draw_rect)

class Planet(pygame.sprite.Sprite):
    """
    Represents a planet with gravitational pull.
    """
    def __init__(self, x, y, planet_type_name):
        super().__init__()
        self.planet_type_name = planet_type_name
        type_data = PLANET_TYPES[planet_type_name]
        
        self.color = type_data["color"]
        self.size = random.randint(type_data["min_size"], type_data["max_size"])
        self.gravity_strength = type_data["gravity_strength"]
        self.gravity_radius = type_data["gravity_radius"]

        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.size, self.size), self.size)
        self.rect = self.image.get_rect(center=(x, y))
        self.x = float(x)
        self.y = float(y)

    def draw(self, screen, camera_x, camera_y):
        """
        Draws the planet on the screen relative to the camera.
        """
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        draw_rect = self.image.get_rect(center=(screen_x, screen_y))
        SCREEN.blit(self.image, draw_rect)

class MiningSafezone:
    """
    Represents a dedicated mining zone with a high concentration of asteroids and mining NPCs.
    """
    def __init__(self, x, y, radius, max_asteroids, max_npcs):
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.max_asteroids = max_asteroids
        self.max_npcs = max_npcs
        self.asteroids_in_zone = pygame.sprite.Group() # Asteroids specifically in this zone
        self.npcs_in_zone = pygame.sprite.Group() # NPCs specifically in this zone

    def draw(self, screen, camera_x, camera_y, zoom_factor):
        """
        Draws the mining safezone circle.
        """
        screen_x, screen_y = GameManager.world_to_screen_static(self.x, self.y, camera_x, camera_y, zoom_factor)
        scaled_radius = int(self.radius * zoom_factor)
        
        if scaled_radius > 0:
            safezone_surface = pygame.Surface((scaled_radius * 2, scaled_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(safezone_surface, MINING_ZONE_COLOR, (scaled_radius, scaled_radius), scaled_radius)
            
            safezone_rect = safezone_surface.get_rect(center=(screen_x, screen_y))
            screen.blit(safezone_surface, safezone_rect)

class MiningNPC(pygame.sprite.Sprite):
    """
    A non-hostile NPC that mines asteroids within its assigned safezone.
    """
    def __init__(self, x, y, zone_id):
        super().__init__()
        self.original_image = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, NPC_COLOR, [(12, 0), (0, 25), (25, 25)]) # Simple triangle
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        self.x = float(x)
        self.y = float(y)
        self.speed = NPC_MINING_SPEED
        self.angle = 0 # Visual angle
        self.target_asteroid = None
        self.zone_id = zone_id # Which mining zone it belongs to

    def update(self, current_time, asteroids_in_zone, game_manager):
        """
        Moves towards and mines the nearest asteroid in its zone.
        """
        # If current target is gone or mined, find a new one
        if not self.target_asteroid or not self.target_asteroid.alive() or self.target_asteroid.health <= 0:
            self.target_asteroid = self.find_nearest_asteroid(asteroids_in_zone)

        if self.target_asteroid:
            dx = self.target_asteroid.x - self.x
            dy = self.target_asteroid.y - self.y
            distance = math.hypot(dx, dy)

            # Move towards asteroid
            if distance > self.target_asteroid.size / 2: # Stop just before colliding to "mine"
                self.x += self.speed * (dx / distance)
                self.y += self.speed * (dy / distance)
                
                # Update visual angle to face target
                self.angle = math.degrees(math.atan2(dy, dx)) + 90
                self.angle %= 360
            else:
                # Mine the asteroid
                self.target_asteroid.take_damage(NPC_MINING_DAMAGE_PER_TICK)
                if self.target_asteroid.health <= 0:
                    # Drop resources when asteroid is destroyed
                    # Check for Rocky Ore drop if near a Rocky Planet
                    is_near_rocky_planet = False
                    for planet in game_manager.planets:
                        if planet.planet_type_name == "Rocky Planet":
                            dist_to_planet = math.hypot(self.target_asteroid.x - planet.x, self.target_asteroid.y - planet.y)
                            if dist_to_planet < planet.size + NEAR_PLANET_DISTANCE:
                                is_near_rocky_planet = True
                                break
                    
                    if is_near_rocky_planet and random.random() < ROCKY_ORE_DROP_CHANCE:
                        game_manager.material_drops_group.add(MaterialDrop(self.target_asteroid.x, self.target_asteroid.y, "RockyOre", ROCKY_ORE_AMOUNT, MATERIAL_DROP_SIZE))
                    
                    # Always drop regular materials
                    material_type, amount = self.target_asteroid.get_material_drop()
                    if material_type:
                        game_manager.material_drops_group.add(MaterialDrop(self.target_asteroid.x, self.target_asteroid.y, material_type, amount, MATERIAL_DROP_SIZE))
                    
                    self.target_asteroid.kill() # Remove asteroid from its group
                    self.target_asteroid = None # Clear target
                    # The game manager will re-spawn asteroids in the zone

        # Update rect for collision detection (using world coordinates)
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

        # Rotate image for drawing
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def find_nearest_asteroid(self, asteroids_in_zone):
        """Finds the nearest asteroid within the NPC's zone."""
        nearest_asteroid = None
        min_dist = float('inf')
        for asteroid in asteroids_in_zone:
            dist = math.hypot(self.x - asteroid.x, self.y - asteroid.y)
            if dist < min_dist:
                min_dist = dist
                nearest_asteroid = asteroid
        return nearest_asteroid

    def draw(self, screen, camera_x, camera_y, zoom_factor):
        """
        Draws the mining NPC on the screen relative to the camera.
        """
        screen_x, screen_y = GameManager.world_to_screen_static(self.x, self.y, camera_x, camera_y, zoom_factor)
        scaled_width = int(self.original_image.get_width() * zoom_factor)
        scaled_height = int(self.original_image.get_height() * zoom_factor)
        if scaled_width > 0 and scaled_height > 0:
            scaled_npc_image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))
            scaled_rotated_npc_image = pygame.transform.rotate(scaled_npc_image, self.angle)
            draw_rect = scaled_rotated_npc_image.get_rect(center=(screen_x, screen_y))
            screen.blit(scaled_rotated_npc_image, draw_rect)

class EnemyBase(pygame.sprite.Sprite):
    """
    Represents a static enemy base with turrets and missile launchers.
    Enemies become stronger closer to the base.
    """
    def __init__(self, x, y, size, game_manager):
        super().__init__()
        self.game_manager = game_manager # Reference to game manager for projectile spawning
        self.size = size
        self.max_health = ENEMY_BASE_HEALTH
        self.health = self.max_health
        self.x = float(x)
        self.y = float(y)
        self.rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)

        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(self.image, ENEMY_BASE_COLOR, (0, 0, self.size, self.size), border_radius=10)
        pygame.draw.circle(self.image, (150, 0, 0), (self.size // 2, self.size // 2), self.size // 4) # Central core

        self.turret_positions = [] # Relative positions of turrets
        self.missile_launcher_positions = [] # Relative positions of missile launchers

        # Define turret positions (e.g., corners of the base)
        turret_offset = self.size // 2 - 15
        self.turret_positions.append((-turret_offset, -turret_offset)) # Top-left
        self.turret_positions.append((turret_offset, -turret_offset))  # Top-right
        self.turret_positions.append((-turret_offset, turret_offset))  # Bottom-left
        self.turret_positions.append((turret_offset, turret_offset))   # Bottom-right

        self.last_turret_shot_time = pygame.time.get_ticks()
        self.last_missile_shot_time = pygame.time.get_ticks()

    def update(self, current_time, player_pos):
        """
        Updates the base's turrets and missile launchers.
        """
        # Turret firing logic
        if current_time - self.last_turret_shot_time > ENEMY_BASE_TURRET_FIRE_RATE:
            self.last_turret_shot_time = current_time
            for rel_x, rel_y in self.turret_positions:
                turret_world_x = self.x + rel_x
                turret_world_y = self.y + rel_y

                dx = player_pos[0] - turret_world_x
                dy = player_pos[1] - turret_world_y
                target_angle = (math.degrees(math.atan2(dy, dx)) + 90) % 360

                # Calculate accuracy offset based on distance to player
                dist_to_player = math.hypot(player_pos[0] - self.x, player_pos[1] - self.y)
                # Linearly interpolate accuracy: closer = smaller offset
                # When dist = 0, offset = MIN_OFFSET. When dist = PROXIMITY_RADIUS, offset = MAX_OFFSET.
                # Clamp to prevent negative or excessive offsets
                accuracy_ratio = min(1.0, dist_to_player / ENEMY_BASE_PROXIMITY_RADIUS)
                accuracy_offset = ENEMY_BASE_TURRET_ACCURACY_MIN_OFFSET + (ENEMY_BASE_TURRET_ACCURACY_MAX_OFFSET - ENEMY_BASE_TURRET_ACCURACY_MIN_OFFSET) * accuracy_ratio
                
                actual_angle = target_angle + random.uniform(-accuracy_offset, accuracy_offset)
                
                # Spawn projectile
                self.game_manager.enemy_projectiles.add(Projectile(turret_world_x, turret_world_y, actual_angle, ENEMY_LASER_SPEED, TURRET_COLOR, ENEMY_BASE_TURRET_DAMAGE))

        # Missile launcher firing logic
        if current_time - self.last_missile_shot_time > ENEMY_BASE_MISSILE_FIRE_RATE:
            self.last_missile_shot_time = current_time
            # Define missile launcher positions (moved here from __init__ to ensure it's always defined)
            launcher_offset = self.size // 2 - 30
            self.missile_launcher_positions = []
            self.missile_launcher_positions.append((0, -launcher_offset)) # Top center
            self.missile_launcher_positions.append((0, launcher_offset))  # Bottom center

            for rel_x, rel_y in self.missile_launcher_positions:
                launcher_world_x = self.x + rel_x
                launcher_world_y = self.y + rel_y

                # Spawn homing missile targeting the player
                self.game_manager.enemy_projectiles.add(HomingMissile(launcher_world_x, launcher_world_y, 0, 
                                                                       ENEMY_LASER_SPEED * 0.8, MISSILE_LAUNCHER_COLOR, 
                                                                       self.game_manager.player, ENEMY_BASE_MISSILE_DAMAGE, 10)) # Slower, but homing


    def take_damage(self, amount):
        """Reduces base health."""
        self.health -= amount
        if self.health < 0:
            self.health = 0
            # Potentially trigger base destruction event here

    def draw(self, screen, camera_x, camera_y, zoom_factor):
        """
        Draws the enemy base and its components.
        """
        screen_x, screen_y = GameManager.world_to_screen_static(self.x, self.y, camera_x, camera_y, zoom_factor)
        scaled_size = int(self.size * zoom_factor)
        
        if scaled_size > 0:
            scaled_base_image = pygame.transform.scale(self.image, (scaled_size, scaled_size))
            draw_rect = scaled_base_image.get_rect(center=(screen_x, screen_y))
            screen.blit(scaled_base_image, draw_rect)

            # Draw turrets
            turret_size = int(10 * zoom_factor) or 1
            for rel_x, rel_y in self.turret_positions:
                turret_screen_x, turret_screen_y = GameManager.world_to_screen_static(self.x + rel_x, self.y + rel_y, camera_x, camera_y, zoom_factor)
                pygame.draw.circle(screen, TURRET_COLOR, (int(turret_screen_x), int(turret_screen_y)), turret_size)
                pygame.draw.circle(screen, WHITE, (int(turret_screen_x), int(turret_screen_y)), turret_size, 1) # Outline

            # Draw missile launchers
            launcher_size = int(15 * zoom_factor) or 1
            # Ensure missile_launcher_positions is defined before iterating
            if hasattr(self, 'missile_launcher_positions'):
                for rel_x, rel_y in self.missile_launcher_positions:
                    launcher_screen_x, launcher_screen_y = GameManager.world_to_screen_static(self.x + rel_x, self.y + rel_y, camera_x, camera_y, zoom_factor)
                    pygame.draw.rect(screen, MISSILE_LAUNCHER_COLOR, (launcher_screen_x - launcher_size // 2, launcher_screen_y - launcher_size // 2, launcher_size, launcher_size), border_radius=int(launcher_size * 0.2))
                    pygame.draw.rect(screen, WHITE, (launcher_screen_x - launcher_size // 2, launcher_screen_y - launcher_size // 2, launcher_size, launcher_size), 1, border_radius=int(launcher_size * 0.2)) # Outline

            # Draw health bar for the base
            if self.health < self.max_health:
                bar_width = int(self.size * zoom_factor)
                bar_height = int(10 * zoom_factor)
                health_percentage = self.health / self.max_health
                current_health_width = int(bar_width * health_percentage)

                health_bar_bg_rect = pygame.Rect(screen_x - bar_width // 2, screen_y + scaled_size // 2 + int(10 * zoom_factor), bar_width, bar_height)
                health_bar_rect = pygame.Rect(screen_x - bar_width // 2, screen_y + scaled_size // 2 + int(10 * zoom_factor), current_health_width, bar_height)

                pygame.draw.rect(screen, RED, health_bar_bg_rect)
                pygame.draw.rect(screen, GREEN, health_bar_rect)


# --- Game Manager ---
class GameManager:
    """
    Manages all game objects and game state, including the camera and mining laser.
    """
    def __init__(self):
        self.player = Player()
        self.asteroids = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.ship_parts_group = pygame.sprite.Group() # New group for ship parts
        self.material_drops_group = pygame.sprite.Group() # New group for material drops
        self.planets = pygame.sprite.Group() # New group for planets
        self.mining_zones = [] # List to hold MiningSafezone objects
        self.mining_npcs = pygame.sprite.Group() # Group for all mining NPCs
        self.enemy_base = None # New: Enemy Base

        self.game_over = False
        self.last_enemy_spawn_time = pygame.time.get_ticks()

        # Camera position (top-left corner of the visible world area)
        self.camera_x = self.player.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.y - SCREEN_HEIGHT // 2

        # Mining laser state (for mouse-activated lasers)
        self.mining_laser_active = False # True when 'F' is held for non-auto-mining tools
        self.mouse_world_x = 0
        self.mouse_world_y = 0

        # Auto-mining laser state
        self.auto_mine_active = False # True when F is pressed and auto-mining is ongoing
        self.targeted_asteroids = [] # List to hold asteroids currently being auto-mined
        self.auto_mine_charge = AUTO_MINE_MAX_CHARGE # Current charge of the auto-mining laser

        # Space Station
        self.space_station = None
        self.spawn_space_station() # Spawn station at game start

        # Trading Outpost (new)
        self.trading_outpost = None

        self.last_regen_time = pygame.time.get_ticks() # For health regeneration

        # Game State
        self.game_state = "PLAYING" # "PLAYING", "PAUSED_AT_STATION", "INVENTORY", "ECONOMY_SHOP", "SHIP_UPGRADING", "SHIP_SHOP", "MINING_TOOLS_MENU", "ENERGY_CORE_MENU", "ANTENNA_MENU", "WEAPONS_MENU", "PROPULSION_MENU", "JUMP_DRIVE_SELECT_TARGET", "JUMP_DRIVE_ALIGNING", "JUMP_DRIVE_WARP", "TRADING_OUTPOST_MENU"
        self.previous_game_state = "PLAYING" # To return to correct state after inventory
        self.e_pressed_last_frame = False # To detect single key press for 'E'
        self.i_pressed_last_frame = False # To detect single key press for 'I'
        self.f_pressed_last_frame = False # To detect single key press for 'F' (auto-mine)

        # Ping System
        self.last_ping_time = 0
        self.outgoing_ping_active = False
        self.outgoing_ping_start_time = 0
        self.outgoing_ping_world_pos = (0, 0)
        self.incoming_ping_active = False
        self.incoming_ping_start_time = 0
        self.ping_t_pressed_last_frame = False # To detect single 'T' press

        # Buttons for menus
        self.buttons = {} # Stores {'button_name': pygame.Rect} for click detection
        self.last_button_press_time = 0 # Track last time any menu button was pressed

        # Current Energy Core
        self.current_energy_core = "Standard Core"

        # Jump Drive attributes
        self.last_jump_time = 0
        self.jump_target_world_pos = None
        self.jump_initiation_start_time = 0 # Used for alignment and warp duration
        self.jump_rings_active = False
        self.jump_rings_start_time = 0
        self.jump_drive_zoom_active = False # Flag to control zoom level
        self.r_pressed_last_frame = False

        # Weapon selection for menu
        self.selected_weapon_slot = 1 # 1 or 2, for assigning weapons in menu

        self.spawn_initial_asteroids()
        self.spawn_initial_planets() # Spawn planets at game start
        self.spawn_mining_zones() # Spawn mining zones
        self.spawn_enemy_base() # Spawn enemy base

    @staticmethod
    def world_to_screen_static(world_x, world_y, camera_x, camera_y, zoom_factor):
        """
        Static method to convert world coordinates to screen coordinates, considering camera offset and zoom.
        Used by classes that don't have direct access to GameManager instance.
        """
        screen_x = (world_x - camera_x) * zoom_factor
        screen_y = (world_y - camera_y) * zoom_factor
        return screen_x, screen_y

    def spawn_initial_asteroids(self):
        """Spawns a set number of asteroids around the player's initial position."""
        for _ in range(MAX_ASTEROIDS):
            self.spawn_asteroid()

    def spawn_asteroid(self, in_mining_zone=None):
        """
        Spawns a single asteroid at a random location.
        If in_mining_zone is provided, spawns within that zone.
        """
        x, y = 0, 0
        if in_mining_zone:
            # Spawn within the specified mining zone
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, in_mining_zone.radius)
            x = in_mining_zone.x + distance * math.cos(angle)
            y = in_mining_zone.y + distance * math.sin(angle)
        else:
            # Spawn generally in the world, relative to player
            x = self.player.x + random.randint(-WORLD_SPAWN_OFFSET, WORLD_SPAWN_OFFSET)
            y = self.player.y + random.randint(-WORLD_SPAWN_OFFSET, WORLD_SPAWN_OFFSET)
            
            # Ensure general asteroids don't spawn in mining zones, main safezone, or enemy base proximity
            attempts = 0
            max_attempts = 5
            while attempts < max_attempts:
                is_in_safezone = False
                # Check main safezone
                dist_to_station = math.hypot(x - self.space_station.x, y - self.space_station.y)
                if dist_to_station < SAFEZONE_RADIUS:
                    is_in_safezone = True
                
                # Check mining zones
                for zone in self.mining_zones:
                    dist_to_zone = math.hypot(x - zone.x, y - zone.y)
                    if dist_to_zone < zone.radius:
                        is_in_safezone = True
                        break
                
                # Check enemy base proximity
                if self.enemy_base:
                    dist_to_base = math.hypot(x - self.enemy_base.x, y - self.enemy_base.y)
                    if dist_to_base < ENEMY_BASE_PROXIMITY_RADIUS:
                        is_in_safezone = True

                if not is_in_safezone:
                    break # Found a good spot
                
                # If in a safezone, try new coordinates
                x = self.player.x + random.randint(-WORLD_SPAWN_OFFSET, WORLD_SPAWN_OFFSET)
                y = self.player.y + random.randint(-WORLD_SPAWN_OFFSET, WORLD_SPAWN_OFFSET)
                attempts += 1
            
            if attempts == max_attempts: # Fallback if no good spot found
                print("Warning: Could not find suitable general asteroid spawn location.")
                return # Don't spawn if no good spot after attempts


        size = random.randint(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE)
        resources = random.randint(ASTEROID_MIN_RESOURCES, ASTEROID_MAX_RESOURCES)
        
        is_stealth = False
        if random.random() < STEALTH_ASTEROID_SPAWN_CHANCE:
            is_stealth = True
        
        new_asteroid = Asteroid(x, y, size, resources, is_stealth)
        self.asteroids.add(new_asteroid)
        if in_mining_zone:
            in_mining_zone.asteroids_in_zone.add(new_asteroid)


    def spawn_enemy(self):
        """Spawns an enemy at a random location just outside the current screen view,
        ensuring it's outside the safezone, mining zones, and enemy base.
        Now includes a chance to spawn FastEnemy."""
        spawn_margin = 100 # Margin outside the screen
        
        # Try to find a spawn location outside the safezone and mining zones
        attempts = 0
        max_attempts = 10
        while attempts < max_attempts:
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                x = self.camera_x + random.randint(0, SCREEN_WIDTH)
                y = self.camera_y - spawn_margin
            elif side == 'bottom':
                x = self.camera_x + random.randint(0, SCREEN_WIDTH)
                y = self.camera_y + SCREEN_HEIGHT + spawn_margin
            elif side == 'left':
                x = self.camera_x - spawn_margin
                y = self.camera_y + random.randint(0, SCREEN_HEIGHT)
            else: # right
                x = self.camera_x + SCREEN_WIDTH + spawn_margin
                y = self.camera_y + random.randint(0, SCREEN_HEIGHT)
            
            # Check if the proposed spawn location is within the main safezone
            dist_to_station = math.hypot(x - self.space_station.x, y - self.space_station.y)
            if dist_to_station < SAFEZONE_RADIUS:
                attempts += 1
                continue # Try again if in main safezone

            # Check if the proposed spawn location is within any mining safezone
            is_in_mining_zone = False
            for zone in self.mining_zones:
                dist_to_zone = math.hypot(x - zone.x, y - zone.y)
                if dist_to_zone < zone.radius:
                    is_in_mining_zone = True
                    break
            
            if is_in_mining_zone:
                attempts += 1
                continue # Try again if in a mining zone

            # Check if the proposed spawn location is too close to the enemy base
            if self.enemy_base:
                dist_to_base = math.hypot(x - self.enemy_base.x, y - self.enemy_base.y)
                if dist_to_base < self.enemy_base.size + 100: # Don't spawn inside or right next to base
                    attempts += 1
                    continue

            # If we reach here, the location is outside all safezones and the base
            # Decide enemy type
            roll = random.random()
            if roll < ELITE_ENEMY_SPAWN_CHANCE:
                self.enemies.add(EliteEnemy(x, y))
            elif roll < ELITE_ENEMY_SPAWN_CHANCE + FAST_ENEMY_SPAWN_CHANCE:
                self.enemies.add(FastEnemy(x, y))
            else:
                self.enemies.add(Enemy(x, y))
            return # Successfully spawned an enemy
        print("Could not find a suitable enemy spawn location outside safezones after multiple attempts.")


    def spawn_space_station(self):
        """Spawns the space station at a random location far from the origin."""
        x = random.randint(-SPACESTATION_SPAWN_RANGE, SPACESTATION_SPAWN_RANGE)
        y = random.randint(-SPACESTATION_SPAWN_RANGE, SPACESTATION_SPAWN_RANGE)
        self.space_station = SpaceStation(x, y, SPACESTATION_SIZE)
        print(f"Space Station spawned at world coordinates: ({x}, {y})")

    def spawn_planet(self):
        """Spawns a single planet at a random location far from the origin."""
        x = random.randint(-PLANET_SPAWN_RANGE, PLANET_SPAWN_RANGE)
        y = random.randint(-PLANET_SPAWN_RANGE, PLANET_SPAWN_RANGE)
        planet_type_name = random.choice(list(PLANET_TYPES.keys()))
        new_planet = Planet(x, y, planet_type_name)
        self.planets.add(new_planet)

        # If it's a Gas Giant, spawn a Trading Outpost at its center
        if planet_type_name == "Gas Giant" and self.trading_outpost is None: # Ensure only one trading outpost for now
            outpost_data = OUTPOST_TYPES["Trading Outpost"]
            self.trading_outpost = TradingOutpost(x, y, outpost_data["size"], outpost_data["color"])
            print(f"Trading Outpost spawned at Gas Giant: ({x}, {y})")


    def spawn_initial_planets(self):
        """Spawns a set number of planets."""
        for _ in range(MAX_PLANETS):
            self.spawn_planet()

    def spawn_mining_zones(self):
        """Spawns a set number of mining safezones."""
        for i in range(NUM_MINING_ZONES):
            # Spawn far from origin and other zones
            x = random.randint(-MINING_ZONE_SPAWN_RANGE, MINING_ZONE_SPAWN_RANGE)
            y = random.randint(-MINING_ZONE_SPAWN_RANGE, MINING_ZONE_SPAWN_RANGE)
            
            # Ensure it's not too close to the main space station or enemy base
            attempts = 0
            max_attempts = 5
            while attempts < max_attempts:
                too_close = False
                if math.hypot(x - self.space_station.x, y - self.space_station.y) < SAFEZONE_RADIUS + MINING_ZONE_RADIUS + 200:
                    too_close = True
                if self.enemy_base and math.hypot(x - self.enemy_base.x, y - self.enemy_base.y) < ENEMY_BASE_PROXIMITY_RADIUS + MINING_ZONE_RADIUS + 200:
                    too_close = True

                if not too_close:
                    break
                
                x = random.randint(-MINING_ZONE_SPAWN_RANGE, MINING_ZONE_SPAWN_RANGE)
                y = random.randint(-MINING_ZONE_SPAWN_RANGE, MINING_ZONE_SPAWN_RANGE)
                attempts += 1
            
            if attempts == max_attempts:
                print(f"Warning: Could not find suitable location for Mining Zone {i+1}.")
                continue

            new_zone = MiningSafezone(x, y, MINING_ZONE_RADIUS, MINING_ZONE_MAX_ASTEROIDS, MINING_ZONE_MAX_NPCS)
            self.mining_zones.append(new_zone)
            print(f"Mining Zone {i+1} spawned at ({x}, {y}) with radius {MINING_ZONE_RADIUS}")

    def spawn_mining_npc(self, mining_zone):
        """Spawns a mining NPC within a specific mining zone."""
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, mining_zone.radius * 0.8) # Spawn slightly inwards
        x = mining_zone.x + distance * math.cos(angle)
        y = mining_zone.y + distance * math.sin(angle)
        
        new_npc = MiningNPC(x, y, mining_zone) # Pass the zone object itself
        self.mining_npcs.add(new_npc)
        mining_zone.npcs_in_zone.add(new_npc)

    def spawn_enemy_base(self):
        """Spawns the enemy base at a random location far from the origin,
        and not too close to the space station or mining zones."""
        x = random.randint(-ENEMY_BASE_SPAWN_RANGE, ENEMY_BASE_SPAWN_RANGE)
        y = random.randint(-ENEMY_BASE_SPAWN_RANGE, ENEMY_BASE_SPAWN_RANGE)

        attempts = 0
        max_attempts = 10
        while attempts < max_attempts:
            too_close = False
            # Check proximity to space station
            dist_to_station = math.hypot(x - self.space_station.x, y - self.space_station.y)
            if dist_to_station < SAFEZONE_RADIUS + ENEMY_BASE_PROXIMITY_RADIUS + 500: # Ensure good separation
                too_close = True

            # Check proximity to mining zones
            for zone in self.mining_zones:
                dist_to_zone = math.hypot(x - zone.x, y - zone.y)
                if dist_to_zone < zone.radius + ENEMY_BASE_PROXIMITY_RADIUS + 500:
                    too_close = True
                    break
            
            if not too_close:
                break # Found a good spot
            
            x = random.randint(-ENEMY_BASE_SPAWN_RANGE, ENEMY_BASE_SPAWN_RANGE)
            y = random.randint(-ENEMY_BASE_SPAWN_RANGE, ENEMY_BASE_SPAWN_RANGE)
            attempts += 1
        
        if attempts == max_attempts:
            print("Warning: Could not find suitable location for Enemy Base. Spawning at default.")
            x, y = 3000, 3000 # Fallback if no good spot found

        self.enemy_base = EnemyBase(x, y, ENEMY_BASE_SIZE, self)
        print(f"Enemy Base spawned at world coordinates: ({x}, {y})")


    def world_to_screen(self, world_x, world_y):
        """
        Converts world coordinates to screen coordinates, considering camera offset and zoom.
        """
        zoom_factor = JUMP_DRIVE_ZOOM_FACTOR if self.jump_drive_zoom_active else 1.0
        
        # Calculate position relative to camera's top-left world coordinate
        # Then scale by zoom factor
        screen_x = (world_x - self.camera_x) * zoom_factor
        screen_y = (world_y - self.camera_y) * zoom_factor
        return screen_x, screen_y

    def is_visible_on_screen(self, obj_x, obj_y, obj_radius):
        """
        Checks if an object is currently visible on the screen, considering camera offset and zoom.
        obj_radius is half the object's width/height for a circular/square object.
        """
        zoom_factor = JUMP_DRIVE_ZOOM_FACTOR if self.jump_drive_zoom_active else 1.0
        
        # Convert object's world coordinates to screen coordinates
        screen_x, screen_y = self.world_to_screen(obj_x, obj_y)
        
        # Scale the object's radius by the zoom factor
        scaled_radius = obj_radius * zoom_factor

        # Check if the object's bounding box intersects the screen area
        return (screen_x + scaled_radius > 0 and screen_x - scaled_radius < SCREEN_WIDTH and
                screen_y + scaled_radius > 0 and screen_y - scaled_radius < SCREEN_HEIGHT)


    def start_auto_mine_targeting(self):
        """Identifies and sets targets for the auto-mining laser."""
        self.targeted_asteroids.clear()
        potential_targets = []
        for asteroid in self.asteroids:
            dist_to_asteroid = math.hypot(self.player.x - asteroid.x, self.player.y - asteroid.y)
            # Check if within auto-mine range AND visible on screen
            if (not asteroid.is_stealth or asteroid.is_revealed) and \
               dist_to_asteroid <= AUTO_MINE_RANGE and self.is_visible_on_screen(asteroid.x, asteroid.y, asteroid.size):
                potential_targets.append(asteroid)
        
        # Sort by distance and take the closest ones
        potential_targets.sort(key=lambda a: math.hypot(self.player.x - a.x, self.player.y - a.y))
        self.targeted_asteroids = potential_targets[:AUTO_MINE_TARGET_COUNT]


    def handle_input(self, keys, current_time):
        """Handles player input and menu navigation."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0] # Left mouse button

        # Convert mouse screen position to world coordinates
        self.mouse_world_x = mouse_pos[0] + self.camera_x
        self.mouse_world_y = mouse_pos[1] + self.camera_y

        # Find enemy or base under mouse cursor for targeting
        hovered_target = None
        # Check if mouse is over enemy base first
        if self.enemy_base and self.enemy_base.rect.collidepoint(self.mouse_world_x, self.mouse_world_y):
            hovered_target = self.enemy_base
        else:
            # Otherwise, check for enemies
            for enemy in self.enemies:
                if enemy.rect.collidepoint(self.mouse_world_x, self.mouse_world_y):
                    hovered_target = enemy
                    break # Found one, no need to check others

        # Check for button press cooldown
        can_press_button = (current_time - self.last_button_press_time > BUTTON_PRESS_COOLDOWN)

        # Handle 'E' key for space station/outpost interaction
        e_pressed_this_frame = keys[pygame.K_e]
        if e_pressed_this_frame and not self.e_pressed_last_frame and can_press_button:
            if self.game_state == "PLAYING":
                # Check for Space Station interaction
                dist_to_station = math.hypot(self.player.x - self.space_station.x, self.player.y - self.space_station.y)
                if dist_to_station < SPACESTATION_INTERACT_DISTANCE:
                    self.game_state = "PAUSED_AT_STATION" # Enter main station menu
                    self.last_button_press_time = current_time # Reset cooldown
                    print("Entered Space Station!")
                # Check for Trading Outpost interaction
                elif self.trading_outpost and math.hypot(self.player.x - self.trading_outpost.x, self.player.y - self.trading_outpost.y) < self.trading_outpost.size + 50:
                    self.game_state = "TRADING_OUTPOST_MENU"
                    self.last_button_press_time = current_time
                    print("Entered Trading Outpost!")
            elif self.game_state == "PAUSED_AT_STATION":
                self.game_state = "PLAYING" # Exit station to playing
                self.last_button_press_time = current_time # Reset cooldown
                print("Exited Space Station. Resuming game.")
            elif self.game_state == "TRADING_OUTPOST_MENU":
                self.game_state = "PLAYING" # Exit outpost to playing
                self.last_button_press_time = current_time # Reset cooldown
                print("Exited Trading Outpost. Resuming game.")
            # No direct 'E' exit from sub-menus, must use 'Back' button
        self.e_pressed_last_frame = e_pressed_this_frame

        # Handle 'I' key for inventory
        i_pressed_this_frame = keys[pygame.K_i]
        if i_pressed_this_frame and not self.i_pressed_last_frame and can_press_button:
            if self.game_state == "INVENTORY":
                self.game_state = self.previous_game_state # Return to previous state
                self.last_button_press_time = current_time # Reset cooldown
                print("Closed Inventory.")
            else:
                self.previous_game_state = self.game_state # Store current state
                self.game_state = "INVENTORY" # Go to inventory
                self.last_button_press_time = current_time # Reset cooldown
                print("Opened Inventory!")
        self.i_pressed_last_frame = i_pressed_this_frame

        # Handle 'F' key for all mining tools
        f_pressed_this_frame = keys[pygame.K_f]
        if self.game_state == "PLAYING":
            if self.player.current_mining_tool == "AutoMiningLaser":
                if f_pressed_this_frame and not self.f_pressed_last_frame: # Toggle on F press
                    if self.auto_mine_active: # If active, deactivate
                        self.auto_mine_active = False
                        self.targeted_asteroids.clear()
                        print("Auto-mining laser deactivated.")
                    elif self.auto_mine_charge > 0: # If inactive and has charge, activate
                        self.auto_mine_active = True
                        self.start_auto_mine_targeting()
                        if not self.targeted_asteroids: # If no targets found, immediately deactivate
                            self.auto_mine_active = False
                            print("Auto-mining laser activated, but no visible targets found.")
                        if self.auto_mine_active:
                            print(f"Auto-mining laser activated! Targeting {len(self.targeted_asteroids)} asteroids.")
                    elif self.auto_mine_charge <= 0:
                        print("Auto-mining laser has no charge!")
            else: # For Drill, ShortRangeLaser, LongRangeLaser
                self.mining_laser_active = f_pressed_this_frame # Active while F is held

        self.f_pressed_last_frame = f_pressed_this_frame


        # Handle 'T' key for ping function (only in PLAYING state, with cooldown)
        t_pressed_this_frame = keys[pygame.K_t]
        if t_pressed_this_frame and not self.ping_t_pressed_last_frame and can_press_button:
            if self.game_state == "PLAYING" and current_time - self.last_ping_time > PING_COOLDOWN:
                self.outgoing_ping_active = True
                self.outgoing_ping_start_time = current_time
                self.outgoing_ping_world_pos = (self.player.x, self.player.y)
                self.incoming_ping_active = False # Reset incoming ping on new outgoing
                self.last_ping_time = current_time
                self.last_button_press_time = current_time
                print("Ping initiated!")
        self.ping_t_pressed_last_frame = t_pressed_this_frame

        # Handle 'R' key for Jump Drive
        r_pressed_this_frame = keys[pygame.K_r]
        if r_pressed_this_frame and not self.r_pressed_last_frame and can_press_button:
            if self.game_state == "PLAYING" and self.player.current_engine_type == "Hyper Drive":
                # Hyper Drive cooldown influenced by energy core
                effective_jump_cooldown = JUMP_DRIVE_COOLDOWN / self.player.recharge_rate_multiplier
                if current_time - self.last_jump_time > effective_jump_cooldown:
                    self.game_state = "JUMP_DRIVE_SELECT_TARGET"
                    self.jump_drive_zoom_active = True # Zoom out for target selection
                    self.last_button_press_time = current_time
                    print("Jump Drive activated: Select target.")
                else:
                    remaining_cooldown = (effective_jump_cooldown - (current_time - self.last_jump_time)) / 1000.0
                    print(f"Jump Drive on cooldown. Remaining: {remaining_cooldown:.1f}s")
            elif self.game_state == "JUMP_DRIVE_SELECT_TARGET":
                # If R is pressed again in target selection, cancel jump
                self.game_state = "PLAYING"
                self.jump_drive_zoom_active = False
                self.jump_target_world_pos = None
                self.last_button_press_time = current_time
                print("Jump Drive cancelled.")
        self.r_pressed_last_frame = r_pressed_this_frame


        # --- Game State Specific Input Handling (other than mining tools) ---
        if self.game_state == "PLAYING":
            self.player.update(keys, current_time, self.game_state) # Player movement

            if keys[pygame.K_SPACE]:
                # Determine target for weapon 1 based on its type
                # For homing/swarm, use the hovered_target (enemy or base)
                target_for_slot1 = None
                if self.player.weapon_slot_1 in ["Homing Missile", "Swarm Rocket"]:
                    target_for_slot1 = hovered_target # Use hovered enemy or base as target
                    if not target_for_slot1: # If no hovered target, don't fire homing/swarm
                        pass # Do nothing, effectively preventing fire
                
                # Only attempt to fire if it's a Laser (doesn't need a target) or if a target is found for homing/swarm
                if self.player.weapon_slot_1 == "Laser" or (self.player.weapon_slot_1 in ["Homing Missile", "Swarm Rocket"] and target_for_slot1):
                    new_projectile = self.player.shoot(current_time, 1, target_for_slot1)
                    if new_projectile:
                        if isinstance(new_projectile, list): # For swarm rockets
                            self.player_projectiles.add(*new_projectile)
                        else:
                            self.player_projectiles.add(new_projectile)

            if keys[pygame.K_LCTRL]: # New key for second weapon slot
                # Determine target for weapon 2 based on its type
                target_for_slot2 = None
                if self.player.weapon_slot_2 in ["Homing Missile", "Swarm Rocket"]:
                    target_for_slot2 = hovered_target # Use hovered enemy or base as target
                    if not target_for_slot2: # If no hovered target, don't fire homing/swarm
                        pass # Do nothing, effectively preventing fire

                # Only attempt to fire if it's a Laser (doesn't needs a target) or if a target is found for homing/swarm
                if self.player.weapon_slot_2 == "Laser" or (self.player.weapon_slot_2 in ["Homing Missile", "Swarm Rocket"] and target_for_slot2):
                    new_projectile = self.player.shoot(current_time, 2, target_for_slot2)
                    if new_projectile:
                        if isinstance(new_projectile, list): # For swarm rockets
                            self.player_projectiles.add(*new_projectile)
                        else:
                            self.player_projectiles.add(new_projectile)
            
        elif self.game_state == "PAUSED_AT_STATION":
            if mouse_clicked and can_press_button: # Left mouse button click for menu navigation
                if 'resume_button' in self.buttons and self.buttons['resume_button'].collidepoint(mouse_pos):
                    self.game_state = "PLAYING"
                    self.last_button_press_time = current_time # Reset cooldown
                    print("Resuming game.")
                elif 'economy_button' in self.buttons and self.buttons['economy_button'].collidepoint(mouse_pos):
                    self.game_state = "ECONOMY_SHOP"
                    self.last_button_press_time = current_time # Reset cooldown
                    print("Entering Economy Shop.")
                elif 'upgrade_button' in self.buttons and self.buttons['upgrade_button'].collidepoint(mouse_pos):
                    self.game_state = "SHIP_UPGRADING"
                    self.last_button_press_time = current_time # Reset cooldown
                    print("Entering Ship Upgrading.")
                elif 'shop_button' in self.buttons and self.buttons['shop_button'].collidepoint(mouse_pos):
                    self.game_state = "SHIP_SHOP"
                    self.last_button_press_time = current_time # Reset cooldown
                    print("Entering Ship Shop.")

        elif self.game_state == "SHIP_UPGRADING":
            if mouse_clicked and can_press_button:
                if 'mining_tools_button' in self.buttons and self.buttons['mining_tools_button'].collidepoint(mouse_pos):
                    self.game_state = "MINING_TOOLS_MENU"
                    self.last_button_press_time = current_time # Reset cooldown
                    print("Entering Mining Tools Menu.")
                elif 'energy_core_button' in self.buttons and self.buttons['energy_core_button'].collidepoint(mouse_pos):
                    self.game_state = "ENERGY_CORE_MENU"
                    self.last_button_press_time = current_time # Reset cooldown
                    print("Entering Energy Core Menu.")
                elif 'antenna_radar_button' in self.buttons and self.buttons['antenna_radar_button'].collidepoint(mouse_pos):
                    self.game_state = "ANTENNA_MENU" # Change state to Antenna Menu
                    self.last_button_press_time = current_time # Reset cooldown
                    print("Entering Antenna/Radar Systems Menu.")
                elif 'weapons_button' in self.buttons and self.buttons['weapons_button'].collidepoint(mouse_pos):
                    self.game_state = "WEAPONS_MENU"
                    self.last_button_press_time = current_time # Reset cooldown
                    print("Entering Weapons Menu.")
                elif 'propulsion_button' in self.buttons and self.buttons['propulsion_button'].collidepoint(mouse_pos):
                    self.game_state = "PROPULSION_MENU"
                    self.last_button_press_time = current_time # Reset cooldown
                    print("Entering Propulsion Menu.")
                elif 'back_button' in self.buttons and self.buttons['back_button'].collidepoint(mouse_pos):
                    self.game_state = "PAUSED_AT_STATION" # Go back to main station menu
                    self.last_button_press_time = current_time # Reset cooldown
                    print("Returning to Space Station main menu.")

        elif self.game_state == "MINING_TOOLS_MENU":
            if mouse_clicked and can_press_button:
                # No "Laser" button anymore
                if 'drill_button' in self.buttons and self.buttons['drill_button'].collidepoint(mouse_pos):
                    self.player.current_mining_tool = "Drill"
                    # If switching from AutoMiningLaser, deactivate it
                    if self.auto_mine_active:
                        self.auto_mine_active = False
                        self.targeted_asteroids.clear()
                    self.last_button_press_time = current_time # Reset cooldown
                    print(f"Mining tool set to: {self.player.current_mining_tool}")
                elif 'short_range_laser_button' in self.buttons and self.buttons['short_range_laser_button'].collidepoint(mouse_pos):
                    self.player.current_mining_tool = "ShortRangeLaser"
                    if self.auto_mine_active:
                        self.auto_mine_active = False
                        self.targeted_asteroids.clear()
                    self.last_button_press_time = current_time # Reset cooldown
                    print(f"Mining tool set to: {self.player.current_mining_tool}")
                elif 'long_range_laser_button' in self.buttons and self.buttons['long_range_laser_button'].collidepoint(mouse_pos):
                    self.player.current_mining_tool = "LongRangeLaser"
                    if self.auto_mine_active:
                        self.auto_mine_active = False
                        self.targeted_asteroids.clear()
                    self.last_button_press_time = current_time # Reset cooldown
                    print(f"Mining tool set to: {self.player.current_mining_tool}")
                elif 'auto_mining_laser_button' in self.buttons and self.buttons['auto_mining_laser_button'].collidepoint(mouse_pos):
                    self.player.current_mining_tool = "AutoMiningLaser"
                    self.last_button_press_time = current_time # Reset cooldown
                    print(f"Mining tool set to: {self.player.current_mining_tool}")
                elif 'back_button' in self.buttons and self.buttons['back_button'].collidepoint(mouse_pos):
                    self.game_state = "SHIP_UPGRADING" # Go back to ship upgrading menu
                    self.last_button_press_time = current_time # Reset cooldown
                    print("Returning to Ship Upgrading menu.")

        elif self.game_state == "ENERGY_CORE_MENU":
            if mouse_clicked and can_press_button:
                if 'standard_core_button' in self.buttons and self.buttons['standard_core_button'].collidepoint(mouse_pos):
                    self.player.recharge_rate_multiplier = 1.0
                    self.player.power_output_multiplier = 1.0
                    self.current_energy_core = "Standard Core"
                    self.last_button_press_time = current_time # Reset cooldown
                    print("Energy Core set to: Standard Core")
                elif 'advanced_core_button' in self.buttons and self.buttons['advanced_core_button'].collidepoint(mouse_pos):
                    self.player.recharge_rate_multiplier = 1.5 # Example multiplier
                    self.player.power_output_multiplier = 1.2 # Example multiplier
                    self.current_energy_core = "Advanced Core"
                    self.last_button_press_time = current_time # Reset cooldown
                    print("Energy Core set to: Advanced Core")
                elif 'back_button' in self.buttons and self.buttons['back_button'].collidepoint(mouse_pos):
                    self.game_state = "SHIP_UPGRADING"
                    self.last_button_press_time = current_time # Reset cooldown
                    print("Returning to Ship Upgrading menu.")

        elif self.game_state == "ANTENNA_MENU": # New menu state
            if mouse_clicked and can_press_button:
                if 'basic_antenna_button' in self.buttons and self.buttons['basic_antenna_button'].collidepoint(mouse_pos):
                    self.player.set_antenna("Basic Antenna")
                    self.last_button_press_time = current_time
                elif 'standard_antenna_button' in self.buttons and self.buttons['standard_antenna_button'].collidepoint(mouse_pos):
                    self.player.set_antenna("Standard Antenna")
                    self.last_button_press_time = current_time
                elif 'advanced_antenna_button' in self.buttons and self.buttons['advanced_antenna_button'].collidepoint(mouse_pos):
                    self.player.set_antenna("Advanced Antenna")
                    self.last_button_press_time = current_time
                elif 'back_button' in self.buttons and self.buttons['back_button'].collidepoint(mouse_pos):
                    self.game_state = "SHIP_UPGRADING"
                    self.last_button_press_time = current_time
                    print("Returning to Ship Upgrading menu.")

        elif self.game_state == "WEAPONS_MENU": # New menu state for weapons
            if mouse_clicked and can_press_button:
                # Slot selection buttons
                if 'slot1_button' in self.buttons and self.buttons['slot1_button'].collidepoint(mouse_pos):
                    self.selected_weapon_slot = 1
                    self.last_button_press_time = current_time
                elif 'slot2_button' in self.buttons and self.buttons['slot2_button'].collidepoint(mouse_pos):
                    self.selected_weapon_slot = 2
                    self.last_button_press_time = current_time
                
                # Weapon assignment buttons
                if 'laser_weapon_button' in self.buttons and self.buttons['laser_weapon_button'].collidepoint(mouse_pos):
                    self.player.set_weapon("Laser", self.selected_weapon_slot)
                    self.last_button_press_time = current_time
                elif 'laser_turret_buttom' in self.buttons and self.buttons['laser_turret_button'].collidepoint(mouse_pos):
                    self.player.set_weapon("Homing Missile", self.selected_weapon_slot)
                    self.last_button_press_time = current_time
                elif 'mini_gun_turret_button' in self.buttons and self.buttons['min_gun_turret_button'].collidepoint(mouse_pos):
                    self.player.set_weapon("Homing Missile", self.selected_weapon_slot)
                    self.last_button_press_time = current_time
                elif 'homing_missile_button' in self.buttons and self.buttons['homing_missile_button'].collidepoint(mouse_pos):
                    self.player.set_weapon("Homing Missile", self.selected_weapon_slot)
                    self.last_button_press_time = current_time
                elif 'swarm_rocket_button' in self.buttons and self.buttons['swarm_rocket_button'].collidepoint(mouse_pos):
                    self.player.set_weapon("Swarm Rocket", self.selected_weapon_slot)
                    self.last_button_press_time = current_time
                elif 'none_weapon_button' in self.buttons and self.buttons['none_weapon_button'].collidepoint(mouse_pos):
                    self.player.set_weapon("None", self.selected_weapon_slot)
                    self.last_button_press_time = current_time

                elif 'back_button' in self.buttons and self.buttons['back_button'].collidepoint(mouse_pos):
                    self.game_state = "SHIP_UPGRADING"
                    self.last_button_press_time = current_time
                    print("Returning to Ship Upgrading menu.")

        elif self.game_state == "PROPULSION_MENU":
            if mouse_clicked and can_press_button:
                if 'standard_thruster_button' in self.buttons and self.buttons['standard_thruster_button'].collidepoint(mouse_pos):
                    self.player.set_engine("Standard Thruster")
                    self.last_button_press_time = current_time
                elif 'ion_engine_button' in self.buttons and self.buttons['ion_engine_button'].collidepoint(mouse_pos):
                    self.player.set_engine("Ion Engine")
                    self.last_button_press_time = current_time
                elif 'space_thruster_button' in self.buttons and self.buttons['space_thruster_button'].collidepoint(mouse_pos):
                    self.player.set_engine("Space Thruster")
                    self.last_button_press_time = current_time
                elif 'hyper_drive_button' in self.buttons and self.buttons['hyper_drive_button'].collidepoint(mouse_pos): # New button
                    self.player.set_engine("Hyper Drive")
                    self.last_button_press_time = current_time
                elif 'back_button' in self.buttons and self.buttons['back_button'].collidepoint(mouse_pos):
                    self.game_state = "SHIP_UPGRADING"
                    self.last_button_press_time = current_time
                    print("Returning to Ship Upgrading menu.")

        elif self.game_state == "JUMP_DRIVE_SELECT_TARGET":
            if mouse_clicked:
                # Convert mouse screen position to world position using the zoom factor
                self.jump_target_world_pos = (
                    self.player.x + (mouse_pos[0] - SCREEN_WIDTH // 2) / JUMP_DRIVE_ZOOM_FACTOR,
                    self.player.y + (mouse_pos[1] - SCREEN_HEIGHT // 2) / JUMP_DRIVE_ZOOM_FACTOR
                )
                self.game_state = "JUMP_DRIVE_ALIGNING" # Transition to alignment phase
                self.jump_initiation_start_time = current_time # Start timer for alignment
                self.jump_drive_zoom_active = False # Zoom back in for alignment animation
                self.last_button_press_time = current_time
                print(f"Jump target selected: {self.jump_target_world_pos}. Initiating alignment.")

        elif self.game_state == "TRADING_OUTPOST_MENU":
            if mouse_clicked and can_press_button:
                if 'trade_crystal_button' in self.buttons and self.buttons['trade_crystal_button'].collidepoint(mouse_pos):
                    # Check if player has enough resources
                    required_gold = GAS_GIANT_CRYSTAL_TRADE_COST["Gold"]
                    required_silicon = GAS_GIANT_CRYSTAL_TRADE_COST["Silicon"]
                    required_ship_parts = GAS_GIANT_CRYSTAL_TRADE_COST["Ship Parts"]

                    if self.player.gold_ore >= required_gold and \
                       self.player.silicon_ore >= required_silicon and \
                       self.player.ship_parts >= required_ship_parts:
                        
                        self.player.gold_ore -= required_gold
                        self.player.silicon_ore -= required_silicon
                        self.player.ship_parts -= required_ship_parts
                        self.player.add_material("GasGiantCrystal", GAS_GIANT_CRYSTAL_TRADE_AMOUNT)
                        print(f"Traded for {GAS_GIANT_CRYSTAL_TRADE_AMOUNT} Gas Giant Crystal!")
                    else:
                        print("Insufficient resources for trade!")
                    self.last_button_press_time = current_time
                elif 'back_button' in self.buttons and self.buttons['back_button'].collidepoint(mouse_pos):
                    self.game_state = "PLAYING" # Go back to playing state
                    self.last_button_press_time = current_time
                    print("Returning to game.")

        elif self.game_state in ["ECONOMY_SHOP", "SHIP_SHOP"]: # For other placeholder menus
            if mouse_clicked and can_press_button:
                if 'back_button' in self.buttons and self.buttons['back_button'].collidepoint(mouse_pos):
                    self.game_state = "PAUSED_AT_STATION"
                    self.last_button_press_time = current_time # Reset cooldown
                    print("Returning to previous menu.")


    def update_game_state(self, current_time):
        """Updates all game objects and handles collisions."""
        if self.game_over:
            return

        # --- Camera Update (Damped Movement with Zoom) ---
        # Determine the target camera position based on player and zoom level
        zoom_factor = JUMP_DRIVE_ZOOM_FACTOR if self.jump_drive_zoom_active else 1.0

        # Calculate the effective width/height of the world visible on screen
        effective_screen_width_world_units = SCREEN_WIDTH / zoom_factor
        effective_screen_height_world_units = SCREEN_HEIGHT / zoom_factor

        # Desired camera top-left position to center the player
        target_camera_x = self.player.x - effective_screen_width_world_units / 2
        target_camera_y = self.player.y - effective_screen_height_world_units / 2

        # Damped movement for the camera
        # This makes the camera smoothly follow the player, even with zoom changes
        self.camera_x += (target_camera_x - self.camera_x) / 10
        self.camera_y += (target_camera_y - self.camera_y) / 10

        # Only update game world if playing
        if self.game_state == "PLAYING":
            # Update Enemy Base
            if self.enemy_base:
                self.enemy_base.update(current_time, (self.player.x, self.player.y))
                # If base is destroyed, remove it
                if self.enemy_base.health <= 0:
                    print("Enemy Base Destroyed!")
                    self.enemy_base = None # Remove the base

            # Update enemies
            for enemy in list(self.enemies): # Iterate over a copy to allow safe removal
                # Calculate proximity multiplier for enemy buffs
                proximity_multiplier = 1.0
                if self.enemy_base:
                    dist_to_base = math.hypot(enemy.x - self.enemy_base.x, enemy.y - self.enemy_base.y)
                    if dist_to_base < ENEMY_BASE_PROXIMITY_RADIUS:
                        # Closer to base = higher multiplier (e.g., from 1.0 to 2.0)
                        # When dist = PROXIMITY_RADIUS, multiplier = 1.0
                        # When dist = 0, multiplier = 2.0
                        proximity_multiplier = 1.0 + (1.0 - (dist_to_base / ENEMY_BASE_PROXIMITY_RADIUS))
                        proximity_multiplier = min(2.0, max(1.0, proximity_multiplier)) # Clamp between 1.0 and 2.0

                enemy.update((self.player.x, self.player.y), current_time, proximity_multiplier)
                
                # Cull enemies if they are too far from the player
                dist_to_player = math.hypot(enemy.x - self.player.x, enemy.y - self.player.y)
                if dist_to_player > WORLD_CULL_DISTANCE:
                    enemy.kill()
                    continue # Skip to next enemy

                # Cull enemies if they enter the safezone
                dist_to_station = math.hypot(enemy.x - self.space_station.x, enemy.y - self.space_station.y)
                if dist_to_station < SAFEZONE_RADIUS:
                    enemy.kill()
                    print(f"Enemy culled: Entered safezone at ({enemy.x:.0f}, {enemy.y:.0f})")
                    continue # Skip to next enemy

                # Cull enemies if they enter any mining safezone
                is_in_mining_zone = False
                for zone in self.mining_zones:
                    dist_to_zone = math.hypot(enemy.x - zone.x, enemy.y - zone.y)
                    if dist_to_zone < zone.radius:
                        is_in_mining_zone = True
                        break
                if is_in_mining_zone:
                    enemy.kill()
                    print(f"Enemy culled: Entered mining safezone at ({enemy.x:.0f}, {enemy.y:.0f})")
                    continue

                new_projectile = enemy.shoot(current_time)
                if new_projectile:
                    self.enemy_projectiles.add(new_projectile)

            # Update projectiles, passing camera position for off-screen culling
            for proj in list(self.player_projectiles): # Iterate over a copy to allow safe removal
                # Pass current_time and game_manager to all player projectiles, HomingMissile uses it for lifetime/retargeting
                proj.update(self.camera_x, self.camera_y, current_time, self) # Pass 'self' (GameManager instance)
            
            for proj in list(self.enemy_projectiles):
                # Enemy projectiles are simple, no homing, so no need for current_time or game_manager
                proj.update(self.camera_x, self.camera_y, current_time, self) # Pass self for homing missiles from base


            # Cull asteroids if they are too far from the player (only general asteroids, not in mining zones)
            for asteroid in list(self.asteroids): # Iterate over a copy to safely remove elements
                is_in_mining_zone = False
                for zone in self.mining_zones:
                    if asteroid in zone.asteroids_in_zone:
                        is_in_mining_zone = True
                        break
                
                if not is_in_mining_zone: # Only cull general asteroids
                    dist_to_player = math.hypot(asteroid.x - self.player.x, asteroid.y - self.player.y)
                    if dist_to_player > WORLD_CULL_DISTANCE:
                        asteroid.kill()

            # Cull material drops if they are too far from the player
            for material_drop in list(self.material_drops_group):
                dist_to_player = math.hypot(material_drop.x - self.player.x, material_drop.y - self.player.y)
                if dist_to_player > WORLD_CULL_DISTANCE:
                    material_drop.kill()

            # Spawn new asteroids if needed (after culling)
            # Prioritize filling up mining zones first
            for zone in self.mining_zones:
                while len(zone.asteroids_in_zone) < zone.max_asteroids:
                    self.spawn_asteroid(in_mining_zone=zone)
            
            # Then spawn general asteroids if needed
            while len(self.asteroids) < MAX_ASTEROIDS + sum(z.max_asteroids for z in self.mining_zones): # Total asteroids
                self.spawn_asteroid()

            # Spawn new enemies if needed
            if len(self.enemies) < MAX_ENEMIES and current_time - self.last_enemy_spawn_time > ENEMY_SPAWN_TIMER:
                self.spawn_enemy()
                self.last_enemy_spawn_time = current_time

            # Update Mining NPCs
            for zone in self.mining_zones:
                # Cull NPCs if their zone is too far from the player
                dist_to_zone = math.hypot(self.player.x - zone.x, self.player.y - zone.y)
                if dist_to_zone > WORLD_CULL_DISTANCE + zone.radius + 100: # Cull zone if too far
                    for npc in list(zone.npcs_in_zone):
                        npc.kill()
                        self.mining_npcs.remove(npc)
                    for asteroid in list(zone.asteroids_in_zone):
                        asteroid.kill()
                        self.asteroids.remove(asteroid) # Remove from global group too
                    continue # Skip to next zone

                # Ensure max NPCs are present in the zone
                while len(zone.npcs_in_zone) < zone.max_npcs:
                    self.spawn_mining_npc(zone)

                # Update NPCs in this zone
                for npc in list(zone.npcs_in_zone): # Iterate over a copy to allow safe removal
                    # If NPC is culled (e.g., zone too far), it won't be in zone.npcs_in_zone anymore
                    if npc not in self.mining_npcs: # Check if it's still in the global group
                        zone.npcs_in_zone.remove(npc) # Remove from zone's group if already culled globally
                        continue
                    npc.update(current_time, zone.asteroids_in_zone, self) # Pass the zone's asteroids and game_manager
                    # If NPC gets too far from its zone, cull it (e.g., bugged movement)
                    if math.hypot(npc.x - zone.x, npc.y - zone.y) > zone.radius + 50:
                        npc.kill()
                        self.mining_npcs.remove(npc)
                        zone.npcs_in_zone.remove(npc)


            # Apply gravitational pull from planets
            for planet in self.planets:
                dx = planet.x - self.player.x
                dy = planet.y - self.player.y
                distance = math.hypot(dx, dy)

                if 0 < distance < planet.gravity_radius:
                    # Calculate gravitational force, stronger closer to center
                    # Using a simple linear falloff for now
                    pull_magnitude = planet.gravity_strength * (1 - (distance / planet.gravity_radius))
                    
                    # Apply force to player's position, factoring in gravity resistance
                    # Divide by gravity_resistance_multiplier: higher resistance means less pull
                    # If gravity_resistance_multiplier is very low (e.g., Ion Engine on Gas Giant),
                    # the pull_magnitude will be effectively multiplied, making it harder to escape.
                    if distance > 0: # Avoid division by zero
                        self.player.x += (pull_magnitude / self.player.engine_gravity_resistance_multiplier) * (dx / distance)
                        self.player.y += (pull_magnitude / self.player.engine_gravity_resistance_multiplier) * (dy / distance)

            # Reveal stealth asteroids if Advanced Antenna is equipped
            if ANTENNA_TYPES[self.player.current_antenna_type]["reveals_stealth"]:
                for asteroid in self.asteroids:
                    if asteroid.is_stealth and not asteroid.is_revealed:
                        asteroid.is_revealed = True
                        # Change image to revealed color
                        asteroid.image.fill((0,0,0,0)) # Clear existing drawing
                        pygame.draw.circle(asteroid.image, STEALTH_ASTEROID_REVEAL_COLOR, (asteroid.size, asteroid.size), asteroid.size)
            else: # If advanced antenna is not equipped, ensure stealth asteroids are not revealed
                for asteroid in self.asteroids:
                    if asteroid.is_stealth and asteroid.is_revealed:
                        asteroid.is_revealed = False
                        # Revert image to hidden color
                        asteroid.image.fill((0,0,0,0)) # Clear existing drawing
                        pygame.draw.circle(asteroid.image, asteroid.original_color, (asteroid.size, asteroid.size), asteroid.size)


            # --- Mining Logic (based on current tool) ---
            if self.player.current_mining_tool == "Drill":
                if self.mining_laser_active: # Drill is activated by holding 'F' while colliding
                    for asteroid in list(self.asteroids): # Iterate over a copy for safe removal
                        # Only mine if asteroid is visible or if it's a stealth asteroid and revealed
                        if (not asteroid.is_stealth or asteroid.is_revealed) and pygame.sprite.collide_rect(self.player, asteroid):
                            asteroid.take_damage(MINING_LASER_DAMAGE_PER_TICK * self.player.power_output_multiplier)
                            if asteroid.health <= 0:
                                # Check for Rocky Ore drop if near a Rocky Planet
                                is_near_rocky_planet = False
                                for planet in self.planets:
                                    if planet.planet_type_name == "Rocky Planet":
                                        dist_to_planet = math.hypot(asteroid.x - planet.x, asteroid.y - planet.y)
                                        if dist_to_planet < planet.size + NEAR_PLANET_DISTANCE: # Within planet's radius + buffer
                                            is_near_rocky_planet = True
                                            break
                                
                                if is_near_rocky_planet and random.random() < ROCKY_ORE_DROP_CHANCE:
                                    self.material_drops_group.add(MaterialDrop(asteroid.x, asteroid.y, "RockyOre", ROCKY_ORE_AMOUNT, MATERIAL_DROP_SIZE))
                                
                                # Always drop regular materials
                                material_type, amount = asteroid.get_material_drop()
                                if material_type:
                                    self.material_drops_group.add(MaterialDrop(asteroid.x, asteroid.y, material_type, amount, MATERIAL_DROP_SIZE))
                                asteroid.kill()
                                # No direct spawn_asteroid here, let the general spawning logic handle it
            elif self.player.current_mining_tool in ["ShortRangeLaser", "LongRangeLaser"]:
                if self.mining_laser_active: # Lasers are activated by holding 'F' and aiming with mouse
                    mining_range = SHORT_RANGE_LASER_RANGE if self.player.current_mining_tool == "ShortRangeLaser" else LONG_RANGE_LASER_RANGE
                    # Mouse world coordinates are updated in handle_input based on mouse position
                    dist_to_cursor = math.hypot(self.mouse_world_x - self.player.x, self.mouse_world_y - self.player.y)
                    if dist_to_cursor <= mining_range:
                        for asteroid in list(self.asteroids):
                            dist_to_asteroid = math.hypot(self.mouse_world_x - asteroid.x, self.mouse_world_y - asteroid.y)
                            # Only mine if asteroid is visible or if it's a stealth asteroid and revealed
                            if (not asteroid.is_stealth or asteroid.is_revealed) and dist_to_asteroid < asteroid.size:
                                asteroid.take_damage(MINING_LASER_DAMAGE_PER_TICK * self.player.power_output_multiplier)
                                if asteroid.health <= 0:
                                    # Check for Rocky Ore drop if near a Rocky Planet
                                    is_near_rocky_planet = False
                                    for planet in self.planets:
                                        if planet.planet_type_name == "Rocky Planet":
                                            dist_to_planet = math.hypot(asteroid.x - planet.x, asteroid.y - planet.y)
                                            if dist_to_planet < planet.size + NEAR_PLANET_DISTANCE:
                                                is_near_rocky_planet = True
                                                break
                                    
                                    if is_near_rocky_planet and random.random() < ROCKY_ORE_DROP_CHANCE:
                                        self.material_drops_group.add(MaterialDrop(asteroid.x, asteroid.x, "RockyOre", ROCKY_ORE_AMOUNT, MATERIAL_DROP_SIZE))
                                    
                                    # Always drop regular materials
                                    material_type, amount = asteroid.get_material_drop()
                                    if material_type:
                                        self.material_drops_group.add(MaterialDrop(asteroid.x, asteroid.y, material_type, amount, MATERIAL_DROP_SIZE))
                                    asteroid.kill()
                                    # No direct spawn_asteroid here, let the general spawning logic handle it
            elif self.player.current_mining_tool == "AutoMiningLaser":
                if self.auto_mine_active:
                    # Decrease charge
                    self.auto_mine_charge = max(0, self.auto_mine_charge - AUTO_MINE_CHARGE_DECREASE_RATE * self.player.power_output_multiplier)
                    if self.auto_mine_charge <= 0:
                        self.auto_mine_active = False
                        self.targeted_asteroids.clear()
                        print("Auto-mining stopped: Charge depleted.")
                    else:
                        # Apply continuous damage to targeted asteroids
                        asteroids_to_remove = []
                        for asteroid in self.targeted_asteroids:
                            # Ensure asteroid is still valid and visible before damaging
                            if (not asteroid.is_stealth or asteroid.is_revealed) and asteroid in self.asteroids and self.is_visible_on_screen(asteroid.x, asteroid.y, asteroid.size):
                                asteroid.take_damage(MINING_LASER_DAMAGE_PER_TICK * self.player.power_output_multiplier) # Using MINING_LASER_DAMAGE_PER_TICK for continuous damage
                                if asteroid.health <= 0:
                                    # Check for Rocky Ore drop if near a Rocky Planet
                                    is_near_rocky_planet = False
                                    for planet in self.planets:
                                        if planet.planet_type_name == "Rocky Planet":
                                            dist_to_planet = math.hypot(asteroid.x - planet.x, asteroid.y - planet.y)
                                            if dist_to_planet < planet.size + NEAR_PLANET_DISTANCE:
                                                is_near_rocky_planet = True
                                                break
                                    
                                    if is_near_rocky_planet and random.random() < ROCKY_ORE_DROP_CHANCE:
                                        self.material_drops_group.add(MaterialDrop(asteroid.x, asteroid.x, "RockyOre", ROCKY_ORE_AMOUNT, MATERIAL_DROP_SIZE))
                                    
                                    # Always drop regular materials
                                    material_type, amount = asteroid.get_material_drop()
                                    if material_type:
                                        self.material_drops_group.add(MaterialDrop(asteroid.x, asteroid.y, material_type, amount, MATERIAL_DROP_SIZE))
                                    asteroid.kill()
                                    # No direct spawn_asteroid here, let the general spawning logic handle it
                                    asteroids_to_remove.append(asteroid)
                            else: # If asteroid is no longer valid or visible, remove from targets
                                asteroids_to_remove.append(asteroid)
                        
                        # Remove mined/invalid asteroids from the targeted list
                        for asteroid in asteroids_to_remove:
                            if asteroid in self.targeted_asteroids: # Check if it's still in the list
                                self.targeted_asteroids.remove(asteroid)
                        
                        # If all current targets are mined, find new ones
                        if not self.targeted_asteroids and self.auto_mine_charge > 0: # Only seek new if charge is available
                            self.start_auto_mine_targeting()
                            if not self.targeted_asteroids: # If still no targets, deactivate auto-mine
                                self.auto_mine_active = False
                                print("Auto-mining completed all visible targets. Deactivating.")
                else: # Auto-mine is not active, refill charge
                    self.auto_mine_charge = min(AUTO_MINE_MAX_CHARGE, self.auto_mine_charge + AUTO_MINE_CHARGE_REFILL_RATE * self.player.recharge_rate_multiplier)


                # Resource magnetism is continuous when AutoMiningLaser is equipped AND active
                if self.auto_mine_active: # Only magnet if auto-mine is active
                    for drop in list(self.material_drops_group) + list(self.ship_parts_group):
                        dx = self.player.x - drop.x
                        dy = self.player.y - drop.y
                        dist = math.hypot(dx, dy)

                        if dist > 0:
                            # Move towards player
                            move_x = (dx / dist) * RESOURCE_MAGNET_SPEED
                            move_y = (dy / dist) * RESOURCE_MAGNET_SPEED
                            drop.x += move_x
                            drop.y += move_y
                            drop.rect.centerx = int(drop.x)
                            drop.rect.centery = int(drop.y)

                        # Check for collection if close enough (to avoid infinite movement)
                        if pygame.sprite.collide_rect(self.player, drop):
                            if isinstance(drop, MaterialDrop):
                                self.player.add_material(drop.material_type, drop.amount)
                            elif isinstance(drop, ShipPart):
                                self.player.add_ship_parts(drop.amount)
                            drop.kill()


            # --- Collision Detection (Combat) ---
            # Player Projectiles vs Enemies
            hits = pygame.sprite.groupcollide(self.player_projectiles, self.enemies, True, False)
            for projectile, enemies_hit in hits.items():
                for enemy in enemies_hit:
                    enemy.take_damage(projectile.damage) # Use projectile's damage
                    if enemy.health <= 0:
                        enemy.kill() # Remove enemy
                        self.player.add_xp(enemy.xp_value) # Add XP based on enemy type
                        # Ship part drop chance based on enemy type
                        if random.random() < enemy.drop_chance:
                            self.ship_parts_group.add(ShipPart(enemy.x, enemy.y, SHIP_PART_SIZE * enemy.ship_part_amount)) # Adjust size based on amount

            # Player Projectiles vs Enemy Base
            if self.enemy_base:
                hits = pygame.sprite.spritecollide(self.enemy_base, self.player_projectiles, True)
                for projectile in hits:
                    self.enemy_base.take_damage(projectile.damage)
                    if self.enemy_base.health <= 0:
                        print("Enemy Base Destroyed!")
                        self.enemy_base = None # Remove the base

            # Enemy Projectiles vs Player
            hits = pygame.sprite.spritecollide(self.player, self.enemy_projectiles, True)
            for projectile in hits:
                self.player.take_damage(projectile.damage) # Use projectile's damage

            # Player vs Ship Parts (Collection) - This is now handled by magnetism for AutoMiningLaser
            # Only manually collect if AutoMiningLaser is NOT active
            if not (self.player.current_mining_tool == "AutoMiningLaser" and self.auto_mine_active):
                collected_parts = pygame.sprite.spritecollide(self.player, self.ship_parts_group, True)
                for part in collected_parts:
                    self.player.add_ship_parts(part.size // SHIP_PART_SIZE) # Add amount based on part size

            # Player vs Material Drops (Collection) - This is now handled by magnetism for AutoMiningLaser
            # Only manually collect if AutoMiningLaser is NOT active
            if not (self.player.current_mining_tool == "AutoMiningLaser" and self.auto_mine_active):
                collected_materials = pygame.sprite.spritecollide(self.player, self.material_drops_group, True)
                for material_drop in collected_materials:
                    self.player.add_material(material_drop.material_type, material_drop.amount)

            # Check for game over
            if self.player.health <= 0:
                self.game_over = True

            # --- Ping System Update ---
            if self.outgoing_ping_active:
                elapsed_time_ping = (current_time - self.outgoing_ping_start_time) / 1000.0 # in seconds
                # Ping radius now affected by radar_range_multiplier
                current_radius = PING_OUTGOING_SPEED * elapsed_time_ping * self.player.radar_range_multiplier

                # Check if the ping has exceeded the screen boundaries
                if current_radius > SCREEN_WIDTH / 2 or current_radius > SCREEN_HEIGHT / 2:
                    if not self.incoming_ping_active: # Trigger incoming ping only once
                        self.incoming_ping_active = True
                        self.incoming_ping_start_time = current_time

                # Deactivate outgoing ping after its lifetime
                if elapsed_time_ping > PING_OUTGOING_LIFETIME:
                    self.outgoing_ping_active = False

            if self.incoming_ping_active:
                elapsed_time_incoming = (current_time - self.incoming_ping_start_time) / 1000.0
                alpha = max(0, 255 - int(255 * (elapsed_time_incoming / PING_INCOMING_DURATION)))
            
                player_screen_x, player_screen_y = self.world_to_screen(self.player.x, self.player.y)
                station_screen_x, station_screen_y = self.world_to_screen(self.space_station.x, self.space_station.y)

                dx = station_screen_x - player_screen_x
                dy = station_screen_y - player_screen_y
                distance = math.hypot(dx, dy)

                if distance > 0:
                    dir_x = dx / distance
                    dir_y = dy / distance

                    beam_end_x = player_screen_x + dir_x * PING_BEAM_LENGTH * zoom_factor
                    beam_end_y = player_screen_y + dir_y * PING_BEAM_LENGTH * zoom_factor

                    ping_beam_color_with_alpha = (PING_COLOR[0], PING_COLOR[1], PING_COLOR[2], alpha)
                    
                    line_surface = pygame.Surface(SCREEN.get_size(), pygame.SRCALPHA)
                    pygame.draw.line(line_surface, ping_beam_color_with_alpha,
                                     (player_screen_x, player_screen_y),
                                     (beam_end_x, beam_end_y), int(3 * zoom_factor) or 1)
                    SCREEN.blit(line_surface, (0, 0))

                for planet in self.planets:
                    planet_screen_x, planet_screen_y = self.world_to_screen(planet.x, planet.y)

                    dx_p = planet_screen_x - player_screen_x
                    dy_p = planet_screen_y - player_screen_y
                    distance_p = math.hypot(dx_p, dy_p)

                    if distance_p > 0:
                        dir_x_p = dx_p / distance_p
                        dir_y_p = dy_p / distance_p

                        beam_end_x_p = player_screen_x + dir_x_p * PING_BEAM_LENGTH * zoom_factor
                        beam_end_y_p = player_screen_y + dir_y_p * PING_BEAM_LENGTH * zoom_factor

                        planet_ping_color_with_alpha = (YELLOW[0], YELLOW[1], YELLOW[2], alpha)

                        line_surface_p = pygame.Surface(SCREEN.get_size(), pygame.SRCALPHA)
                        pygame.draw.line(line_surface_p, planet_ping_color_with_alpha,
                                         (player_screen_x, player_screen_y),
                                         (beam_end_x_p, beam_end_y_p), int(3 * zoom_factor) or 1)
                        SCREEN.blit(line_surface_p, (0, 0))

                        pygame.draw.circle(SCREEN, planet_ping_color_with_alpha, (int(planet_screen_x), int(planet_screen_y)), int(5 * zoom_factor) or 1)
                        
                        # Scale font size for planet name or use a smaller font
                        scaled_font_size = max(10, int(FONT.get_height() * zoom_factor))
                        scaled_font = pygame.font.Font(None, scaled_font_size)
                        planet_name_text = scaled_font.render(planet.planet_type_name, True, (255,255,255,alpha))
                        planet_name_rect = planet_name_text.get_rect(center=(planet_screen_x, planet_screen_y - int(20 * zoom_factor)))
                        SCREEN.blit(planet_name_text, planet_name_rect)

                # Draw ping for stealth asteroids if revealed
                if ANTENNA_TYPES[self.player.current_antenna_type]["reveals_stealth"]:
                    for asteroid in self.asteroids:
                        if asteroid.is_stealth and asteroid.is_revealed:
                            asteroid_screen_x, asteroid_screen_y = self.world_to_screen(asteroid.x, asteroid.y)
                            
                            dx_a = asteroid_screen_x - player_screen_x
                            dy_a = asteroid_screen_y - player_screen_y
                            distance_a = math.hypot(dx_a, dy_a)

                            if distance_a > 0:
                                dir_x_a = dx_a / distance_a
                                dir_y_a = dy_a / distance_a

                                beam_end_x_a = player_screen_x + dir_x_a * PING_BEAM_LENGTH * zoom_factor
                                beam_end_y_a = player_screen_y + dir_y_a * PING_BEAM_LENGTH * zoom_factor

                                stealth_asteroid_ping_color_with_alpha = (STEALTH_ASTEROID_REVEAL_COLOR[0], STEALTH_ASTEROID_REVEAL_COLOR[1], STEALTH_ASTEROID_REVEAL_COLOR[2], alpha)

                                line_surface_a = pygame.Surface(SCREEN.get_size(), pygame.SRCALPHA)
                                pygame.draw.line(line_surface_a, stealth_asteroid_ping_color_with_alpha,
                                                 (player_screen_x, player_screen_y),
                                                 (beam_end_x_a, beam_end_y_a), int(3 * zoom_factor) or 1)
                                SCREEN.blit(line_surface_a, (0, 0))

                                pygame.draw.circle(SCREEN, stealth_asteroid_ping_color_with_alpha, (int(asteroid_screen_x), int(asteroid_screen_y)), int(5 * zoom_factor) or 1)


        # --- Jump Drive state logic ---
        if self.game_state == "JUMP_DRIVE_ALIGNING":
            elapsed_time = current_time - self.jump_initiation_start_time
            
            # Calculate target angle
            dx = self.jump_target_world_pos[0] - self.player.x
            dy = self.jump_target_world_pos[1] - self.player.y
            target_angle_rad = math.atan2(dy, dx) # Angle relative to positive x-axis
            target_angle_deg = (math.degrees(target_angle_rad) + 90) % 360 # Convert to our 0=up, 90=left convention

            # Update player angle towards target
            self.player.update(pygame.key.get_pressed(), current_time, self.game_state, target_angle_deg)

            # Check if alignment is complete
            # Compare current angle to target angle, accounting for wrap-around
            angle_diff = (target_angle_deg - self.player.angle + 180 + 360) % 360 - 180
            if abs(angle_diff) < 2 or elapsed_time >= JUMP_DRIVE_ALIGNMENT_DURATION: # Tolerance for alignment or timeout
                self.game_state = "JUMP_DRIVE_WARP" # Transition to warp phase
                self.jump_rings_active = True
                self.jump_rings_start_time = current_time # Reset timer for warp animation
                print("Alignment complete. Initiating warp.")

        elif self.game_state == "JUMP_DRIVE_WARP":
            elapsed_time = current_time - self.jump_rings_start_time
            if elapsed_time >= JUMP_DRIVE_WARP_DURATION:
                self.player.x = self.jump_target_world_pos[0]
                self.player.y = self.jump_target_world_pos[1]
                self.game_state = "PLAYING"
                self.jump_drive_zoom_active = False # Ensure zoom is reset
                self.jump_rings_active = False # Stop rings
                self.last_jump_time = current_time # Start cooldown
                print(f"Jump successful to ({self.player.x:.0f}, {self.player.y:.0f})")

        # Health regeneration when in any station menu state
        if self.game_state in ["PAUSED_AT_STATION", "ECONOMY_SHOP", "SHIP_UPGRADING", "SHIP_SHOP", "MINING_TOOLS_MENU", "ENERGY_CORE_MENU", "ANTENNA_MENU", "WEAPONS_MENU", "PROPULSION_MENU", "TRADING_OUTPOST_MENU"]:
            if self.player.health < self.player.max_health:
                if current_time - self.last_regen_time > HEALTH_REGEN_INTERVAL:
                    self.player.health = min(self.player.max_health, self.player.health + HEALTH_REGEN_INCREMENT)
                    self.last_regen_time = current_time

    def find_nearest_enemy(self, max_range=None):
        """
        Finds the nearest enemy to the player within a given range AND visible on screen.
        """
        nearest_enemy = None
        min_dist = float('inf')
        for enemy in self.enemies:
            dist = math.hypot(self.player.x - enemy.x, self.player.y - enemy.y)
            # Check if within max_range (if provided) AND visible on screen
            if (max_range is None or dist <= max_range) and \
               self.is_visible_on_screen(enemy.x, enemy.y, enemy.image.get_width() / 2) and \
               dist < min_dist:
                min_dist = dist
                nearest_enemy = enemy
        return nearest_enemy

    def find_nearest_enemy_or_base_to_point(self, point_x, point_y, max_range=None):
        """
        Finds the nearest enemy or the enemy base to a specific point within a given range.
        Used for re-targeting homing missiles.
        """
        nearest_target = None
        min_dist = float('inf')

        # Check enemies
        for enemy in self.enemies:
            dist = math.hypot(point_x - enemy.x, point_y - enemy.y)
            if (max_range is None or dist <= max_range) and dist < min_dist:
                min_dist = dist
                nearest_target = enemy
        
        # Check enemy base
        if self.enemy_base:
            dist_to_base = math.hypot(point_x - self.enemy_base.x, point_y - self.enemy_base.y)
            if (max_range is None or dist_to_base <= max_range) and dist_to_base < min_dist:
                min_dist = dist_to_base
                nearest_target = self.enemy_base

        return nearest_target


    def draw_ui(self):
        """Draws the player's health, XP, and level on the screen."""
        health_text = FONT.render(f"Health: {self.player.health}/{self.player.max_health}", True, GREEN)
        SCREEN.blit(health_text, (10, 10))

        # XP Bar and Level
        xp_bar_width = 200
        xp_bar_height = 20
        xp_bar_x = 10
        xp_bar_y = 40
        xp_percentage = self.player.current_xp / self.player.xp_threshold
        current_xp_bar_width = int(xp_bar_width * xp_percentage)

        pygame.draw.rect(SCREEN, GRAY, (xp_bar_x, xp_bar_y, xp_bar_width, xp_bar_height), 2) # XP bar outline
        pygame.draw.rect(SCREEN, BLUE, (xp_bar_x, xp_bar_y, current_xp_bar_width, xp_bar_height)) # XP bar fill

        xp_text = FONT.render(f"XP: {self.player.current_xp}/{self.player.xp_threshold} (Level {self.player.level})", True, WHITE)
        SCREEN.blit(xp_text, (xp_bar_x + xp_bar_width + 10, xp_bar_y))

        # Draw "Press E to enter station/outpost" message if near
        if self.game_state == "PLAYING":
            dist_to_station = math.hypot(self.player.x - self.space_station.x, self.player.y - self.space_station.y)
            if dist_to_station < SPACESTATION_INTERACT_DISTANCE + 50: # Slightly larger trigger area for message
                enter_text = FONT.render("Press 'E' to enter Space Station", True, WHITE)
                text_rect = enter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
                SCREEN.blit(enter_text, text_rect)
            elif self.trading_outpost and math.hypot(self.player.x - self.trading_outpost.x, self.player.y - self.trading_outpost.y) < self.trading_outpost.size + 50:
                enter_text = FONT.render("Press 'E' to enter Trading Outpost", True, WHITE)
                text_rect = enter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
                SCREEN.blit(enter_text, text_rect)


        # Draw "Press I for Inventory" message
        if self.game_state in ["PLAYING", "PAUSED_AT_STATION", "ECONOMY_SHOP", "SHIP_UPGRADING", "SHIP_SHOP", "MINING_TOOLS_MENU", "ENERGY_CORE_MENU", "ANTENNA_MENU", "WEAPONS_MENU", "PROPULSION_MENU", "TRADING_OUTPOST_MENU"]:
            inventory_hint_text = FONT.render("Press 'I' for Inventory", True, WHITE)
            inventory_hint_rect = inventory_hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
            SCREEN.blit(inventory_hint_text, inventory_hint_rect)

        # Draw Mining Tool Activation Hint
        if self.game_state == "PLAYING":
            if self.player.current_mining_tool == "AutoMiningLaser":
                # Auto-Mine Charge Bar
                charge_bar_width = 150
                charge_bar_height = 15
                charge_bar_x = SCREEN_WIDTH - charge_bar_width - 10
                charge_bar_y = 10
                charge_percentage = self.auto_mine_charge / AUTO_MINE_MAX_CHARGE
                current_charge_bar_width = int(charge_bar_width * charge_percentage)

                pygame.draw.rect(SCREEN, GRAY, (charge_bar_x, charge_bar_y, charge_bar_width, charge_bar_height), 2) # Charge bar outline
                pygame.draw.rect(SCREEN, CHARGE_BAR_COLOR, (charge_bar_x, charge_bar_y, current_charge_bar_width, charge_bar_height)) # Charge bar fill

                charge_text = FONT.render(f"Charge: {int(self.auto_mine_charge)}%", True, WHITE)
                SCREEN.blit(charge_text, (charge_bar_x - 80, charge_bar_y))

                # Auto-Mine Status/Hint
                if self.auto_mine_active:
                    auto_mine_status_text = FONT.render("Auto-Mine Active (Press 'F' to Stop)", True, YELLOW)
                    auto_mine_status_rect = auto_mine_status_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
                    SCREEN.blit(auto_mine_status_text, auto_mine_status_rect)
                elif self.auto_mine_charge <= 0:
                    auto_mine_hint_text = FONT.render("Auto-Mine: No Charge (Refilling)", True, ORANGE)
                    auto_mine_hint_rect = auto_mine_hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
                    SCREEN.blit(auto_mine_hint_text, auto_mine_hint_rect) # Corrected variable name
                else:
                    auto_mine_hint_text = FONT.render("Press 'F' to Auto-Mine", True, YELLOW)
                    auto_mine_hint_rect = auto_mine_hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
                    SCREEN.blit(auto_mine_hint_text, auto_mine_hint_rect)
            else:
                # Hint for other mining tools
                mining_tool_hint_text = FONT.render(f"Hold 'F' to use {self.player.current_mining_tool}", True, YELLOW)
                mining_tool_hint_rect = mining_tool_hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
                SCREEN.blit(mining_tool_hint_text, mining_tool_hint_rect)

            # Hyper Drive Cooldown Bar
            if self.player.current_engine_type == "Hyper Drive":
                effective_jump_cooldown = JUMP_DRIVE_COOLDOWN / self.player.recharge_rate_multiplier
                remaining_cooldown = max(0, effective_jump_cooldown - (pygame.time.get_ticks() - self.last_jump_time))

                if remaining_cooldown > 0:
                    cooldown_bar_width = 150
                    cooldown_bar_height = 15
                    cooldown_bar_x = SCREEN_WIDTH - cooldown_bar_width - 10
                    cooldown_bar_y = 50 # Position below auto-miner charge bar, or higher if auto-miner isn't shown

                    cooldown_percentage = 1 - (remaining_cooldown / effective_jump_cooldown)
                    current_cooldown_bar_width = int(cooldown_bar_width * cooldown_percentage)

                    pygame.draw.rect(SCREEN, GRAY, (cooldown_bar_x, cooldown_bar_y, cooldown_bar_width, cooldown_bar_height), 2) # Cooldown bar outline
                    pygame.draw.rect(SCREEN, COOLDOWN_BAR_COLOR, (cooldown_bar_x, cooldown_bar_y, current_cooldown_bar_width, cooldown_bar_height)) # Cooldown bar fill

                    cooldown_text = FONT.render(f"Jump CD: {remaining_cooldown / 1000:.1f}s", True, WHITE)
                    SCREEN.blit(cooldown_text, (cooldown_bar_x - 100, cooldown_bar_y))

            # Weapon Slot 1 and 2 info
            weapon1_text = FONT.render(f"Slot 1 (Space): {self.player.weapon_slot_1}", True, WHITE)
            SCREEN.blit(weapon1_text, (10, 70))
            weapon2_text = FONT.render(f"Slot 2 (L-Ctrl): {self.player.weapon_slot_2}", True, WHITE)
            SCREEN.blit(weapon2_text, (10, 100))

            # Enemy Base Proximity Warning
            if self.enemy_base:
                dist_to_base = math.hypot(self.player.x - self.enemy_base.x, self.player.y - self.enemy_base.y)
                if dist_to_base < ENEMY_BASE_PROXIMITY_RADIUS:
                    warning_text = "WARNING: Approaching Enemy Base!"
                    # Scale warning intensity based on proximity
                    proximity_ratio = 1 - (dist_to_base / ENEMY_BASE_PROXIMITY_RADIUS) # 0 when far, 1 when close
                    
                    # Interpolate color from green to yellow to red
                    if proximity_ratio < 0.5:
                        # Green to Yellow
                        r = int(PROXIMITY_GREEN[0] + (PROXIMITY_YELLOW[0] - PROXIMITY_GREEN[0]) * (proximity_ratio * 2))
                        g = int(PROXIMITY_GREEN[1] + (PROXIMITY_YELLOW[1] - PROXIMITY_GREEN[1]) * (proximity_ratio * 2))
                        b = int(PROXIMITY_GREEN[2] + (PROXIMITY_YELLOW[2] - PROXIMITY_GREEN[2]) * (proximity_ratio * 2))
                    else:
                        # Yellow to Red
                        r = int(PROXIMITY_YELLOW[0] + (PROXIMITY_RED[0] - PROXIMITY_YELLOW[0]) * ((proximity_ratio - 0.5) * 2))
                        g = int(PROXIMITY_YELLOW[1] + (PROXIMITY_RED[1] - PROXIMITY_YELLOW[1]) * ((proximity_ratio - 0.5) * 2))
                        b = int(PROXIMITY_YELLOW[2] + (PROXIMITY_RED[2] - PROXIMITY_YELLOW[2]) * ((proximity_ratio - 0.5) * 2))
                    warning_color = (r, g, b)

                    warning_font_size = int(MENU_FONT.get_height() * (1 + proximity_ratio * 0.5)) # Grow text
                    warning_font = pygame.font.Font(None, warning_font_size)
                    warning_surf = warning_font.render(warning_text, True, warning_color)
                    warning_rect = warning_surf.get_rect(center=(SCREEN_WIDTH // 2, 50))
                    SCREEN.blit(warning_surf, warning_rect)


    def draw_game_objects(self):
        """Draws all game objects relative to the camera, with zoom."""
        zoom_factor = JUMP_DRIVE_ZOOM_FACTOR if self.jump_drive_zoom_active else 1.0

        # Draw Safezone (around space station)
        if self.space_station:
            safezone_screen_x, safezone_screen_y = self.world_to_screen(self.space_station.x, self.space_station.y)
            scaled_safezone_radius = int(SAFEZONE_RADIUS * zoom_factor)
            
            # Create a semi-transparent surface for the safezone circle
            safezone_surface = pygame.Surface((scaled_safezone_radius * 2, scaled_safezone_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(safezone_surface, SAFEZONE_COLOR, (scaled_safezone_radius, scaled_safezone_radius), scaled_safezone_radius)
            
            safezone_rect = safezone_surface.get_rect(center=(safezone_screen_x, safezone_screen_y))
            SCREEN.blit(safezone_surface, safezone_rect)

        # Draw Mining Safezones
        for zone in self.mining_zones:
            zone.draw(SCREEN, self.camera_x, self.camera_y, zoom_factor)

        # Draw Enemy Base Proximity Ring
        if self.enemy_base:
            dist_to_base = math.hypot(self.player.x - self.enemy_base.x, self.player.y - self.enemy_base.y)
            if dist_to_base < ENEMY_BASE_PROXIMITY_RADIUS:
                proximity_screen_x, proximity_screen_y = self.world_to_screen(self.enemy_base.x, self.enemy_base.y)
                scaled_proximity_radius = int(ENEMY_BASE_PROXIMITY_RADIUS * zoom_factor)
                
                # Interpolate color and thickness
                proximity_ratio = 1 - (dist_to_base / ENEMY_BASE_PROXIMITY_RADIUS)
                
                # Color interpolation (Green -> Yellow -> Red)
                if proximity_ratio < 0.5:
                    r = int(PROXIMITY_GREEN[0] + (PROXIMITY_YELLOW[0] - PROXIMITY_GREEN[0]) * (proximity_ratio * 2))
                    g = int(PROXIMITY_GREEN[1] + (PROXIMITY_YELLOW[1] - PROXIMITY_GREEN[1]) * (proximity_ratio * 2))
                    b = int(PROXIMITY_GREEN[2] + (PROXIMITY_YELLOW[2] - PROXIMITY_GREEN[2]) * (proximity_ratio * 2))
                    alpha = int(PROXIMITY_GREEN[3] + (PROXIMITY_YELLOW[3] - PROXIMITY_GREEN[3]) * (proximity_ratio * 2))
                else:
                    r = int(PROXIMITY_YELLOW[0] + (PROXIMITY_RED[0] - PROXIMITY_YELLOW[0]) * ((proximity_ratio - 0.5) * 2))
                    g = int(PROXIMITY_YELLOW[1] + (PROXIMITY_RED[1] - PROXIMITY_YELLOW[1]) * ((proximity_ratio - 0.5) * 2))
                    b = int(PROXIMITY_YELLOW[2] + (PROXIMITY_RED[2] - PROXIMITY_YELLOW[2]) * ((proximity_ratio - 0.5) * 2))
                    alpha = int(PROXIMITY_YELLOW[3] + (PROXIMITY_RED[3] - PROXIMITY_YELLOW[3]) * ((proximity_ratio - 0.5) * 2))
                
                proximity_color = (r, g, b, alpha)
                
                # Thickness interpolation (thinner when far, thicker when close)
                thickness = max(1, int(5 * proximity_ratio * zoom_factor)) # Min thickness 1

                # Pulsating effect for radius
                pulse_factor = (math.sin(pygame.time.get_ticks() / 100.0) + 1) / 2 # 0 to 1
                pulsating_radius = scaled_proximity_radius * (1 + 0.05 * pulse_factor) # Max 5% pulse

                proximity_surface = pygame.Surface((int(pulsating_radius * 2), int(pulsating_radius * 2)), pygame.SRCALPHA)
                pygame.draw.circle(proximity_surface, proximity_color, (int(pulsating_radius), int(pulsating_radius)), int(pulsating_radius), thickness)
                
                proximity_rect = proximity_surface.get_rect(center=(proximity_screen_x, proximity_screen_y))
                SCREEN.blit(proximity_surface, proximity_rect)


        # Draw Space Station
        screen_x, screen_y = self.world_to_screen(self.space_station.x, self.space_station.y)
        scaled_size = int(self.space_station.size * zoom_factor)
        # Re-draw station image scaled
        if scaled_size > 0: # Avoid drawing if size becomes 0
            scaled_station_image = pygame.transform.scale(self.space_station.image, (scaled_size, scaled_size))
            draw_rect = scaled_station_image.get_rect(center=(screen_x, screen_y))
            SCREEN.blit(scaled_station_image, draw_rect)

        # Draw Trading Outpost (new)
        if self.trading_outpost:
            screen_x, screen_y = self.world_to_screen(self.trading_outpost.x, self.trading_outpost.y)
            scaled_size = int(self.trading_outpost.size * zoom_factor)
            if scaled_size > 0:
                scaled_outpost_image = pygame.transform.scale(self.trading_outpost.image, (scaled_size, scaled_size))
                draw_rect = scaled_outpost_image.get_rect(center=(screen_x, screen_y))
                SCREEN.blit(scaled_outpost_image, draw_rect)

        # Draw Enemy Base
        if self.enemy_base:
            self.enemy_base.draw(SCREEN, self.camera_x, self.camera_y, zoom_factor)


        # Draw Asteroids
        for asteroid in self.asteroids:
            # Only draw if not stealth or if revealed
            if not asteroid.is_stealth or asteroid.is_revealed:
                screen_x, screen_y = self.world_to_screen(asteroid.x, asteroid.y)
                scaled_size = int(asteroid.size * zoom_factor)
                if scaled_size > 0:
                    # Use asteroid.image which is already updated for revealed state
                    scaled_asteroid_image = pygame.transform.scale(asteroid.image, (scaled_size * 2, scaled_size * 2))
                    draw_rect = scaled_asteroid_image.get_rect(center=(screen_x, screen_y))
                    SCREEN.blit(scaled_asteroid_image, draw_rect)
                    # Draw health bar for asteroid (also scaled)
                    if asteroid.health < asteroid.max_health:
                        bar_width = int(asteroid.size * 2 * zoom_factor)
                        bar_height = int(5 * zoom_factor)
                        health_percentage = asteroid.health / asteroid.max_health
                        current_health_width = int(bar_width * health_percentage)

                        health_bar_bg_rect = pygame.Rect(screen_x - scaled_size, screen_y + scaled_size + int(5 * zoom_factor), bar_width, bar_height)
                        health_bar_rect = pygame.Rect(screen_x - scaled_size, screen_y + scaled_size + int(5 * zoom_factor), current_health_width, bar_height)

                        pygame.draw.rect(SCREEN, RED, health_bar_bg_rect)
                        pygame.draw.rect(SCREEN, GREEN, health_bar_rect)


        # Draw Enemies
        for enemy in self.enemies:
            screen_x, screen_y = self.world_to_screen(enemy.x, enemy.y)
            scaled_width = int(enemy.original_image.get_width() * zoom_factor)
            scaled_height = int(enemy.original_image.get_height() * zoom_factor)
            if scaled_width > 0 and scaled_height > 0:
                scaled_enemy_image = pygame.transform.scale(enemy.original_image, (scaled_width, scaled_height))
                scaled_rotated_enemy_image = pygame.transform.rotate(scaled_enemy_image, enemy.angle)
                draw_rect = scaled_rotated_enemy_image.get_rect(center=(screen_x, screen_y))
                SCREEN.blit(scaled_rotated_enemy_image, draw_rect)

        # Draw Planets
        for planet in self.planets:
            screen_x, screen_y = self.world_to_screen(planet.x, planet.y)
            scaled_size = int(planet.size * zoom_factor)
            if scaled_size > 0:
                scaled_planet_image = pygame.transform.scale(planet.image, (scaled_size * 2, scaled_size * 2))
                draw_rect = scaled_planet_image.get_rect(center=(screen_x, screen_y))
                SCREEN.blit(scaled_planet_image, draw_rect)

        # Draw Mining NPCs
        for npc in self.mining_npcs:
            npc.draw(SCREEN, self.camera_x, self.camera_y, zoom_factor)

        # Draw Projectiles (including HomingMissiles and SwarmRockets)
        for projectile in self.player_projectiles:
            screen_x, screen_y = self.world_to_screen(projectile.x, projectile.y)
            
            # Scale projectile image based on its type
            if isinstance(projectile, HomingMissile): # Covers both HomingMissile and SwarmRocketProjectile
                scaled_width = int(projectile.original_image.get_width() * zoom_factor)
                scaled_height = int(projectile.original_image.get_height() * zoom_factor)
                if scaled_width > 0 and scaled_height > 0:
                    scaled_projectile_image = pygame.transform.scale(projectile.original_image, (scaled_width, scaled_height))
                    scaled_rotated_projectile_image = pygame.transform.rotate(scaled_projectile_image, projectile.angle)
                    draw_rect = scaled_rotated_projectile_image.get_rect(center=(screen_x, screen_y))
                    SCREEN.blit(scaled_rotated_projectile_image, draw_rect)
            else: # Regular Projectile
                scaled_width = int(5 * zoom_factor)
                scaled_height = int(10 * zoom_factor)
                if scaled_width > 0 and scaled_height > 0:
                    scaled_projectile_image = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
                    pygame.draw.rect(scaled_projectile_image, projectile.color, (0, 0, scaled_width, scaled_height))
                    draw_rect = scaled_projectile_image.get_rect(center=(screen_x, screen_y))
                    SCREEN.blit(scaled_projectile_image, draw_rect)

        for projectile in self.enemy_projectiles:
            screen_x, screen_y = self.world_to_screen(projectile.x, projectile.y)
            scaled_width = int(5 * zoom_factor)
            scaled_height = int(10 * zoom_factor)
            if scaled_width > 0 and scaled_height > 0:
                scaled_projectile_image = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
                pygame.draw.rect(scaled_projectile_image, projectile.color, (0, 0, scaled_width, scaled_height))
                draw_rect = scaled_projectile_image.get_rect(center=(screen_x, screen_y))
                SCREEN.blit(scaled_projectile_image, draw_rect)

        # Draw Ship Parts
        for part in self.ship_parts_group:
            screen_x, screen_y = self.world_to_screen(part.x, part.y)
            scaled_size = int(part.size * zoom_factor)
            if scaled_size > 0:
                scaled_part_image = pygame.transform.scale(part.image, (scaled_size, scaled_size))
                draw_rect = scaled_part_image.get_rect(center=(screen_x, screen_y))
                SCREEN.blit(scaled_part_image, draw_rect)

        # Draw Material Drops
        for material_drop in self.material_drops_group:
            screen_x, screen_y = self.world_to_screen(material_drop.x, material_drop.y)
            scaled_size = int(material_drop.size * zoom_factor)
            if scaled_size > 0:
                scaled_material_image = pygame.transform.scale(material_drop.image, (scaled_size, scaled_size))
                draw_rect = scaled_material_image.get_rect(center=(screen_x, screen_y))
                SCREEN.blit(scaled_material_image, draw_rect)

        # Draw Player
        player_screen_x, player_screen_y = self.world_to_screen(self.player.x, self.player.y)
        scaled_player_width = int(self.player.original_image.get_width() * zoom_factor)
        scaled_player_height = int(self.player.original_image.get_height() * zoom_factor)
        if scaled_player_width > 0 and scaled_player_height > 0:
            scaled_player_image = pygame.transform.scale(self.player.original_image, (scaled_player_width, scaled_player_height))
            scaled_rotated_player_image = pygame.transform.rotate(scaled_player_image, self.player.angle)
            draw_rect = scaled_rotated_player_image.get_rect(center=(player_screen_x, player_screen_y))
            SCREEN.blit(scaled_rotated_player_image, draw_rect)

        # Draw mining laser if active and playing and tool is ShortRangeLaser or LongRangeLaser
        if self.mining_laser_active and self.game_state == "PLAYING" and \
           (self.player.current_mining_tool == "ShortRangeLaser" or \
            self.player.current_mining_tool == "LongRangeLaser"):
            
            player_screen_x, player_screen_y = self.world_to_screen(self.player.x, self.player.y)
            mouse_screen_x, mouse_screen_y = self.world_to_screen(self.mouse_world_x, self.mouse_world_y)

            mining_range_to_draw = 0
            if self.player.current_mining_tool == "ShortRangeLaser":
                mining_range_to_draw = SHORT_RANGE_LASER_RANGE * zoom_factor
            elif self.player.current_mining_tool == "LongRangeLaser":
                mining_range_to_draw = LONG_RANGE_LASER_RANGE * zoom_factor

            dx = mouse_screen_x - player_screen_x
            dy = mouse_screen_y - player_screen_y
            distance = math.hypot(dx, dy)

            if distance > mining_range_to_draw:
                ratio = mining_range_to_draw / distance
                end_x = player_screen_x + dx * ratio
                end_y = player_screen_y + dy * ratio
            else:
                end_x = mouse_screen_x
                end_y = mouse_screen_y

            pygame.draw.line(SCREEN, MINING_LASER_COLOR,
                             (player_screen_x, player_screen_y),
                             (end_x, end_y), int(3 * zoom_factor) or 1)

        # Draw auto-mining laser beams if active
        if self.auto_mine_active and self.game_state == "PLAYING" and self.player.current_mining_tool == "AutoMiningLaser":
            player_screen_x, player_screen_y = self.world_to_screen(self.player.x, self.player.y)
            for asteroid in self.targeted_asteroids:
                asteroid_screen_x, asteroid_screen_y = self.world_to_screen(asteroid.x, asteroid.y)
                pygame.draw.line(SCREEN, AUTO_MINE_BEAM_COLOR,
                                 (player_screen_x, player_screen_y),
                                 (asteroid_screen_x, asteroid_screen_y), int(2 * zoom_factor) or 1)

        # --- Draw Ping Effects ---
        if self.outgoing_ping_active:
            elapsed_time_ping = (pygame.time.get_ticks() - self.outgoing_ping_start_time) / 1000.0
            current_radius = PING_OUTGOING_SPEED * elapsed_time_ping * zoom_factor
            alpha = max(0, 255 - int(255 * (elapsed_time_ping / PING_OUTGOING_LIFETIME))) # Fade out

            ping_surface = pygame.Surface((int(current_radius * 2), int(current_radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(ping_surface, (PING_COLOR[0], PING_COLOR[1], PING_COLOR[2], alpha),
                               (int(current_radius), int(current_radius)), int(current_radius), int(2 * zoom_factor) or 1) # Outline only

            ping_screen_x, ping_screen_y = self.world_to_screen(self.outgoing_ping_world_pos[0], self.outgoing_ping_world_pos[1])
            ping_rect = ping_surface.get_rect(center=(ping_screen_x, ping_screen_y))
            SCREEN.blit(ping_surface, ping_rect)

        if self.incoming_ping_active:
            elapsed_time_incoming = (pygame.time.get_ticks() - self.incoming_ping_start_time) / 1000.0
            alpha = max(0, 255 - int(255 * (elapsed_time_incoming / PING_INCOMING_DURATION)))
            
            player_screen_x, player_screen_y = self.world_to_screen(self.player.x, self.player.y)
            station_screen_x, station_screen_y = self.world_to_screen(self.space_station.x, self.space_station.y)

            dx = station_screen_x - player_screen_x
            dy = station_screen_y - player_screen_y
            distance = math.hypot(dx, dy)

            if distance > 0:
                dir_x = dx / distance
                dir_y = dy / distance

                beam_end_x = player_screen_x + dir_x * PING_BEAM_LENGTH * zoom_factor
                beam_end_y = player_screen_y + dir_y * PING_BEAM_LENGTH * zoom_factor

                ping_beam_color_with_alpha = (PING_COLOR[0], PING_COLOR[1], PING_COLOR[2], alpha)
                
                line_surface = pygame.Surface(SCREEN.get_size(), pygame.SRCALPHA)
                pygame.draw.line(line_surface, ping_beam_color_with_alpha,
                                 (player_screen_x, player_screen_y),
                                 (beam_end_x, beam_end_y), int(3 * zoom_factor) or 1)
                SCREEN.blit(line_surface, (0, 0))

            for planet in self.planets:
                planet_screen_x, planet_screen_y = self.world_to_screen(planet.x, planet.y)

                dx_p = planet_screen_x - player_screen_x
                dy_p = planet_screen_y - player_screen_y
                distance_p = math.hypot(dx_p, dy_p)

                if distance_p > 0:
                    dir_x_p = dx_p / distance_p
                    dir_y_p = dy_p / distance_p

                    beam_end_x_p = player_screen_x + dir_x_p * PING_BEAM_LENGTH * zoom_factor
                    beam_end_y_p = player_screen_y + dir_y_p * PING_BEAM_LENGTH * zoom_factor

                    planet_ping_color_with_alpha = (YELLOW[0], YELLOW[1], YELLOW[2], alpha)

                    line_surface_p = pygame.Surface(SCREEN.get_size(), pygame.SRCALPHA)
                    pygame.draw.line(line_surface_p, planet_ping_color_with_alpha,
                                     (player_screen_x, player_screen_y),
                                     (beam_end_x_p, beam_end_y_p), int(3 * zoom_factor) or 1)
                    SCREEN.blit(line_surface_p, (0, 0))

                    pygame.draw.circle(SCREEN, planet_ping_color_with_alpha, (int(planet_screen_x), int(planet_screen_y)), int(5 * zoom_factor) or 1)
                    
                    # Scale font size for planet name or use a smaller font
                    scaled_font_size = max(10, int(FONT.get_height() * zoom_factor))
                    scaled_font = pygame.font.Font(None, scaled_font_size)
                    planet_name_text = scaled_font.render(planet.planet_type_name, True, (255,255,255,alpha))
                    planet_name_rect = planet_name_text.get_rect(center=(planet_screen_x, planet_screen_y - int(20 * zoom_factor)))
                    SCREEN.blit(planet_name_text, planet_name_rect)

                # Draw ping for stealth asteroids if revealed
                if ANTENNA_TYPES[self.player.current_antenna_type]["reveals_stealth"]:
                    for asteroid in self.asteroids:
                        if asteroid.is_stealth and asteroid.is_revealed:
                            asteroid_screen_x, asteroid_screen_y = self.world_to_screen(asteroid.x, asteroid.y)
                            
                            dx_a = asteroid_screen_x - player_screen_x
                            dy_a = asteroid_screen_y - player_screen_y
                            distance_a = math.hypot(dx_a, dy_a)

                            if distance_a > 0:
                                dir_x_a = dx_a / distance_a
                                dir_y_a = dy_a / distance_a

                                beam_end_x_a = player_screen_x + dir_x_a * PING_BEAM_LENGTH * zoom_factor
                                beam_end_y_a = player_screen_y + dir_y_a * PING_BEAM_LENGTH * zoom_factor

                                stealth_asteroid_ping_color_with_alpha = (STEALTH_ASTEROID_REVEAL_COLOR[0], STEALTH_ASTEROID_REVEAL_COLOR[1], STEALTH_ASTEROID_REVEAL_COLOR[2], alpha)

                                line_surface_a = pygame.Surface(SCREEN.get_size(), pygame.SRCALPHA)
                                pygame.draw.line(line_surface_a, stealth_asteroid_ping_color_with_alpha,
                                                 (player_screen_x, player_screen_y),
                                                 (beam_end_x_a, beam_end_y_a), int(3 * zoom_factor) or 1)
                                SCREEN.blit(line_surface_a, (0, 0))

                                pygame.draw.circle(SCREEN, stealth_asteroid_ping_color_with_alpha, (int(asteroid_screen_x), int(asteroid_screen_y)), int(5 * zoom_factor) or 1)


        # Draw Jump Drive target selection UI
        if self.game_state == "JUMP_DRIVE_SELECT_TARGET":
            # Draw a crosshair at the mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            crosshair_size = 10
            pygame.draw.line(SCREEN, GREEN, (mouse_x - crosshair_size, mouse_y), (mouse_x + crosshair_size, mouse_y), 2)
            pygame.draw.line(SCREEN, GREEN, (mouse_x, mouse_y - crosshair_size), (mouse_x, mouse_y + crosshair_size), 2)
            target_text = FONT.render("Click to select jump target, Press 'R' to cancel", True, WHITE)
            text_rect = target_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            SCREEN.blit(target_text, text_rect)

        # Draw Jump Drive rings during warp initiation
        if self.jump_rings_active and self.game_state == "JUMP_DRIVE_WARP":
            elapsed_time = (pygame.time.get_ticks() - self.jump_rings_start_time) / 1000.0
            
            # Calculate ring expansion radius
            current_radius = JUMP_DRIVE_RING_SPEED * elapsed_time
            alpha = max(0, 255 - int(255 * (elapsed_time / (JUMP_DRIVE_WARP_DURATION / 1000.0))))

            if current_radius < JUMP_DRIVE_MAX_RING_RADIUS:
                # Calculate the rear of the ship
                # Angle for movement is (270 - self.player.angle) % 360
                # Angle for rear is (270 - self.player.angle + 180) % 360 (opposite direction)
                rear_angle_rad = math.radians((270 - self.player.angle + 180) % 360)
                
                # Initial offset from center of ship to its rear
                offset_x = (self.player.original_image.get_height() / 2) * math.cos(rear_angle_rad)
                offset_y = (self.player.original_image.get_height() / 2) * math.sin(rear_angle_rad)

                # Movement vector for rings (opposite to ship's forward direction)
                # Ship's forward direction is (270 - self.player.angle) % 360
                # So, ring movement direction is (270 - self.player.angle + 180) % 360
                ring_move_rad = math.radians((270 - self.player.angle + 180) % 360)
                ring_move_x = JUMP_DRIVE_RING_TRAIL_SPEED * elapsed_time * math.cos(ring_move_rad)
                ring_move_y = JUMP_DRIVE_RING_TRAIL_SPEED * elapsed_time * math.sin(ring_move_rad)

                # Ring origin in world coordinates
                ring_world_x = self.player.x + offset_x + ring_move_x
                ring_world_y = self.player.y + offset_y + ring_move_y

                # Convert to screen coordinates
                ring_screen_x, ring_screen_y = self.world_to_screen(ring_world_x, ring_world_y)

                # Draw the ring
                ring_surface = pygame.Surface((int(current_radius * 2), int(current_radius * 2)), pygame.SRCALPHA)
                pygame.draw.circle(ring_surface, (BLUE[0], BLUE[1], BLUE[2], alpha),
                                   (int(current_radius), int(current_radius)), int(current_radius), int(5 * zoom_factor) or 1) # Thicker rings

                ring_rect = ring_surface.get_rect(center=(ring_screen_x, ring_screen_y))
                SCREEN.blit(ring_surface, ring_rect)

            jump_text = LARGE_FONT.render("JUMP INITIATING...", True, YELLOW)
            jump_rect = jump_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            SCREEN.blit(jump_text, jump_rect)


        # Draw station menus based on game state
        if self.game_state == "PAUSED_AT_STATION":
            self.draw_station_main_menu()
        elif self.game_state == "ECONOMY_SHOP":
            self.draw_economy_shop_menu()
        elif self.game_state == "SHIP_UPGRADING":
            self.draw_ship_upgrading_menu()
        elif self.game_state == "SHIP_SHOP":
            self.draw_ship_shop_menu()
        elif self.game_state == "MINING_TOOLS_MENU":
            self.draw_mining_tools_menu()
        elif self.game_state == "ENERGY_CORE_MENU":
            self.draw_energy_core_menu()
        elif self.game_state == "ANTENNA_MENU":
            self.draw_antenna_menu()
        elif self.game_state == "WEAPONS_MENU":
            self.draw_weapons_menu()
        elif self.game_state == "PROPULSION_MENU":
            self.draw_propulsion_menu()
        elif self.game_state == "TRADING_OUTPOST_MENU": # New menu
            self.draw_trading_outpost_menu()


        # Draw inventory screen if active (always on top)
        if self.game_state == "INVENTORY":
            self.draw_inventory_screen()


    def draw_button(self, text, x, y, width, height, action=None, is_active=False):
        """Helper function to draw a button and return its rect."""
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(x, y, width, height)
        
        current_color = BUTTON_COLOR
        if is_active:
            current_color = ACTIVE_BUTTON_COLOR
        elif button_rect.collidepoint(mouse_pos):
            current_color = BUTTON_HOVER_COLOR

        pygame.draw.rect(SCREEN, current_color, button_rect, border_radius=5)
        pygame.draw.rect(SCREEN, WHITE, button_rect, 2, border_radius=5) # Border

        text_surf = BUTTON_FONT.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=button_rect.center)
        SCREEN.blit(text_surf, text_rect)
        
        # Store the button rect for click detection
        if action:
            self.buttons[action] = button_rect
        return button_rect

    def draw_station_main_menu(self):
        """Draws the main space station menu with navigation buttons."""
        # Darken background
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180)) # Black with 180 alpha (out of 255)
        SCREEN.blit(s, (0, 0))

        # Menu title
        title_text = LARGE_FONT.render("SPACE STATION", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        SCREEN.blit(title_text, title_rect)

        button_width = 250
        button_height = 50
        button_spacing = 20
        start_y = SCREEN_HEIGHT // 2 - 80

        # Clear previous button rects
        self.buttons.clear()

        # Economy Trading Shop Button
        self.draw_button("Economy Trading Shop", (SCREEN_WIDTH - button_width) // 2, start_y, button_width, button_height, 'economy_button')
        
        # Ship Upgrading Button
        self.draw_button("Ship Upgrading", (SCREEN_WIDTH - button_width) // 2, start_y + button_height + button_spacing, button_width, button_height, 'upgrade_button')

        # Ship Shop Button
        self.draw_button("Ship Shop", (SCREEN_WIDTH - button_width) // 2, start_y + 2 * (button_height + button_spacing), button_width, button_height, 'shop_button')

        # Resume Exploration Button
        self.draw_button("Resume Exploration", (SCREEN_WIDTH - button_width) // 2, start_y + 3 * (button_height + button_spacing) + 30, button_width, button_height, 'resume_button')


    def draw_economy_shop_menu(self):
        """Draws the placeholder menu for the Economy Trading Shop."""
        # Darken background
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200)) # Black with higher alpha
        SCREEN.blit(s, (0, 0))

        # Menu title
        title_text = LARGE_FONT.render("ECONOMY TRADING SHOP", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        SCREEN.blit(title_text, title_rect)

        # Placeholder content
        placeholder_text = MENU_FONT.render("Trade materials and resources here!", True, GRAY)
        placeholder_rect = placeholder_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(placeholder_text, placeholder_rect)

        # Clear previous button rects
        self.buttons.clear()
        # Back Button
        self.draw_button("Back", (SCREEN_WIDTH - 150) // 2, SCREEN_HEIGHT - 100, 150, 50, 'back_button')

    def draw_ship_upgrading_menu(self):
        """Draws the placeholder menu for Ship Upgrading."""
        # Darken background
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200)) # Black with higher alpha
        SCREEN.blit(s, (0, 0))

        # Menu title
        title_text = LARGE_FONT.render("SHIP UPGRADING", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        SCREEN.blit(title_text, title_rect)

        button_width = 250
        button_height = 50
        button_spacing = 20
        start_y = SCREEN_HEIGHT // 2 - 100 # Adjusted start_y to fit more buttons

        # Clear previous button rects
        self.buttons.clear()

        # Resource Collection (Mining Tools) Button
        self.draw_button("Resource Collection", (SCREEN_WIDTH - button_width) // 2, start_y, button_width, button_height, 'mining_tools_button')

        # Energy Core Button
        self.draw_button("Energy Core", (SCREEN_WIDTH - button_width) // 2, start_y + button_height + button_spacing, button_width, button_height, 'energy_core_button')
        
        # Antennas/Radar Systems Button
        self.draw_button("Antennas/Radar Systems", (SCREEN_WIDTH - button_width) // 2, start_y + 2 * (button_height + button_spacing), button_width, button_height, 'antenna_radar_button')

        # Weapons Button
        self.draw_button("Weapons", (SCREEN_WIDTH - button_width) // 2, start_y + 3 * (button_height + button_spacing), button_width, button_height, 'weapons_button')

        # Propulsion Button
        self.draw_button("Propulsion", (SCREEN_WIDTH - button_width) // 2, start_y + 4 * (button_height + button_spacing), button_width, button_height, 'propulsion_button')

        # Back Button
        self.draw_button("Back", (SCREEN_WIDTH - button_width) // 2, start_y + 5 * (button_height + button_spacing) + 30, button_width, button_height, 'back_button')


    def draw_mining_tools_menu(self):
        """Draws the menu for selecting mining tools."""
        # Darken background
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200)) # Black with higher alpha
        SCREEN.blit(s, (0, 0))

        # Menu title
        title_text = LARGE_FONT.render("MINING TOOLS", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        SCREEN.blit(title_text, title_rect)

        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = SCREEN_HEIGHT // 2 - 80 # Adjusted start_y to fit new button

        # Clear previous button rects
        self.buttons.clear()

        # Drill Tool Button (now default)
        self.draw_button("Drill", (SCREEN_WIDTH - button_width) // 2, start_y, button_width, button_height, 'drill_button', is_active=(self.player.current_mining_tool == "Drill"))

        # Short Range Laser Tool Button
        self.draw_button("Short Range Laser", (SCREEN_WIDTH - button_width) // 2, start_y + button_height + button_spacing, button_width, button_height, 'short_range_laser_button', is_active=(self.player.current_mining_tool == "ShortRangeLaser"))

        # Long Range Laser Tool Button
        self.draw_button("Long Range Laser", (SCREEN_WIDTH - button_width) // 2, start_y + 2 * (button_height + button_spacing), button_width, button_height, 'long_range_laser_button', is_active=(self.player.current_mining_tool == "LongRangeLaser"))

        # Auto-Mining Laser Tool Button
        self.draw_button("Auto-Mining Laser", (SCREEN_WIDTH - button_width) // 2, start_y + 3 * (button_height + button_spacing), button_width, button_height, 'auto_mining_laser_button', is_active=(self.player.current_mining_tool == "AutoMiningLaser"))


        # Current Tool Display
        current_tool_text = FONT.render(f"Current Tool: {self.player.current_mining_tool}", True, WHITE)
        current_tool_rect = current_tool_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + 4 * (button_height + button_spacing) + 20))
        SCREEN.blit(current_tool_text, current_tool_rect)

        # Back Button
        self.draw_button("Back", (SCREEN_WIDTH - 150) // 2, SCREEN_HEIGHT - 100, 150, 50, 'back_button')

    def draw_energy_core_menu(self):
        """Draws the menu for selecting energy cores."""
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        SCREEN.blit(s, (0, 0))

        title_text = LARGE_FONT.render("ENERGY CORE", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        SCREEN.blit(title_text, title_rect)

        button_width = 250
        button_height = 50
        button_spacing = 20
        start_y = SCREEN_HEIGHT // 2 - 80

        self.buttons.clear()

        # Standard Core
        self.draw_button("Standard Core (Recharge: 1x, Power: 1x)", (SCREEN_WIDTH - button_width) // 2, start_y, button_width, button_height, 'standard_core_button', is_active=(self.current_energy_core == "Standard Core"))

        # Advanced Core
        self.draw_button("Advanced Core (Recharge: 1.5x, Power: 1.2x)", (SCREEN_WIDTH - button_width) // 2, start_y + button_height + button_spacing, button_width, button_height, 'advanced_core_button', is_active=(self.current_energy_core == "Advanced Core"))

        current_core_text = FONT.render(f"Current Core: {self.current_energy_core}", True, WHITE)
        current_core_rect = current_core_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + 2 * (button_height + button_spacing) + 20))
        SCREEN.blit(current_core_text, current_core_rect)

        self.draw_button("Back", (SCREEN_WIDTH - 150) // 2, SCREEN_HEIGHT - 100, 150, 50, 'back_button')

    def draw_antenna_menu(self):
        """Draws the menu for selecting antennas."""
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        SCREEN.blit(s, (0, 0))

        title_text = LARGE_FONT.render("ANTENNAS / RADAR SYSTEMS", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        SCREEN.blit(title_text, title_rect)

        button_width = 250
        button_height = 50
        button_spacing = 20
        start_y = SCREEN_HEIGHT // 2 - 80

        self.buttons.clear()

        # Basic Antenna
        self.draw_button("Basic Antenna (Range: 1x)", (SCREEN_WIDTH - button_width) // 2, start_y, button_width, button_height, 'basic_antenna_button', is_active=(self.player.current_antenna_type == "Basic Antenna"))

        # Standard Antenna
        self.draw_button("Standard Antenna (Range: 1.5x)", (SCREEN_WIDTH - button_width) // 2, start_y + button_height + button_spacing, button_width, button_height, 'standard_antenna_button', is_active=(self.player.current_antenna_type == "Standard Antenna"))

        # Advanced Antenna
        self.draw_button("Advanced Antenna (Range: 2.5x, Reveals Stealth Asteroids)", (SCREEN_WIDTH - button_width) // 2, start_y + 2 * (button_height + button_spacing), button_width, button_height, 'advanced_antenna_button', is_active=(self.player.current_antenna_type == "Advanced Antenna"))

        current_antenna_text = FONT.render(f"Current Antenna: {self.player.current_antenna_type}", True, WHITE)
        current_antenna_rect = current_antenna_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + 3 * (button_height + button_spacing) + 20))
        SCREEN.blit(current_antenna_text, current_antenna_rect)

        self.draw_button("Back", (SCREEN_WIDTH - 150) // 2, SCREEN_HEIGHT - 100, 150, 50, 'back_button')

    def draw_weapons_menu(self):
        """Draws the menu for selecting weapons."""
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        SCREEN.blit(s, (0, 0))

        title_text = LARGE_FONT.render("WEAPONS", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
        SCREEN.blit(title_text, title_rect)

        button_width = 200
        button_height = 40
        button_spacing = 15
        start_y = SCREEN_HEIGHT // 2 - 120 # Adjusted for more buttons

        self.buttons.clear()

        # Weapon Slot Selection
        slot_button_width = 100
        slot_button_x_offset = 100
        self.draw_button("Slot 1", SCREEN_WIDTH // 2 - slot_button_x_offset - slot_button_width // 2, start_y - 60, slot_button_width, button_height, 'slot1_button', is_active=(self.selected_weapon_slot == 1))
        self.draw_button("Slot 2", SCREEN_WIDTH // 2 + slot_button_x_offset - slot_button_width // 2, start_y - 60, slot_button_width, button_height, 'slot2_button', is_active=(self.selected_weapon_slot == 2))

        # Weapon Type Buttons
        self.draw_button("Laser", (SCREEN_WIDTH - button_width) // 2, start_y, button_width, button_height, 'laser_weapon_button')
        self.draw_button("Laser Turret", (SCREEN_WIDTH - button_width) // 2, start_y + button_height + button_spacing, button_width, button_height, 'laser_turret_button')
        self.draw_button("Minigun Turret", (SCREEN_WIDTH - button_width) // 2, start_y + 2 * (button_height + button_spacing), button_width, button_height, 'mini_gun_turret_button')
        self.draw_button("Homing Missile", (SCREEN_WIDTH - button_width) // 2, start_y + 3 * (button_height + button_spacing), button_width, button_height, 'homing_missile_button')
        self.draw_button("Swarm Rocket", (SCREEN_WIDTH - button_width) // 2, start_y + 4 * (button_height + button_spacing), button_width, button_height, 'swarm_rocket_button')
        self.draw_button("None (Empty Slot)", (SCREEN_WIDTH - button_width) // 2, start_y + 5 * (button_height + button_spacing), button_width, button_height, 'none_weapon_button')


        # Current Equipped Weapons Display
        current_weapon1_text = FONT.render(f"Slot 1: {self.player.weapon_slot_1}", True, WHITE)
        current_weapon1_rect = current_weapon1_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + 4 * (button_height + button_spacing) + 80))
        SCREEN.blit(current_weapon1_text, current_weapon1_rect)

        current_weapon2_text = FONT.render(f"Slot 2: {self.player.weapon_slot_2}", True, WHITE)
        current_weapon2_rect = current_weapon2_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + 4 * (button_height + button_spacing) + 110))
        SCREEN.blit(current_weapon2_text, current_weapon2_rect)


        self.draw_button("Back", (SCREEN_WIDTH - 150) // 2, SCREEN_HEIGHT - 50, 150, 50, 'back_button')


    def draw_propulsion_menu(self):
        """Draws the menu for selecting propulsion systems."""
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        SCREEN.blit(s, (0, 0))

        title_text = LARGE_FONT.render("PROPULSION", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        SCREEN.blit(title_text, title_rect)

        button_width = 250
        button_height = 50
        button_spacing = 20
        start_y = SCREEN_HEIGHT // 2 - 80

        self.buttons.clear()

        # Standard Thruster Button
        self.draw_button("Standard Thruster", (SCREEN_WIDTH - button_width) // 2, start_y, button_width, button_height, 'standard_thruster_button', is_active=(self.player.current_engine_type == "Standard Thruster"))

        # Ion Engine Button
        self.draw_button("Ion Engine (High Top Speed, Low Accel, Weak Gravity)", (SCREEN_WIDTH - button_width) // 2, start_y + button_height + button_spacing, button_width, button_height, 'ion_engine_button', is_active=(self.player.current_engine_type == "Ion Engine"))

        # Space Thruster Button
        self.draw_button("Space Thruster (Fast Accel, Lower Top Speed, Strong Gravity)", (SCREEN_WIDTH - button_width) // 2, start_y + 2 * (button_height + button_spacing), button_width, button_height, 'space_thruster_button', is_active=(self.player.current_engine_type == "Space Thruster"))

        # Hyper Drive Button (New)
        self.draw_button("Hyper Drive (Very Fast, Jump Ability)", (SCREEN_WIDTH - button_width) // 2, start_y + 3 * (button_height + button_spacing), button_width, button_height, 'hyper_drive_button', is_active=(self.player.current_engine_type == "Hyper Drive"))

        current_engine_text = FONT.render(f"Current Engine: {self.player.current_engine_type}", True, WHITE)
        current_engine_rect = current_engine_text.get_rect(center=(SCREEN_WIDTH // 2, start_y + 4 * (button_height + button_spacing) + 20))
        SCREEN.blit(current_engine_text, current_engine_rect)

        self.draw_button("Back", (SCREEN_WIDTH - 150) // 2, SCREEN_HEIGHT - 100, 150, 50, 'back_button')


    def draw_ship_shop_menu(self):
        """Draws the placeholder menu for the Ship Shop."""
        # Darken background
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200)) # Black with higher alpha
        SCREEN.blit(s, (0, 0))

        # Menu title
        title_text = LARGE_FONT.render("SHIP SHOP", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        SCREEN.blit(title_text, title_rect)

        # Placeholder content
        placeholder_text = MENU_FONT.render("Buy new ships or customize your current one!", True, GRAY)
        placeholder_rect = placeholder_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(placeholder_text, placeholder_rect)

        # Clear previous button rects
        self.buttons.clear()
        # Back Button
        self.draw_button("Back", (SCREEN_WIDTH - 150) // 2, SCREEN_HEIGHT - 100, 150, 50, 'back_button')

    def draw_trading_outpost_menu(self):
        """Draws the menu for the Trading Outpost."""
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        SCREEN.blit(s, (0, 0))

        title_text = LARGE_FONT.render("TRADING OUTPOST", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        SCREEN.blit(title_text, title_rect)

        text_start_x = SCREEN_WIDTH // 2 - 150
        text_start_y = SCREEN_HEIGHT // 2 - 80
        line_height = 30

        # Display current resources
        current_gold_text = FONT.render(f"Your Gold: {self.player.gold_ore}", True, GOLD_COLOR)
        SCREEN.blit(current_gold_text, (text_start_x, text_start_y))
        current_silicon_text = FONT.render(f"Your Silicon: {self.player.silicon_ore}", True, SILICON_COLOR)
        SCREEN.blit(current_silicon_text, (text_start_x, text_start_y + line_height))
        current_ship_parts_text = FONT.render(f"Your Ship Parts: {self.player.ship_parts}", True, SHIP_PART_COLOR)
        SCREEN.blit(current_ship_parts_text, (text_start_x, text_start_y + 2 * line_height))
        current_crystal_text = FONT.render(f"Your Gas Giant Crystals: {self.player.gas_giant_crystal}", True, GAS_GIANT_CRYSTAL_COLOR)
        SCREEN.blit(current_crystal_text, (text_start_x, text_start_y + 3 * line_height))

        # Display trade offer
        trade_offer_text = MENU_FONT.render(f"Trade {GAS_GIANT_CRYSTAL_TRADE_COST['Gold']} Gold, {GAS_GIANT_CRYSTAL_TRADE_COST['Silicon']} Silicon, {GAS_GIANT_CRYSTAL_TRADE_COST['Ship Parts']} Ship Parts for {GAS_GIANT_CRYSTAL_TRADE_AMOUNT} Gas Giant Crystal", True, YELLOW)
        trade_offer_rect = trade_offer_text.get_rect(center=(SCREEN_WIDTH // 2, text_start_y + 5 * line_height))
        SCREEN.blit(trade_offer_text, trade_offer_rect)

        self.buttons.clear()
        # Trade Button
        self.draw_button("Trade for Crystal", (SCREEN_WIDTH - 200) // 2, text_start_y + 6 * line_height + 20, 200, 50, 'trade_crystal_button')
        # Back Button
        self.draw_button("Back", (SCREEN_WIDTH - 150) // 2, SCREEN_HEIGHT - 100, 150, 50, 'back_button')


    def draw_inventory_screen(self):
        """Draws the inventory screen overlay."""
        # Darken background
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200)) # Black with higher alpha for inventory
        SCREEN.blit(s, (0, 0))

        # Inventory box
        inventory_box_width = 400
        inventory_box_height = 350 # Increased height for new resources
        inventory_box_x = (SCREEN_WIDTH - inventory_box_width) // 2
        inventory_box_y = (SCREEN_HEIGHT - inventory_box_height) // 2
        inventory_rect = pygame.Rect(inventory_box_x, inventory_box_y, inventory_box_width, inventory_box_height)
        pygame.draw.rect(SCREEN, GRAY, inventory_rect, 3) # Outline
        pygame.draw.rect(SCREEN, BLACK, inventory_rect) # Fill

        # Inventory title
        title_text = LARGE_FONT.render("INVENTORY", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, inventory_box_y + 30))
        SCREEN.blit(title_text, title_rect)

        # Material and Ship Parts display
        text_start_x = inventory_box_x + 50
        text_start_y = inventory_box_y + 80
        line_height = 30

        # Ship Parts
        ship_parts_text = INVENTORY_FONT.render(f"Ship Parts: {self.player.ship_parts}", True, SHIP_PART_COLOR)
        SCREEN.blit(ship_parts_text, (text_start_x, text_start_y))

        # Materials
        carbon_text = INVENTORY_FONT.render(f"Carbon: {self.player.carbon_ore}", True, CARBON_COLOR)
        SCREEN.blit(carbon_text, (text_start_x, text_start_y + line_height))
        silicon_text = INVENTORY_FONT.render(f"Silicon: {self.player.silicon_ore}", True, SILICON_COLOR)
        SCREEN.blit(silicon_text, (text_start_x, text_start_y + 2 * line_height))
        gold_text = INVENTORY_FONT.render(f"Gold: {self.player.gold_ore}", True, GOLD_COLOR)
        SCREEN.blit(gold_text, (text_start_x, text_start_y + 3 * line_height))
        
        # New Resources
        rocky_ore_text = INVENTORY_FONT.render(f"Rocky Ore: {self.player.rocky_ore}", True, ROCKY_ORE_COLOR)
        SCREEN.blit(rocky_ore_text, (text_start_x, text_start_y + 4 * line_height))
        gas_giant_crystal_text = INVENTORY_FONT.render(f"Gas Giant Crystal: {self.player.gas_giant_crystal}", True, GAS_GIANT_CRYSTAL_COLOR)
        SCREEN.blit(gas_giant_crystal_text, (text_start_x, text_start_y + 5 * line_height))


        # Hint to close
        close_text = FONT.render("Press 'I' to Close Inventory", True, WHITE)
        close_rect = close_text.get_rect(center=(SCREEN_WIDTH // 2, inventory_box_y + inventory_box_height - 30))
        SCREEN.blit(close_text, close_rect)


    def display_game_over(self):
        """Displays the game over message."""
        game_over_text = LARGE_FONT.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        SCREEN.blit(game_over_text, text_rect)

        # Display final XP and Level instead of score
        final_xp_text = FONT.render(f"Final XP: {self.player.current_xp} (Level {self.player.level})", True, WHITE)
        xp_rect = final_xp_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        SCREEN.blit(xp_text, xp_rect)

        restart_text = FONT.render("Press R to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        SCREEN.blit(restart_text, restart_rect)

    def reset_game(self):
        """Rsesets the game to its initial state."""
        self.player = Player() # Player starts at world origin again
        self.asteroids.empty()
        self.enemies.empty()
        self.player_projectiles.empty()
        self.enemy_projectiles.empty()
        self.ship_parts_group.empty() # Clear ship parts
        self.material_drops_group.empty() # Clear material drops
        self.planets.empty() # Clear planets
        self.mining_zones.clear() # Clear mining zones
        self.mining_npcs.empty() # Clear mining NPCs
        self.enemy_base = None # Reset enemy base

        self.game_over = False
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        # Reset camera to center on new player position
        self.camera_x = self.player.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.y - SCREEN_HEIGHT // 2
        self.mining_laser_active = False # Reset mining laser state
        self.auto_mine_active = False # Reset auto-mine active state
        self.targeted_asteroids.clear() # Clear targeted asteroids
        self.auto_mine_charge = AUTO_MINE_MAX_CHARGE # Reset auto-mine charge
        self.game_state = "PLAYING" # Reset game state
        self.previous_game_state = "PLAYING" # Reset previous game state
        self.e_pressed_last_frame = False # Reset key state for 'E'
        self.i_pressed_last_frame = False # Reset key state for 'I'
        self.f_pressed_last_frame = False # Reset key state for 'F'
        # Reset ping variables
        self.last_ping_time = 0
        self.outgoing_ping_active = False
        self.incoming_ping_active = False
        self.ping_t_pressed_last_frame = False
        self.spawn_space_station() # Re-spawn station for new game
        self.trading_outpost = None # Reset trading outpost
        self.spawn_initial_asteroids()
        self.spawn_initial_planets() # Re-spawn planets
        self.spawn_mining_zones() # Re-spawn mining zones
        self.spawn_enemy_base() # Re-spawn enemy base
        # Reset Energy Core
        self.player.recharge_rate_multiplier = 1.0
        self.player.power_output_multiplier = 1.0
        self.current_energy_core = "Standard Core"
        self.last_button_press_time = 0 # Reset button cooldown
        # Reset Antenna
        self.player.current_antenna_type = "Basic Antenna"
        self.player.radar_range_multiplier = ANTENNA_TYPES[self.player.current_antenna_type]["range_multiplier"]
        # Reset Weapon Slots
        self.player.weapon_slot_1 = "Laser"
        self.player.weapon_slot_2 = "None"
        self.player.last_shot_time_slot1 = 0
        self.player.last_shot_time_slot2 = 0


        # Reset Jump Drive attributes
        self.last_jump_time = 0
        self.jump_target_world_pos = None
        self.jump_initiation_start_time = 0
        self.jump_rings_active = False
        self.jump_rings_start_time = 0
        self.jump_drive_zoom_active = False
        self.r_pressed_last_frame = False


# --- Main Game Loop ---
def game_loop():
    """
    The main loop of the game.
    Handles events, updates game state, and draws everything.
    """
    clock = pygame.time.Clock()
    game_manager = GameManager()
    running = True

    while running:
        current_time = pygame.time.get_ticks() # Get current time in milliseconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_manager.game_over and event.key == pygame.K_r:
                    game_manager.reset_game()
                # Pass all keydown events to handle_input for 'E', 'I', 'F', 'T', Space, LCTRL key logic
                game_manager.handle_input(pygame.key.get_pressed(), current_time)
            if event.type == pygame.KEYUP:
                # Pass all keyup events to handle_input for 'E', 'I', 'F', 'T', Space, LCTRL key logic
                game_manager.handle_input(pygame.key.get_pressed(), current_time)
            # Mouse motion is needed for laser aiming even if not clicked
            if event.type == pygame.MOUSEMOTION:
                game_manager.mouse_world_x = event.pos[0] + game_manager.camera_x
                game_manager.mouse_world_y = event.pos[1] + game_manager.camera_y
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Pass mouse click events to handle_input for menu button logic
                game_manager.handle_input(pygame.key.get_pressed(), current_time)


        keys = pygame.key.get_pressed()
        # Always call handle_input to update player movement and check for spacebar/mouse
        # Note: Mouse clicks are handled by MOUSEBUTTONDOWN event, not continuously by keys.
        # This ensures that the `can_press_button` check is only applied once per click.
        # Player update now takes game_state and target_angle for jump alignment
        game_manager.player.update(keys, current_time, game_manager.game_state) 

        # Update game state
        if not game_manager.game_over:
            game_manager.update_game_state(current_time)

        # Drawing
        SCREEN.fill(BLACK) # Clear screen

        game_manager.draw_game_objects()
        game_manager.draw_ui()

        if game_manager.game_over:
            game_manager.display_game_over()

        pygame.display.flip() # Update the full display Surface to the screen

        clock.tick(FPS) # Control frame rate

    pygame.quit()

if __name__ == "__main__":
    game_loop()