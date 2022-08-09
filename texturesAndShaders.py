from gl import Renderer, color, V3, V2
from texture import Texture
from shaders import flat, gourad

width = 960
height = 540

rend = Renderer(width, height)

rend.active_shader = flat
rend.active_texture = Texture("models/model.bmp")

rend.glLoadModel("models/model.obj",
                 translate = V3(width/2, height/2, 0),
                 rotate = V3(0, 180, 0), 
                 scale = V3(200,200,200))

rend.glFinish("output.bmp")

