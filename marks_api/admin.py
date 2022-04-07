from django.contrib import admin
from .models import Student_data,Data_file
# Register your models here.
class FileAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "standard", "marks"]
admin.site.register(Student_data, FileAdmin)
admin.site.register(Data_file)