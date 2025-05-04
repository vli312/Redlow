#from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import TestUserSerializer, ZipCodeSerializer, NeighbourhoodSerializer, \
    PricesSerializer, MapLocationSerializer, RegionSerializer
from page.models import Region, MapLocation, Neighbourhood, ZipCode, Prices
import json
from sklearn.metrics.pairwise import haversine_distances
from math import radians
import folium
from folium.plugins import FastMarkerCluster, MarkerCluster
import numpy as np
import pandas as pd
import pmdarima as pm


LATEST_YEAR = ['2024-03-31','2024-04-30','2024-05-31','2024-06-30','2024-07-31','2024-08-31','2024-09-30','2024-10-31','2024-11-30','2024-12-31','2025-01-31','2025-02-28']
LATEST_15MONTHS = ['2023-12-31','2024-01-31','2024-02-29','2024-03-31','2024-04-30','2024-05-31','2024-06-30','2024-07-31','2024-08-31','2024-09-30','2024-10-31','2024-11-30','2024-12-31','2025-01-31','2025-02-28']
LATEST_3YEARS = ['2022-03-31','2022-04-30','2022-05-31','2022-06-30','2022-07-31','2022-08-31','2022-09-30','2022-10-31','2022-11-30','2022-12-31','2023-01-31','2023-02-28', \
                 '2023-03-31','2023-04-30','2023-05-31','2023-06-30','2023-07-31','2023-08-31','2023-09-30','2023-10-31','2023-11-30','2023-12-31','2024-01-31','2024-02-29', \
                 '2024-03-31','2024-04-30','2024-05-31','2024-06-30','2024-07-31','2024-08-31','2024-09-30','2024-10-31','2024-11-30','2024-12-31','2025-01-31','2025-02-28']


# Create your views here.
@api_view(['GET'])
def list_zipcodes(request):
    zipcodes = ZipCode.objects.values_list('zip_code', flat=True)
    return Response({'zipcodes':sorted(zipcodes)})


@api_view(['GET'])
def list_neighbourhoods(request):
    #neighbourhoods = Neighbourhood.objects.values_list('id', flat=True)
    #Change 'id' to 'neighbourhood' after implementation
    neighbourhoods = Region.objects.filter(region_type='neighbourhood').values_list('region_name', flat=True)
    states = Region.objects.filter(region_type='neighbourhood').values_list('state', flat=True)
    neighbourhood_state = [str(neighbourhoods[i])+", "+str(states[i]) for i in range(len(states))]
    return Response({'neighbourhood_state':sorted(neighbourhood_state)})


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
    data = json.loads(request.body) # Testing with {"neighbourhood_state":"Pearl District, MD"}
    neighbourhood, state = data["neighbourhood_state"].split(", ")
    recordNeighbourhood = Region.objects.filter(region_type='neighbourhood').get(region_name=str(neighbourhood), state=str(state))
    dataNeighbourhood = RegionSerializer(recordNeighbourhood).data
    location = dataNeighbourhood["location"]
    recordMapLocation = MapLocation.objects.get(id=location)
    dataMapLocation = MapLocationSerializer(recordMapLocation).data
    lat1, lon1 = dataMapLocation["latitude"], dataMapLocation["longitude"]
    neighbourhoods_locations = Region.objects.filter(region_type='neighbourhood').values_list('region_name','state','location')
    neighbourhoods_lat_lon = []
    for _neighbourhood, _state, _location in neighbourhoods_locations:
        otherRecordMapLocation = MapLocation.objects.get(id=_location)
        otherDataMapLocation = MapLocationSerializer(otherRecordMapLocation).data
        lat2, lon2 = otherDataMapLocation["latitude"], otherDataMapLocation["longitude"]
        neighbourhoods_lat_lon.append((str(_neighbourhood)+", "+str(_state), lat2, lon2))
    # Create a Folium map object
    center = [lat1, lon1] # Selected Neighbourhood
    dmv_map = folium.Map(location=center, zoom_start=13)  # Adjust zoom_start as needed
    marker_cluster = MarkerCluster( # Method 3: Cluster + Popup
        name='Neighbourhoods Cluster',
        overlay=True,
        control=False,
        icon_create_function=None)
    for i in range(len(neighbourhoods_lat_lon)):
        location = neighbourhoods_lat_lon[i][1], neighbourhoods_lat_lon[i][2]
        marker = folium.Marker(location=location)
        popup = neighbourhoods_lat_lon[i][0]
        folium.Popup(popup).add_to(marker)
        marker_cluster.add_child(marker)
    marker_cluster.add_to(dmv_map)
    folium.LayerControl().add_to(dmv_map)
    dmv_map.save("templates/page/page_story/folium_map_neighbourhood.html")
    return Response({"status":"success"})


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
        top_7 = [(0, str(zipcode))] + top_7
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



@api_view(['PATCH', 'PUT']) # PUT for bar plot and POST for line plot
def plotPopulate_neighbourhood(request):
    data = json.loads(request.body) # Testing with {"neighbourhood_state":"Pearl District, MD"}
    if request.method == 'PATCH':
        months = []
        home_values = []
        neighbourhood, state = data["neighbourhood_state"].split(", ")
        recordNeighbourhood = Region.objects.filter(region_type='neighbourhood').get(region_name=str(neighbourhood), state=str(state))
        dataNeighbourhood = RegionSerializer(recordNeighbourhood).data
        region = dataNeighbourhood["region_id"]
        for month in LATEST_YEAR:
            recordPrices = Prices.objects.get(region=region, date=month)
            dataPrices = PricesSerializer(recordPrices).data
            months.append(dataPrices['date'])
            home_values.append(dataPrices['home_value'])
        return Response({'months':months, 'home_values':home_values})
    elif request.method == 'PUT':
        neighbourhood, state = data["neighbourhood_state"].split(", ")
        recordNeighbourhood = Region.objects.filter(region_type='neighbourhood').get(region_name=str(neighbourhood), state=str(state))
        dataNeighbourhood = RegionSerializer(recordNeighbourhood).data
        region = dataNeighbourhood["region_id"] # Used in the final section below
        location = dataNeighbourhood["location"]
        recordMapLocation = MapLocation.objects.get(id=location)
        dataMapLocation = MapLocationSerializer(recordMapLocation).data
        lat1, lon1 = dataMapLocation["latitude"], dataMapLocation["longitude"]
        neighbourhoods_locations = Region.objects.filter(region_type='neighbourhood').values_list('region_name','state','location')
        distance_neighbourhoods = []
        for _neighbourhood, _state, _location in neighbourhoods_locations:
            if _neighbourhood == neighbourhood and _state == state:
                continue
            else:
                otherRecordMapLocation = MapLocation.objects.get(id=_location)
                otherDataMapLocation = MapLocationSerializer(otherRecordMapLocation).data
                lat2, lon2 = otherDataMapLocation["latitude"], otherDataMapLocation["longitude"]
                dist = calculate_dist_by_lat_lon(lat1=lat1, lon1=lon1, lat2=lat2, lon2=lon2)
                distance_neighbourhoods.append((dist, _neighbourhood, _state))
        closest_neighbourhoods = []
        closest_home_values = []
        closest_dist = []
        top_7 = sorted(distance_neighbourhoods)[:7]
        recordPrices = Prices.objects.get(region=region, date=LATEST_YEAR[-1])
        dataPrices = PricesSerializer(recordPrices).data
        top_7 = [(0, str(neighbourhood), str(state))] + top_7
        for _dist, _neighbourhood, _state in top_7:
            _recordNeighbourhood = Region.objects.filter(region_type='neighbourhood').get(region_name=_neighbourhood, state=_state)
            _dataNeighbourhood = RegionSerializer(_recordNeighbourhood).data
            _region = _dataNeighbourhood["region_id"]
            recordPrices = Prices.objects.get(region=_region, date=LATEST_YEAR[-1])
            dataPrices = PricesSerializer(recordPrices).data
            closest_neighbourhoods.append(str(_neighbourhood)+", "+str(_state))
            closest_home_values.append(dataPrices['home_value'])
            closest_dist.append(_dist)
        return Response({'closest_neighbourhoods':closest_neighbourhoods, 'closest_home_values':closest_home_values, 'closest_dist':closest_dist})


@api_view(['PATCH']) # PATCH for line plot
def plotForecast_zipcode(request):
    data = json.loads(request.body) # Testing with {"zipcode":"22305","forecast":"3 Months"}
    zipcode = data["zipcode"]
    forecast_option = data["forecast"]
    print(forecast_option)
    if forecast_option == '1': sel_periods = 1
    elif forecast_option == '2': sel_periods = 3
    else: sel_periods = 6
    zeros = np.zeros((len(LATEST_3YEARS),1))
    df = pd.DataFrame(columns=['Home Value'], index=LATEST_3YEARS, data=zeros)
    recordZipCode = ZipCode.objects.get(zip_code=zipcode)
    dataZipCode = ZipCodeSerializer(recordZipCode).data
    region = dataZipCode["region"]
    for month in LATEST_3YEARS:
        recordPrices = Prices.objects.get(region=region, date=month)
        dataPrices = PricesSerializer(recordPrices).data
        #print(dataPrices)
        df.loc[month, 'Home Value'] = dataPrices['home_value']
    #print(df)
    df.index = pd.to_datetime(df.index)
    SARIMA_model = pm.auto_arima(df[['Home Value']], #exogenous=df[[each for each in top_n if each != zipcode]],
                                 start_p=1, start_q=1,
                                 test='adf',
                                 max_p=3, max_q=3, m=12,
                                 start_P=0, seasonal=True,
                                 d=None, D=1,
                                 trace=False,
                                 error_action='ignore',
                                 suppress_warnings=True,
                                 stepwise=True)
    fitted, confint = SARIMA_model.predict(n_periods=sel_periods,
                                           return_conf_int=True)#, exogenous=forecast_df[['month_index']])
    index_of_forecast = pd.date_range(df.index[-1] + pd.DateOffset(months=1), periods=sel_periods, freq='MS')
    months_of_forecast = [str(x)[:10] for x in list(index_of_forecast)]
    lower_confint = pd.Series(confint[:, 0], index=index_of_forecast)
    upper_confint = pd.Series(confint[:, 1], index=index_of_forecast)
    return Response({'months':months_of_forecast, 'forecast':list(fitted), 'lower_confint':list(lower_confint), 'upper_confint':list(upper_confint)})


@api_view(['PATCH']) # PATCH for line plot
def plotForecast_neighbourhood(request):
    data = json.loads(request.body) # Testing with {"neighbourhood_state":"Pearl District, MD","forecast":"3 Months"}
    neighbourhood, state = data["neighbourhood_state"].split(", ")
    forecast_option = data["forecast"]
    #print(forecast_option)
    if forecast_option == '1': sel_periods = 1
    elif forecast_option == '2': sel_periods = 2
    else: sel_periods = 3
    zeros = np.zeros((len(LATEST_15MONTHS),1))
    df = pd.DataFrame(columns=['Home Value'], index=LATEST_15MONTHS, data=zeros) # ONLY 1 YEAR OF CONTINUOUS DATA AVAILABLE
    recordZipCode = Region.objects.get(region_name=neighbourhood, state=state)
    dataZipCode = RegionSerializer(recordZipCode).data
    region = dataZipCode["region_id"]
    for month in LATEST_15MONTHS:
        recordPrices = Prices.objects.get(region=region, date=month)
        dataPrices = PricesSerializer(recordPrices).data
        df.loc[month, 'Home Value'] = dataPrices['home_value']
    df.index = pd.to_datetime(df.index)
    print(df)
    SARIMA_model = pm.auto_arima(df[['Home Value']], #exogenous=df[[each for each in top_n if each != zipcode]],
                                 start_p=1, start_q=1,
                                 test='adf',
                                 max_p=3, max_q=3, m=6, #m=12,
                                 start_P=0, seasonal=True,
                                 d=None, D=1,
                                 trace=False,
                                 error_action='ignore',
                                 suppress_warnings=True,
                                 stepwise=True)
    fitted, confint = SARIMA_model.predict(n_periods=sel_periods,
                                           return_conf_int=True)#, exogenous=forecast_df[['month_index']])
    index_of_forecast = pd.date_range(df.index[-1] + pd.DateOffset(months=1), periods=sel_periods, freq='MS')
    months_of_forecast = [str(x)[:10] for x in list(index_of_forecast)]
    lower_confint = pd.Series(confint[:, 0], index=index_of_forecast)
    upper_confint = pd.Series(confint[:, 1], index=index_of_forecast)
    return Response({'months':months_of_forecast, 'forecast':list(fitted), 'lower_confint':list(lower_confint), 'upper_confint':list(upper_confint)})


#========================================================
#================== Support Functions ===================
#========================================================


def calculate_dist_by_lat_lon(lat1, lon1, lat2, lon2):
    rad1 = [radians(lat1), radians(lon1)]
    rad2 = [radians(lat2), radians(lon2)]
    hsd = haversine_distances([rad1, rad2])
    dist_in_km = hsd * 6371000/1000  # multiply by Earth radius to get kilometers
    return float(dist_in_km[0][1])

