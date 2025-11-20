def camera_update(camera, window, looking_pos: tuple[int, int], target: tuple[int, int], looking_far: bool):
    """
    Плавная камера за игроком с смещением в сторону мыши.

    mouse_x, mouse_y — текущие координаты мыши в мировых координатах
    right_mouse_down — True, если зажата ПКМ
    """
    target_x, target_y = target
    looking_pos_x, looking_pos_y = looking_pos

    # Вектор от игрока к мыши
    k = 0.75 if looking_far else 0.5
    target_x += (looking_pos_x - window.width / 2) * k / camera.zoom
    target_y += (looking_pos_y - window.height / 2) * k / camera.zoom

    # Целевая позиция камеры = позиция игрока + смещение

    # Функция плавного перехода (lerp)
    def lerp(a, b, t):
        return a + (b - a) * t

    smooth = 0.1  # плавность
    new_x = lerp(camera.position[0], target_x, smooth)
    new_y = lerp(camera.position[1], target_y, smooth)

    # Применяем позицию камеры
    camera.position = (new_x, new_y)