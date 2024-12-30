#define USE_ARDUINO_INTERRUPTS true
#include <PulseSensorPlayground.h>

const int PulseWire = A0;  // Capteur de rythme cardiaque connecté à A0
const int TempPin = A1;    // Capteur de température connecté à A1
const int LED13 = 13;      // LED intégrée sur la broche 13
int Threshold = 550;       // Seuil de détection pour le rythme cardiaque

PulseSensorPlayground pulseSensor;

void setup() {
  Serial.begin(115200);          // Initialisation de la communication série
  pulseSensor.analogInput(PulseWire);
  pulseSensor.blinkOnPulse(LED13);
  pulseSensor.setThreshold(Threshold);

  if (pulseSensor.begin()) {
    Serial.println("Capteur initialisé !");
  }
}

float calculateSpo2(int bpm) {
  // Simulation de la valeur SpO2 en fonction du BPM
  // Valeur SpO2 normale : 95% - 100%
  // On peut supposer que pour des BPM extrêmes (<50 ou >120), la SpO2 diminue

  if (bpm < 50) {
    return 90.0 + random(-2, 3);  // Simulation d'une SpO2 réduite
  } else if (bpm > 120) {
    return 92.0 + random(-3, 2);  // Simulation d'une SpO2 légèrement réduite
  } else {
    return 95.0 + random(-1, 5);  // Simulation de SpO2 normale
  }
}

void loop() {
  // Lire la température depuis le capteur LM35
  int tempRaw = analogRead(TempPin);                 // Lire la valeur brute de température
  float voltage = tempRaw * (5.0 / 1024.0);          // Convertir la valeur brute en tension
  float temperature = voltage * 100;                // Convertir la tension en température (°C)

  // Calculer le BPM
  int myBPM = pulseSensor.getBeatsPerMinute();       // Lire le BPM
  if (pulseSensor.sawStartOfBeat()) {
    Serial.println("♥ Battement détecté !");
  }

  // Simuler la valeur SpO2
  float spo2 = calculateSpo2(myBPM);

  // Afficher la température, le BPM et la SpO2
  Serial.print("Temperature : ");
  Serial.print(temperature);
  Serial.println(" °C");

  Serial.print("BPM : ");
  Serial.println(myBPM);

  Serial.print("SpO2 : ");
  Serial.print(spo2);
  Serial.println(" %");

  delay(1000); // Pause d'une seconde pour actualiser les valeurs
}
