import arcade
from game.core.binds import load_binds
from game.core.console import DevConsole
from game.core.camera import camera_update
from game.systems.zoom_system import get_zoom_trigger_list
from game.systems.sound_system import get_step_trigger_list
from game.systems.sound_system import SoundSystem
from game.systems.collision_system import get_wall_list
from game.entities.character.character import Character


class GameView(arcade.View):
    """Основной игровой экран игры."""

    def __init__(self):
        super().__init__()

        # --- Камеры ---
        self.camera = arcade.Camera2D(zoom=1)
        self.gui_camera = arcade.Camera2D()

        # --- Интерфейсы ---
        self.console = DevConsole(self)

        # --- Игровые объекты ---
        self.scene = None
        self.gui = arcade.Scene()
        self.tile_map = None
        self.player = None
        self.footsteps_system = None

        # --- Ввод ---
        self.mouse_pos = (0, 0)

        # --- Управление ---
        self.binds = load_binds("cfg/keybinds.json")
        self.footsteps_system = SoundSystem()
    # ======================================================
    # =                   НАСТРОЙКА МИРА                  =
    # ======================================================
    def setup(self, map_name: str):
        """Подготовка карты, игрока и всех игровых элементов."""
        map_path = f"assets/maps/{map_name}"

        # --- 1. Загрузка карты и сцены ---
        self.tile_map = arcade.load_tilemap(map_path, scaling=1)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        # --- 2. Генерация коллизий и зон звуков шагов ---

        walls = get_wall_list(self.tile_map.object_lists.get("walls", []))
        footsteps = get_step_trigger_list(self.tile_map.object_lists.get("footstep_zones", []))
        zooms = get_zoom_trigger_list(self.tile_map.object_lists.get("zoom", []))
        self.scene.add_sprite_list("walls", use_spatial_hash=True, sprite_list=walls)
        self.scene.add_sprite_list("footstep_zones", sprite_list=footsteps)
        self.scene.add_sprite_list("zooms", sprite_list=zooms)

        # --- 3. Создание игрока ---
        spawn_points = self.tile_map.object_lists.get("spawnpoint", [])
        if not spawn_points:
            raise ValueError("На карте отсутствует слой 'spawnpoint' с точкой спавна!")

        spawn_x, spawn_y = spawn_points[0].shape
        self.player = Character("assets/characters/marsel")
        self.player.position = (spawn_x, spawn_y)



        # Добавляем все части персонажа в сцену
        player_sprite_list = arcade.SpriteList(True)
        for part in (self.player.legs, self.player, self.player.head):
            player_sprite_list.append(part)
        self.scene.add_sprite_list_before("Player", sprite_list=player_sprite_list, before="roofs")


        self.gui.add_sprite("backstage",
                              arcade.SpriteSolidColor(self.window.width, self.window.height, self.window.width / 2,
                                                      self.window.height / 2, (0, 0, 0, 255)))
        # --- 4. Инициализация систем ---

    # ======================================================
    # =                      ОТРИСОВКА                     =
    # ======================================================
    def on_draw(self):
        """Отрисовка сцены и интерфейса."""
        self.clear()

        # --- Игровая сцена ---
        with self.camera.activate():
            self.scene.draw()

        # --- HUD и консоль ---
        with self.gui_camera.activate():
            arcade.draw_text("Heist Game Prototype", 10, 10, arcade.color.WHITE, 18)
            self.console.draw()
            try:
                if self.gui["backstage"][0]:
                    sprite = self.gui["backstage"][0]
                    r, g, b, a = sprite.color
                    a = max(0, a - 2)  # постепенно увеличиваем прозрачность
                    sprite.color = (r, g, b, a)
                    if a <= 0:
                        self.gui["backstage"][0].kill()
            except IndexError:
                pass
            self.gui.draw()

    # ======================================================
    # =                      ЛОГИКА                        =
    # ======================================================
    def on_update(self, delta_time: float):
        """Обновление состояния игры."""
        if not self.player:
            return

        self.player.cupdate(
            walls=self.scene["walls"],
            mouse_pos=self.mouse_pos,
            window_size=(self.window.width, self.window.height),
            camera=self.camera,
            footstep_zones=self.scene["footstep_zones"],
            footstep_system=self.footsteps_system,
        )

        camera_update(
            self.camera,
            self.window,
            self.mouse_pos,
            self.player.position,
            self.player.aiming,
        )

        for roof in self.scene["roofs"]:
            if arcade.check_for_collision(self.player, roof):
                roof: arcade.Sprite
                roof.alpha -= 10 if roof.alpha > 0 else 0
            else:
                if roof.alpha < 255:
                    roof.alpha += 10 if roof.alpha < 255 else 255

        for zoom in self.scene["zooms"]:
            def lerp(a, b, t):
                return a + (b - a) * t
            if arcade.check_for_collision(self.player, zoom):
                self.camera.zoom = lerp(self.camera.zoom, zoom.zoom, 0.1)
            else:
                self.camera.zoom = lerp(self.camera.zoom, 1, 0.1)
    # ======================================================
    # =                     УПРАВЛЕНИЕ                     =
    # ======================================================
    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш."""
        if key in self.binds and self.binds[key].on_press:
            for command in self.binds[key].on_press:
                self.console.execute(command)

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш."""
        if key in self.binds and self.binds[key].on_release:
            for command in self.binds[key].on_release:
                self.console.execute(command)

    def on_text(self, text):
        """Обработка текстового ввода."""
        self.console.on_text(text)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = (x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.player.aiming = True

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.player.aiming = False