from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Employee(AbstractUser):
    first_name = models.TextField(max_length=50)
    dob = models.DateField(max_length=30)
    image = models.ImageField(upload_to='profile_images', blank=True)
    description = models.TextField(blank=True)
    career_start_date = models.DateField(blank=True, max_length=30, null=True)
    position = models.CharField(blank=True, max_length=100)

    class Meta:
        db_table = 'employees'


@receiver(post_save, sender=Employee)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
