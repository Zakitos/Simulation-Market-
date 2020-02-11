from multiprocessing import Process,Value
import threading
import time
import random
import calendar


class Weather (Process) :
    def __init__(self,Temperature_Home_Weather,Lock_Shared_Memory_MHW):
        super().__init__() #On invoque le constructeur de la classe mère
        #Je définie un mutex interne à la classe Weather afin d'éviter tout problème de synchronisation
        #On définit les flag qui se mettront à 1
        self.FLAG_DAY = 0
        self.FLAG_bissextile = 0 #L'année actuelle, 2019, n'est pas bissextile, le flag vaut donc 0
        self.Lock = threading.Lock()  #Lock interne pour le FLAG_DAY
        #Compteur de mois,jour,année -- Cela nous aidera à afficher le mois de l'année.
        self.COUNT_DAY = 1 #Jour 1
        self.COUNT_MONTH = 1 #Mois de janvier
        self.COUNT_YEAR = 2019 #Année initiale : 2019
        #Liste des moyennes de températures pour une année -- Les température minimale de l'année : -13°C -- Température Maximale : +33.2 °C -- Quartier de Lyon La Doua
        self.LTMOY = {"Janvier" : 4.7,"Février" : 7.1,"Mars" : 11.5,"Avril" : 17,"Mai" : 21.7,"Juin" : 25.7,"Juillet" : 27.3,"Aout" : 26.6,"Septembre" : 23.3,"Octobre" : 17.2,"Novembre" : 11.4,"Décembre" : 6.5}
        self.LTMIN = {"Janvier" : -12,"Février" : -3,"Mars" : 5.6,"Avril" : 10.8,"Mai" : 15.5,"Juin" : 19.7,"Juillet" : 21.5,"Aout" : 20.5,"Septembre" : 17.1,"Octobre" : 10.4,"Novembre" : 5.5,"Décembre" : -13}
        self.LTMAX = {"Janvier" : 9.7,"Février" : 12.5,"Mars" : 17.5,"Avril" : 23.2,"Mai" : 27.9,"Juin" : 31.7,"Juillet" : 33.2,"Aout" : 32.7,"Septembre" : 29.5,"Octobre" : 24.1,"Novembre" : 17.3,"Décembre" : 11.7}
        self.numberDay = {"Janvier" : (31,31),"Février" : (28,29),"Mars" : (31,30), "Avril" : (30,30),"Mai" : (31,31),"Juin" : (30,30),"Juillet" : (31,31),"Aout" : (31,31),"Septembre" : (30,30),"Octobre" : (31,31),"Novembre" : (30,30),"Décembre" :(31,31)}
        self.allMonth = ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"]
        #Initialisation de la température -- On écrit directement dans la mémoire partagée
        self.i = 1
        with Lock_Shared_Memory_MHW :
            Temperature_Home_Weather.value = self.LTMOY[self.allMonth[self.COUNT_DAY - 1]] # Initialisation de la température à 4.7°C
            copy = Temperature_Home_Weather.value
        fichier = open("Temperature.txt","w")
        fichier.write(str(copy)+","+str(self.i)+"\n") #Je l'affiche
        fichier.close()

#Méthodes Intérmédiaires :

    # Is_Bissextile : Permet de checker si l'année actuelle est bissextile ou non
    def Is_Bissextile (self):
        if (calendar.isleap(self.COUNT_YEAR)):
            self.FLAG_bissextile = 1
        else :
            self.FLAG_bissextile = 0

    # Show_Temperature : Fonction permettant d'écrire dans un fichier les info de temps et de température
    def write_Temperature(self,Temperature_Home_Weather,Lock_Shared_Memory_MHW):
        self.i = self.i + 1
        with Lock_Shared_Memory_MHW :
            Temperature_Home_Weather.value = round(random.uniform(self.LTMIN[self.allMonth[self.COUNT_MONTH-1]] , self.LTMAX[self.allMonth[self.COUNT_MONTH-1]]),2) #Je réactualise la température
            copy = Temperature_Home_Weather.value
            fichier = open("Temperature.txt","a+")
            fichier.write(str(copy)+","+str(self.i)+"\n") #Je l'affiche
            fichier.close()
#Méthodes s'éxecutant en parralèlles -- 2 thread

    # UPDATE_FLAG_DAY : Thread invoqué mettant FLAG_DAY à 1 toutes les (5/30) secondes . Cette Valeur correspond à la durée d'une journée
    def update_flag_day (self):
        print("Starting thread:",threading.current_thread().name)
        while 1:
                time.sleep(1) # On attend 1s -- Durée d'un jour dans notre programme
                with self.Lock: #MUTEX
                    self.FLAG_DAY = 1

    #UPDATE_TEMPERATURE : Thread invoqué qui permettera de gérer la température et de l'actualiser en fonction de l'état des flags.
    def update_Temperature(self,Temperature_Home_Weather,Lock_Shared_Memory_MHW):
        print("Starting thread:",threading.current_thread().name)
        #print("Année : ",self.COUNT_YEAR,"Mois : ",self.allMonth[self.COUNT_MONTH-1]," Jour n°",self.COUNT_DAY," Température :",self.Temperature, " °C")
        while 1 :
            with self.Lock:
                copy = self.FLAG_DAY
            if(copy == 1): #(5/30)s se sont écoulés, on change de jour
                self.COUNT_DAY = self.COUNT_DAY + 1 #Je passe au jours suivant
                if(self.COUNT_DAY == self.numberDay[self.allMonth[self.COUNT_MONTH-1]][self.FLAG_bissextile] + 1): #Si on atteint le jour de fin de mois + 1
                    self.COUNT_DAY = 1 # Je passe au jour 1
                    self.COUNT_MONTH = self.COUNT_MONTH + 1 #Je passe au mois d'après
                    if (self.COUNT_MONTH == 13): #Si le mois est 13 --> Année prochaine
                        self.COUNT_MONTH = 1; # Je repasse au mois de Janvier
                        self.COUNT_YEAR = self.COUNT_YEAR + 1; #Je passe à l'année suivante
                        self.Is_Bissextile()
                    self.write_Temperature(Temperature_Home_Weather,Lock_Shared_Memory_MHW)
                else: #Si on est encore dans le mois en cours
                    self.write_Temperature(Temperature_Home_Weather,Lock_Shared_Memory_MHW)
                with self.Lock:
                    self.FLAG_DAY = 0 # Une fois que j'ai mis à jour la température, je remet mon flag à 0

    def run(self,Temperature_Home_Weather,Lock_Shared_Memory_MHW):
        a = threading.Thread(target=self.update_flag_day)
        b = threading.Thread(target=self.update_Temperature,args=(Temperature_Home_Weather,Lock_Shared_Memory_MHW))
        a.start()
        b.start()
