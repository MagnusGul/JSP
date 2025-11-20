import arcade

from game.systems.animation_system import AnimatedSprite
from game.entities.character.movement import move_with_collisions
from game.entities.character.sound_handler import get_surface_type
from game.entities.character.animation import animate
from game.entities.character.animation import update_rotation

class Character(AnimatedSprite):
    """Игровой персонаж с анимацией тела, ног и головы."""

    def __init__(
        self,
        assets: str,
        scale: float = 1.0,
        speed: int = 5,
        acceleration: float = 1,
        rotation_speed: int = 10,
    ):
        super().__init__(f"{assets}\\body", scale)
        self.legs = AnimatedSprite(f"{assets}\\walk\\")
        self.head = arcade.Sprite(f"{assets}\\head.png", scale)

        # Движение и повороты
        self.moving = False
        self.speed = speed
        self.acceleration_rate = acceleration
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.rotation_speed = rotation_speed
        self.last_move_angle = 0

        # Гибкость "шеи"
        self.body_follow_angle_threshold = 30
        self.body_follow_speed = 10
        self.walk_cycle_time = 1
        self.aiming = False

    def cupdate(
        self,
        walls: arcade.SpriteList,
        mouse_pos: tuple[int, int],
        window_size: tuple[int, int],
        camera: arcade.Camera2D,
        footstep_zones=None,
        footstep_system=None,
    ):
        # --- Движение с проверкой стен ---
        self.moving = move_with_collisions(self, walls)

        # --- Определяем поверхность ---
        surface_type = get_surface_type(self, footstep_zones)

        animate(self, surface_type, camera, footstep_system)


        # --- Обновление поворотов ---
        update_rotation(self, mouse_pos, window_size, camera, walls)