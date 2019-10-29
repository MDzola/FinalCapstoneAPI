from django.db import models
from .spareitem import SpareItem
from .itemcategory import ItemCategory


class Equipment(models.Model):

    name = models.CharField(max_length=55)
    manufacturer = models.CharField(max_length=55)
    manufacturer_contact = models.CharField(max_length=55)
    equipment_item = models.ForeignKey(SpareItem, on_delete=models.CASCADE)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)