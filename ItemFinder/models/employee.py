from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Employee(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)


    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
