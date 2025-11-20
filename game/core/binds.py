import arcade
import json

class Action:
    def __init__(self, on_press=None, on_release=None):
        self.on_press = on_press
        self.on_release = on_release

def load_binds(filepath: str) -> dict[int, Action]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    binds = {}
    for key_name, actions in data.items():
        key_value = getattr(arcade.key, key_name.upper(), None)
        if key_value is None:
            print(f"⚠ Неизвестная клавиша: {key_name}")
            continue

        binds[key_value] = Action(
            on_press=actions.get("on_press"),
            on_release=actions.get("on_release")
        )

    return binds
