import json
import numpy as np
import matplotlib.pyplot as plt

json_file = open("./geojson.json")
geo_features = json.load(json_file)["features"]
write_file = open("./jsoninformation.txt", "w")

months = {
	"01": "January",
	"02": "February",
	"03": "March",
	"04": "April",
	"05": "May",
	"06": "June",
	"07": "July",
	"08": "August",
	"09": "September",
	"10": "October",
	"11": "November",
	"12": "December",
}

information = {}
for feature in geo_features:
	timestamp = feature["properties"]["timestamp"]
	timestamp_array = timestamp.split("T")
	timestamp_array[0] = timestamp_array[0].split("-")
	# information[timestamp_array[0][2] + ' ' + months[timestamp_array[0][1]] +  ' ' + timestamp_array[0][0]][timestamp_array[1]] = feature["geometry"]["coordinates"]
	date = timestamp_array[0][2] + ' ' + months[timestamp_array[0][1]] +  ' ' + timestamp_array[0][0]
	if date not in information:
		information[date] = {}
	if timestamp_array[1][-1] == "Z":
		timestamp_array[1] = timestamp_array[1][0:len(timestamp_array[1])-1] + " UTC"
	else:
		timestamp_array[1] = timestamp_array[1][0:len(timestamp_array[1])-6] + " UTC" + timestamp_array[1][len(timestamp_array[1])-6:]
	information[date][timestamp_array[1]] = feature["geometry"]["coordinates"]

	# MARK: TIMESTAMP FINDER
	try: 
		feature["properties"]["timestamp"]
		print("timestamp found!")
	except:
		pass



json_info = json.dumps(information, indent=2)
write_file.write(json_info)
