from rest_framework import serializers
from .models import TestUser
from page.models import ZipCode, Neighbourhood, Prices, MapLocation

class TestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestUser
        fields = '__all__'

class ZipCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZipCode
        fields = '__all__'

class NeighbourhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighbourhood
        fields = '__all__'

class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = '__all__'

class MapLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapLocation
        fields = '__all__'
