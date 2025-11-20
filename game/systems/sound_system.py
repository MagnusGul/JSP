import math
import os

import arcade
import random

class StepTrigger(arcade.SpriteSolidColor):
    def __init__(self, width, height, x, y, sound_type: str):
        super().__init__(
            width,
            height,
            x,
            y,
            arcade.color.TRANSPARENT_BLACK,
        )
        self.sound_type = sound_type


class SoundSystem:
    def __init__(self):
        step_sound_packs = os.listdir(f"assets\\sounds\\footsteps")
        self.step_sounds = {}
        for pack in step_sound_packs:
            sound_list = os.listdir(f"assets\\sounds\\footsteps\\{pack}")
            self.step_sounds[pack] = [arcade.load_sound(f"assets/sounds/footsteps/{pack}/{sound}") for sound in sound_list]

    def play_step(self, sound_type: str, camera_pos: tuple[float, float], source_pos: tuple[float, float]):
        """Проигрывает шаг с учётом позиции камеры и расстояния"""

        if sound_type not in self.step_sounds:
            return

        sound = random.choice(self.step_sounds[sound_type])

        # === 1. Получаем позицию игрока и камеры ===
        cam_x, cam_y = camera_pos
        src_x, src_y = source_pos
        # === 2. Рассчитываем расстояние и угол ===
        dx = src_x - cam_x
        dy = src_y - cam_y
        distance = math.sqrt(dx * dx + dy * dy)

        # === 3. Делаем затухание громкости по расстоянию ===
        max_hear_distance = 800  # дальше — тише (в пикселях)
        volume = max(0.0, 1.0 - (distance / max_hear_distance))

        # === 4. Позиционируем в стерео по горизонтали ===
        # dx нормализуется от -1 (лево) до +1 (право)
        stereo_pan = max(-1.0, min(1.0, dx / 400))  # 400 пикселей = полный разброс по панораме

        # === 5. Подаём звук с учётом громкости и панорамы ===
        arcade.play_sound(sound, volume=volume, pan=stereo_pan)


def get_step_trigger_list(footstep_trigger_obj_list: list):
    footstep_zones = arcade.SpriteList(use_spatial_hash=True)
    for obj in footstep_trigger_obj_list:
        xs = [p[0] for p in obj.shape]
        ys = [p[1] for p in obj.shape]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        zone = StepTrigger(max_x - min_x, max_y - min_y, (min_x + max_x) / 2, (min_y + max_y) / 2, obj.properties.get("sound", "default"))
        footstep_zones.append(zone)

    return footstep_zones