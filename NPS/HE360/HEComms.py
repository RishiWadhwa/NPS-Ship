import csv
import os
import json
import numpy as np
import os.path
from pathlib import Path

directories = Path('./').glob('*')
cur_file = ''

all_file = open('./HE-CSVs/all-comms.csv', 'w')
all_writer = csv.writer(all_file)

all_writer.writerow(["id", "freq", "comm"])
all_comms = []

for directory in directories:
	for file in directory.glob('*.geojson'):
		json_file = open(file)
		geo_features = json.load(json_file)["features"]

		for feature in geo_features:
			freq = None
			try:
				freq = feature["properties"]["frequency"]
			except:
				pass

			comm_channel = None
			try:
				comm_channel = feature["properties"]["soi"]
			except:
				pass

			curr_comms = [feature["id"], freq, comm_channel]
			if curr_comms not in all_comms:
				all_comms.append(curr_comms)

for comm in all_comms:
	all_writer.writerow(comm)