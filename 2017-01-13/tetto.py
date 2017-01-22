from pyplasm import *
from scipy import *  
from numpy import *  
import math
import csv


def disegnaTetto(vertici,inclinazione,lunghezza):
    """
    createRoof ritorna l'HPC di un tetto secondo 3 parametri: un file .lines che descrive il perimetro della base del tetto, i gradi della pendenza delle falde, 
    la lunghezza della pendenza delle falde.
    I vertici devono essere scritti in una lista fatta in questo modo [[x1,y1],[x2,y2],...] e devono essere presi in ordine orario 
    @param vertexes: lista dei vertici del tetto
    @param angle: l'angolo di inclinazione che si vuole dare alla falda
    @param diagonal: lunghezza della pendenza della falda
    @return struttura: l'HPC del tetto
    """

    direzioni = getDirezioniVertici(vertici)
    listaFalde = []
    
    #Mi ciclo tutte le direzioni dei punti nel piano e per ogni coppia mi costruisco le falde
    for i in range(len(direzioni)-1):
        listaFalde.append(disegnaFalda(vertici[i],vertici[i+1],inclinazione,lunghezza,direzioni[i]))
    listaFalde.append(disegnaFalda(vertici[len(direzioni)-1],vertici[0],inclinazione,lunghezza,direzioni[len(direzioni)-1]))

    equazioniRette = []
    for i in range(len(listaFalde)):
        equazioniRette.append(getEquazioneRetta(listaFalde[i][2],listaFalde[i][3]))

    intersezioni = []
    for i in range(len(equazioniRette)-1):
        intersezioni.append(getIntersezione(equazioniRette[i],equazioniRette[i+1]))
    intersezioni.append(getIntersezione(equazioniRette[len(equazioniRette)-1],equazioniRette[0]))


    disegnaFalde = []
    for i in range(len(direzioni)):
        if i == 0:
            falda = MKPOL([[[listaFalde[i][0][0],listaFalde[i][0][1],0],
                            [listaFalde[i][1][0],listaFalde[i][1][1],0],
                            [intersezioni[i][0],intersezioni[i][1],listaFalde[1][2][2]],
                            [intersezioni[len(direzioni)-1][0],intersezioni[len(direzioni)-1][1],listaFalde[0][2][2]]],
                           [[4,3,2,1]],None])    
        else:
            falda = MKPOL([[[listaFalde[i][0][0],listaFalde[i][0][1],0],
                            [listaFalde[i][1][0],listaFalde[i][1][1],0],
                            [intersezioni[i][0],intersezioni[i][1],listaFalde[1][2][2]],
                            [intersezioni[i-1][0],intersezioni[i-1][1],listaFalde[0][2][2]]],
                           [[4,3,2,1]],None])
            
        disegnaFalde.append(falda)

    verticiTerrazzo = [[] for _ in range(len(intersezioni)+1)]
    for i in range (len(intersezioni)):
        verticiTerrazzo[i].append(intersezioni[i][0])
        verticiTerrazzo[i].append(intersezioni[i][1])
        if i==len(intersezioni)-1:
            verticiTerrazzo[i+1].append(intersezioni[0][0])
            verticiTerrazzo[i+1].append(intersezioni[0][1])
        
    contorno = POLYLINE(verticiTerrazzo)
    contorno = SOLIDIFY(contorno)
    terrazzo = T(3)(listaFalde[0][2][2])(contorno)
    terrazzo = TEXTURE("texture/tetto.jpg")(terrazzo)
    tetto = STRUCT(disegnaFalde)
    tetto = TEXTURE(["texture/tetto.jpg", TRUE, FALSE, 1, 1, 0, 3, 3])(tetto)
    return STRUCT([terrazzo,tetto])





#Funzione che restituisce i vertici della falda, dati due vertici, l'inclinazione voluta,
#la lunghezza e l'orientamento rispetto agli assi del piano cartesiano
def disegnaFalda(v1, v2, inclinazione, lunghezza, orientamento):

    v1v2 = sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)
    v2v3 = abs(v2[1] - v1[1]) 
    #calcolo l'angolo compreso tra i due segmenti
    angolo = math.asin(v2v3/v1v2)
    angolo2 = PI/2 - angolo   
    #calcolo la lunghezza del segmento, noto l'angolo compreso
    v2v4 = lunghezza * math.cos(inclinazione)
    #calcolo l'altezza a cui deve essere posta la falda
    altezza = sqrt(lunghezza**2 - v2v4**2)
    v2v5 = v2v4 * math.cos(angolo2)
    v4v5 = sqrt(v2v4**2 - v2v5**2)    
    #A seconda dell'orientamento del segmento nello spazio cartesiano,
    #mi calcolo le restanti coordinate che formeranno la falda finale
    if orientamento=="sinistra su":
        v6 = [v2[0] + v2v5,v2[1] + v4v5,altezza]
        v7 = [v1[0] + v2v5,v1[1] + v4v5,altezza]
    elif orientamento=="sinistra giu" or orientamento=="sinistra":
        v6 = [v2[0] - v2v5,v2[1] + v4v5,altezza]
        v7 = [v1[0] - v2v5,v1[1] + v4v5,altezza]
    elif orientamento=="destra giu" or orientamento=="giu" or orientamento=="destra":
        v6 = [v2[0] - v2v5,v2[1] - v4v5,altezza]
        v7 = [v1[0] - v2v5,v1[1] - v4v5,altezza]
    elif orientamento=="destra su" or orientamento=="su":
        v6 = [v2[0] + v2v5,v2[1] - v4v5,altezza]
        v7 = [v1[0] + v2v5,v1[1] - v4v5,altezza]

    return [v1,v2,v6,v7]



#Funzione che, dati due vertici, v1 e v2, restituisce l'equazione della retta che li comprende
def getEquazioneRetta(v1,v2):

    #Punti con la stessa x: retta // Y
    if v1[0]==v2[0]:
        retta = [1,0,v1[0]]
    #Punti con la stessa y: retta // X
    elif v1[1]==v2[1]:
        retta = [0,1,v1[1]]
    else:
        #Calcolo il valore del coefficiente angolare
        m=(float(v2[1]) - float(v1[1]))/(float(v2[0]) - float(v1[0]))
        #Calcolo il valore del termine noto
        q=float(v1[1]) - m*float(v1[0])
        retta = [-m,1,q]
        
    return retta

def getIntersezione(l1,l2):
    #Coefficienti
    A = matrix([[l1[0], l1[1]], [l2[0], l2[1]]])  
    #Valori noti  
    b = array([l1[2], l2[2]])  
    # la funzione linalg.solve risolve sistemi lineari
    point = linalg.solve(A, b)  
    return point

#Array di direzioni, dato un array di vertici
def getDirezioniVertici(vertici):
    direzioni=[]
    for i in range(0,len(vertici)-1):
        p1x = vertici[i][0]
        p1y = vertici[i][1]
        p2x = vertici[i+1][0]
        p2y = vertici[i+1][1]

        if p2x > p1x:
            if p2y > p1y:
                direzioni.append("destra su")
            elif p2y == p1y:
                direzioni.append("destra")
            else:
                direzioni.append("destra giu")
        elif p2x == p1x:
            if p2y > p1y:
                direzioni.append("su")
            else:
                direzioni.append("giu")

        else:
            if p2y > p1y:
                direzioni.append("sinistra su")
            elif p2y == p1y:
                direzioni.append("sinistra")
            else:
                direzioni.append("sinistra giu")
       
    #Ultimo caso
    p1x = vertici[len(vertici)-1][0]
    p1y = vertici[len(vertici)-1][1]
    p2x = vertici[0][0]
    p2y = vertici[0][1]
    if p2x > p1x:
        if p2y > p1y:
            direzioni.append("destra su")
        elif p2y == p1y:
            direzioni.append("destra")
        else:
            direzioni.append("destra giu")
    elif p2x == p1x:
        if p2y > p1y:
            direzioni.append("su")
        else:
            direzioni.append("giu")
    else:
        if p2y > p1y:
            direzioni.append("sinistra su")
        elif p2y == p1y:
            direzioni.append("sinistra")
        else:
            direzioni.append("sinistra giu")
       
    return direzioni

def getDimensionAndPosition(HPCObject):
    sizeObj = SIZE([1,2,3])(HPCObject)
    c = CUBOID([0.1,0.1,0.1])
    box = STRUCT([c,HPCObject])
    box = BOX([1,2,3])(box)
    distance=SIZE([1,2,3])(box)
    position=[(distance[0]-sizeObj[0])*.03,(distance[1]-sizeObj[1])*.03,(distance[2]-sizeObj[2])*.03]
    dimAndPos=[sizeObj,position]
    return dimAndPos


def getVerticiTetto(house):
    dimensione = getDimensionAndPosition(house)[0]
    posizione = getDimensionAndPosition(house)[1]
    vertici=[]
    vertici.append([posizione[0]*.03,posizione[1]*.03])
    vertici.append([posizione[0]*.03,posizione[1]*.03+dimensione[1]])
    vertici.append([dimensione[0]+posizione[0]*.03,dimensione[1]+posizione[1]*.03])
    vertici.append([posizione[0]*.03+dimensione[0],posizione[1]*.03])
    
    altezza=2
    tetto = disegnaTetto(vertici,PI/4,altezza)

    return tetto
