from rest_framework import serializers

from .models import MonitoringObject, Sensor, SensorType, SensorReading, SensorStatus, LiftSensorEvent


class SensorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorType
        fields = '__all__'


class MonitoringObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringObject
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = '__all__'


class SensorStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorStatus
        fields = '__all__'


class LiftSensorEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiftSensorEvent
        fields = '__all__'
