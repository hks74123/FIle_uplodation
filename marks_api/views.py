from tkinter import S
from django.shortcuts import render
from rest_framework import generics
import io, csv, pandas as pd
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer,StudentSerializer
from .models import Student_data

# Create your views here.
class InsertStudentData(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        reader = pd.read_csv(file)
        for _, row in reader.iterrows():
            new_file = Student_data(
                       id = row['id'],
                       name= row["Name"],
                       standard= row['Standard'],
                       marks= round(0.1*row["marks"],3),
                       )
            new_file.save()
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)