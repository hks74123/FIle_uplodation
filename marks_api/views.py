from dataclasses import field
from tkinter import S
from urllib import response
from django.shortcuts import render
from rest_framework import generics
import io, csv, pandas as pd
from rest_framework.response import Response
from rest_framework import status
from marks_api.serializers import FileUploadSerializer,StudentSerializer  
from marks_api.models import Student_data,Data_file
from django.http import JsonResponse   
import os
from django.conf import settings

# Create your views here.

# View for inserting data to database on uploading full file in a single chunk
class InsertStudentData(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    
    # view for handeling post request
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #Validating file data
        api_file = serializer.validated_data['file']
        
        #reading file
        file_reader = pd.read_csv(api_file)
        save_file = Data_file(data_csv = request.FILES['file'])
        save_file.save() 
        #Saving Content of file to database 
        for _, row in file_reader.iterrows():
            new_file = Student_data(
                       id = row['id'],
                       name= row["Name"],
                       standard= row['Standard'],
                       marks= round(0.1*row["marks"],3),
                       )
            new_file.save()
        return Response({"status": "success"},
                        status.HTTP_201_CREATED)
    

# View for Chunk uplodation
class Get_chunk_files(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    
    # Handeling the PUT requests
    def put(self, request, *args, **kwargs):
        # Getting the details that are recived from api
        api_file = request.FILES['file'].read()
        file_name= request.POST['filename']
        existing_path = request.POST['existingPath']
        file_end = request.POST['end']
        next_slice = request.POST['nextSlice']

        # Validating the api data
        if api_file=="" or file_name=="" or existing_path=="" or file_end=="" or next_slice=="":
            res = JsonResponse({'data':'Invalid Request'})
            return res
        else:
            if existing_path == 'null':
                # Uploading and setting the path of file
                path = 'media/' + file_name
                with open(path, 'wb+') as destination: 
                    destination.write(api_file)
                
                # Creating a model instance of Data_file
                FileFolder = Data_file()     
                FileFolder.existingPath = file_name
                FileFolder.eof = file_end
                FileFolder.name = file_name
                FileFolder.save()
                if int(file_end):
                    res = JsonResponse({'data':'Uploaded Successfully','existingPath': file_name})
                else:
                    res = JsonResponse({'existingPath': file_name})
                return res

            else:
                path = 'media/' + existing_path
                model_id = Data_file.objects.get(existingPath=existing_path)
                if model_id.name == file_name:
                    if not model_id.eof:
                        # Adding Chunks to existing file
                        with open(path, 'ab+') as destination: 
                            destination.write(api_file)
                        if int(file_end):
                            # At end of the file saving it's path and details to database
                            model_id.data_csv = f'/{file_name}'
                            model_id.eof = int(file_end)
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
