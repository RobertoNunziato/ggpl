from pyplasm import *

#Funzione di supporto che prende come parametro di input l'array delle dimensioni lungo X,Y o Z
#e restituisce in output la lunghezza lungo X,Y o Z della porta/finestra
def getLength(list):
    length = 0
    for elem in list:
        length = length + elem
    return length


X = [.1,.6,.1]
Y = [.05]
Z = [.3,.2,.2,.2,.2,.2,.2,.2,.3]
occupancy = [[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1]]
glassDepth = .01

def buildDoor(X,Y,Z,occupancy):
    def drawDoor(dx,dy,dz):           
        #Verifico se va effettuato un cambiamento di scala lungo X
        if(dx<getLength(X)):
            scaling = (dx/getLength(X)*1.)
            for i in range(0,len(X)):
                X[i] = X[i]*scaling
        #Verifico se va effettuato un cambiamento di scala lungo Y
        if(dy<Y[0]):
            scaling = (dy/Y[0]*1.)
            Y[0] = Y[0]*scaling
        #Verifico se va effettuato un cambiamento di scala lungo Z
        if(dz<getLength(Z)):
            scaling = (dz/getLength(Z)*1.)
            for i in range(0,len(Z)):
                Z[i] = Z[i]*scaling
              
        length = getLength(X)
        draw = []        
        #Mi scorro l'array Z delle 'strisce' orizzontali
        for zI in range(0,len(Z)):
            #Mi prendo il vettore di booleani(Es: [1,1,1])
            vector = occupancy[zI]
            cont = 0
            #Per ogni valore booleano, controllo se la cella deve essere piena(legno) o vuota(vetro)
            for xI in vector:
                if xI==1:
                    draw.append(COLOR([51/255.,25/255.,0,1]))
                    prod1 = PROD([QUOTE([X[cont]]),QUOTE(Y)])
                    prod2 = PROD([prod1,QUOTE([Z[zI]])])
                    draw.append(prod2)
                if xI==0:
                    draw.append(COLOR([224/255.,224/255.,224/255.,1]))
                    prod1 = PROD([QUOTE([X[cont]]),QUOTE([glassDepth])])
                    prod2 = PROD([prod1,QUOTE([Z[zI]])])
                    draw.append(T([1,2,3])([0,Y[0]/2-glassDepth/2,0]))
                    draw.append(prod2)
                    draw.append(T([1,2,3])([0,-Y[0]/2+glassDepth/2,0]))                    
                draw.append(T([1,2,3])([X[cont],0,0]))
                cont = cont+1
            #Mi riposiziono lungo l'asse del valore della lunghezza ed alzandomi di quello dell'altezza del blocco
            draw.append(T([1,2,3])([-length,0,Z[zI]]))
        
        #Disegno la maniglia della porta
        draw.append(COLOR([224/255.,224/255.,224/255.,1]))
        draw.append(T([1,2,3])([.03,-.01,-getLength(Z)/2]))
        handle = CUBOID([.1,.01,.01])
        draw.append(handle)
    
        #2^ maniglia
        draw.append(COLOR([224/255.,224/255.,224/255.,1]))
        draw.append(T(2)(Y[0]+.01))
        handle = CUBOID([.1,.01,.01])
        draw.append(handle)

        return STRUCT(draw)
    return drawDoor


X2 = [.1,.5,.05,.5,.1,.1,.5,.05,.5,.1]
Y2 = [.05]
Z2 = [.1,.60,.02,.60,.02,.60,.1,.60,.1]
occupancy2 = [[1,1,1,1,1,1,1,1,1,1],[1,0,1,0,1,1,0,1,0,1],[1,1,1,1,1,1,1,1,1,1],
              [1,0,1,0,1,1,0,1,0,1],[1,1,1,1,1,1,1,1,1,1],[1,0,1,0,1,1,0,1,0,1],
              [1,1,1,1,1,1,1,1,1,1],[1,0,0,0,0,0,0,0,0,1],[1,1,1,1,1,1,1,1,1,1]]

def buildWindow(X2,Y2,Z2,occupancy2):
    def drawWindow(dx,dy,dz):  
        #Verifico se va effettuato un cambiamento di scala lungo X
        if(dx<getLength(X2)):
            scaling = (dx/getLength(X2)*1.)
            for i in range(0,len(X2)):
                X2[i] = X2[i]*scaling
        #Verifico se va effettuato un cambiamento di scala lungo Y
        if(dy<Y2[0]):
            scaling = (dy/Y2[0]*1.)
            Y2[0] = Y2[0]*scaling
        #Verifico se va effettuato un cambiamento di scala lungo Z
        if(dz<getLength(Z2)):
            scaling = (dz/getLength(Z2)*1.)
            for i in range(0,len(Z2)):
                Z2[i] = Z2[i]*scaling
     
        length = getLength(X2)
        window = []    
        for zI in range(0,len(Z2)):
            vector = occupancy2[zI]
            cont = 0
            for xI in vector:
                if xI==1:
                    window.append(COLOR([160/255.,82/255.,45/255.,1]))
                    prod1 = PROD([QUOTE([X2[cont]]),QUOTE(Y2)])
                    prod2 = PROD([prod1,QUOTE([Z2[zI]])])
                    window.append(prod2)         
                if xI==0:
                    window.append(COLOR([204/255.,255,255,1]))
                    prod1 = PROD([QUOTE([X2[cont]]),QUOTE([glassDepth])])
                    prod2 = PROD([prod1,QUOTE([Z2[zI]])])
                    window.append(T([1,2,3])([0,Y2[0]/2-glassDepth/2,0]))
                    window.append(prod2)
                    window.append(T([1,2,3])([0,-Y2[0]/2+glassDepth/2,0]))

                window.append(T([1,2,3])([X2[cont],0,0]))
                cont = cont+1
            window.append(T([1,2,3])([-length,0,Z2[zI]]))
            
        #Disegno la maniglia della finestra
        #window.append(COLOR(BLACK))
        #window.append(T([1,2,3])([getLength(X2)/2.,-.02,-getLength(Z2)/2.-.4]))
        #handle = CUBOID([.02,.02,.2])
        #window.append(handle)

        return STRUCT(window)
    return drawWindow