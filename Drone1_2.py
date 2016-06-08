# -*- coding: utf-8 -*-

#Fichier stocké sur Raspberry Pi, Interface le Drone Terrestre Wifi / R&T Enterprise
#Communication en I²C avec les esclaves arduinos, en correpondance avec la version 3.0 et 3.1
#@author : Clément Courtel, étudiant IUT St-Malo dpt Réseaux et Télécommunication
#@version 2.0.1, MAJ du 27/04

import smbus
import time
i=1

# Remplacer 0 par 1 si nouveau Raspberry
bus = smbus.SMBus(1)

#Plan d'adressage des cartes esclaves
address1 = 0x10 #arduino0Propulsion
address2 = 0x20 #arduino1Direction

#Initialisation des valeurs
m=300
d= 800
klaxon = 21
eclairage = 20
servo_X = 1190
servo_Y = 1390
precision_camera = 4
precision_direction = 5
precision_pwm = 5
delais = 0.1
              
#BOUCLE
print"                  __---~~~~--__                      __--~~~~---__"
print"                `\---~~~~~~~~\\                    //~~~~~~~~---/'" 
print"                  \/~~~~~~~~~\||                  ||/~~~~~~~~~\/ "
print"                              `\\                //'"
print"                                `\\            //'"
print"                                  ||          ||"      
print"                        ______--~~~~~~~~~~~~~~~~~~--______"              
print"                   ___ // _-~                        ~-_ \\ ___ " 
print"                  `\__)\/~                              ~\/(__/'"          
print"                   _--`-___                            ___-'--_  "      
print"                 /~     `\ ~~~~~~~~------------~~~~~~~~ /'     ~\ "       
print"                /|        `\         ________         /'        |\ "    
print"               | `\   ______`\_      \------/      _/'______   /' | "         
print"               |   `\_~-_____\ ~-________________-~ /_____-~_/'   |  "
print"               `.     ~-__________________________________-~     .'   "    
print"               `.      [_______/------|~~|------\_______]      .'"
print"                `\--___((____)(________\/________)(____))___--/'  "         
print"                 |>>>>>>||                            ||<<<<<<|"

print "/-----------------------------------------------------------------------"
print "/----------------------       Bienvenue dans        --------------------"
print "/----------------------    l'interface de pilotage  --------------------"
print "/----------------------              du             --------------------"
print "/----------------------    Drone Terrestre Wifi     --------------------"
print "/----------------------   Version 2.0.1 MAJ 27/04   --------------------"
print "/----------------------         By Clement C.       --------------------"
print "/-----------------------------------------------------------------------"

print""
print""

print"----    z : ^    ----------------  u : Cam H ------------  o : STOP ---"
print" q : <= ---- d : =>  ----  h :Cam G ------ k : Cam D --- l : Leds ---- "
print "-- s : reculer    --------------  j : Cam B  ------------m : Klaxon---"
print ""
print "---- w : L-M1 -- x : L-M2 -- c : Laser"

 

while i==1:
	b = raw_input("Entrez la commande (o : STOP) :") # caractère

	#Affichage sur l'interface
	
	if (b == 'z') : #Avancer
		m = m + precision_pwm
		bus.write_word_data(address1,0x00,m)
		print "11 = Avancer : ", m
		time.sleep(delais)
		reponse = bus.read_byte(address1)
		print "La reponse de l'arduino : ", reponse
	
	elif (b == 's') : #Reculer ralentir
		m = m - precision_pwm
		bus.write_word_data(address1,0x00,m)
		print "13 = Reculer : ", m
		time.sleep(delais)
		reponse = bus.read_byte(address1)
		print "La reponse de l'arduino : ", reponse
	
	elif (b == 'q') : #Virage Gauche
		d = d + precision_direction
		bus.write_word_data(address2,0x00,d)
		print "Gauche : ", d
		time.sleep(delais)
		reponse = bus.read_byte(address2)
		print "La reponse de l'arduino : ", reponse
	
	elif (b == 'd') : #Virage Droite
		d = d - precision_direction
		bus.write_word_data(address2,0x00,d)
		print "Droite : ", d
		time.sleep(delais)
		reponse = bus.read_byte(address2)
		print "La reponse de l'arduino : ", reponse

	elif (b == 'o') : #Arret d'urgence Moteur
		m = 300
		bus.write_word_data(address1,0x00,m)
		print "10 = Arret moteur "
		time.sleep(delais)
		reponse = bus.read_byte(address1)
		print "La reponse de l'arduino : ", reponse
		
	elif (b == 'h') : #Rotation Caméra X +
		servo_X = servo_X + precision_camera
		bus.write_word_data(address2,0x00,servo_X)
		print "16 = Rotation_X : ", servo_X
		time.sleep(delais)
		reponse = bus.read_byte(address2)
		print "La reponse de l'arduino : ", reponse

	elif (b == 'k') : #Rotation Caméra X -
		servo_X = servo_X - precision_camera
		bus.write_word_data(address2,0x00,servo_X)
		print "16 = Rotation_X : ", servo_X
		time.sleep(delais)
		reponse = bus.read_byte(address2)
		print "La reponse de l'arduino : ", reponse

	elif (b == 'u') : #Rotation Caméra Y +
		servo_Y = servo_Y + precision_camera
		bus.write_word_data(address2,0x00,servo_Y)
		print "18 = Rotation_Y : ", servo_Y
		time.sleep(delais)
		reponse = bus.read_byte(address2)
		print "La reponse de l'arduino : ", reponse

	elif (b == 'j') : #Rotation Caméra Y -
		servo_Y = servo_Y - precision_camera
		bus.write_word_data(address2,0x00,servo_Y)
		print "18 = Rotation_Y : ", servo_Y
		time.sleep(delais)
		reponse = bus.read_byte(address2)
		print "La reponse de l'arduino : ", reponse
		
	elif (b == 'w') : #Lance Missile 1
		bus.write_word_data(address2,0x00,22)
		print "20 = Lancement Missile 1 "
		time.sleep(delais)
		reponse = bus.read_byte(address2)
		print "La reponse de l'arduino : ", reponse
		
	elif (b == 'x') : #Lance Missile 2
		bus.write_word_data(address2,0x00,23)
		print "21 = Lancement Missile 2 "
		time.sleep(delais)
		reponse = bus.read_byte(address2)
		print "La reponse de l'arduino : ", reponse
		
	elif (b == 'm') : #Klaxon
		bus.write_word_data(address1,0x00,21)
		print "Klaxon"
		time.sleep(delais)
		reponse = bus.read_byte(address1)
		print "La reponse de l'arduino : ", reponse
		
	
	elif (b== 'l') : #éclairage
		bus.write_word_data(address2,0x00,20)
		print "25 = Allumage éclairage"
		print "26 = Extinction éclairage"
		time.sleep(delais)
		reponse = bus.read_byte(address2)
		print "La reponse de l'arduino : ", reponse
		
	elif (b== 'c') : #laser
		bus.write_word_data(address2,0x00,24)
		print "24 = Allumage Laser"
		time.sleep(delais)
		reponse = bus.read_byte(address2)
		print "Reponse de l'arduino : ", reponse
			
	elif (b=='help') : #onglet paramètrage
		print"----    z : ^    ----------------  u : Cam H ------------  o : STOP ---"
		print" q : <= ---- d : =>  ----  h :Cam G ------ k : Cam D --- l : Leds ---- "
		print "-- s : reculer    --------------  j : Cam B  ------------m : Klaxon---"
		print ""
		print "---- w : L-M1 -- x : L-M2 -- c : Laser"
		print""
		print "Indice moteur m = ", m
		print "Indice direction d =", d
		print "Indice servo X servo_X =",servo_X
		print "Indice servo Y servo_Y =",servo_Y
		print "Incrementation camera =", precision_camera
		print "Incrementation direction =", precision_direction
		print "Incrementation puissance moteur =", precision_pwm
		print "delai = ", delais
		print""