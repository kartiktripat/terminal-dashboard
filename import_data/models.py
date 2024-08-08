from django.db import models

class Terminal(models.Model):
    station_code = models.CharField(max_length=100)
    station_name = models.CharField(max_length=100)
    division = models.CharField(max_length=100)
    zone = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    working_hours_from = models.CharField(max_length=100, null=True, blank=True)
    working_hours_to = models.CharField(max_length=100, null=True, blank=True)
    terminal_type = models.CharField(max_length=100)
    avg_rakes_handling = models.FloatField(null=True, blank=True)
    line_count = models.FloatField(null=True, blank=True)
    handling_type = models.CharField(max_length=100, null=True, blank=True)
    warehouse_available_yes_no = models.CharField(max_length=10, null=True, blank=True)  # Correct column name
    owner = models.CharField(max_length=100, null=True, blank=True)
    associated_weighbridge = models.CharField(max_length=100, null=True, blank=True)
    alternate_weighbridge = models.CharField(max_length=100, null=True, blank=True)
    tank_handling_yes_no = models.CharField(max_length=10, null=True, blank=True)  # Correct column name
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    
    class Meta:
        db_table = 'terminal_data'


