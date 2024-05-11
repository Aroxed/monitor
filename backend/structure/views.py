from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F, Q
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone
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

    # Total sensors
    result['total_sensors'] = Sensor.objects.count()

    # Active sensors
    result['active_sensors'] = Sensor.objects.filter(is_active__in=[True]).count()

    # Total objects
    result['total_objects'] = MonitoringObject.objects.count()

    # Total objects with area > 100 sq meters
    result['total_objects_area'] = MonitoringObject.objects.filter(area_sq_meter__gt=100).count()

    # Total lifts
    result['total_lifts'] = Sensor.objects.filter(sensor_type__the_type='lift').count()

    # Active lifts
    result['active_lifts'] = LiftSensorEvent.objects.filter(current_state='ok').count()

    # Active lifts list by days of the current week
    active_lifts_list = []
    failed_lifts_list = []
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    for day in range(7):
        current_day = start_of_week + timedelta(days=day)
        lifts_not_working = LiftSensorEvent.objects.filter(
            timestamp__range=(current_day, current_day),
            current_state='failed'
        ).count()
        lifts_working = LiftSensorEvent.objects.filter(
            timestamp__range=(current_day, current_day),
            current_state='ok'
        ).count()
        active_lifts_list.append(lifts_working)
        failed_lifts_list.append(lifts_not_working)
    result['active_lifts_list'] = active_lifts_list
    result['failed_lifts_list'] = failed_lifts_list

    # Events per day for the current week
    events_per_day = []
    for day in range(7):
        current_day = start_of_week + timedelta(days=day)
        events_count = (
                LiftSensorEvent.objects.filter(timestamp__range=(current_day, current_day), ).count() +
                SensorReading.objects.filter(timestamp__range=(current_day, current_day), ).count() +
                SensorStatus.objects.filter(timestamp__range=(current_day, current_day), ).count() +
                SensorFluidLevel.objects.filter(timestamp__range=(current_day, current_day), ).count()
        )
        events_per_day.append(events_count)
    result['events_per_day'] = events_per_day

    # Gas consumption per day
    gas_consumption_per_day = []
    sensor_type_gas = SensorType.objects.get(name='Gas')
    for day in range(7):
        current_day = start_of_week + timedelta(days=day)
        gas_sensor_ids = Sensor.objects.filter(sensor_type=sensor_type_gas).values_list('id', flat=True)
        gas_consumption = \
            SensorReading.objects.filter(sensor_id__in=gas_sensor_ids,
                                         timestamp__range=(current_day, current_day)).aggregate(
                Sum('value'))[
                'value__sum']
        gas_consumption_per_day.append(gas_consumption or 0)
    result['gas_consumption_per_day'] = gas_consumption_per_day

    # Water consumption per day
    water_consumption_per_day = []
    sensor_type_water = SensorType.objects.get(name='Water')
    for day in range(7):
        current_day = start_of_week + timedelta(days=day)
        water_sensor_ids = Sensor.objects.filter(sensor_type=sensor_type_water).values_list('id', flat=True)
        water_consumption = \
            SensorReading.objects.filter(sensor_id__in=water_sensor_ids,
                                         timestamp__range=(current_day, current_day)).aggregate(
                Sum('value'))['value__sum']
        water_consumption_per_day.append(water_consumption or 0)
    result['water_consumption_per_day'] = water_consumption_per_day

    # Positive statuses
    result['positive_statuses'] = SensorStatus.objects.filter(status='on').count()

    # Total events
    result['total_events'] = (
            LiftSensorEvent.objects.count() +
            SensorReading.objects.count() +
            SensorStatus.objects.count() +
            SensorFluidLevel.objects.count()
    )

    return JsonResponse(result)


def monitoring_objects(request, id):
    mo = MonitoringObject.objects.get(id=id)
    # sensors = Sensor.objects.filter(sensor_type=SensorType.objects.get(name=''))
    sensors = Sensor.objects.filter(monitoring_object_id=id)

    temperature = SensorReading.objects.filter(sensor__monitoring_object__pk=id,
                                               sensor__sensor_type__name='Temperature').order_by('-timestamp')[:3]
    temperature_warning = SensorReading.objects.filter(
        Q(sensor__normal_min__gte=F('value')) | Q(sensor__normal_max__lte=F('value')),
        sensor__monitoring_object__pk=id,
        sensor__sensor_type__name='Temperature').order_by(
        '-timestamp')[:1]
    humidity = SensorReading.objects.filter(sensor__monitoring_object__pk=id,
                                            sensor__sensor_type__name='Humidity').order_by('-timestamp')[:3]
    humidity_warning = SensorReading.objects.filter(
        Q(sensor__normal_min__gte=F('value')) | Q(sensor__normal_max__lte=F('value')),
        sensor__monitoring_object__pk=id,
        sensor__sensor_type__name='Humidity').order_by(
        '-timestamp')[:1]
    gas = SensorFluidLevel.objects.filter(sensor__monitoring_object__pk=id, sensor__sensor_type__name='Gas').order_by(
        '-timestamp')[:3]
    water = SensorFluidLevel.objects.filter(sensor__monitoring_object__pk=id,
                                            sensor__sensor_type__name='Water').order_by('-timestamp')[:3]

    lift = LiftSensorEvent.objects.filter(sensor__monitoring_object__pk=id).order_by('-timestamp')[:3]

    return render(request, 'pages/mo.html', {'mo': mo, 'sensors': sensors,
                                             'temperature': temperature,
                                             # 'temperature_warning': temperature_warning,
                                             # 'humidity_warning': humidity_warning,
                                             'humidity': humidity,
                                             'gas': gas, 'water': water, 'lift': lift})


def admin_index(request):
    return render(request, 'pages/index.html', {'segment': 'index'})


def send_email(request):
    send_mail("Hello from Django", "Hello from Django", settings.EMAIL_HOST_USER,
              ['petrashenko@gmail.com'],
              auth_password=settings.EMAIL_HOST_PASSWORD)
    return HttpResponse('email sent')
