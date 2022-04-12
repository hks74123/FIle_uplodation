from django.db import models

# Create your models here.
class Student_data(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    name = models.CharField(max_length=100)
    standard = models.CharField(max_length=200)
    marks = models.FloatField() 

    def __str__(self):
        return self.name

class Data_file(models.Model):
    data_csv = models.FileField(upload_to='media/imgs', null=True,blank=True)
    existingPath = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)
    eof = models.BooleanField()
  