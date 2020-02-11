import random
import threading
import time
import queue
import os
import signal
from multiprocessing import Process,Value

class Market(Process):

    def __init__(self,Temperature_Home_Weather,Lock_Shared_Memory_MHW):
        self.OFFRE = 0
        self.i = 1
        self.j = 1
        self.DEMANDE = 0
        self.achats = 0
        self.ventes = 0
        self.ecarts_achats_ventes = 0
        self.flag_temperature = 0
        self.flag_offre_demande = 0
        with Lock_Shared_Memory_MHW :
            self.TEMPERATURE = Temperature_Home_Weather.value #Température initiale
        self.PRIX = 0.1450 #Prix du Kwh en € moyen initial
        self.LockTemperature = threading.Lock()
        self.LockAchats_Ventes = threading.Lock()
        fichier = open("Prix.txt","w")
        fichier.write(str(self.PRIX)+","+str(self.i)+"\n") #Je l'affiche
        fichier.close()
        fichier = open("Achats_Ventes.txt","w")
        fichier.write(str(self.achats)+","+str(self.ventes)+","+str(self.j)+"\n") #Je l'affiche
        fichier.close()
        print("PID MARKET : ", os.getpid())

    def facteur_temperature(self,):
        with self.LockTemperature:
            copy = self.TEMPERATURE
        return (((7*pow(10,-6)*copy*copy)-(0.0247*copy)+(1.5621)))
        #si flag = 0
        #recuperer température
        # flag = 1

    def update_ventes_achats(self,q_ventes,q_achats):
        while 1:
            time.sleep(1)
            with self.LockAchats_Ventes:
                self.achats = round(q_achats.get(),2)
                self.ventes = round(q_ventes.get(),2)
            q_achats.put(0)
            q_ventes.put(0)
            self.j = self.j + 1
            fichier = open("Achats_Ventes.txt","a+")
            fichier.write(str(self.achats)+","+str(self.ventes)+","+str(self.j)+"\n") #Je l'affiche
            fichier.close()

    def update_temperature (self,Temperature_Home_Weather,Lock_Shared_Memory_MHW): #Mise à jour de la température
        print("Starting thread:",threading.current_thread().name)
        #is flag_temperature == 1 && flag_offre_demande = 0
        while 1 :
            time.sleep(1)
            with Lock_Shared_Memory_MHW :
                with self.LockTemperature:
                    self.TEMPERATURE = Temperature_Home_Weather.value #Température initiale

    def update_prix (self,Temperature_Home_Weather,q_ventes, q_achats): #Mise à jour du prix
        print("Starting thread Market Update_Prix:",threading.current_thread().name)
        while 1 :
            time.sleep(1) # On attend 1s -- Durée d'un jour dans notre programme, prix actualisé toutes les secondes
            print("Market Achats : ",self.achats)
            print("Market Ventes : ",self.ventes)
            with self.LockAchats_Ventes:
                self.ecarts_achats_ventes = self.achats - self.ventes
            self.i = self.i +1
            x = self.facteur_temperature()
            #print(x, "blabla")
            self.PRIX = (((x-1.193175)*self.PRIX)/10000) + self.PRIX + (self.ecarts_achats_ventes/100000)
            if (self.PRIX <= 0):
                self.PRIX = 0
            fichier = open("Prix.txt","a+")
            fichier.write(str(self.PRIX)+","+str(self.i)+"\n") #Je l'affiche
            fichier.close()

    def handler(self,reception,frame):
        print("TREMBLEMENT DE TERRE SUR LYON")
        self.PRIX = self.PRIX + 1

    def run(self,Temperature_Home_Weather,Lock_Shared_Memory_MHW,q_achats,q_ventes):
        t1 = threading.Thread(target=self.update_temperature,args=(Temperature_Home_Weather,Lock_Shared_Memory_MHW))
        t2 = threading.Thread(target=self.update_ventes_achats,args=(q_ventes, q_achats))
        t3 = threading.Thread(target=self.update_prix,args=(Temperature_Home_Weather,q_ventes, q_achats))
        t1.start()
        t2.start()
        t3.start()
        signal.signal(signal.SIGUSR1, self.handler)
        """threading.Thread(target=self.consommation,args=(Temperature_Home_Weather,)).start()
        threading.Thread(target=self.production,args=(Temperature_Home_Weather,)).start()
        threading.Thread(target=self.taux,args=(Temperature_Home_Weather,)).start()"""
#Market --> Processus à lancer en premier
#Suivi de Home
#Suivi de Market
