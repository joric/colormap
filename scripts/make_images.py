from PIL import Image
import numpy as np
import sys

width = height = 4096
img = Image.new("RGB", (width, height))
pixels = img.load()

def make_lookup(filename):
    im1 = Image.open(filename)
    pixels = im1.load()

    filename = filename.replace('.png','.lookup.png')
    print(f'saving lookup as {filename}...')

    im2 = Image.new("RGB", (width, height))
    data = im2.load()

    for y in range(height):
        for x in range(width):
            r,g,b = pixels[x, y]
            ofs = r + g*256 + b*256*256
            data[ofs % width, ofs // height] = x*width + y

    im2.save(filename)

def morton():
    def interleave_bits8(x):
        # Interleave lower 8 bits of x with zeros, producing 24 bits spaced
        x &= 0xFF
        x = (x | (x << 16)) & 0xFF0000FF
        x = (x | (x << 8)) & 0x0F00F00F
        x = (x | (x << 4)) & 0xC30C30C3
        x = (x | (x << 2)) & 0x49249249
        return x

    def morton3D(r, g, b):
        # Interleave bits of r, g, b to get Morton code
        return (interleave_bits8(r) << 2) | (interleave_bits8(g) << 1) | interleave_bits8(b)

    # Create a list of all RGB colors with their Morton indices
    colors = []
    for r in range(256):
        sys.stderr.write(f'{r*100//256}%\r')
        for g in range(256):
            for b in range(256):
                code = morton3D(r, g, b)
                colors.append( (code, (r, g, b)) )

    print("Sorting colors by Morton order...")

    colors.sort(key=lambda x: x[0])

    print("Assigning pixels...")

    idx = 0
    for y in range(height):
        for x in range(width):
            pixels[x, y] = colors[idx][1]
            idx += 1

def hsv_sorted():
    print('allocating...')
    # Generate all unique RGB combinations
    colors = np.array([[r, g, b] for r in range(256) for g in range(256) for b in range(256)], dtype=np.uint8)

    # Sort colors to form a smooth gradient
    # Sorting by hue-lightness-saturation (HLS) tends to look pleasant
    import colorsys

    def rgb_to_hsv(color):
        return colorsys.rgb_to_hsv(color[0]/255, color[1]/255, color[2]/255)

    print('sorting...')

    # Sort using HLS values
    colors = sorted(colors, key=rgb_to_hsv)

    print('converting...')

    # Convert to flat NumPy array and reshape to image shape
    pixels = np.array(colors, dtype=np.uint8).reshape((height, width, 3))

    image = Image.fromarray(pixels, 'RGB')

def lindbloom():
    def getPixelColor(x, y):
        r = x % 256
        g = y % 256
        b = (x // 256 + (y // 256) * 16) % 256
        return (r, g, b)

    for y in range(height):
        for x in range(width):
            pixels[x, y] = getPixelColor(x, y)

generators = [
    'lindbloom',
#    'morton',
#    'hsv_sorted'
]

generate = True

for gen in generators:
    filename = f'../images/{gen}.png'

    if generate:
        print(f'generating {gen}...')
        globals()[gen]()
        print(f'saving image as {filename}...')
        img.save(filename)

    #make_lookup(filename)
