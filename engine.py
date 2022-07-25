from gl import Renderer, color, V2

width = 500
height = 500

rend = Renderer()

rend.glCreateWindow(width, height)
rend.glViewport(int(width / 4),
                int(height / 4),
                int(50),
                int(50))

# # rend.glClearColor(0,0.5,0)
# # rend.glClear()
rend.glClearViewport(color(0.5,0,0))

# rend.glViewport(int(width / 4), int(height / 4), 25, 25)

# rend.glClearViewport(color(0,0.5,0))

#rend.glVPoint(0,0)


P1 = [V2(165, 380), V2(185, 360), V2(180, 330), V2(207, 345), V2(233, 330), V2(230, 360), V2(250, 380), V2(220, 385), V2(205, 410), V2(193, 383)]
P2 = [V2(321, 335), V2(288, 286), V2(339, 251), V2(374, 302)]
P3 = [V2(377, 249), V2(411, 197), V2(436, 249)]

def drawPol(poligonos):
    for i in range(len(poligonos)):
        rend.glLine(poligonos[i], poligonos[(i + 1) % len(poligonos)])

drawPol(P1)
rend.glFillPoly(P1)

rend.glFinish("triangulo.bmp")