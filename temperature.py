def analyze_temperature(data):
    try:
        temp = float(data.split(":")[1].strip().replace("°C", ""))
        anomaly = "Normal"
        if temp < 35.0:
            anomaly = "Hypothermia"
        elif temp > 38.0:
            anomaly = "Fever"
        return {"temperature": temp, "anomaly": anomaly}
    except Exception as e:
        return {"error": str(e)}
