from .functions import interp

red = (255, 150, 100)
green = (100, 255, 100)
blue = (100, 100, 255)
purple = (153, 51, 255)
white = (255, 255, 255)
black = (0, 0, 0, 0)
yellow = (255, 250, 102)


def NaturalColorMap(value):
    if value < 1 and value > 0:
        color = (
            interp(0, 255, value**0.5),
            interp(55, 0, value),
            interp(200, 0, value**2),
        )
    else:
        color = (255, 0, 0)
    return color


def GreyScaleColorMap(value):
    if value < 1 and value > 0:
        color = (
            255-value*255,
            255-value*255,
            255-value*255,
        )
    else:
        color = (0, 0, 0)
    return color
