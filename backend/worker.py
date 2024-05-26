# Define your API endpoint

# Define your API endpoint

import random
# Define your API endpoint
import threading
import time

import requests

# Define your API endpoint
API_BASE_URL = 'http://127.0.0.1:8000/structure/'

# Define the event types and their corresponding serializer classes
EVENT_TYPES = {
    'SensorReading': {'serializer': 'SensorReadingSerializer', 'url': 'sensor-readings'},
    'SensorStatus': {'serializer': 'SensorStatusSerializer', 'url': 'sensor-statuses'},
    'LiftSensorEvent': {'serializer': 'LiftSensorEventSerializer', 'url': 'lift-sensor-events'}
}

# Define the number of events to generate in each iteration
NUM_EVENTS = 15


# Function to get a random sensor ID from the database
def get_random_sensor_id():
    try:
        # Fetch all sensor IDs from the database or your API
        response = requests.get(API_BASE_URL + 'sensors/')
        if response.status_code == 200:
            sensor_ids = [sensor['id'] for sensor in response.json()]
            return random.choice(sensor_ids)
        else:
            print(f"Failed to fetch sensor IDs. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred while fetching sensor IDs: {str(e)}")
    return None


# Function to generate random events
def generate_events():
    events = []
    for _ in range(NUM_EVENTS):
        event_type = random.choice(list(EVENT_TYPES.keys()))
        event_data = generate_event_data(event_type)
        events.append({'event_type': event_type, 'event_data': event_data})
    return events


# Function to generate event data based on event type
def generate_event_data(event_type):
    if event_type == 'SensorReading':
        return {
            'sensor': get_random_sensor_id(),
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'value': random.uniform(0, 100)
        }
    elif event_type == 'SensorStatus':
        return {
            'sensor': get_random_sensor_id(),
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'status': random.choice(['on', 'off'])
        }
    elif event_type == 'LiftSensorEvent':
        return {
            'sensor': get_random_sensor_id(),
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'current_level': random.randint(1, 10),
            'current_state': random.choice(['ok', 'failed']),
            'is_passenger_in_lift': random.choice([True, False]),
            'are_doors_open': random.choice([True, False])
        }


# Function to send events to the API
def send_events(events):
    for event in events:
        event_type = event['event_type']
        event_data = event['event_data']
        serializer_name = EVENT_TYPES[event_type]['serializer']
        endpoint = EVENT_TYPES[event_type]['url']
        try:
            response = requests.post(API_BASE_URL + endpoint + '/',
                                     data = event_data)
            if response.status_code == 201:
                print(f"Event ({event_type}) added successfully.")
            else:
                print(f"Failed to add event ({event_type}). Status code: {response.status_code}")
        except Exception as e:
            print(f"Error occurred while adding event ({event_type}): {str(e)}")


# Function to periodically generate and send events
def generate_and_send_events(interval):
    while True:
        events = generate_events()
        send_events(events)
        time.sleep(interval)


# Start a thread for generating and sending events
if __name__ == "__main__":
    interval = 5  # seconds, adjust as needed
    event_thread = threading.Thread(target=generate_and_send_events, args=(interval,))
    event_thread.start()
