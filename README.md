# ColorMap

_The objective of allRGB is simple: To create images with one pixel for every RGB color (16,777,216); not one color missing, and not one color twice._


Images Containing All Colors, and Their Limitations

This project originated from Bruce Lindbloom's "An RGB Image Containing All Possible Colors", which takes the RGB B value
like a "page" index and creates 256 sub-images for each possible value.

Bruce Lindbloom's An RGB Image Containing All Possible Colors.

* http://www.brucelindbloom.com/downloads/RGB16Million.png
* http://www.brucelindbloom.com (formulas)


```python
def getPixelColor(x, y):
    r = x % 256
    g = y % 256
    b = x // 256 + (y // 256) * 16
    return r, g, b
```


## References

* https://brandcolors.net
* https://allrgb.com
* https://github.com/allrgb
* http://www.kindofdoon.com/2020/06/visualizing-color-space-in-2d.html
* http://www.kindofdoon.com/2020/05/color-navigation-map.html
* https://github.com/JoaoCostaIFG/allRGB
* https://theodorelindsey.io/blog/2016/12/28/ProceduralAllColorImages.html
