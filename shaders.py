import random
from math import sin

def flat(render, **kwargs):

    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    triangleNormal = kwargs["triangleNormal"]

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        # P = Au + Bv + Cw
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    dirLight = render.dirLight
    intensity = (triangleNormal.x * -dirLight.x) + (triangleNormal.y * -dirLight.y) + (triangleNormal.z * -dirLight.z)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def flat_static(render, **kwargs):

    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    triangleNormal = kwargs["triangleNormal"]

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        # P = Au + Bv + Cw
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    dirLight = render.dirLight
    intensity = (triangleNormal.x * -dirLight.x) + (triangleNormal.y * -dirLight.y) + (triangleNormal.z * -dirLight.z)

    b *= intensity if random.random() > 0.5 else 0
    g *= intensity if random.random() > 0.5 else 0
    r *= intensity if random.random() > 0.5 else 0

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def flat_negative(render, **kwargs):

    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    triangleNormal = kwargs["triangleNormal"]

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        # P = Au + Bv + Cw
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    dirLight = render.dirLight
    intensity = (triangleNormal.x * -dirLight.x) + (triangleNormal.y * -dirLight.y) + (triangleNormal.z * -dirLight.z)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return (1 - r), (1 - g), (1 - b)
    else:
        return 0,0,0

def flat_old_tv_i_think(render, **kwargs):

    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    triangleNormal = kwargs["triangleNormal"]
    point = kwargs["point"]

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        # P = Au + Bv + Cw
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    dirLight = render.dirLight
    intensity = (triangleNormal.x * -dirLight.x) + (triangleNormal.y * -dirLight.y) + (triangleNormal.z * -dirLight.z)

    b *= intensity 
    g *= intensity 
    r *= intensity 

    if intensity > 0:
        if (point[1] % 2 != 0):
            return (1 - r), (1 - g), (1 - b)
        return r, g, b
    else:
        return 0,0,0

def flat_poly(render, **kwargs):

    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    triangleNormal = kwargs["triangleNormal"]
    point = kwargs["point"]
    max = kwargs["max"]

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        # P = Au + Bv + Cw
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    dirLight = render.dirLight
    intensity = (triangleNormal.x * -dirLight.x) + (triangleNormal.y * -dirLight.y) + (triangleNormal.z * -dirLight.z)

    b *= intensity * (point[1] / max[1]) 
    g *= intensity * (point[1] / max[1])
    r *= intensity * (point[1] / max[1])

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def flat_glitch(render, **kwargs):

    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    triangleNormal = kwargs["triangleNormal"]
    point = kwargs["point"]
    max = kwargs["max"]

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        # P = Au + Bv + Cw
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    dirLight = render.dirLight
    intensity = (triangleNormal.x * -dirLight.x) + (triangleNormal.y * -dirLight.y) + (triangleNormal.z * -dirLight.z)

    b *= intensity 
    g *= intensity 
    r *= intensity 

    if intensity > 0:
        if (max[0] % 2 != 0):
            return random.random(), random.random(), random.random()
        return r, g, b
    else:
        return 0,0,0

def flat_old_tv(render, **kwargs):

    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    triangleNormal = kwargs["triangleNormal"]
    point = kwargs["point"]

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        # P = Au + Bv + Cw
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        g *= texColor[1]
        r *= texColor[0]

    dirLight = render.dirLight
    intensity = (triangleNormal.x * -dirLight.x) + (triangleNormal.y * -dirLight.y) + (triangleNormal.z * -dirLight.z)

    b *= intensity * abs(sin(point[1]))
    g *= intensity * abs(sin(point[1]))
    r *= intensity * abs(sin(point[1]))

    if intensity > 0: 
        return r, g, b
    else:
        return 0,0,0

def flat_greenles_poly(render, **kwargs):

    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs["vColor"]
    tA, tB, tC = kwargs["texCoords"]
    triangleNormal = kwargs["triangleNormal"]
    point = kwargs["point"]
    max = kwargs["max"]

    b /= 255
    r /= 255

    if render.active_texture:
        # P = Au + Bv + Cw
        tU = tA[0] * u + tB[0] * v + tC[0] * w
        tV = tA[1] * u + tB[1] * v + tC[1] * w

        texColor = render.active_texture.getColor(tU, tV)

        b *= texColor[2]
        r *= texColor[0]

    dirLight = render.dirLight
    intensity = (triangleNormal.x * -dirLight.x) + (triangleNormal.y * -dirLight.y) + (triangleNormal.z * -dirLight.z)

    b *= intensity * (point[1] / max[1])
    r *= intensity * (point[0] / max[0])

    if intensity > 0:
        return r, 0, b
    else:
        return 0,0,0

