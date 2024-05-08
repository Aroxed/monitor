from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets

from .generator import Generator
from .models import SensorType, MonitoringObject, Sensor, SensorReading, SensorStatus, LiftSensorEvent, SensorFluidLevel
from .serializers import SensorTypeSerializer, MonitoringObjectSerializer, SensorSerializer, SensorReadingSerializer, \
    SensorStatusSerializer, LiftSensorEventSerializer


class SensorTypeViewSet(viewsets.ModelViewSet):
    queryset = SensorType.objects.all()
    serializer_class = SensorTypeSerializer


class MonitoringObjectViewSet(viewsets.ModelViewSet):
    queryset = MonitoringObject.objects.all()
    serializer_class = MonitoringObjectSerializer


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer


class SensorStatusViewSet(viewsets.ModelViewSet):
    queryset = SensorStatus.objects.all()
    serializer_class = SensorStatusSerializer


class LiftSensorEventViewSet(viewsets.ModelViewSet):
    queryset = LiftSensorEvent.objects.all()
    serializer_class = LiftSensorEventSerializer


def generate(request):
    counts = {'MonitoringObject': 5, 'Sensor': 10, 'SensorReading': 10, 'SensorStatus': 10}
    Generator(counts).run()
    return HttpResponse('ok')


def button_statistics(request):
    result = dict()
    result['total_sensors'] = len(Sensor.objects.all())
    result['active_sensors'] = len(Sensor.objects.filter(is_active=True))
    result['total_objects'] = len(MonitoringObject.objects.all())
    result['total_objects'] = len(MonitoringObject.objects.all())
    result['total_objects_area'] = len(MonitoringObject.objects.filter(area_sq_meter__gt=100))
    result['total_lifts'] = len(Sensor.objects.filter(sensor_type__the_type='lift'))
    result['active_lifts'] = len(LiftSensorEvent.objects.filter(current_state='ok'))
    result['positive_statuses'] = len(SensorStatus.objects.filter(status='on'))
    result['total_events'] = (len(LiftSensorEvent.objects.all()) + len(SensorReading.objects.all()) +
                              len(SensorStatus.objects.all()) + len(SensorFluidLevel.objects.all()))
    return JsonResponse(result)
