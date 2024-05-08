from django.contrib import admin

from .models import MonitoringObject, Sensor, SensorType, SensorReading, SensorStatus, LiftSensorEvent


@admin.register(MonitoringObject)
class MonitoringObjectAdmin(admin.ModelAdmin):
    list_display = ('address', 'area_sq_meter')


@admin.register(SensorType)
class SensorTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'the_type')


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('monitoring_object', 'sensor_type', 'is_active')


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'value', 'timestamp')
    list_filter = ('sensor',)


@admin.register(SensorStatus)
class SensorStatusAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'status', 'timestamp')
    list_filter = ('sensor', 'status')


class LiftSensorEventAdmin(admin.ModelAdmin):
    list_display = (
    'sensor', 'current_level', 'current_state', 'is_passenger_in_lift', 'are_doors_open', 'timestamp')
    list_filter = ('current_state', 'is_passenger_in_lift', 'are_doors_open')
    search_fields = ('monitoring_object__address',)


admin.site.register(LiftSensorEvent, LiftSensorEventAdmin)
