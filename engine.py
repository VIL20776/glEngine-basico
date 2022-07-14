from gl import Renderer, color

width = 100
height = 100

rend = Renderer()

rend.glCreateWindow(width, height)
rend.glViewport(int(width / 4),
                int(height / 4),
                int(width / 4),
                int(height / 4))

rend.glClearColor(0,0.5,0)
rend.glClear()
rend.glClearViewport(color(0.5,0,0))


rend.glVPoint(0,0)

rend.glFinish("output.bmp")