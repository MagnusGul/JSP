import arcade
from game.menu.widgets.button import Button

def animate_exit(self, delta_time: float):
    """Анимация ухода кнопок и логотипа при старте игры."""
    offset = self.UI_SPEED * delta_time

    # Двигаем UI и кнопки вверх
    for sprite in [*self.scene["ui"], *self.scene["buttons"]]:
        sprite.center_y += offset
        if sprite.bottom > self.window.height:
            sprite.kill()

    # Логотип уходит влево
    for logo in self.scene["logo"]:
        logo.center_x -= self.LOGO_SPEED * delta_time * 2.5
        if logo.right < 0:
            logo.kill()


def fade_to_black(self):
    """Постепенное затемнение перед загрузкой игры."""
    backstage = self.scene["backstage"][0]
    if not backstage:
        return

    r, g, b, a = backstage.color
    a = min(a + 2, 255)
    backstage.color = (r, g, b, a)
    for player in self.players:
        player.volume = player.volume - a * player.volume / 255
    if a >= 255:
        self.loading_view.setup("dacha.tmx")
        self.window.show_view(self.loading_view)
        self.loading_done = False  # предотвратить повтор

def create_background(self, bg_choice):
    """Фон меню."""
    if bg_choice == 1:
        self.bg = arcade.Sprite("assets/menu/background.jpg")
    else:
        self.bg = arcade.Sprite("assets/menu/dacha.jpg")
    self.bg.center_x = self.window.width / 2
    self.bg.center_y = self.window.height / 2
    self.scene.add_sprite("background", self.bg)

def create_players(self, bg_choice):
    if bg_choice == 1:
        music = arcade.load_sound("assets/menu/menu_school.mp3")
        bg = arcade.load_sound("assets/menu/menu_school_bg.mp3")
    else:
        music = arcade.load_sound("assets/menu/menu_dacha.mp3")
        bg = arcade.load_sound("assets/menu/menu_dacha_bg.mp3")
    self.music_player = arcade.play_sound(music, loop=True, volume=0.1)
    self.bg_player = arcade.play_sound(bg, loop=True, volume=0.1)
    self.players = [self.music_player, self.bg_player]

def create_menu_overlay(self):
    """Полупрозрачный прямоугольник под кнопками."""
    overlay = arcade.SpriteSolidColor(
        self.window.width,
        self.MENU_HEIGHT,
        self.window.width / 2,
        self.window.height - self.MENU_HEIGHT / 2,
        (0, 0, 0, 100)
    )
    self.scene.add_sprite("ui", overlay)

def create_logo(self):
    """Логотип игры."""
    logo = arcade.Sprite("assets/menu/logo.png")
    logo.left = 10
    logo.bottom = 10
    self.scene.add_sprite("logo", logo)

def create_buttons(self):
    """Кнопки главного меню."""
    self.start_button = Button(
        "assets/buttons/start",
        self.window.width - 200,
        self.window.height - 45,
        on_click=self.start_game
    )
    self.settings_button = Button(
        "assets/buttons/settings",
        self.window.width - 400,
        self.window.height - 45
    )
    self.scene.add_sprite("buttons", self.start_button)
    self.scene.add_sprite("buttons", self.settings_button)

def create_backstage_layer(self):
    """Прозрачный слой для плавного затемнения при переходе."""
    backstage = arcade.SpriteSolidColor(
        self.window.width,
        self.window.height,
        self.window.width / 2,
        self.window.height / 2,
        (0, 0, 0, 0)
    )
    self.scene.add_sprite("backstage", backstage)

import time
import math

def animate_background(self):
    """Плавное движение фона по синусоиде."""
    elapsed = (time.time() - self.start_time) * 0.5
    amplitude_x = 15
    amplitude_y = 10

    self.bg.center_x = (
            self.window.width / 2 + math.sin(elapsed * 2) * amplitude_x
    )
    self.bg.center_y = (
            self.window.height / 2 + math.sin(elapsed * 2) * math.cos(elapsed * 2) * amplitude_y
    )