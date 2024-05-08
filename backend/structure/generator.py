import random
from datetime import datetime, timedelta
from random import randint

from faker import Faker

from structure.models import *


class Generator:
    def __init__(self, counts):
        self.faker = Faker(locale='en_US')
        self.counts = counts

    def clear_database(self):
        for obj in self.counts.keys():
            klass = globals()[obj]
            klass.objects.all().delete()

    def generate_continuous_datetimes(self, start_date, end_date):
        current_date = start_date
        while current_date < end_date:
            yield current_date
            interval_minutes = random.randint(1, 60 * 24)  # Random interval between 1 and 120 minutes
            current_date += timedelta(minutes=interval_minutes)

    def generate(self):

        for _ in range(self.counts['MonitoringObject']):
            address = self.faker.address()
            MonitoringObject.objects.create(address=address, area_sq_meter=randint(1, 1000))

            LiftSensorEvent.objects.all().delete()
            SensorFluidLevel.objects.all().delete()
            SensorStatus.objects.all().delete()
            SensorReading.objects.all().delete()
            Sensor.objects.all().delete()
            SensorType.objects.all().delete()

            the_types = {'lift': ['Lift Sensor'],
                         'moment': ['Temperature', 'Humidity'],
                         'fluid': ['Gas', 'Water', 'Electricity']}
            for the_type_name, the_type_list in the_types.items():
                for the_type in the_type_list:
                    SensorType.objects.create(name=the_type, the_type=the_type_name)

        for monitoring_object in MonitoringObject.objects.all():
            for sensor_type in SensorType.objects.all()[:random.randint(0, SensorType.objects.count())]:
                normal_min = 0
                normal_max = 0
                max_per_day = 0

                if sensor_type.name == 'Temperature':
                    normal_min = 15
                    normal_max = 35
                if sensor_type.name == 'Humidity':
                    normal_min = 700
                    normal_max = 800
                if sensor_type.name == 'Gas':
                    max_per_day = 20
                if sensor_type.name == 'Water':
                    max_per_day = 1
                if sensor_type.name == 'Electricity':
                    max_per_day = 10

                Sensor.objects.create(monitoring_object=monitoring_object,
                                      sensor_type=sensor_type,
                                      normal_min=normal_min,
                                      normal_max=normal_max,
                                      max_per_day=max_per_day,
                                      is_active=randint(0, 1))
        fake_datetime_generator = self.generate_continuous_datetimes(datetime(2024, 1, 1, 0, 0),
                                                                     datetime.now())
        sensor_fluid_level = 0

        for sensor in Sensor.objects.all():
            fake_datetime = next(fake_datetime_generator)
            if sensor.sensor_type.the_type == 'moment':
                SensorReading.objects.create(value=randint(sensor.normal_min, sensor.normal_max),
                                             sensor=sensor,
                                             timestamp=fake_datetime)
            if sensor.sensor_type.the_type == 'fluid':
                sensor_fluid_level += randint(0, sensor.max_per_day)
                SensorFluidLevel.objects.create(value=sensor_fluid_level,
                                                sensor=sensor,
                                                timestamp=fake_datetime)
            if sensor.sensor_type.the_type == 'lift':
                LiftSensorEvent.objects.create(current_level=random.randint(1, 10),
                                               current_state=random.choice(['ok', 'failed']),
                                               is_passenger_in_lift=random.choice([True, False]),
                                               are_doors_open=random.choice([True, False]),
                                               sensor=sensor,
                                               timestamp=fake_datetime)
            fake_datetime = next(fake_datetime_generator)
            SensorStatus.objects.create(sensor=sensor,
                                        status=SensorStatus.STATUS_CHOICES[random.randint(0, 1)][0],
                                        timestamp=fake_datetime)

    def run(self):
        self.clear_database()
        self.generate()
