from gl import Renderer, color, V3, V2

width = 960
height = 520

rend = Renderer(width, height)

rend.glLoadModel("fox.obj",
                 translate = V3(width/2, height/2, 0),
                 scale = V3(200,200,200))

rend.glFinish("output.bmp")