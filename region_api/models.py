from django.db import models

# Create your models here.

class TestUser(models.Model):
    age = models.IntegerField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

