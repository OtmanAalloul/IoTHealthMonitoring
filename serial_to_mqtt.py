import serial
import paho.mqtt.client as mqtt
import time
import serial.tools.list_ports
from spo2 import analyze_spo2

# Configuration du port série
serial_port = "COM5"  # Vérifiez que COM5 est disponible
baud_rate = 115200

# Configuration MQTT
broker = "localhost"  # Utilisez localhost si Mosquitto est sur votre machine
port = 1883
temperature_topic = "iot/temperature"
heartrate_topic = "iot/heartrate"
spo2_topic = "iot/spo2"  # Nouveau topic pour SpO2

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
                    if "Temperature" in line:
                        temp = line.split(":")[1].strip().replace("°C", "")
                        client.publish(temperature_topic, temp)
                        print(f"Température publiée : {temp} °C")
                    elif "BPM" in line:
                        bpm = line.split(":")[1].strip()
                        client.publish(heartrate_topic, bpm)
                        print(f"BPM publié : {bpm}")
                    elif "SpO2" in line:
                        spo2_data = analyze_spo2(line)
                        if "spo2" in spo2_data:
                            client.publish(spo2_topic, spo2_data["spo2"])
                            print(f"SpO2 publié : {spo2_data['spo2']} % - Anomalie : {spo2_data['anomaly']}")
                        else:
                            print(f"Erreur dans les données SpO2 : {spo2_data['error']}")
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
