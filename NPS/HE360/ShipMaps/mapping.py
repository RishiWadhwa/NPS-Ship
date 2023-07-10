import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
import os
import csv
import cartopy.crs as ccrs

main_csv = open('../HE-CSVs/all-data.csv')
csv_reader = csv.reader(main_csv)
header = next(csv_reader)

comms_csv = open('../HE-CSVs/all-comms.csv')
comm_reader = csv.reader(comms_csv)
header = next(comm_reader)

matched_csv = open('../Planet/matched-data.csv')
matched_reader = csv.reader(matched_csv)
header = next(matched_reader)

matched_ids = []
for line in matched_reader:
    try:
        matched_ids.append(int(line[0]))
    except:
        pass

comms = [line for line in comm_reader]
for i in range(len(comms)):
    comms[i][0] = int(comms[i][0])

all_data = [line for line in csv_reader]

all_coords = {}
all_comms = {}

for commlink in comms:
    all_comms[commlink[0]] = [commlink[1], commlink[2]] # [freq, channel name]

for dp in all_data:
    if dp[0] not in all_coords.keys():
        all_coords[dp[0]] = []
    ar = all_coords[dp[0]]
    ar.append([dp[1], dp[2]])
    all_coords[dp[0]] = ar

def mapping_base(id):
    df = pd.read_csv("../HE-CSVs/all-data.csv", delimiter=',', skiprows=0, low_memory=False)
    geometry = [Point(xy) for xy in zip(df['x'], df['y'])]
    gdf = GeoDataFrame(df, geometry=geometry)   
    _, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.PlateCarree()})
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    gdf.plot(ax=world.plot(ax=ax), marker='', color='white', markersize=15, transform=ccrs.PlateCarree())
    plt.xlim(-180, 180)
    plt.ylim(-90,90)
    plt.scatter([-117.1300], [32.6848], color='yellow')
    plt.text(-117.1300, 32.6848, "SD Navy Base", color='yellow')
    # plt.xlabel(f"{all_comms[int(ship_id)][1]}", color='blue')
    # plt.ylabel(f"{all_comms[int(ship_id)][0]}", color='blue')

planet_ids = []
for a_id in matched_ids:
    keys = list(all_coords.keys())
    planet_ids.append(keys.index(str(a_id)) + 1)


while True:
    print(f"There are {len(all_coords.keys())} ships, please type a number from 1-{len(all_coords.keys())} to view its ship track or 0 to leave. You can type 'planet' to view the planet ID locations.")
    loopCheck = True
    ans = 0    
    while loopCheck:
        ans = input('> ')
        try:
            ans = int(ans)
            loopCheck = False
        except:
            if ans.isalpha() and ans.lower() == 'planet':
                print(f'Planet.com ID spots: {planet_ids} ')
            else:
                print('Invalid, try again.')
    if ans == 0:
        break
    else:         
        ship_id = list(all_coords.keys())[ans-1]
        mapping_base(ship_id)
        ans = 0
        big_ar = all_coords[ship_id]
        x, y = [], []
        for ar in big_ar:
            x.append(float(ar[0]))
            y.append(float(ar[1]))
        plt.scatter(x,y, color='red', transform=ccrs.PlateCarree())
        plt.text(x[0],y[0],f"Point!",color='red')
        freq = all_comms[int(ship_id)][0] if all_comms[int(ship_id)][0] != '' else '---'
        try:
            freq = float(freq) / 1000.0 # MHz to GHz
        except:
            pass
        
        plt.suptitle(f'Ship: {ship_id}\n{all_comms[int(ship_id)][1]} | {freq}GHz', fontsize=12)
        
        status = True
        if int(ship_id) not in matched_ids:
            status = False

        classification = 'Unknown'
        # X-band, S-band, iridium, GPS, VHF, L-band
        if all_comms[int(ship_id)][1] == 'X-Band RADAR':
            classification = 'Government/Military' # uncommon for civilian, commonly found in military/government applications
        elif all_comms[int(ship_id)][1] == 'S-Band RADAR':
            classification = 'Any Ships' # 
        elif all_comms[int(ship_id)][1] == 'iridium':
            classification = 'Any Ships' # initially made for civilian applications, used for military as well
        elif all_comms[int(ship_id)][1] == 'L-Band Mobile Satellite':
            classification = 'Military' # has LIMITED civilian uses 
        elif all_comms[int(ship_id)][1] == 'GPS':
            classification = 'DoD Monitored' # open to civilians THROUGH DoD
        elif all_comms[int(ship_id)][1] == 'VHF':
            classification = 'Civilian' # made FOR civilians specifically
        else:
            classification = 'Civilian'

        planet_status = 'Yes' if status else 'No'
        plt.title(f'HE360: Yes  |  Planet.com: {planet_status}\nPlanet.com: {classification}', fontsize=8, loc='right')
        print(matched_ids)
        print(ship_id)
        plt.show()
