from django.db import models


class SensorType(models.Model):
    SENSOR_TYPE_CHOICES = (
        ('lift', 'Lift'),
        ('moment', 'Momentary'),
        ('fluid', 'Fluid'),
    )
    name = models.CharField(max_length=50, unique=True)
    the_type = models.CharField(max_length=10, choices=SENSOR_TYPE_CHOICES)

    def __str__(self):
        return self.name


class MonitoringObject(models.Model):
    address = models.CharField(max_length=255)
    area_sq_meter = models.FloatField()

    def __str__(self):
        return self.address


class Sensor(models.Model):
    monitoring_object = models.ForeignKey(MonitoringObject, on_delete=models.CASCADE)
    sensor_type = models.ForeignKey(SensorType, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    normal_min = models.FloatField()
    normal_max = models.FloatField()
    max_per_day = models.FloatField()

    def __str__(self):
        return f"{self.sensor_type} sensor for {self.monitoring_object}"


class Event(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    class Meta:
        abstract = True


class SensorReading(Event):
    value = models.FloatField()

    def __str__(self):
        return f"Sensor Reading ({self.sensor.sensor_type}) at {self.timestamp}"


class SensorFluidLevel(Event):
    value = models.FloatField()

    def __str__(self):
        return f"Sensor Fluid Level ({self.sensor.sensor_type}) at {self.timestamp}"


class SensorStatus(Event):
    STATUS_CHOICES = (
        ('on', 'On'),
        ('off', 'Off'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Sensor Status ({self.sensor.sensor_type}) changed to {self.status} at {self.timestamp}"


class LiftSensorEvent(Event):
    current_level = models.PositiveSmallIntegerField(default=1)
    current_state = models.CharField(max_length=10, choices=(('ok', 'OK'), ('failed', 'Failed')))
    is_passenger_in_lift = models.BooleanField(default=False)
    are_doors_open = models.BooleanField(default=False)

    def __str__(self):
        return f"Lift Sensor Event at {self.timestamp}"
