__author__ = "Branden Hall"
__copyright__ = "Copyright 2016, Branden Hall"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "bhall@automatastudios.com"
__status__ = "Production"

import argparse
from PIL import Image

# parse out the arguments
parser = argparse.ArgumentParser(description='Convert animated GIF to arrays of bytes.')
parser.add_argument('gif', help='GIF to process')
args = parser.parse_args()

# load the image
im = Image.open(args.gif)
width, height = im.size
frame = Image.new("RGBA", im.size, (0,0,0))
next = im.convert("RGBA")
frame.paste(next, next.getbbox(), mask=next)
complete = False

while not complete:
    data = frame.convert("RGB").getdata()
    x = 0
    y = 0
    dir = 1
    result = []
    for i in range(width * height):
        result += data[(y * width) + x]

        x += dir
        if dir == 1 and x == width:
            x = width - 1
            y += 1
            dir = -1
        elif dir == -1 and x == -1:
            x = 0
            y += 1
            dir = 1

    print(result)

    try:
        im.seek(im.tell() + 1)
        im.palette.dirty = 1
        im.palette.rawmode = "RGB"
        next = im.convert("RGBA")
        frame.paste(next, next.getbbox(), mask=next)

    except EOFError:
        complete = True
