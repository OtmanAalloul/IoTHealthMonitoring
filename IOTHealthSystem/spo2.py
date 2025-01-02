def analyze_spo2(data):
    try:
        # Extraire la valeur de SpO2
        spo2 = float(data.split(":")[1].strip().replace("%", "").strip())  # Convertir en float
        spo2 = round(spo2)  # Arrondir à l'entier le plus proche
        anomaly = "Normal"
        if spo2 < 90:
            anomaly = "Hypoxia"
        elif spo2 > 100:
            anomaly = "Possible Error"  # Gérer des valeurs irréalistes
        return {"spo2": spo2, "anomaly": anomaly}
    except Exception as e:
        return {"error": str(e)}
