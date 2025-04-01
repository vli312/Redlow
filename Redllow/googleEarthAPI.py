import googlemaps
import os
import requests

def get_dmv_map(api_key, location, zoom=10, maptype="roadmap", size=[600,400]):
    try:
        gmaps = googlemaps.Client(key=api_key)
        static_map_url = gmaps.static_map(center=location, zoom=zoom, size=size, maptype=maptype)
        static_map_url_string = str(static_map_url) # added line.
        response = requests.get(static_map_url_string)
        response.raise_for_status()
        return response.content

    except googlemaps.exceptions.ApiError as e:
        print(f"Google Maps API Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def save_map_to_file(map_data, filename="dmv_map.png"):
    if map_data:
        with open(filename, "wb") as f:
            f.write(map_data)
        print(f"Map saved to {filename}")

if __name__ == "__main__":
    #key = os.environ.get("GOOGLE_MAPS_API_KEY")
    api_key = 'AIzaSyBO6zsn6om2Xnrjwe_Bw_9Nl3WtUbSn5ws'

    if not api_key:
        print("Error: Google Maps API key not found.")
    else:
        dmv_map = get_dmv_map(api_key, location="Washington, DC")
        save_map_to_file(dmv_map)

        satellite_map = get_dmv_map(api_key, location="Arlington, VA", zoom=12, maptype="satellite", size=[600,400])
        save_map_to_file(satellite_map, "arlington_satellite.png")

        terrain_map = get_dmv_map(api_key, location="Rockville, MD", zoom=11, maptype="terrain", size=[600,400])
        save_map_to_file(terrain_map, "rockville_terrain.png")