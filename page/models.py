from django.contrib.auth.models import User
from django.db import models

class MapLocation(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"Location ({self.latitude}, {self.longitude})"


class Region(models.Model):
    REGION_TYPES = [
        ('neighbourhood', 'Neighbourhood'),
        ('zip', 'Zip Code'),
    ]
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    metro = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    size_rank = models.IntegerField()
    region_type = models.CharField(max_length=20, choices=REGION_TYPES)
    location = models.OneToOneField(MapLocation, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.region_name} ({self.region_type})"

class Neighbourhood(models.Model):
    region = models.OneToOneField(Region, on_delete=models.CASCADE, limit_choices_to={'region_type': 'neighbourhood'})
    location = models.OneToOneField(MapLocation, on_delete=models.CASCADE, null=True)  # Allow null value

    def __str__(self):
        return self.region.region_name

class ZipCode(models.Model):
    zip_code = models.CharField(max_length=10, null=True)
    region = models.OneToOneField(Region, on_delete=models.CASCADE, primary_key=True)  # Use region as the primary key
    location = models.OneToOneField(MapLocation, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.zip_code

class Prices(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    date = models.DateField()
    home_value = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.region.region_name} on {self.date}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.region.region_name}"


# hard coded passwords
regular_user = {"username": "James", "pw": "nicepwd4$"}
admin_user = {"username": "Victor", "pw": "adminpwd4$"}