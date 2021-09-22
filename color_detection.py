from functools import reduce

from PIL import Image, ImageStat

MONOCHROMATIC_MAX_VARIANCE = 0.005
COLOR = 1000
MAYBE_COLOR = 100


def detect_color_image(file):
    v = ImageStat.Stat(Image.open(file)).var
    is_monochromatic = reduce(lambda x, y: x and y < MONOCHROMATIC_MAX_VARIANCE, v, True)
    print(file, '-->\t')
    if is_monochromatic:
        print("Monochromatic image", )
    else:
        if len(v) == 3:
            maxmin = abs(max(v) - min(v))
            if maxmin > COLOR:
                print("Color\t\t\t", )
            elif maxmin > MAYBE_COLOR:
                print("Maybe color\t", )
            else:
                print("grayscale\t\t", )
            print(f"({maxmin})")
        elif len(v) == 1:
            print("Black and white")
        else:
            print("Don't know...")


# detect_color_image("images/photo_2021-07-03_15-37-36.jpg")
