import folium
from folium.plugins import FastMarkerCluster
import pandas as pd



# Getting the Georeference dataset for zipcodes in US
df_georef_zip = pd.read_csv(r'./Base_Data/georef-united-states-of-america-zc-point.csv', sep=';')
df_georef_zip = df_georef_zip[['Zip Code', 'Geo Point']]
df_georef_zip['Latitude'] = df_georef_zip['Geo Point'].apply(lambda x: x.split(', ')[0]).astype(float)
df_georef_zip['Longitude'] = df_georef_zip['Geo Point'].apply(lambda x: x.split(', ')[1]).astype(float)
df_georef_zip.drop('Geo Point', axis=1, inplace=True)

# Making a Zipcode mapping for DMV
df_zillow_zip = pd.read_excel(r'./Base_Data/zillow_base_data.xlsx', sheet_name='ZIP')
df_dmv_zip = df_zillow_zip[['RegionName']].copy()
df_dmv_zip = pd.merge(left=df_dmv_zip, right=df_georef_zip, how='left', left_on='RegionName', right_on='Zip Code')

# Plotting the zip codes on the Folium map
#latitudes = list(df_dmv_zip['Latitude'])
#longitudes = list(df_dmv_zip['Longitude'])
zip_popups = list(df_dmv_zip['Zip Code'].astype(str))

# Define the center of the DMV area (e.g., Washington, D.C.)
dmv_center = [38.8951, -77.0364]  # Latitude, Longitude

# Create a Folium map object
dmv_map = folium.Map(location=dmv_center, zoom_start=9)  # Adjust zoom_start as needed

# Add a marker each for all zipcodes (Washington, D.C.)
#folium.Marker(dmv_center, popup="Washington, D.C.").add_to(dmv_map)
#FastMarkerCluster(data=list(zip(latitudes, longitudes)), popups=zip_popups).add_to(dmv_map)
for i in range(len(zip_popups)):
    folium.Marker([df_dmv_zip['Latitude'].iloc[i], df_dmv_zip['Longitude'].iloc[i]], popup=zip_popups[i]).add_to(dmv_map)

#Save the map to an html file.
dmv_map.save("dmv_map_zip.html")

print("Map saved to dmv_map.html")