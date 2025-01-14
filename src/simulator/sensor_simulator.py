import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime
import uuid

class SensorSimulator:
    def __init__(self, broker="localhost", port=1883, machine_count=5):
        self.broker = broker
        self.port = port
        self.machine_count = machine_count
        self.client = mqtt.Client()
        self.machine_states = self._initialize_machine_states()

    def _initialize_machine_states(self):
        states = {}
        for i in range(self.machine_count):
            states[f"machine_{i}"] = {
                "baseline_temp": random.uniform(60, 70),
                "baseline_vibration": random.uniform(0.8, 1.2),
                "baseline_pressure": random.uniform(95, 105)
            }
        return states

    def start_simulation(self):
        try:
            self.client.connect(self.broker, self.port, 60)
            print(f"Connected to MQTT broker")
            self.client.loop_start()
            
            while True:
                for machine_id in self.machine_states.keys():
                    self._publish_reading(machine_id)
                time.sleep(1)
                
        except Exception as e:
            print(f"Error: {e}")
            raise