import arcade
import os

class Button(arcade.Sprite):
    def __init__(self, textures, center_x=0, center_y=0, scale=1.0,
                 on_click=None, on_hover=None):
        """
        Кнопка на основе Sprite.

        :param textures: список из 2–3 текстур:
                         [обычная, наведённая, нажатая]
        :param center_x: позиция X
        :param center_y: позиция Y
        :param scale: масштаб
        :param on_click: функция при клике
        :param on_hover: функция при наведении
        """
        textures_names = os.listdir(textures)
        textures_list = []
        for texture in textures_names:
            textures_list.append(arcade.load_texture(os.path.join(textures, texture)))
        super().__init__(path_or_texture=textures_list[0], center_x=center_x, center_y=center_y, scale=scale)
        self.textures = textures_list
        self.on_click = on_click
        self.on_hover = on_hover

        self._hovered = False
        self._pressed = False

    def check_hover(self, x, y):
        """Проверить, наведён ли курсор на кнопку"""
        hovered = self.left < x < self.right and self.bottom < y < self.top
        if hovered and not self._hovered:
            self._hovered = True
            self._set_hover_texture()
            if self.on_hover:
                self.on_hover()
        elif not hovered and self._hovered:
            self._hovered = False
            self._set_normal_texture()

    def on_press(self):
        """Вызывается при нажатии мыши на кнопку"""
        if self._hovered:
            self._pressed = True
            self._set_pressed_texture()
            if self.on_click:
                self.on_click()

    def on_release(self):
        """Вызывается при отпускании мыши"""
        self._pressed = False
        if self._hovered:
            self._set_hover_texture()
        else:
            self._set_normal_texture()

    def _set_normal_texture(self):
        if len(self.textures) > 0:
            self.texture = self.textures[0]

    def _set_hover_texture(self):
        if len(self.textures) > 1:
            self.texture = self.textures[1]
        else:
            self.texture = self.textures[0]

    def _set_pressed_texture(self):
        if len(self.textures) > 2:
            self.texture = self.textures[2]
        elif len(self.textures) > 1:
            self.texture = self.textures[1]
        else:
            self.texture = self.textures[0]
