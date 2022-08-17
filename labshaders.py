from gl import Renderer, color, V3, V2
from texture import Texture
from shaders import flat, flat_negative, flat_static, someting_flat

width = 960
height = 540

rend = Renderer(width, height)

rend.active_shader = someting_flat
rend.active_texture = Texture("texture.bmp")

rend.glLoadModel("fox.obj",
                 translate = V3(width/2, height/6, 0),
                 rotate = V3(0, 135, 0),
                 scale = V3(5,5,5))

rend.glFinish("output.bmp")

