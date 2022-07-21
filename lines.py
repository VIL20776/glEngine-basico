from gl import Renderer, color, V2

width = 500
height = 500

rend = Renderer()

rend.glCreateWindow(width, height)

def drawPol(poligonos):
    for i in range(len(poligonos)):
        rend.glLine(poligonos[i], poligonos[(i + 1) % len(poligonos)])

P1 = [V2(150, 100),V2(250, 400), V2(350, 100)]
P2 = [V2(150, 100),V2(150, 400), V2(350, 400), V2(350, 100)]
P3 = [V2(150, 100),V2(100, 400), V2(250, 450), V2(400, 400), V2(350, 100)]
P4 = [V2(100, 100),V2(100, 400), V2(250, 450), V2(400, 400), V2(400, 100), V2(250, 50)]
P5 = [V2(100, 100),V2(100, 400), V2(250, 450), V2(500, 500),V2(400, 400), V2(400, 100), V2(250, 50)]

drawPol(P1)
rend.glFinish("fig1.bmp")

rend.glClear()

drawPol(P2)
rend.glFinish("fig2.bmp")

rend.glClear()

drawPol(P3)
rend.glFinish("fig3.bmp")

rend.glClear()

drawPol(P4)
rend.glFinish("fig4.bmp")

rend.glClear()

drawPol(P5)
rend.glFinish("fig5.bmp")

rend.glClear()
