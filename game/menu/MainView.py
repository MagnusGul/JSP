import random
import threading

from game.core.GameView import GameView
from game.menu.fun import *


class MainMenuView(arcade.View):
    """
    Главное меню игры, построенное на Sprite и Scene.
    Содержит анимированный фон, логотип и кнопки.
    """

    MENU_HEIGHT = 90
    LOGO_SPEED = 240  # пикселей/сек при уходе логотипа
    UI_SPEED = 200     # пикселей/сек при уходе кнопок

    def __init__(self):
        super().__init__()
        self.scene = arcade.Scene()
        self.start_time = time.time()

        # Служебные флаги
        self.is_loading = False
        self.loading_done = False
        self.loading_view = None

        # --- Создание элементов меню ---
        bg_choice = random.randint(1, 2)
        create_background(self, bg_choice)
        create_players(self, bg_choice)
        create_menu_overlay(self)
        create_logo(self)
        create_buttons(self)
        create_backstage_layer(self)

    # --------------------------
    #   Основные события
    # --------------------------

    def on_draw(self):
        """Рисуем сцену и анимированный фон."""
        self.clear()
        self.scene.draw()
        animate_background(self)

    def on_update(self, delta_time: float):
        """Анимация ухода и затемнение при загрузке."""
        if self.is_loading:
            animate_exit(self, delta_time)

        if self.loading_done:
            fade_to_black(self)

    # --------------------------
    #   Управление мышью
    # --------------------------

    def on_mouse_motion(self, x, y, dx, dy):
        for button in self.scene["buttons"]:
            button.check_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.scene["buttons"]:
            btn.on_press()

    def on_mouse_release(self, x, y, button, modifiers):
        for btn in self.scene["buttons"]:
            btn.on_release()

    def start_game(self):
        """При нажатии 'Start' запускаем фоновую загрузку."""
        if self.is_loading:
            return
        self.is_loading = True
        threading.Thread(target=self._create_view, daemon=True).start()

    def _create_view(self):
        """Создаёт объект GameView в фоне."""
        self.loading_view = GameView()
        self.loading_done = True