def analyze_temperature(data):
    try:
        temp = float(data.split(":")[1].strip().replace("°C", ""))
        anomaly = "Normal"
        if temp < 36.1:
            anomaly = "Hypothermia"
        elif temp > 37.2:
            anomaly = "Fever"
        return {"temperature": temp, "anomaly": anomaly}
    except Exception as e:
        return {"error": str(e)}
