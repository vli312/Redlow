from cProfile import Profile

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Detail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    role = models.CharField(default="regular", max_length=50)

@receiver(post_save, sender=User)
def create_user_details(sender, instance, created, **kwargs):
    if created:
        Detail.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_details(sender, instance, **kwargs):
    instance.detail.save()