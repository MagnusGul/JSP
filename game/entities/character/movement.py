import arcade

def move_with_collisions(character, walls: arcade.SpriteList):
    """Движение по осям с проверкой коллизий."""
    target_dx, target_dy = character.change_x, character.change_y
    if target_dx and target_dy:
        target_dx *= 0.7
        target_dy *= 0.7

    def approach(current: float, target: float, rate: float) -> float:
        """Плавно приближаем current к target."""
        if current < target:
            return min(target, current + rate)
        if current > target:
            return max(target, current - rate)
        return current

    character.velocity_x = approach(character.velocity_x, target_dx, character.acceleration_rate)
    character.velocity_y = approach(character.velocity_y, target_dy, character.acceleration_rate)

    for attr, vel in (("center_x", character.velocity_x), ("center_y", character.velocity_y)):
        if vel:
            setattr(character, attr, getattr(character, attr) + vel)
            if arcade.check_for_collision_with_list(character, walls):
                setattr(character, attr, getattr(character, attr) - vel)
                if attr == "center_x":
                    character.velocity_x = 0
                else:
                    character.velocity_y = 0

    for part in (character.legs, character.head):
        part.center_x, part.center_y = character.center_x, character.center_y

    if abs(character.velocity_x) > 0 or abs(character.velocity_y) > 0:
        return True
    else:
        return False