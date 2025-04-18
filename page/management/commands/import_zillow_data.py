import pandas as pd
from django.core.management.base import BaseCommand
from page.models import Region, Prices, MapLocation, ZipCode, Neighbourhood
import googlemaps
import time
import os
from django.conf import settings

# Initialize Google Maps client
gmaps = googlemaps.Client(key='AIzaSyA2xFYbh29CbigMzRl-gvHX346UAm-vS0o')

class Command(BaseCommand):
    help = 'Import Zillow data from Excel and populate Region, Prices, and MapLocation tables.'

    def handle(self, *args, **kwargs):

        self.stdout.write(self.style.WARNING("Clearing old Regions, Prices, ZipCodes, and Neighbourhoods..."))

        Prices.objects.all().delete()
        ZipCode.objects.all().delete()
        Neighbourhood.objects.all().delete()
        Region.objects.all().delete()
        MapLocation.objects.all().delete()

        data_path = os.path.join(settings.BASE_DIR, 'Base_Data', 'zillow_base_data.xlsx')

        # Sheets to process
        sheet_map = {
            'ZIP': 'zip',
            'Neighbourhood': 'neighbourhood',
        }

        for sheet_name, region_type in sheet_map.items():
            df = pd.read_excel(data_path, sheet_name=sheet_name)
            metadata_columns = [
                'RegionID', 'SizeRank', 'RegionName', 'RegionType',
                'StateName', 'State', 'City', 'Metro', 'CountyName'
            ]
            date_columns = df.columns.difference(metadata_columns)

            for index, row in df.iterrows():
                region_name = row['RegionName']
                state = row['State']
                metro = row['Metro']
                county = row['CountyName']
                size_rank = row['SizeRank']

                location = self.create_map_location(region_name, county, metro)

                region, _ = Region.objects.get_or_create(
                    region_name=region_name,
                    metro=metro,
                    county=county,
                    state=state,
                    region_type=region_type,
                    defaults={
                        'size_rank': size_rank,
                        'location': location
                    }
                )

                # Create ZIP or Neighbourhood model linked to Region
                if region_type == 'zip':
                    ZipCode.objects.get_or_create(
                        region=region,
                        defaults={'zip_code': region_name, 'location': location}
                    )
                elif region_type == 'neighbourhood':
                    Neighbourhood.objects.get_or_create(
                        region=region,
                        defaults={'location': location}
                    )

                for date_col in date_columns:
                    home_value = row[date_col]
                    if pd.notnull(home_value):
                        try:
                            date = pd.to_datetime(str(date_col), errors='coerce').date()
                            if date:
                                Prices.objects.get_or_create(
                                    region=region,
                                    date=date,
                                    home_value=home_value
                                )
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(
                                f"Failed to insert price for {region_name} on {date_col}: {e}"
                            ))

                self.stdout.write(self.style.SUCCESS(f"[{region_type}] Imported: {region_name}"))


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
