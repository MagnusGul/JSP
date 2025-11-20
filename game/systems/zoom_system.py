import arcade


class ZoomTrigger(arcade.SpriteSolidColor):
    def __init__(self, width, height, center_x=0, center_y=0, zoom_k = 1):
        super().__init__(width, height, center_x, center_y, arcade.color.TRANSPARENT_BLACK)

        self.zoom = zoom_k


def get_zoom_trigger_list(obj_list):
    zoom_list = arcade.SpriteList(use_spatial_hash=True)
    for obj in obj_list:
        xs = [p[0] for p in obj.shape]
        ys = [p[1] for p in obj.shape]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        zoom_trig = ZoomTrigger(max_x - min_x, max_y - min_y, (min_x + max_x) / 2, (min_y + max_y) / 2,
                         obj.properties.get("zoom", "default"))
        zoom_list.append(zoom_trig)
    return zoom_list