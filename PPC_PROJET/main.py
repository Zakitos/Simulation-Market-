import Weather
import random
import Home
import Market
import queue
import os
from threading import Lock
from multiprocessing import Process,Value

if __name__ == "__main__":

#Initialisation Shared_Memory et de son mutex
    Temperature_Home_Weather = Value('d')
    Lock_Shared_Memory_MHW = Lock()

    q_don = queue.Queue(maxsize=0)
    q_demandes = queue.Queue(maxsize=0)
    q_achats = queue.Queue(maxsize=0)
    q_ventes = queue.Queue(maxsize=0)
    q_don.put(0)
    q_demandes.put(0)
    q_achats.put(0)
    q_ventes.put(0)
#Processus Weather -- Home -- Market
    print("\t\t\t\t\t TC ENERGY MARKET -- ABOHAM HATOUM ")
    print("Objectif : Simuler un Marché d'énergie entre des maisons autonomes")
    print("Les règles sont simples : \n Il existe 3 type de maisons , possédant des politiques différentes : \n --> Capitaliste : Je suis en déficit d'énergie, j'achète au marché , sinon je vends \n --> Communiste : Tout ce que j'ai en excès je le donne aux autres habitations, si je suis en déficit je demande aux autres habitations si elles ont                    de l'énergie a me donner, sinon j'achète sur le marché en derniers recours \n --> Mixte : Pareil que Communiste sauf que je donne que si une maison a besoin d'énergie")
    print("Pour la démonstration nous simulerons un quartier de 10 maisons :")
    p = Weather.Weather(Temperature_Home_Weather,Lock_Shared_Memory_MHW)
    home1 = Home.Home("Home 1",Temperature_Home_Weather,Lock_Shared_Memory_MHW, random.randint(0,3))
    home2 = Home.Home("Home 2",Temperature_Home_Weather,Lock_Shared_Memory_MHW, random.randint(0,3))
    home3 = Home.Home("Home 3",Temperature_Home_Weather,Lock_Shared_Memory_MHW, random.randint(0,3))
    home4 = Home.Home("Home 4",Temperature_Home_Weather,Lock_Shared_Memory_MHW, random.randint(0,3))
    home5 = Home.Home("Home 5",Temperature_Home_Weather,Lock_Shared_Memory_MHW, random.randint(0,3))
    home6 = Home.Home("Home 6",Temperature_Home_Weather,Lock_Shared_Memory_MHW, random.randint(0,3))
    home7 = Home.Home("Home 7",Temperature_Home_Weather,Lock_Shared_Memory_MHW, random.randint(0,3))
    home8 = Home.Home("Home 8",Temperature_Home_Weather,Lock_Shared_Memory_MHW, random.randint(0,3))
    home9 = Home.Home("Home 9",Temperature_Home_Weather,Lock_Shared_Memory_MHW, random.randint(0,3))
    home10 = Home.Home("Home 10",Temperature_Home_Weather,Lock_Shared_Memory_MHW, random.randint(0,3))
    market = Market.Market(Temperature_Home_Weather,Lock_Shared_Memory_MHW)
    print("Le graphique permet d'avoir des informations sur le prix , la température et les achats et ventes des différentes habitations")
    input("Appuie sur n'importe quelle touche pour continuer et afficher le graphique : ")
    p.run(Temperature_Home_Weather,Lock_Shared_Memory_MHW)
    home1.run(Temperature_Home_Weather,Lock_Shared_Memory_MHW, q_don, q_demandes, q_ventes, q_achats)
    home3.run(Temperature_Home_Weather,Lock_Shared_Memory_MHW, q_don, q_demandes, q_ventes, q_achats)
    home3.run(Temperature_Home_Weather,Lock_Shared_Memory_MHW, q_don, q_demandes, q_ventes, q_achats)
    home4.run(Temperature_Home_Weather,Lock_Shared_Memory_MHW, q_don, q_demandes, q_ventes, q_achats)
    home5.run(Temperature_Home_Weather,Lock_Shared_Memory_MHW, q_don, q_demandes, q_ventes, q_achats)
    home6.run(Temperature_Home_Weather,Lock_Shared_Memory_MHW, q_don, q_demandes, q_ventes, q_achats)
    home7.run(Temperature_Home_Weather,Lock_Shared_Memory_MHW, q_don, q_demandes, q_ventes, q_achats)
    home8.run(Temperature_Home_Weather,Lock_Shared_Memory_MHW, q_don, q_demandes, q_ventes, q_achats)
    home9.run(Temperature_Home_Weather,Lock_Shared_Memory_MHW, q_don, q_demandes, q_ventes, q_achats)
    home10.run(Temperature_Home_Weather,Lock_Shared_Memory_MHW, q_don, q_demandes, q_ventes, q_achats)
    market.run(Temperature_Home_Weather,Lock_Shared_Memory_MHW,q_achats,q_ventes)
    os.system("python3 Graphique.py")
