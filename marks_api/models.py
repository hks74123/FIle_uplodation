from django.db import models

# Create your models here.
class Student_data(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    name = models.CharField(max_length=100)
    standard = models.CharField(max_length=200)
    marks = models.FloatField() 

    def __str__(self):
        return self.name
   
  