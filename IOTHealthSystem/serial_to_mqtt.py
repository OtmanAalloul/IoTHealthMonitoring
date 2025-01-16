import serial
import paho.mqtt.client as mqtt
import time

# Configuration du port série
serial_port = "COM5"  # Vérifiez que COM5 est disponible
baud_rate = 115200

# Configuration MQTT
broker = "localhost"  # Utilisez localhost si Mosquitto est sur votre machine
port = 1884
temperature_topic = "iot/temperature"
heartrate_topic = "iot/heartrate"
spo2_topic = "iot/spo2"

# Connexion au broker MQTT
client = mqtt.Client()
try:
    client.connect(broker, port, 60)
    print(f"Connecté au broker MQTT sur {broker}:{port}.")
except Exception as e:
    print(f"Erreur de connexion au broker MQTT : {e}")
    exit()

# Connexion au port série
try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    print(f"Connecté au port série {serial_port} avec un baud_rate de {baud_rate}.")
except Exception as e:
    print(f"Erreur de connexion au port série : {e}")
    ser = None

# Lecture et publication des données
if ser:
    try:
        while True:
            if ser.in_waiting > 0:  # Vérifie si des données sont disponibles
                try:
                    line = ser.readline().decode('utf-8').strip()
                    print(f"Données reçues : {line}")

                    # Split the line into key-value pairs
                    parts = line.split(";")
                    data = {}
                    for part in parts:
                        key, value = part.split(":")
                        data[key.strip()] = value.strip()

                    # Publish each value to its respective topic
                    if "Temperature" in data:
                        client.publish(temperature_topic, data["Temperature"])
                        print(f"Température publiée : {data['Temperature']} °C")

                    if "BPM" in data:
                        client.publish(heartrate_topic, data["BPM"])
                        print(f"BPM publié : {data['BPM']}")

                    if "SpO2" in data:
                        client.publish(spo2_topic, data["SpO2"])
                        print(f"SpO2 publié : {data['SpO2']} %")

                except Exception as e:
                    print(f"Erreur lors de la lecture ou de la publication : {e}")
            else:
                time.sleep(0.1)  # Pause pour éviter de consommer trop de ressources
    except KeyboardInterrupt:
        print("\nInterruption du script. Fermeture des connexions...")
        ser.close()
        client.disconnect()
        print("Connexions fermées proprement.")
else:
    print("Impossible de se connecter au port série. Vérifiez votre configuration.")
