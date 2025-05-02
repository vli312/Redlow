from django.urls import path
from .views import list_zipcodes, list_neighbourhoods, mapFilter_zipcode, mapFilter_neighbourhood, plotPopulate_zipcode, \
    plotPopulate_neighbourhood, plotForecast_zipcode, plotForecast_neighbourhood

app_name = 'region_api'

urlpatterns = [
    path('list_zipcodes', list_zipcodes, name='list_zipcodes'),
    path('list_neighbourhoods', list_neighbourhoods, name='list_neighbourhoods'),
    path('mapFilter_zipcode', mapFilter_zipcode, name='mapFilter_zipcode'),
    path('mapFilter_neighbourhood', mapFilter_neighbourhood, name='mapFilter_neighbourhood'),
    path('plotPopulate_zipcode', plotPopulate_zipcode, name='plotPopulate_zipcode'),
    path('plotPopulate_neighbourhood', plotPopulate_neighbourhood, name='plotPopulate_neighbourhood'),
    path('plotForecast_zipcode', plotForecast_zipcode, name='plotForecast_zipcode'),
    path('plotForecast_neighbourhood', plotForecast_neighbourhood, name='plotForecast_neighbourhood'),
]