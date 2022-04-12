from dataclasses import field
from tkinter import S
from urllib import response
from django.shortcuts import render
from rest_framework import generics
import io, csv, pandas as pd
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer,StudentSerializer  
from .models import Student_data,Data_file
from .exceptions import ChunkedUploadError
from django.http import JsonResponse   
import os
from django.conf import settings

# Create your views here.
class InsertStudentData(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        reader = pd.read_csv(file)
        save_file = Data_file(data_csv = request.FILES['file'])
        save_file.save()  
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
    

class Get_chunk_files(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    
    def put(self, request, *args, **kwargs):
        file = request.FILES['file'].read()
        fileName= request.POST['filename']
        existingPath = request.POST['existingPath']
        end = request.POST['end']
        nextSlice = request.POST['nextSlice']

        if file=="" or fileName=="" or existingPath=="" or end=="" or nextSlice=="":
            res = JsonResponse({'data':'Invalid Request'})
            return res
        else:
            if existingPath == 'null':
                path = 'media/' + fileName
                with open(path, 'wb+') as destination: 
                    destination.write(file)
                FileFolder = Data_file()     
                FileFolder.existingPath = fileName
                FileFolder.eof = end
                FileFolder.name = fileName
                FileFolder.save()
                if int(end):
                    res = JsonResponse({'data':'Uploaded Successfully','existingPath': fileName})
                else:
                    res = JsonResponse({'existingPath': fileName})
                return res

            else:
                path = 'media/' + existingPath
                model_id = Data_file.objects.get(existingPath=existingPath)
                if model_id.name == fileName:
                    if not model_id.eof:
                        with open(path, 'ab+') as destination: 
                            destination.write(file)
                        if int(end):
                            model_id.data_csv = f'/{fileName}'
                            model_id.eof = int(end)
                            model_id.save()
                            res = JsonResponse({'data':'Uploaded Successfully','existingPath':model_id.existingPath})
                        else:
                            res = JsonResponse({'existingPath':model_id.existingPath})    
                        return res
                    else:
                        res = JsonResponse({'data':'EOF found. Invalid request'})
                        return res
                else:
                    res = JsonResponse({'data':'No such file exists in the existingPath'})
                    return res
