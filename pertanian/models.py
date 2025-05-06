from django.db import models
from django.core.validators import RegexValidator
from user.models import CustomUser

name_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9\s\-]+$',
    message="Nama hanya boleh mengandung nama, angka, dan strip '-'"
)
address_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9\s,.\-]+$',
    message="Address hanya dapat berisi huruf, angka, spasi, koma, titik, dan strip '-'"
)

class Plant(models.Model):
    name = models.CharField(max_length=100, validators=[name_validator])
    plant_type = models.CharField(max_length=50)
    harvest_time = models.IntegerField(help_text="Harvest time in days")
    description = models.TextField()
    seed_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Field(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fields')
    field_name = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in hectares")
    address = models.TextField(validators=[address_validator])
    registered_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.field_name} - {self.user.nama}"

class Planting(models.Model):
    STATUS_CHOICES = (
        ('Preparation', 'Preparation'),
        ('Planting', 'Planting'),
        ('Maintenance', 'Maintenance'),
        ('Harvest', 'Harvest'),
        ('Failed', 'Failed'),
    )
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='plantings')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='plantings')
    planting_date = models.DateField()
    estimated_harvest = models.DateField()
    seed_count = models.IntegerField()
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Preparation')
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.plant.name} at {self.field.field_name}"