from django.db import models
from .employee import Employee
from .spareitem import SpareItem

class RequisitionOrder(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    isComplete = models.BooleanField(default=False)
    spare_item = models.ManyToManyField(SpareItem, through="RequisitionItem")



    class Meta:
            verbose_name = ("order")
            verbose_name_plural = ("orders")
