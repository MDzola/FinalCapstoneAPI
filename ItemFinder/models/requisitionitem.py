from django.db import models
from .requisition import RequisitionOrder
from .spareitem import SpareItem


class RequisitionItem(models.Model):
    """
    Creates the join table for the many to many relationship between order and product
    Author: Group Code
    methods: none
    """

    requisitionOrder = models.ForeignKey(RequisitionOrder, on_delete=models.CASCADE, related_name='cart')
    spareItem = models.ForeignKey(SpareItem, on_delete=models.CASCADE, related_name='cart')