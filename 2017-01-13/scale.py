from pyplasm import *
from larlib import *

def ggpl_stairs_with_landings(dx,dy,dz):
    pianerottoloX = 1
    pianerottoloY = dy
    #Prendiamo come riferimento dei valori ideali di pedata e alzata
    pedataIdeale = .29
    alzataIdeale = .17
    #Larghezza del gradino
    larghezza = DIV([dy,2])
    dzMezzi = DIV([dz,2])
    #Determiniamo il numero dei gradini e le misure di pedata e alzata effettive
    pedataTot = dx - 2*pianerottoloX
    restoPedata = modf(pedataTot/pedataIdeale)[0]
    numGradini = modf(pedataTot/pedataIdeale)[1]
    pedata = DIV([pedataTot,numGradini])
    alzata = DIV([dzMezzi,numGradini+1])
    #Costruiamo la prima rampa di scale
    scala = []
    for x in range(0,int(numGradini)):
        scala.append(CUBOID([pedata,larghezza,alzata]))
        scala.append(T([1,2,3])([pedata,0,alzata]))
    #Inseriamo il primo pianerottolo
    scala.append(CUBOID([pianerottoloX,pianerottoloY,alzata]))
    scala.append(R([1,2])(PI))
    scala.append(T([1,2,3])([0,-2*larghezza,alzata]))
    #Costruiamo la seconda rampa di scale
    for x in range(0,int(numGradini)):
        scala.append(CUBOID([pedata,larghezza,alzata]))
        scala.append(T([1,2,3])([pedata,0,alzata]))
    #Inseriamo il secondo pianerottolo
    scala.append(CUBOID([pianerottoloX,pianerottoloY,alzata]))
    scala.append(R([1,2])(PI))
    #Verifichiamo la correttezza delle misure
    #print(SIZE([1,2,3])(BOX([1,2,3])(STRUCT(scala))))
    
    return STRUCT(scala)