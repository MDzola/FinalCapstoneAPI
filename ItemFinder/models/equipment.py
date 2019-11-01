from django.db import models


class Equipment(models.Model):

    name = models.CharField(max_length=55)
    manufacturer = models.CharField(max_length=55)
    manufacturer_contact = models.CharField(max_length=55)
