import arcade

def get_wall_list(wall_obj_list: list):
    wall_list = arcade.SpriteList(use_spatial_hash=True)
    for obj in wall_obj_list:
        if not obj.shape or len(obj.shape) < 2:
            continue

        xs, ys = zip(*obj.shape)
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        width = int(max_x - min_x)
        height = int(max_y - min_y)

        wall = arcade.SpriteSolidColor(
            width,
            height,
            min_x + width / 2,
            min_y + height / 2,
            arcade.color.TRANSPARENT_BLACK,
        )
        wall_list.append(wall)

    return wall_list