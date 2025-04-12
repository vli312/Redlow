import folium

# Define the center of the DMV area (e.g., Washington, D.C.)
dmv_center = [38.8951, -77.0364]  # Latitude, Longitude

# Create a Folium map object
dmv_map = folium.Map(location=dmv_center, zoom_start=9)  # Adjust zoom_start as needed

# Add a marker for Washington, D.C.
folium.Marker(dmv_center, popup="Washington, D.C.").add_to(dmv_map)

#Save the map to an html file.
dmv_map.save("dmv_map.html")

print("Map saved to dmv_map.html")