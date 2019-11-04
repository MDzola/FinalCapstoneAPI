from django.db import models
from django.urls import reverse
from .itemcategory import ItemCategory


class SpareItem(models.Model):


    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    critical_quantity = models.IntegerField()


    class Meta:
        verbose_name = ("Item")
        verbose_name_plural = ("Items")

    def new_inventory(self, num):
        inv = self.quantity - num
        return inv