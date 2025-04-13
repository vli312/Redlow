import pandas as pd
from django.core.management.base import BaseCommand
from page.models import Region, Prices, MapLocation
import googlemaps
import time

# Initialize Google Maps client
gmaps = googlemaps.Client(key='AIzaSyBO6zsn6om2Xnrjwe_Bw_9Nl3WtUbSn5ws')

class Command(BaseCommand):
    help = 'Populates the database with region and price data from the Zillow dataset'

    def handle(self, *args, **kwargs):
        # Load the Excel file
        file_path = 'Base_Data/zillow_base_data.xlsx'  # Update to the correct path
        excel_data = pd.read_excel(file_path, sheet_name='ZIP')

        # Extract ZIP data
        zip_data = excel_data[['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'CountyName', 'Metro']]

        # Extract date columns (this dynamically selects all columns with dates)
        date_columns = [col for col in excel_data.columns if isinstance(col, pd.Timestamp)]

        # Iterate over rows to extract region data and insert it
        for _, row in zip_data.iterrows():
            region_name = row['RegionName']
            region_id = row['RegionID']
            state = row['StateName']
            metro = row['Metro']
            county = row['CountyName']
            size_rank = row['SizeRank']

            # Create Region object
            region, created = Region.objects.get_or_create(
                region_id=region_id,
                region_name=region_name,
                state=state,
                metro=metro,
                county=county,
                size_rank=size_rank,
                region_type='zip'  # or 'neighbourhood', depending on your data
            )

            # Fetch latitude and longitude using Google Maps API
            location = self.create_map_location(region_name, county, metro)
            if location:
                region.location = location
                region.save()

            # Insert Prices data dynamically for each date column
            for date in date_columns:
                home_value = row[date]  # Price for the region on the specific date
                Prices.objects.create(
                    region=region,
                    date=date,
                    home_value=home_value,
                    latitude=location.latitude,  # Store latitude
                    longitude=location.longitude  # Store longitude
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with region and price data'))

    def create_map_location(self, region_name, county, metro):
        """
        This function is used to generate geographic data (latitude, longitude) for each region.
        It uses the Google Maps API to fetch the actual data.
        """
        address = f"{region_name}, {county}, {metro}"
        lat, lon = self.get_lat_lon(address)
        if lat and lon:
            # Create and store the location in the MapLocation model
            return MapLocation.objects.create(latitude=lat, longitude=lon)
        return None

    def get_lat_lon(self, address):
        """
        This function uses the Google Maps API to get the latitude and longitude from the address.
        It retries the request in case of rate limiting or failure.
        """
        try:
            geocode_result = gmaps.geocode(address)

            if geocode_result:
                lat = geocode_result[0]['geometry']['location']['lat']
                lon = geocode_result[0]['geometry']['location']['lng']
                return lat, lon
            else:
                self.stdout.write(self.style.WARNING(f"Geocoding failed for address: {address}"))
                return None, None
        except googlemaps.exceptions.Timeout:
            self.stdout.write(self.style.WARNING(f"Timeout while geocoding address: {address}. Retrying..."))
            time.sleep(1)  # Wait for 1 second before retrying
            return self.get_lat_lon(address)
        except googlemaps.exceptions.ApiError as e:
            self.stdout.write(self.style.ERROR(f"API error while geocoding address: {address} - {e}"))
            return None, None
