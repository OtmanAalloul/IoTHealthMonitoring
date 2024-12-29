import serial
import paho.mqtt.client as mqtt
import time
import serial.tools.list_ports

# Configuration du port série
serial_port = "COM5"  # Vérifiez que COM5 est disponible
baud_rate = 115200

# Configuration MQTT
broker = "localhost"  # Utilisez localhost si Mosquitto est sur votre machine
port = 1883
temperature_topic = "iot/temperature"
heartrate_topic = "iot/heartrate"

# Connexion au broker MQTT
client = mqtt.Client()
client.connect(broker, port, 60)

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
