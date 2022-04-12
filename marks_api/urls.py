from django.contrib import admin
from django.urls import path,include
from .views import Get_chunk_files, InsertStudentData

urlpatterns = [
    path('fileuplodation/', InsertStudentData.as_view(), name='upload-file'),
    path('chunkuplodation/', Get_chunk_files.as_view(), name='chunk-files'),
]