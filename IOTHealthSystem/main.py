from flask import Flask, jsonify, render_template
from IOTHealthSystem.temperature import analyze_temperature
from IOTHealthSystem.heartrate import analyze_heart_rate
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Stockage temporaire des données
data_store = {"temperature": None, "heartrate": None}

# Callback MQTT
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    if topic == "iot/temperature":
        data_store["temperature"] = float(payload)
    elif topic == "iot/heartrate":
        data_store["heartrate"] = int(payload)
    elif topic == "iot/spo2":  # Ajout du SpO2
        data_store["spo2"] = float(payload)


def on_connect(client, userdata, flags, rc):
    print("Connecté au broker MQTT")
    client.subscribe("iot/temperature")
    client.subscribe("iot/heartrate")
    client.subscribe("iot/spo2")


# Configurer MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1884, 60)
mqtt_client.loop_start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/temperature", methods=["GET"])
def get_temperature():
    temp = data_store["temperature"]
    if temp is not None:
        return jsonify(analyze_temperature(f"Temperature: {temp} °C"))
    return jsonify({"error": "No temperature data available"})

@app.route("/heartrate", methods=["GET"])
def get_heartrate():
    bpm = data_store["heartrate"]
    if bpm is not None:
        return jsonify(analyze_heart_rate(f"BPM: {bpm}"))
    return jsonify({"error": "No heart rate data available"})

@app.route("/spo2", methods=["GET"])
def get_spo2():
    spo2 = data_store.get("spo2")  # Assurez-vous que 'spo2' est bien dans `data_store`
    if spo2 is not None:
        return jsonify({"spo2": spo2})
    return jsonify({"error": "No SpO2 data available"})


if __name__ == "__main__":
    app.run(debug=True)
