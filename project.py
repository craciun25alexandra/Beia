# Exemplu simplu pentru un dispozitiv Raspberry Pi care trimite date prin MQTT

import time
import random
import json
import paho.mqtt.client as mqtt

# Configurații pentru broker MQTT
mqtt_broker = "mqtt.beia-telemetrie.ro"
mqtt_port = 1883
mqtt_topic = "/training/device/alexandra-craciun/"

# Funcție pentru a simula datele de la senzori
def generate_sensor_data():
    sensor_data = {
        'temperature' : round(random.uniform(20, 43)),
        'glucose_level' : round(random.uniform(50, 140)) 
    }
    return sensor_data

# Funcție callback pentru a gestiona conexiunea la broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectat la broker MQTT cu codul:", rc)
    client.subscribe(mqtt_topic)

# Funcție callback pentru a gestiona primirea mesajelor MQTT
def on_message(client, userdata, msg):
    print("Mesaj primit de la broker MQTT:", msg.payload.decode())

# Inițializare client MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Conectare la broker MQTT
mqtt_client.connect(mqtt_broker, mqtt_port, keepalive=60)

# Începe bucla de ascultare pentru mesaje
mqtt_client.loop_start()

# Simulare trimitere date periodice prin MQTT
try:
    while True:
        sensor_data = generate_sensor_data()
        mqtt_client.publish(mqtt_topic, json.dumps(sensor_data))
        print("Date trimise prin MQTT:", sensor_data)
        time.sleep(5)  # Trimite datele la fiecare 5 secunde

except KeyboardInterrupt:
    print("Oprire manuală.")

finally:
    mqtt_client.disconnect()
    mqtt_client.loop_stop()
