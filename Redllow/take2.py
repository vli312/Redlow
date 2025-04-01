from gmplot import GoogleMapPlotter

# Center coordinates for the DMV region
dmv_center_lat = 38.9072
dmv_center_lng = -77.0369

# Create the map
gmap = GoogleMapPlotter(dmv_center_lat, dmv_center_lng, zoom=9, apikey="AIzaSyBO6zsn6om2Xnrjwe_Bw_9Nl3WtUbSn5ws")

# Save the map to an HTML file
gmap.draw("dmv_region_map_gmplot.html")