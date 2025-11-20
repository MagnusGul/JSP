import arcade

def get_surface_type(character, footstep_zones) -> str:
    """Определяем тип поверхности под ногами."""
    zones = arcade.check_for_collision_with_list(character, footstep_zones)
    return zones[0].sound_type if zones else "default"