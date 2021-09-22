import io

from PIL import Image
from colorthief import ColorThief


# im = Image.open(f"{os.getcwd()}/images/photo_2021-07-03_20-41-55.jpg")
# with open("images/photo_2021-07-03_15-37-08.jpg", "rb") as f:
#     im = Image.open(f)
#     im.show()
# print(im.format, im.size, im.mode)

# color_thief = ColorThief(f"{os.getcwd()}/images/photo_2021-07-03_15-37-08.jpg")
# get the dominant color
# dominant_color = color_thief.get_color(quality=1)
# build a color palette
# palette = color_thief.get_palette(color_count=6)
# database.insert_row(palette, "JOANA", "CANNAN")
# print(dominant_color)
# print(palette)
# print(database.get_name(palette))


def resize(byteimage):
    img = Image.open(io.BytesIO(byteimage))
    maxsize = (30, 30)
    img.thumbnail(maxsize)
    byte_io = io.BytesIO()
    img.save(byte_io, "png")
    return byte_io
    # for f in os.listdir('images'):
    #     if f.endswith('.jpg'):
    #         i = Image.open(f'images/{f}')
    #         # fn, fext = os.path.splitext(f)
    #         i.thumbnail(maxsize, Image.ANTIALIAS)
    #         if not os.path.exists('resized'):
    #             os.mkdir('resized')
    #         i.save(f'resized/{f}')


# resize()

def extract_colors(image_path):
    color_thief = ColorThief(image_path)
    palette = color_thief.get_palette(color_count=6)
    return palette
    # for f in os.listdir('resized'):
    #     if f.endswith('.jpg'):
    #         color_thief = ColorThief(f"resized/{f}")
    #         palette = color_thief.get_palette(color_count=6)


# extract_colors()


def process_image(byteimage):
    img = resize(byteimage)
    code = extract_colors(img)
    return code
