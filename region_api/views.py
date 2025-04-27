#from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import TestUserSerializer, ZipCodeSerializer, NeighbourhoodSerializer, PricesSerializer, MapLocationSerializer
from page.models import Region, MapLocation, Neighbourhood, ZipCode, Prices
import json
from sklearn.metrics.pairwise import haversine_distances
from math import radians
import folium
from folium.plugins import FastMarkerCluster, MarkerCluster


LATEST_YEAR = ['2024-03-31','2024-04-30','2024-05-31','2024-06-30','2024-07-31','2024-08-31','2024-09-30','2024-10-31','2024-11-30','2024-12-31','2025-01-31','2025-02-28']


# Create your views here.
@api_view(['GET'])
def list_zipcodes(request):
    zipcodes = ZipCode.objects.values_list('zip_code', flat=True)
    return Response({'zipcodes':zipcodes})


@api_view(['GET'])
def list_neighbourhoods(request):
    neighbourhoods = Neighbourhood.objects.values_list('id', flat=True) # Change 'id' to 'neighbourhood' after implementation
    return Response({'neighbourhoods':neighbourhoods})


@api_view(['PATCH'])
def mapFilter_zipcode(request):
    data = json.loads(request.body) # Testing with {"zipcode":"22305"}
    zipcode = data["zipcode"]
    recordZipCode = ZipCode.objects.get(zip_code=str(zipcode))
    dataZipCode = ZipCodeSerializer(recordZipCode).data
    region = dataZipCode["region"] # (Not) Used in the final section below
    location = dataZipCode["location"]
    recordMapLocation = MapLocation.objects.get(id=location)
    dataMapLocation = MapLocationSerializer(recordMapLocation).data
    lat1, lon1 = dataMapLocation["latitude"], dataMapLocation["longitude"]
    zipcodes_locations = ZipCode.objects.values_list('zip_code','location')
    zipcodes_lat_lon = []
    for _zipcode, _location in zipcodes_locations:
        otherRecordMapLocation = MapLocation.objects.get(id=_location)
        otherDataMapLocation = MapLocationSerializer(otherRecordMapLocation).data
        lat2, lon2 = otherDataMapLocation["latitude"], otherDataMapLocation["longitude"]
        zipcodes_lat_lon.append((_zipcode, lat2, lon2))
    # Create a Folium map object
    center = [lat1, lon1] # Selected ZipCode
    dmv_map = folium.Map(location=center, zoom_start=13)  # Adjust zoom_start as needed
    marker_cluster = MarkerCluster( # Method 3: Cluster + Popup
        name='Zip Codes Cluster',
        overlay=True,
        control=False,
        icon_create_function=None)
    for i in range(len(zipcodes_lat_lon)):
        location = zipcodes_lat_lon[i][1], zipcodes_lat_lon[i][2]
        marker = folium.Marker(location=location)
        popup = zipcodes_lat_lon[i][0]
        folium.Popup(popup).add_to(marker)
        marker_cluster.add_child(marker)
    marker_cluster.add_to(dmv_map)
    folium.LayerControl().add_to(dmv_map)
    dmv_map.save("templates/page/page_story/folium_map_zipcode.html")
    return Response({"status":"success"})


@api_view(['PATCH'])
def mapFilter_neighbourhood(request):
    return Response(TestUserSerializer({'name':'sandy','age':29}).data)


@api_view(['PATCH', 'PUT']) # PATCH for line plot and PUT for bar plot 
def plotPopulate_zipcode(request):
    data = json.loads(request.body) # Testing with {"zipcode":"22305"}
    if request.method == 'PATCH':
        months = []
        home_values = []
        zipcode = data["zipcode"]
        #print(zipcode)
        recordZipCode = ZipCode.objects.get(zip_code=str(zipcode))
        dataZipCode = ZipCodeSerializer(recordZipCode).data
        #print(dataZipCode)
        region = dataZipCode["region"]
        for month in LATEST_YEAR:
            recordPrices = Prices.objects.get(region=region, date=month)
            dataPrices = PricesSerializer(recordPrices).data
            months.append(dataPrices['date'])
            home_values.append(dataPrices['home_value'])
        return Response({'months':months, 'home_values':home_values})
    elif request.method == 'PUT':
        zipcode = data["zipcode"]
        recordZipCode = ZipCode.objects.get(zip_code=str(zipcode))
        dataZipCode = ZipCodeSerializer(recordZipCode).data
        region = dataZipCode["region"] # Used in the final section below
        location = dataZipCode["location"]
        recordMapLocation = MapLocation.objects.get(id=location)
        dataMapLocation = MapLocationSerializer(recordMapLocation).data
        lat1, lon1 = dataMapLocation["latitude"], dataMapLocation["longitude"]
        #print(dataMapLocation)
        #zipcodes = ZipCode.objects.values_list('zip_code', flat=True)
        #locations = ZipCode.objects.values_list('location', flat=True)
        zipcodes_locations = ZipCode.objects.values_list('zip_code','location')
        #print(zipcodes)
        #print(locations)
        #print(zipcodes_locations)
        distance_zipcodes = []
        for _zipcode, _location in zipcodes_locations:
            if _zipcode == zipcode:
                continue
            else:
                otherRecordMapLocation = MapLocation.objects.get(id=_location)
                otherDataMapLocation = MapLocationSerializer(otherRecordMapLocation).data
                lat2, lon2 = otherDataMapLocation["latitude"], otherDataMapLocation["longitude"]
                dist = calculate_dist_by_lat_lon(lat1=lat1, lon1=lon1, lat2=lat2, lon2=lon2)
                distance_zipcodes.append((dist, _zipcode))
        #print(distance_zipcodes)
        closest_zipcodes = []
        closest_home_values = []
        closest_dist = []
        top_7 = sorted(distance_zipcodes)[:7]
        for _dist, _zipcode in top_7:
            _recordZipCode = ZipCode.objects.get(zip_code=_zipcode)
            _dataZipCode = ZipCodeSerializer(_recordZipCode).data
            _region = _dataZipCode["region"]
            recordPrices = Prices.objects.get(region=_region, date=LATEST_YEAR[-1])
            dataPrices = PricesSerializer(recordPrices).data
            closest_zipcodes.append(_zipcode)
            closest_home_values.append(dataPrices['home_value'])
            closest_dist.append(_dist)
        #print({'closest_zipcodes':closest_zipcodes, 'closest_home_values':closest_home_values, 'closest_dist':closest_dist})
        return Response({'closest_zipcodes':closest_zipcodes, 'closest_home_values':closest_home_values, 'closest_dist':closest_dist})



@api_view(['POST', 'PUT']) # PUT for bar plot and POST for line plot
def plotPopulate_neighbourhood(request):
    return Response(TestUserSerializer({'name':'sandy','age':29}).data)

#========================================================
#================== Support Functions ===================
#========================================================

def calculate_dist_by_lat_lon(lat1, lon1, lat2, lon2):
    rad1 = [radians(lat1), radians(lon1)]
    rad2 = [radians(lat2), radians(lon2)]
    hsd = haversine_distances([rad1, rad2])
    dist_in_km = hsd * 6371000/1000  # multiply by Earth radius to get kilometers
    return float(dist_in_km[0][1])
