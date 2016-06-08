/*
   Code arduino N1 pour le Drone Terrestre Wifi / R&T Enterprise
   Fonctions de direction, rotation caméra, éclairage avant, lance-missile
   Communication en I²C avec le Rpi
   @author : Clément Courtel, étudiant IUT St-Malo dpt Réseaux et Télécommunications
   @version : 3.1.2, 
   MAJ du 30/04 : Direction par servoMoteur
*/

#include <Servo.h>  // bibliothèque Servomoteur caméra
#include <Wire.h> // bibliothèque I2C
#define SLAVE_ADDRESS 0x20 // adresse esclave

Servo servo1;  // servo1_cameraX
Servo servo2;  // servo2_cameraY
Servo servo3; //servo3_missile
Servo servo4; //servo4_Direction

int dR[3], s; //Variables reçu de l'I²C
int a; //Valeur s mappé

boolean f = 0, l=0; // état des feux/laser avants
char i ; //indice tableau
char ack; //valeur s'acquittement

void setup() {
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  servo1.attach(4); // caméra X
  servo2.attach(3); // caméra Y
  servo4.attach(7); // Direction
  servo3.attach(8); // lance missile


  pinMode(6, OUTPUT); // Lumière avant
  pinMode(9, OUTPUT); // Laser

  servo1.write(90); // initialisation du servo X à 90°
  servo2.write(90); // initialisation du servo Y à 90°
  servo3.write(90); // initialisation lance-missile à 90°
  servo4.write(90); 

}

void loop() {
  // Remise à 0 de l'indice du tableau
  i = 0;

  // Si la valeur est comprise entre 640 et 1360, tranche direction
  if ((s >= 600) && (s<=700)){
    a = map(s,600,700,40,140);
    servo4.write(a);
    ack = 14;
    s=0;
  }
    
  else if ((s >= 1100) && (s <= 1280)) { // Caméra_X
    a = map(s,1100,1280,0,180);
    servo1.write(a); // positionnement = pin 4
    ack = 16; 
    s=0;
  }

  else if ((s >= 1300) && (s <= 1480)){ // Caméra_ Y
    a = map(s, 1300, 1480, 0, 180); //redéfinie dR entre 0 et 180
    servo2.write(a); // positionnement = pin 5
    ack = 18;
    s = 0;
  }

  else if (s == 20){ // éclairage
    f = !f;
    digitalWrite(6, f);
      if (f == 0){ack = 26;}
      else {ack = 25;}
    s = 0;
  } 
  else if (s==22){ // Missile 1 
    servo3.write(0);
    ack = 20;
  }
  else if (s ==23){ // Missile 2
    servo3.write(180);
    ack = 21;
  }
  else if (s==24){ //Laser
    l = !l;
    digitalWrite(9,l);
      if (l == 0){ack = 24;}
      else {ack = 23;}
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

