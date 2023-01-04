from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    brand = models.CharField(max_length=50, null=False, blank=False)
    last_updated = models.DateField(auto_now=True)

class Brand(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20)