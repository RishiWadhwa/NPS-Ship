import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import csv
import os
import os.path

if not os.path.isdir('./HE-CSVs'):
	os.mkdir('./HE-CSVs')

directories = Path('./').glob('*')
cur_file = ''

cur_coords = []
coord_plts = []

all_file = open('./HE-CSVs/all-data.csv', 'w')
ais_file = open('./HE-CSVs/ais-data.csv', 'w')
other_file = open('./HE-CSVs/other-data.csv', 'w')

all_writer = csv.writer(all_file)
ais_writer = csv.writer(ais_file)
other_writer = csv.writer(other_file)

all_writer.writerow(["id", "x", "y", "date", "time"])
ais_writer.writerow(["id", "x", "y", "date", "time"])
other_writer.writerow(["id", "x", "y", "date", "time"])

for directory in directories:	
	print(directory)
	for file in directory.glob('*.geojson'):
		cur_file = str(file).replace('/', '-').replace('.geojson', '')

		if "ELLIPSES" not in str(file):
			cur_mkfile = open(f'./HE-CSVs/{cur_file}-data.csv', 'w')
			writer = csv.writer(cur_mkfile)			
			writer.writerow(["id", "x", "y", "date", "time"])

			json_file = open(file)
			geo_features = json.load(json_file)["features"]

			ship_id = ""
			coords = []
			for feature in geo_features:
				coords = feature["geometry"]["coordinates"]
				cur_coords.append(feature["geometry"]["coordinates"])
				ship_id = feature["id"]
				date, time = None, None

				try:
					timestamp = feature["properties"]["received_at"]
					date, time = timestamp.split('T')
					year, month, day = date.split('-')
					date = month + ' / ' + day + ' / ' + year
					time = time[0:len(time)-1] + ' UTC'
				except:
					timestamp = None
				
				if 'AIS' in cur_file:
					ais_writer.writerow([ship_id, coords[0], coords[1], date, time])
				else:
					other_writer.writerow([ship_id, coords[0], coords[1], date, time])

				writer.writerow([ship_id, coords[0], coords[1], date, time])
				all_writer.writerow([ship_id, coords[0], coords[1], date, time])
			
			x = []
			y = []
			while type(cur_coords[0][0]) is not float:
				cur_coords = cur_coords[0]
			for coord in cur_coords:
				x.append(coord[0])
				try: 
					y.append(coord[1])
				except:
					pass

			xmin, yxmin, xmax, yxmax = min(x), y[x.index(min(x))], max(x), y[x.index(max(x))]
			ymin, xymin, ymax, xymax = min(y), x[y.index(min(y))], max(y), x[y.index(max(y))]

			x = np.array(x)
			y = np.array(y)
			cur_plt = plt.scatter(x, y, label=f'{cur_file}')
			coord_plts.append(cur_plt)

			cur_mkfile.close()			
			cur_coords = []

fig_legend = plt.figure()

for coord_plt in coord_plts:
    plt.figure(coord_plt.figure.number)
    plt.legend(loc='upper left')

    # Copy the legend from the current plot to the legend figure
    legend = plt.gca().get_legend()
    if legend:
        fig_legend.legend(handles=legend.legendHandles, labels=legend.get_texts())

    plt.legend().remove()


# # Show the legend separately
# fig_legend.savefig('legend.png')

# if os.name == 'nt':  # For Windows
#     os.startfile('legend.png')
# else:  # For macOS and Linux
#     opener = 'open' if os.sys.platform == 'darwin' else 'xdg-open'
#     os.system(f'{opener} legend.png')

plt.show()










