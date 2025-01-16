from flask import Flask, jsonify, render_template
import paho.mqtt.client as mqtt
from send_alerte import send_email

app = Flask(__name__)

# Données des capteurs
data = {"temperature": "--", "heartrate": "--", "spo2": "--"}
alert_status = {"alert_sent": False, "parameter": None}  # Statut d'alerte
anomaly_count = {"count": 0}  # Compteur global des anomalies

# État des anomalies signalées
anomalies_reported = {"temperature": False, "heartrate": False, "spo2": False}

# Vérification des anomalies
def check_anomalies():
    global anomaly_count
    anomalies = []

    # Température
    if data["temperature"] != "--":
        temp = float(data["temperature"])
        if temp < 36.1 or temp > 37.2:
            if not anomalies_reported["temperature"]:  # Nouvelle anomalie détectée
                anomalies.append(f"Température : {temp} °C")
                anomalies_reported["temperature"] = True
                anomaly_count["count"] += 1
                alert_status["alert_sent"] = True
                alert_status["parameter"] = "Température"
        else:
            anomalies_reported["temperature"] = False  # Réinitialiser si normal

    # Fréquence cardiaque
    if data["heartrate"] != "--":
        heartrate = int(data["heartrate"])
        if heartrate < 60 or heartrate > 100:
            if not anomalies_reported["heartrate"]:  # Nouvelle anomalie détectée
                anomalies.append(f"Fréquence cardiaque : {heartrate} BPM")
                anomalies_reported["heartrate"] = True
                anomaly_count["count"] += 1
                alert_status["alert_sent"] = True
                alert_status["parameter"] = "Fréquence cardiaque"
        else:
            anomalies_reported["heartrate"] = False  # Réinitialiser si normal

    # SpO₂
    if data["spo2"] != "--":
        spo2 = float(data["spo2"])
        if spo2 < 90:
            if not anomalies_reported["spo2"]:  # Nouvelle anomalie détectée
                anomalies.append(f"Saturation en oxygène : {spo2} %")
                anomalies_reported["spo2"] = True
                anomaly_count["count"] += 1
                alert_status["alert_sent"] = True
                alert_status["parameter"] = "Saturation en oxygène"
        else:
            anomalies_reported["spo2"] = False  # Réinitialiser si normal

    # Envoyer un email si des anomalies sont détectées
    if anomalies:
        subject = "Alerte : Anomalies détectées"
        body = "Les anomalies suivantes ont été détectées :\n\n" + "\n".join(anomalies)
        send_email(subject, body, "nsiparadise@gmail.com")
        print("Anomalie détectée et email envoyé.")

# MQTT Callback Functions
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()

    if topic == "iot/temperature":
        data["temperature"] = payload
    elif topic == "iot/heartrate":
        data["heartrate"] = payload
    elif topic == "iot/spo2":
        data["spo2"] = payload

    check_anomalies()

client = mqtt.Client()
client.on_message = on_message
client.connect("localhost", 1884, 60)
client.subscribe("iot/#")
client.loop_start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data')
def api_data():
    return jsonify(data)

@app.route('/api/anomaly_count')
def api_anomaly_count():
    return jsonify(anomaly_count)

@app.route('/api/alert_status')
def api_alert_status():
    # Réinitialiser après récupération
    status = alert_status.copy()
    alert_status["alert_sent"] = False
    alert_status["parameter"] = None
    return jsonify(status)

if __name__ == '__main__':
    app.run(debug=True)
