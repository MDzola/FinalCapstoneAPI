from django.db import models

class VendorItem(models.Model):
    """
    Creates the join table for the many to many relationship between order and product
    Author: Group Code
    methods: none
    """


    price = models.DecimalField(max_digits=7, decimal_places=2)
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, related_name='cart')
    spareItem = models.ForeignKey("SpareItem", on_delete=models.CASCADE, related_name='cart')