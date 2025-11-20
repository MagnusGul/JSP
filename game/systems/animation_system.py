import arcade
import os

class AnimatedSprite(arcade.Sprite):
    def __init__(self, textures_path: str, scale: float = 1.0, frame_delay: float = 0.1):
        texture_files = sorted(
            [f for f in os.listdir(textures_path) if f.lower().endswith((".png", ".jpg"))]
        )
        if not texture_files:
            raise FileNotFoundError(f"Нет текстур в папке: {textures_path}")
        super().__init__(arcade.load_texture(os.path.join(textures_path, texture_files[0])), scale)
        self.textures = [
            arcade.load_texture(os.path.join(textures_path, filename))
            for filename in texture_files
        ]

        # Анимационные параметры
        self.frame_index = 0
        self.timer = 0.0
        self.frame_delay = frame_delay

    def animate(self, delta_time: float = 1 / 60):
        """Обновить кадр анимации (FPS-независимо)."""
        self.timer += delta_time
        if self.timer >= self.frame_delay:
            self.timer -= self.frame_delay
            self.frame_index = (self.frame_index + 1) % len(self.textures)
            self.texture = self.textures[self.frame_index]
            return True
        return False

    def set_default(self):
        """Вернуть анимацию в исходное состояние."""
        if self.frame_index != 0:
            self.frame_index = 0
            self.timer = 0.0
            self.texture = self.textures[0]
            return True
        return False