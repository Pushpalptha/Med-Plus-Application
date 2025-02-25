from django.contrib import admin
from django.contrib import admin
from .models import MedicationInfo, Category


class MedicationInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'image', 'created_at')  
    search_fields = ('name', 'composition') 
    list_filter = ('category', 'created_at')  

admin.site.register(MedicationInfo, MedicationInfoAdmin)
admin.site.register(Category)
