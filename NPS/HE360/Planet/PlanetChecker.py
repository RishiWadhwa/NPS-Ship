import json
import os
import requests
import csv

all_file = open('../HE-CSVs/all-data.csv', 'r')
reader = csv.reader(all_file)

header_formatting = next(reader)

all_data = []
for row in reader:
	all_data.append(row)
all_file.close()

planet_json = open('planetjson.json')
planet_data = json.load(planet_json)

all_planet_data = []

for feature in planet_data["features"]:
	# timestamp
	ts = feature["properties"]["observed"]
	date, time = ts.split('T')
	year, month, day = date.split('-')
	date = month + ' / ' + day + ' / ' + year
	time = time[0:len(time)-1] + ' UTC'

	# center point
	topL, topR, bottomL, bottomR = feature["geometry"]["coordinates"][0][0], feature["geometry"]["coordinates"][0][1], feature["geometry"]["coordinates"][0][2], feature["geometry"]["coordinates"][0][3]
	midX, midY = (topR[0] + topL[0])/2, (topR[1] + bottomR[1])/2
	ship_id = None
	all_planet_data.append([ship_id, midX, midY, date, time])

ship_found = False

for i in range(len(all_planet_data)):
	planet_dp = all_planet_data[i]
	for he_dp in all_data:
		if he_dp[3] == planet_dp[3]:
			if round(float(he_dp[1]), 2) == round(planet_dp[1],2) and round(float(he_dp[2]), 2) == round(planet_dp[2],2):
				all_planet_data[i][0] = he_dp[0]
				print("Ship found! ", str(he_dp[0]))
				ship_found = True

if not ship_found:
	print("No ship matches up!")

matched_data = open('./matched-data.csv', 'w')
writer = csv.writer(matched_data)
writer.writerow(header_formatting)

for dp in all_planet_data:
	writer.writerow(dp)

matched_data.close()

