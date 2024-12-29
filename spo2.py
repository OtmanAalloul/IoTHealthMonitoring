def analyze_spo2(data):
    try:
        spo2 = int(data.split(":")[1].strip().replace("%", ""))
        anomaly = "Normal"
        if spo2 < 90:
            anomaly = "Hypoxia"
        return {"spo2": spo2, "anomaly": anomaly}
    except Exception as e:
        return {"error": str(e)}
