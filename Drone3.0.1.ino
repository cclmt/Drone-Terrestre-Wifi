/*
   Code arduino N0 pour le Drone Terrestre Wifi / R&T Enterprise
   Fonctions de propulsion PWM, signalement lumineux , capteur ultrason, klaxon
   Communication en I²C avec le Rpi (programme 2.0.1)
   @author : Clément Courtel, étudiant IUT St-Malo dpt Réseaux et Télécommunications
   @version : 3.0.1, MAJ du 27/04
*/

#include <Wire.h> // bibliothèque I2C
#include <NewPing.h> // bibliothèque pour capteur ultrason
#define SLAVE_ADDRESS 0x10 // adresse esclave

NewPing sonar(8, 9, 200); // TRIGERS -  ECHO -- Distancemax

char ack; // Variable qui contient la valeur d'acquittement, voir rapport
int dR[3], s; // Valeurs reçu de l'I²C
int a; // Valeur s mappée
char i;

void setup() {
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  pinMode(3, OUTPUT); // marche AR
  pinMode(5, OUTPUT); // Marche AV
  pinMode(2, OUTPUT); // Leds Rouges
  pinMode(4, OUTPUT); // Led Blanche
  pinMode(10, OUTPUT); //Buzzer
}

void loop() {
  // Remise à 0 de l'indice du tableau
  i = 0;

  // Si la valeur reçu est 0 alors le moteur s'arrête, les leds Stop s'alluments
  if (s == 0 || s == 300) {
    digitalWrite(5, 0);
    digitalWrite(3, 0);
    digitalWrite(4, LOW);
    digitalWrite(2, HIGH);
    ack = 10;
  }

  // Si la valeur reçu est comprise entre 301 et 550, il y a vérification des distances puis une possible marche avant
  else if ((s >= 301) && (s <= 550))
  {
    if (sonar.ping_cm() < 10) {
      ack = 12;
      s = 0;
    }
    else {
      a = map(s, 301, 550, 50, 235); // Limitation de vitesse logiciel
      analogWrite(5, a);
      analogWrite(3, 0);
      digitalWrite(4, LOW);
      digitalWrite(2, LOW);
      ack = 11;
    }
  }
  // Si la valeur est comprise entre 50 et 299, il y a marche arrière
  else if ((s >= 50) && (s <= 299)) {
    a = map(s, 50, 299, 50, 235); // Limitation de vitesse logiciel
    analogWrite(5, 0);
    analogWrite(3, a);
    digitalWrite(4, HIGH);
    digitalWrite(2, LOW);
    ack = 13;
  }

  else if (s==21){
    buzz(10, 2500, 1000); // buzz the buzzer on pin 4 at 2500Hz for 1000 milliseconds
    s=0;
  }
}

void receiveData(int byteCount) {
  while (Wire.available()) {
    dR[i] = Wire.read();
    i++;
  }
  s = dR[1] + dR[2] * 256;
}

void sendData() {
  Wire.write(ack);
}

void buzz(int targetPin, long frequency, long length) {
  
  long delayValue = 1000000/frequency/2; // calculate the delay value between transitions
  //// 1 second's worth of microseconds, divided by the frequency, then split in half since
  //// there are two phases to each cycle
  
  long numCycles = frequency * length/ 1000; // calculate the number of cycles for proper timing
  
  //// multiply frequency, which is really cycles per second, by the number of seconds to
  //// get the total number of cycles to produce
  
 for (long i=0; i < numCycles; i++){ // for the calculated length of time...
    digitalWrite(targetPin,HIGH); // write the buzzer pin high to push out the diaphram
    delayMicroseconds(delayValue); // wait for the calculated delay value
    digitalWrite(targetPin,LOW); // write the buzzer pin low to pull back the diaphram
    delayMicroseconds(delayValue); // wait againf or the calculated delay value
  }

}

