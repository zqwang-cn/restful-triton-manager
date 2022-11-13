from django.db import models
from model.models import Model


# Create your models here.
class Repository(models.Model):
    name = models.CharField(unique=True, max_length=100)
    models = models.ManyToManyField(Model)
    
    def __str__(self):
        return self.name