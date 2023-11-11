from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save


class Consumer(models.Model):
    consumer_name = models.CharField (max_length=70, blank=False)
    consumer_phone = models.CharField (max_length=11, blank=False)
    consumer_info = models.TextField (max_length=500, blank=True)
    def __str__(self):
        return f"{self.consumer_name}"

class Storage (models.Model):
    storage_address = models.CharField (max_length=120, blank=False)
    storage_phone = models.CharField (max_length=11, blank=True)
    storage_info = models.TextField (max_length=500, blank=True)
    def __str__(self):
        return f"{self.storage_address}"

class Order(models.Model):
    consumer = models.ForeignKey (Consumer, on_delete=models.CASCADE)
    storage = models.ForeignKey (Storage, on_delete=models.SET_NULL, null=True)
    order_info = models.TextField (max_length=250, blank=True)
    def __str__(self):
        return f"{self.id}"

class Material (models.Model):
    material_name = models.CharField (max_length=50, blank=False)
    def __str__(self):
        return f"{self.material_name}"

class Material_in(models.Model):
    order = models.ForeignKey (Order, on_delete=models.CASCADE)
    material_name = models.ForeignKey (Material, on_delete=models.CASCADE)
    material_count = models.PositiveIntegerField (blank=False, default=1)
    def __str__(self):
        return f"{self.material_name}, {self.order}"