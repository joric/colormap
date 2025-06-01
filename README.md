# ColorMap

Interactive RGB color map

## Brand Colors

_The biggest collection of official brand color codes around._

* https://brandcolors.net

## Color Navigation Maps

_Images Containing All Colors, and Their Limitations. This project originated from Bruce Lindbloom's "An RGB Image Containing All Possible Colors", which takes the RGB B value._

* http://www.kindofdoon.com/2020/05/color-navigation-map.html

### Bruce Lindbloom

* http://www.brucelindbloom.com/index.html?RGB16Million.html

```python
def getPixelColor(x, y):
    r = x % 256
    g = y % 256
    b = x // 256 + (y // 256) * 16
    return r, g, b
```

### AllRGB

_The objective of allRGB is simple: To create images with one pixel for every RGB color (16,777,216); not one color missing, and not one color twice._

* Web: https://allrgb.com
* Source code: https://github.com/allrgb

## References

* https://theodorelindsey.io/blog/2016/12/28/ProceduralAllColorImages.html
* https://en.wikipedia.org/wiki/Wikipedia:Featured_picture_candidates/All_24-bit_RGB_colors

