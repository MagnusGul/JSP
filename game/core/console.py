import arcade


class DevConsole:
    """Простая внутренняя консоль разработчика для Arcade 3.0."""

    def __init__(self, game):
        self.game = game
        self.visible = False
        self.input_text = ""
        self.output_lines = []
        self.font_size = 18
        self.max_lines = 30

        # === Словарь команд ===
        self.commands = {
            # Управление консолью
            "console_toggle": self.toggle,
            "execute": self._execute_if_visible,
            "clear_last_sym": lambda: setattr(self, "input_text", self.input_text[:-1]),

            # Телепорт игрока
            "tp": lambda x, y: self._tp(int(x), int(y)),

            # Скорость движения игрока
            "speed": lambda value: setattr(self.game.player, "speed", float(value)),

            # Управление движением (debug)
            "+up": lambda: setattr(self.game.player, "change_y", self.game.player.speed),
            "-up": lambda: setattr(self.game.player, "change_y", 0),

            "+down": lambda: setattr(self.game.player, "change_y", -self.game.player.speed),
            "-down": lambda: setattr(self.game.player, "change_y", 0),

            "+left": lambda: setattr(self.game.player, "change_x", -self.game.player.speed),
            "-left": lambda: setattr(self.game.player, "change_x", 0),

            "+right": lambda: setattr(self.game.player, "change_x", self.game.player.speed),
            "-right": lambda: setattr(self.game.player, "change_x", 0),

            # Перезагрузка карты
            "map": lambda name: self.game.setup(f"{name}.tmx"),
        }

    # --------------------------
    #   Основные методы
    # --------------------------

    def toggle(self):
        """Показать/скрыть консоль."""
        self.visible = not self.visible

    def draw(self):
        """Рендер консоли."""
        if not self.visible:
            return

        width, height = self.game.window.width, self.game.window.height

        # Фон (Arcade 3.0: используем draw_lrbt_rectangle_filled)
        arcade.draw_lrbt_rectangle_filled(
            left=0,
            right=width,
            bottom=0,
            top=height,
            color=(0, 0, 0, 160)
        )

        # Вывод последних строк
        y = height - 80
        for line in reversed(self.output_lines[-self.max_lines:]):
            color = arcade.color.WHITE
            if line.startswith("Error:"):
                color = arcade.color.RED
            elif line.startswith("Info:"):
                color = arcade.color.LIGHT_GREEN
            arcade.draw_text(line, 10, y, color, self.font_size)
            y -= self.font_size + 6

        # Строка ввода
        arcade.draw_text(
            f"> {self.input_text}",
            10,
            height - 40,
            arcade.color.YELLOW,
            self.font_size
        )

    def on_text(self, text: str):
        """Обработка ввода символов."""
        if not self.visible:
            return
        if text == "`":
            return  # Игнорируем клавишу открытия консоли
        self.input_text += text

    def on_key_press(self, key, modifiers):
        """Обработка клавиш Enter и Backspace."""
        if not self.visible:
            return

        if key == arcade.key.ENTER:
            self.execute(self.input_text)
            self.input_text = ""
        elif key == arcade.key.BACKSPACE and self.input_text:
            self.input_text = self.input_text[:-1]

    def execute(self, command: str):
        """Выполнить команду."""
        if not command.strip():
            return

        parts = command.split()
        cmd, *args = parts

        if cmd in self.commands:
            try:
                self.commands[cmd](*args)
                self.output_lines.append(f"Info: {command}")
            except Exception as e:
                self.output_lines.append(f"Error: {e}")
        else:
            self.output_lines.append(f"Error: Unknown command '{cmd}'")

    # --------------------------
    #   Вспомогательные методы
    # --------------------------

    def _tp(self, x: int, y: int):
        """Телепорт игрока на координаты тайлов."""
        self.game.player.center_x = x * 32
        self.game.player.center_y = y * 32

    def _execute_if_visible(self):
        """Выполнить текущий ввод (если консоль открыта)."""
        if self.visible:
            self.execute(self.input_text)
            self.input_text = ""
