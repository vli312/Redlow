from django.db import models
from django.contrib.auth.models import User

class Region(models.Model):
    REGION_TYPES = [
        ('neighbourhood', 'Neighbourhood'),
        ('zip', 'Zip Code'),
    ]
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(max_length=100)
    size_rank = models.IntegerField()
    state = models.CharField(max_length=50)
    metro = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    region_type = models.CharField(max_length=20, choices=REGION_TYPES)

    def __str__(self):
        return f"{self.region_name} ({self.region_type})"


class Neighbourhood(models.Model):
    region = models.OneToOneField(Region, on_delete=models.CASCADE, limit_choices_to={'region_type': 'neighbourhood'})

    def __str__(self):
        return self.region.region_name


class ZipCode(models.Model):
    region = models.OneToOneField(Region, on_delete=models.CASCADE, limit_choices_to={'region_type': 'zip'})

    def __str__(self):
        return self.region.region_name


class Prices(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    date = models.DateField()
    home_value = models.DecimalField(max_digits=12, decimal_places=2)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.region.region_name} on {self.date}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Authenticated user
    region = models.ForeignKey('Region', on_delete=models.CASCADE)  # Could be property, neighborhood, or zip
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.region.region_name}"

# hard coded passwords
regular_user = {"username": "James", "pw": "nicepwd4$"}
admin_user = {"username": "Victor", "pw": "adminpwd4$"}