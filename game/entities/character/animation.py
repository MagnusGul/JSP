import math
import arcade

# --- Анимация ходьбы ---
def apply_camera_shake(character, camera):
    """Добавляем лёгкую тряску камеры при ходьбе."""
    character.walk_cycle_time += 1 / 60
    amplitude, frequency = 1.0, 5.0
    offset_y = math.sin(character.walk_cycle_time * frequency) * amplitude
    offset_x = math.cos(character.walk_cycle_time * frequency * 0.5) * amplitude * 0.3
    camera.position = (
        camera.position[0] + offset_x,
        camera.position[1] + offset_y,
    )

def animate(character, surface_type, camera, footstep_system):
    if character.moving:
        character.last_move_angle = 90 - math.degrees(math.atan2(character.velocity_y, character.velocity_x))
        apply_camera_shake(character, camera)
        character.legs.animate()

        if character.animate() and character.legs.frame_index == 2:
            footstep_system.play_step(surface_type, (camera.position.x, camera.position.y), character.position)
    else:
        if character.legs.set_default():
            footstep_system.play_step(surface_type, (camera.position.x, camera.position.y), character.position)
        character.set_default()

def update_rotation(
    player,
    mouse_pos: tuple[int, int],
    window_size: tuple[int, int],
    camera: arcade.Camera2D,
    walls: arcade.SpriteList,
):
    """Отвечает за плавный поворот головы и тела."""
    mouse_x, mouse_y = mouse_pos
    window_width, window_height = window_size
    old_angle, old_head_angle = player.angle, player.head.angle

    # === 1. Вычисляем угол к мыши ===
    mouse_world_x = mouse_x - window_width / 2 + camera.position[0] * camera.zoom
    mouse_world_y = mouse_y - window_height / 2 + camera.position[1] * camera.zoom
    dx = mouse_world_x - player.center_x * camera.zoom
    dy = mouse_world_y - player.center_y * camera.zoom
    target_angle = 90 - math.degrees(math.atan2(dy, dx))

    # === 2. Плавный поворот головы ===
    angle_diff = (target_angle - player.head.angle + 540) % 360 - 180
    if abs(angle_diff) < player.rotation_speed:
        player.head.angle = target_angle
    else:
        player.head.angle += player.rotation_speed * (1 if angle_diff > 0 else -1)

    # === 3. Поворот тела, если голова сильно ушла ===
    body_diff = (player.head.angle - player.angle + 540) % 360 - 180
    if abs(body_diff) > player.body_follow_angle_threshold:
        move_body = (
            body_diff - player.body_follow_angle_threshold * (1 if body_diff > 0 else -1)
            if abs(body_diff) - player.body_follow_angle_threshold < player.body_follow_speed
            else player.body_follow_speed * (1 if body_diff > 0 else -1)
        )
        player.angle += move_body

    # === 4. Ноги следуют за направлением движения ===
    if abs(player.head.angle - player.last_move_angle) > 90:
        player.last_move_angle -= 180
    player.legs.angle = player.last_move_angle

    # === 5. Проверка коллизий при повороте ===
    if arcade.check_for_collision_with_list(player, walls):
        player.angle = old_angle
        if abs(body_diff) > player.body_follow_angle_threshold:
            player.head.angle = old_head_angle