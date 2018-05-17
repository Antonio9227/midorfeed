from django.db import models

# Create your models here.

class Champion(models.Model):
    key= models.IntegerField(null=False, primary_key=True)  # numerical ID of champ
    name=models.CharField(max_length=20)
    id=models.CharField(max_length=20)  # internal name of the champion
