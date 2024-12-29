def analyze_heart_rate(data):
    try:
        bpm = int(data.split(":")[1].strip().replace("BPM", ""))
        anomaly = "Normal"
        if bpm < 60:
            anomaly = "Bradycardia"
        elif bpm > 100:
            anomaly = "Tachycardia"
        return {"heartrate": bpm, "anomaly": anomaly}
    except Exception as e:
        return {"error": str(e)}
