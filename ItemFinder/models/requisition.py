from django.db import models
from .employee import Employee



class Requisition(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)

    class Meta:
            verbose_name = ("order")
            verbose_name_plural = ("orders")
