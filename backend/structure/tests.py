from datetime import datetime
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import RequestFactory
from django.test import TestCase

from structure.generator import Generator
from structure.models import *
from .views import monitoring_objects


class GeneratorTestCase(TestCase):
    def test_clear_database(self):
        counts = {'MonitoringObject': 2, 'SensorType': 3}
        generator = Generator(counts)

        # Create some objects
        for obj in counts.keys():
            klass = globals()[obj]
            klass.objects.create()

        # Check if database is cleared
        generator.clear_database()
        for obj in counts.keys():
            klass = globals()[obj]
            self.assertEqual(klass.objects.count(), 0)

    def test_generate_continuous_datetimes(self):
        generator = Generator({})
        start_date = datetime(2024, 1, 1, 0, 0)
        end_date = datetime(2024, 1, 1, 1, 0)

        # Generate datetime objects
        datetimes = list(generator.generate_continuous_datetimes(start_date, end_date))

        # Check if datetimes are generated correctly
        self.assertEqual(len(datetimes), 60)  # 60 minutes between start and end

        # Check if datetimes are in ascending order
        for i in range(len(datetimes) - 1):
            self.assertLess(datetimes[i], datetimes[i + 1])

    def test_generate(self):
        counts = {'MonitoringObject': 2, 'SensorType': 3}
        generator = Generator(counts)

        # Generate data
        generator.run()

        # Check if data is generated correctly
        self.assertEqual(MonitoringObject.objects.count(), counts['MonitoringObject'])
        self.assertEqual(SensorType.objects.count(), counts['SensorType'])
        self.assertEqual(Sensor.objects.count(), counts['MonitoringObject'] * counts['SensorType'])
        self.assertEqual(SensorReading.objects.count(), counts['MonitoringObject'] * counts['SensorType'])
        self.assertEqual(SensorStatus.objects.count(), counts['MonitoringObject'] * counts['SensorType'])
        self.assertEqual(SensorFluidLevel.objects.count(), counts['MonitoringObject'] * counts['SensorType'])
        self.assertEqual(LiftSensorEvent.objects.count(), counts['MonitoringObject'] * counts['SensorType'])


class MonitoringObjectsTestCase(TestCase):
    def setUp(self):
        # Create a monitoring object for testing
        self.mo = MonitoringObject.objects.create(address="Test Address", area_sq_meter=100)

        # Create some sensors associated with the monitoring object
        self.temperature_sensor = Sensor.objects.create(monitoring_object=self.mo, sensor_type__name='Temperature')
        self.humidity_sensor = Sensor.objects.create(monitoring_object=self.mo, sensor_type__name='Humidity')
        self.gas_sensor = Sensor.objects.create(monitoring_object=self.mo, sensor_type__name='Gas')
        self.water_sensor = Sensor.objects.create(monitoring_object=self.mo, sensor_type__name='Water')

    @patch('structure.views.render')
    def test_monitoring_objects(self, mock_render):
        # Create mock sensor readings and events
        SensorReading.objects.bulk_create([
            SensorReading(sensor=self.temperature_sensor, value=25),
            SensorReading(sensor=self.humidity_sensor, value=750),
            SensorReading(sensor=self.gas_sensor, value=15),
            SensorReading(sensor=self.water_sensor, value=0.5)
        ])
        LiftSensorEvent.objects.bulk_create([
            LiftSensorEvent(sensor=self.temperature_sensor, current_level=5, current_state='ok',
                            is_passenger_in_lift=True, are_doors_open=True),
            LiftSensorEvent(sensor=self.temperature_sensor, current_level=7, current_state='failed',
                            is_passenger_in_lift=False, are_doors_open=False)
        ])

        # Mock the request
        request = RequestFactory().get('/')
        request.user = User.objects.create(username='test_user')

        # Call the view function
        monitoring_objects(request, self.mo.id)

        # Assert that the render function was called with the correct parameters
        mock_render.assert_called_once_with(request, 'pages/mo.html', {
            'mo': self.mo,
            'sensors': [self.temperature_sensor, self.humidity_sensor, self.gas_sensor, self.water_sensor],
            'temperature': SensorReading.objects.filter(sensor=self.temperature_sensor).order_by('-timestamp')[:3],
            'temperature_warning': SensorReading.objects.filter(sensor=self.temperature_sensor).order_by('-timestamp')[
                                   :1],
            'humidity': SensorReading.objects.filter(sensor=self.humidity_sensor).order_by('-timestamp')[:3],
            'humidity_warning': SensorReading.objects.filter(sensor=self.humidity_sensor).order_by('-timestamp')[:1],
            'gas': SensorFluidLevel.objects.filter(sensor=self.gas_sensor).order_by('-timestamp')[:3],
            'water': SensorFluidLevel.objects.filter(sensor=self.water_sensor).order_by('-timestamp')[:3],
            'lift': LiftSensorEvent.objects.filter(sensor__monitoring_object=self.mo).order_by('-timestamp')[:3]
        })
