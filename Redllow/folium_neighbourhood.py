import folium
from folium.plugins import MarkerCluster
import pandas as pd
import googlemaps
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env file



# Getting the Georeference dataset for zipcodes in US
gmaps = googlemaps.Client(key=os.environ['GOOGLE_MAPS_KEY'])

# Retrieve latitude and longitude for a address = 'neighbourhood, state' input
def get_neighbourhood_coords(address):
    result = gmaps.geocode(address)
    try:
        latitude, longitude = result[0]['geometry']['location']['lat'], result[0]['geometry']['location']['lng']
    except:
        latitude, longitude = 38.8951, -77.0364 # Giving DC center as default location for unassignable neighbourhoods
    return [latitude, longitude]

# Making a Zipcode mapping for DMV
df_zillow_neighbourhood = pd.read_excel(r'./Base_Data/zillow_base_data.xlsx', sheet_name='Neighbourhood')
df_dmv_neighbourhood = df_zillow_neighbourhood[['RegionName', 'State']].copy()
df_dmv_neighbourhood['Address'] = df_dmv_neighbourhood['RegionName'].str.cat(df_dmv_neighbourhood['State'], sep=', ', join='left', na_rep='-')
df_dmv_neighbourhood['Coordinates']=df_dmv_neighbourhood['Address'].apply(get_neighbourhood_coords) 

# Plotting the neighbourhoods on the Folium map
neighbourhood_popups = list(df_dmv_neighbourhood['Address'])
coords = list(df_dmv_neighbourhood['Coordinates'])

# Define the center of the DMV area (e.g., Washington, D.C.)
dmv_center = [38.8951, -77.0364]  # Latitude, Longitude

# Create a Folium map object
dmv_map = folium.Map(location=dmv_center, zoom_start=9)  # Adjust zoom_start as needed

marker_cluster = MarkerCluster( # Method 3: Cluster + Popup
    name='Neighbourhood Cluster',
    overlay=True,
    control=False,
    icon_create_function=None
)
for i in range(len(neighbourhood_popups)):
    location = coords[i]
    marker = folium.Marker(location=location)
    popup = neighbourhood_popups[i]
    folium.Popup(popup).add_to(marker)
    marker_cluster.add_child(marker)
marker_cluster.add_to(dmv_map)
folium.LayerControl().add_to(dmv_map);


#Save the map to an html file.
dmv_map.save("dmv_map_neighbourhood.html")

print("Map saved to dmv_map_neighbourhood.html")