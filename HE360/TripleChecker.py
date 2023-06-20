import json
import csv
import os

ais_file = open('./HE-CSVs/ais-data.csv')
other_file = open('./HE-CSVs/other-data.csv')
planet_file = open('./Planet/matched-data.csv')

matched_file = open('./trip-matched-data.csv', 'w')
matched_writer = csv.writer(matched_file)

ais_reader = csv.reader(ais_file)
other_reader = csv.reader(other_file)
planet_reader = csv.reader(planet_file)

headers = []
headers.append(next(ais_reader))
headers.append(next(other_reader))
headers.append(next(planet_reader))

matched_writer.writerow(["id", "x", "y", "date", "time"])

ais_data, other_data, planet_data = [line for line in ais_reader], [line for line in other_reader], [line for line in planet_reader]


for ais_dp in ais_data:
	for other_dp in other_data:
		for planet_dp in planet_data:
			if planet_dp[3] == ais_dp[3] and ais_dp[3] == other_dp[3]:
				if round(float(planet_dp[1]), 2) == round(float(ais_dp[1]), 2) and round(float(planet_dp[1]), 2) == round(float(other_dp[1]), 2):
					if round(float(planet_dp[2]), 2) == round(float(ais_dp[2]), 2) and round(float(planet_dp[2]), 2) == round(float(other_dp[2]), 2):
						if planet_dp[0] != '' or planet_dp[0] != ' ' or planet_dp[0] is not None:
							if planet_dp[0] == other_dp[0] and planet_dp[0] == ais_dp[0]:
								matched_writer.writerow(other_dp)
								print("Ship Found!", other_dp[0])
								print("Mission failed!")
						else:
							if ais_dp[0] == other_dp[0]:
								matched_writer.writerow(other_dp)
								print("Ship Found!", other_dp[0])

matched_file.close()



