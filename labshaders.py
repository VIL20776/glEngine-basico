from gl import Renderer, color, V3
from texture import Texture
from shaders import flat_negative, flat_static, flat_old_tv_i_think, flat_poly, flat_glitch, flat_old_tv, flat_greenles_poly

width = 960
height = 540

rotate = V3(0, 135, 0)
scale = V3(2, 2, 2)

rend = Renderer(width, height)

rend.active_texture = Texture("texture.bmp")

rend.active_shader = flat_old_tv
rend.glLoadModel("fox.obj",
                 translate = V3(width/6, height/8, 0), rotate= rotate, scale= scale)

rend.active_shader = flat_old_tv_i_think
rend.glLoadModel("fox.obj",
                 translate = V3(width/2, height/8, 0), rotate= rotate, scale= scale)

rend.active_shader = flat_poly
rend.glLoadModel("fox.obj",
                 translate = V3(width/1.25, height/9, 0), rotate= rotate, scale= scale)

rend.active_shader = flat_glitch
rend.glLoadModel("fox.obj",
                 translate = V3(width/6, height/3, 0), rotate= rotate, scale= scale)

rend.active_shader = flat_negative
rend.glLoadModel("fox.obj",
                 translate = V3(width/2, height/3, 0), rotate= rotate, scale= scale)

rend.active_shader = flat_static
rend.glLoadModel("fox.obj",
                 translate = V3(width/1.25, height/3, 0), rotate= rotate, scale= scale)

rend.glFinish("output.bmp")

