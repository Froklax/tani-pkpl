from django.contrib import admin
from .models import Plant, Field, Planting

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'plant_type', 'harvest_time', 'seed_price')
    search_fields = ('name', 'plant_type')
    list_filter = ('plant_type',)

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('field_name', 'user', 'area', 'is_active')
    search_fields = ('field_name', 'user__nama')
    list_filter = ('is_active',)

@admin.register(Planting)
class PlantingAdmin(admin.ModelAdmin):
    list_display = ('id', 'field', 'plant', 'planting_date', 'estimated_harvest', 'status')
    search_fields = ('field__field_name', 'plant__name')
    list_filter = ('status', 'planting_date')