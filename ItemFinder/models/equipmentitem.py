from django.db import models
from .equipment import Equipment
from .spareitem import SpareItem

class EquipementItem(models.Model):
    """
    Creates the join table for the many to many relationship between order and product
    Author: Group Code
    methods: none
    """

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='cart')
    spareItem = models.ForeignKey(SpareItem, on_delete=models.CASCADE, related_name='cart')