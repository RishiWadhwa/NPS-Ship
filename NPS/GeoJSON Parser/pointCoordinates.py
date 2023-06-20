import json
from scipy.spatial import Delaunay
import numpy as np
import matplotlib.pyplot as plt

# Open GeoJSON file
pointfile = open("pointCoords.json")
features = json.load(pointfile, parse_float=float)["features"]

# Move all point coordinates into points as tuples of (x, y) / (long, lat)
x,y = [],[]
for feature in features:
    if feature["geometry"]["type"] == "Point":        
        x.append(feature["geometry"]["coordinates"][0])
        y.append(feature["geometry"]["coordinates"][1])
    elif feature["geometry"]["type"] == "LineString":
        for coordinate in feature["geometry"]["coordinates"]:
            x.append(coordinate[0])
            y.append(coordinate[1])

x1,y1,x2,y2 = x[0],y[0],x[len(x)-1],y[len(y)-1]

x = np.array(x)
y = np.array(y)

coefficients = np.polyfit(x, y, 100)




plt.scatter(x, y)
plt.plot(np.linspace(min(x), max(x), 100), np.polyval(coefficients, np.linspace(min(x), max(x), 100)))
plt.xlim(x1,x2)
plt.ylim(y1,y2)

plt.show()
