from django.db import models


class Vendor(models.Model):

    name = models.CharField(max_length=55)
    contact = models.CharField(max_length=100)

    class Meta:
        verbose_name = ("vendor")
        verbose_name_plural = ("vendors")