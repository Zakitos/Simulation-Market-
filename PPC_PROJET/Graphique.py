import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
plt.style.use('ggplot') #Style CSS du graphique
fig = plt.figure() #Figure globale
def animate (i):
    global fig
    ax1 = fig.add_subplot(2,1,1) #Graphique position haute
    graph_temperature = open('Temperature.txt','r').read()
    lines = graph_temperature.split('\n')
    xs = [] #Axe x
    ys = [] #Axe y
    for line in lines:
        if len(line) > 1:
            y,x = line.split(',') #Je sépare les x et y dans le fichier
            xs.append(float(x)) #Je les ajoutes au axes
            ys.append(float(y))
    ax1.clear()
    plt.title('Marché Boursier')
    ax1.set_xlabel('Jours')
    ax1.set_ylabel('Température')
    ax1.plot(xs,ys,'b',linewidth=2.5) #Epaisseur 2.5

    ax2 = fig.add_subplot(2,2,3) #Je passe a la position basse gauche
    graph_prix= open('Prix.txt','r').read()
    lines = graph_prix.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            y,x = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    ax2.clear()
    plt.ylabel('Prix (€)')
    plt.xlabel('Jours')
    ax2.plot(xs,ys,'r',linewidth=2.5)

    ax3 = fig.add_subplot(2,2,4)
    graph_temperature = open('Achats_Ventes.txt','r').read()
    lines = graph_temperature.split('\n')
    achats_tab = []
    ventes_tab = []
    xs = []
    for line in lines:
        if len(line) > 1:
            achats,ventes,x = line.split(',')
            achats_tab.append(float(achats))
            ventes_tab.append(float(ventes))
            xs.append(x)
    ax3.clear()
    ax3.set_xlabel('Jours')
    ax3.set_ylabel('Achats/Ventes')
    ax3.plot(xs,achats_tab,'b',linewidth=2.5,label="Achats (Wh/jour)")
    ax3.plot(xs,ventes_tab,'g',linewidth=2.5,label="Ventes (Wh/jour)")
    ax3.legend(loc='upper right') #Affichage de la position de la légende


ani = animation.FuncAnimation(fig,animate,interval = 1000)
plt.show()
