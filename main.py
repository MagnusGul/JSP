import arcade
from game.menu.MainView import MainMenuView

# === Константы ===
SCREEN_TITLE = "Heist Prototype"

if __name__ == "__main__":
    window = arcade.Window(title=SCREEN_TITLE, fullscreen=True, resizable=True, vsync=True)
    window.show_view(MainMenuView())
    arcade.run()
