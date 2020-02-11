import random
import threading
import time
from multiprocessing import Process,Value
class Home(Process):

    def __init__(self,nom,Temperature_Home_Weather,Lock_Shared_Memory_MHW, politique):
        self.NOM = nom
        self.NUM_POL = politique
        if (self.NUM_POL == 0):
            self.NAME_POLITIQUE = "COMMUNISTE"
        elif (self.NUM_POL == 1):
            self.NAME_POLITIQUE = "CAPITALISTE"
        else:
            self.NAME_POLITIQUE = "Libéral"
        self.NB_INSTALLATION = random.randint(1,5)
        self.NB_MENAGE = random.randint(1, 8)
        with Lock_Shared_Memory_MHW :
            self.TEMPERATURE = Temperature_Home_Weather.value
        self.NB_CONSOMMATION = 0
        self.NB_PRODUCTION = 0
        self.DEMANDE = 0
        self.STOCKAGE = 0
        self.LOCK_CONSOMMATION = threading.Lock()
        self.LOCK_PRODUCTION = threading.Lock()
        self.LockTemperature = threading.Lock()
        self.TAUX_CONSOMMATION = 1
        self.ETAT = ""
        print(self.NOM, " : ")
        print("--> Nombres d'installation photovolatiques : ",self.NB_INSTALLATION)
        print("--> Nombre de ménages dans le foyer :", self.NB_MENAGE)
        print("--> Politique : ", self.NAME_POLITIQUE)
    def consommation(self) :
        print("Starting thread:",threading.current_thread().name)
        while 1:
            alpha = 7**(-6) * self.TEMPERATURE - 0.0247 * self.TEMPERATURE + 1.5621 #temperature à récuperer
            self.LOCK_CONSOMMATION.acquire()
            self.NB_CONSOMMATION = round(self.NB_MENAGE * alpha * 3.011, 2)
            self.LOCK_CONSOMMATION.release()
            time.sleep(1)
    def production(self) :
        print("Starting thread:",threading.current_thread().name)
        while 1:
            self.LOCK_PRODUCTION.acquire()
            self.NB_PRODUCTION = round(random.uniform(2.72, 3.83) * self.NB_INSTALLATION, 2)
            self.LOCK_PRODUCTION.release()
            time.sleep(1)

    def taux(self,q_don, q_demandes, q_ventes, q_achats) :
        print("Starting thread:",threading.current_thread().name)
        while 1:
            time.sleep(1)
            with self.LOCK_PRODUCTION:
                with self.LOCK_CONSOMMATION:
                    self.TAUX_CONSOMMATION = round(self.NB_CONSOMMATION - self.NB_PRODUCTION, 2)
                    copy = self.TAUX_CONSOMMATION
            if self.TAUX_CONSOMMATION > 0:
                self.ETAT = "deficit"
            else :
                self.ETAT = "exces"

            print(self.NOM, " conso ", self.NB_CONSOMMATION, "prod ", self.NB_PRODUCTION)

            if self.NUM_POL == 0: #communiste
                if self.ETAT == "exces":
                    self.give(-1*self.TAUX_CONSOMMATION, q_don) #donne aux autres maisons
                    print(self.NOM, " (communiste) donne ", -self.TAUX_CONSOMMATION)
                else:
                    s = q_don.get()
                    q_don.put(s)
                    self.give(self.TAUX_CONSOMMATION, q_demandes) #ajoute une demande
                    print(self.NOM, " (communiste) fait une demande ")
                    time.sleep(0.1) #attend 100ms
                    print(self.NOM, " (communiste) attend 100 ms")
                    if self.TAUX_CONSOMMATION <= s:
                        self.give(self.TAUX_CONSOMMATION, q_don) #il y assez, il prend le don
                        print(self.NOM, " (communiste) prend ", self.TAUX_CONSOMMATION)
                    else:
                        if s < self.TAUX_CONSOMMATION and s > 0:
                            self.give(s, q_don) #prend ce qu'il y a
                            print(self.NOM, " (communiste) prend", s)
                            print("Il manque ", (self.TAUX_CONSOMMATION-s), self.NOM, " va sur le marché")
                            self.give((self.TAUX_CONSOMMATION-s), q_achats)
                            print(self.NOM, " (communiste) achete ", (self.TAUX_CONSOMMATION-s))
                        else:
                            print("Il n'ya pas assez d'energie disponible dans don, ", self.NOM, " va sur le marché")
                            self.give(self.TAUX_CONSOMMATION, q_achats)
                            print(self.NOM, " (communiste) achete ", self.TAUX_CONSOMMATION)
                    self.give(-self.TAUX_CONSOMMATION, q_demandes) #retrait demande

            if self.NUM_POL == 1:
                if self.ETAT == "exces":
                    print(self.NOM, " (capitaliste) vend ", -self.TAUX_CONSOMMATION)
                    self.give(-self.TAUX_CONSOMMATION, q_ventes) #vend sur le marché
                else:
                    print(self.NOM, " (capitaliste) achete ", self.TAUX_CONSOMMATION)
                    self.give(self.TAUX_CONSOMMATION, q_achats) #achete sur le marché

            if self.NUM_POL == 2:
                if self.ETAT == "exces":
                    if (q_demandes.empty() or q_demandes.get() == 0) :
                        self.give(-self.TAUX_CONSOMMATION, q_ventes) #pas de demande, vend sur le marché
                        print("pas de demande", self.NOM, " (mixte) vend ", -self.TAUX_CONSOMMATION)
                    else:
                        self.give(-self.TAUX_CONSOMMATION, q_don) #il y a demande, don
                        print("il y a une demande", self.NOM, " (mixte) donne ", -self.TAUX_CONSOMMATION)
                else:
                    s = q_don.get()
                    q_don.put(s)
                    self.give(self.TAUX_CONSOMMATION, q_demandes) #ajout demande
                    print(self.NOM, " (mixte) demande ", self.TAUX_CONSOMMATION)
                    time.sleep(0.1) #attend 100 ms
                    print(self.NOM, " (mixte) attend 100 ms")
                    if self.TAUX_CONSOMMATION <= s:
                        self.give(self.TAUX_CONSOMMATION, q_don) #il y assez, il prend le don
                        print(self.NOM, " (mixte) prend ", self.TAUX_CONSOMMATION)
                    else:
                        if s < self.TAUX_CONSOMMATION and s > 0 :
                            self.give(s, q_don) #prend ce qu'il y a
                            print(self.NOM, " (mixte) prend ", s)
                            print("Il manque ", (self.TAUX_CONSOMMATION-s) ,self.NOM, " va  sur le marché")
                            self.give((self.TAUX_CONSOMMATION-s), q_achats) #achete ce qui manque
                            print(self.NOM, " (mixte) achete ", (self.TAUX_CONSOMMATION-s))
                        else:
                            print("Il n'y a pas assez d'energie disponible dans don, ",self.NOM, " va  sur le marché")
                            self.give(self.TAUX_CONSOMMATION, q_achats) #achete tout sur le marché
                            print(self.NOM, " (mixte) achete ", self.TAUX_CONSOMMATION)
                    self.give(-self.TAUX_CONSOMMATION, q_demandes) #retrait demande


    def give(self, n, queue):
        s = queue.get()
        queue.put(s + n)

    def update_temperature(self,Temperature_Home_Weather,Lock_Shared_Memory_MHW):
        print("Starting thread:",threading.current_thread().name)
        while 1 :
            time.sleep(1)
            with Lock_Shared_Memory_MHW :
                with self.LockTemperature:
                    self.TEMPERATURE = Temperature_Home_Weather.value #Température initiale

    def run(self,Temperature_Home_Weather, Lock_Shared_Memory_MHW, q_don, q_demandes, q_ventes, q_achats):
        t1 = threading.Thread(target=self.update_temperature,args=(Temperature_Home_Weather,Lock_Shared_Memory_MHW))
        t2 = threading.Thread(target=self.consommation)
        t3 = threading.Thread(target=self.production)
        t4 = threading.Thread(target=self.taux,args=(q_don, q_demandes, q_ventes, q_achats))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
