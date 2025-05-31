# download less file from https://brandcolors.net

import re
import json
from collections import *

features = []

colors = defaultdict(set)

for i,s in enumerate(open('brandcolors.less').read().splitlines()):
    #if i==100: break
    if m := re.search(r"@bc-([a-z0-9\-]+): #([0-9a-fA-F]+);", s):
        t,h = [m.group(1), m.group(2)]
        #print(s,t,h)
        title = ' '.join(map(str.capitalize, t.split('-')))
        color = tuple([int(h[i:i+2], 16) for i in (0, 2, 4)] if len(h)==6 else [int(h[i:i+1]*2,16) for i in (0,1,2)])
        #print(title,rgb)

        base = re.sub(r'\s\d+$', '', title)

        if color not in colors[base]:
            features.append({'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': color}, 'properties': {'title':title}})
        else:
            #print('duplicate detected', title, base)
            pass

        colors[base].add(color)


json.dump({'type': 'FeatureCollection', 'features': features}, open('../markers.json','w'), indent=2)
