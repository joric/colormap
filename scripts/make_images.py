from PIL import Image
import numpy as np
import sys
import colorsys

def make_lookup(filename):
    im1 = Image.open(filename)
    pixels = im1.load()

    filename = filename.replace('.png','.lookup.png')
    print(f'saving lookup as {filename}...')

    im2 = Image.new("RGB", (im1.width, im1.height))
    data = im2.load()

    for y in range(height):
        for x in range(width):
            r,g,b = pixels[x, y]
            ofs = r + g*256 + b*256*256
            data[ofs % width, ofs // height] = x*width + y

    im2.save(filename)

def morton():
    width = height = 4096
    img = Image.new("RGB", (width, height))
    pixels = img.load()

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

    return img

def hsv_sorted():
    print('allocating...')
    # Generate all unique RGB combinations
    colors = np.array([[r, g, b] for r in range(256) for g in range(256) for b in range(256)], dtype=np.uint8)

    # Sort colors to form a smooth gradient
    # Sorting by hue-lightness-saturation (HLS) tends to look pleasant

    def rgb_to_hsv(color):
        return colorsys.rgb_to_hsv(color[0]/255, color[1]/255, color[2]/255)

    print('sorting...')

    # Sort using HLS values
    colors = sorted(colors, key=rgb_to_hsv)

    print('converting...')

    # Convert to flat NumPy array and reshape to image shape
    pixels = np.array(colors, dtype=np.uint8).reshape((height, width, 3))

    return Image.fromarray(pixels, 'RGB')

def lindbloom(size=4096):
    width = height = size
    img = Image.new("RGB", (width, height))
    pixels = img.load()

    def getPixelColor(x, y):
        r = x % 256
        g = y % 256
        b = (x // 256 + (y // 256) * 16) % 256
        return (r, g, b)

    for y in range(height):
        for x in range(width):
            pixels[x, y] = getPixelColor(x, y)

    return img

def hsv(size=4096):
    x = np.linspace(0, 1, size, dtype=np.float32)
    y = np.linspace(0, 1, size, dtype=np.float32)
    xx, yy = np.meshgrid(x, y)
    
    # Hue: 0° to 360° (left to right)
    h = xx
    
    # Saturation: 
    # - 1.0 (full color) at middle (y=0.5)
    # - 0.0 (white) at top (y=1)
    # - 0.0 (black) at bottom (y=0)
    s = 4 * yy * (1 - yy)  # Smooth parabola (peaks at y=0.5)
    
    # Value: 
    # - 0.0 (black) at bottom (y=0)
    # - 1.0 (bright) from middle to top
    v = np.minimum(2 * yy, 1)  # Linear until y=0.5, then 1.0
    
    # Convert HSV to RGB
    rgb = np.zeros((size, size, 3), dtype=np.float32)
    for i in range(size):
        for j in range(size):
            rgb[i, j] = colorsys.hsv_to_rgb(h[i, j], s[i, j], v[i, j])
    
    # Apply gamma correction for better perceptual smoothness
    rgb = np.clip(rgb, 0, 1)
    rgb = (rgb ** (1/2.2)) * 255  # sRGB gamma correction
    rgb = rgb.astype(np.uint8)
    
    return Image.fromarray(rgb)

generators = [
#    'lindbloom',
#    'morton',
#    'hsv_sorted'
    'hsv',
]

generate = True

for gen in generators:
    filename = f'../images/{gen}.png'

    if generate:
        print(f'generating {gen}...')
        img = globals()[gen]()
        print(f'saving image as {filename}...')
        img.save(filename)

    #make_lookup(filename)
