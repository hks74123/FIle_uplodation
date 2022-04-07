from rest_framework import serializers
from .models import Student_data, Data_file

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class StudentSerializer(serializers.Serializer):
    class Meta:
        model=Student_data
        fields=['id','name','standard','marks']

