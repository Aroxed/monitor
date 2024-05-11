from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (SensorTypeViewSet, MonitoringObjectViewSet, SensorViewSet, SensorReadingViewSet,
                    SensorStatusViewSet,
                    generate, LiftSensorEventViewSet, button_statistics, monitoring_objects, send_email)

router = DefaultRouter()
router.register(r'sensor-types', SensorTypeViewSet)
router.register(r'monitoring-objects', MonitoringObjectViewSet)
router.register(r'sensors', SensorViewSet)
router.register(r'sensor-readings', SensorReadingViewSet)
router.register(r'sensor-statuses', SensorStatusViewSet)
router.register(r'lift-sensor-events', LiftSensorEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('generate', generate),
    path('button_statistics', button_statistics),
    path('mo/<int:id>', monitoring_objects),
    path('send_email', send_email),
]
