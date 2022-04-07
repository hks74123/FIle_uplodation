from django.contrib import admin
from django.urls import path,include
from .views import InsertStudentData

urlpatterns = [
    path('fileuplodation/', InsertStudentData.as_view(), name='upload-file'),
]