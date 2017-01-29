from pyplasm import *
from tetto import *
from scale import *
from porteEfinestre import *


def costruisciElemento(fileLines,tipoElemento):
    with open(fileLines, "rb") as file:
        reader = csv.reader(file, delimiter=",")
        elementi = []
        
        if tipoElemento == "porte" or tipoElemento == "finestre" or tipoElemento == "pavimento":
            cuboid = []
            cont = 0
            for riga in reader:
                cont = cont + 1
                cuboid.append([float(riga[1]),float(riga[0])])
                if(cont == 4):
                    elementi.append(MKPOL([cuboid,[[1,2,3,4]],None]))
                    cuboid = []
                    cont = 0
                    
        if tipoElemento == "muriPerimetrali" or tipoElemento == "muriInterni":
            for riga in reader:
                elementi.append(POLYLINE([[float(riga[1]), float(riga[0])],[float(riga[3]), float(riga[2])]]))
                
    struttura = STRUCT(elementi)  
    
    if tipoElemento == "muriPerimetrali":
        struttura = OFFSET([6,6])(struttura)
        struttura = PROD([struttura, Q(120)])
    elif tipoElemento == "muriInterni":
        struttura = OFFSET([3,3])(struttura)
        struttura = PROD([struttura, Q(120)])
    elif tipoElemento == "porte":
        struttura = PROD([struttura, Q(70)])
    elif tipoElemento == "finestre":
        struttura = PROD([struttura, Q(60)])
        struttura = T(3)(30)(struttura)
            
    return struttura


def posizionaElementi(filename, tipoElemento):
    with open(filename, "rb") as file:
        reader = csv.reader(file, delimiter=",")
        elementi = []
        if tipoElemento=="porte" or tipoElemento=="finestre" or tipoElemento=="scala":
            cuboid = []
            cont = 0
            for riga in reader:
                cont = cont + 1
                cuboid.append([float(riga[1]),float(riga[0])])
                if(cont == 4):
                    cubo = STRUCT([MKPOL([cuboid,[[1,2,3,4]],None])])
                    cubo = PROD([cubo,Q(70)])
                    if tipoElemento=="finestre":
                        cubo = (T(3)(30))(cubo)
                    elementi.append(cubo)
                    cuboid = []
                    cont = 0
    return elementi


def inserisciElemento(fileLines,muro,tipoElemento,tipoMuro):
    dimAndPosElem = []
    
    for elem in posizionaElementi(fileLines,tipoElemento):
        if tipoElemento == "porte" or tipoElemento == "finestre":
            muro2 = DIFFERENCE([muro, elem])
            elemento = DIFFERENCE([muro, muro2]) 
        elif tipoElemento == "scala":
            elemento =DIFFERENCE([muro,elem])       
        dimElemento = SIZE([1,2])(elemento)
        if dimElemento[0]!=0.0 and dimElemento[1]!=0.0:
            dimAndPosElem.append(getDimAndPos(elemento))
    elementi =[]
    for d in dimAndPosElem:
        if d[0][0]>d[0][1]: 
            if tipoElemento == "porte":
                elemento = buildDoor(X,Y,Z,occupancy)(1,.05,3)
                elemento = ruota(elemento,2)
            elif tipoElemento == "finestre":
                elemento = buildWindow(X2,Y2,Z2,occupancy2)(2.5,.05,2.74)
                elemento = ruota(elemento,2)
            elif tipoElemento == "scala":
                elemento = ggpl_stairs_with_landings(d[0][0]*.01,(d[0][1]*.01)/2,d[0][2]*.03)   
                elemento = ruota(elemento,3)       
            if tipoElemento == "porte":
                elemento = ridimensiona(elemento,d[0][0]*.03,d[0][1]*.03,d[0][2]*.03)
            elif tipoElemento == "finestre":
                elemento = ridimensiona(elemento,d[0][0]*.03,d[0][1]*.03,d[0][2]*.0255)
        else:
            if tipoElemento == "porte":
                elemento = buildDoor(X,Y,Z,occupancy)(1,.05,3)
                elemento = ruota(elemento,1)
            elif tipoElemento == "finestre":
                elemento = buildWindow(X2,Y2,Z2,occupancy2)(2.5,.05,2.74)            
                elemento = ruota(elemento,1)
            elif tipoElemento == "scala":
                elemento = ggpl_stairs_with_landings(d[0][0]*.01,(d[0][1]*.01)/2,d[0][2]*.03)   
                elemento = ruota(elemento,4)                     
            if tipoElemento == "porte":
                elemento = ridimensiona(elemento,d[0][0]*.03,d[0][1]*.03,d[0][2]*.03)
            elif tipoElemento == "finestre":
                elemento = ridimensiona(elemento,d[0][0]*.03,d[0][1]*.03,d[0][2]*.0255)
                
        elemento = STRUCT([T([1,2,3])(d[1]),elemento]) 
        
        if tipoMuro == "muriPerimetrali":            
            if d[0][0]>d[0][1]:
                elemento = STRUCT([T(2)(-Y[0]*2.65),elemento])
            else:            
                elemento = STRUCT([T(1)(-Y[0]*2.65),elemento])
        elif tipoMuro == "muriInterni":
            if d[0][0]>d[0][1]:
                elemento = STRUCT([T(2)(-Y[0]*4),elemento])
            else:            
                elemento = STRUCT([T(1)(-Y[0]),elemento])

        if tipoElemento == "porte":            
            lunghezzaPorta = getLength(X)
            spazio = (d[0][1]*.03) - lunghezzaPorta
            elemento = STRUCT([T(2)(-spazio*.15),elemento])
        elif tipoElemento == "scala":
            elemento = STRUCT([R([1,2])(PI),elemento])
            elemento = STRUCT([T([1,2,3])([d[1][0]*4.31,d[1][1]*9.95,d[1][2]*.01]),elemento])
              
        elementi.append(elemento)
    return STRUCT(elementi)


def getDimAndPos(elemento):
    dimensioni = SIZE([1,2,3])(elemento)
    c = CUBOID([0.1,0.1,0.1])
    box = STRUCT([c,elemento])
    box = BOX([1,2,3])(box)
    distance = SIZE([1,2,3])(box)
    posizione = [(distance[0]-dimensioni[0])*.03,(distance[1]-dimensioni[1])*.03,(distance[2]-dimensioni[2])*.03]
    dimAndPos=[dimensioni,posizione]
    
    return dimAndPos


def ridimensiona(elemento,x,y,z):
    dim = getDimAndPos(elemento)[0]
    fattoreX = x/dim[0]
    fattoreY = y/dim[1]
    fattoreZ = z/dim[2]
    elementoDimensionato = STRUCT([S([1,2,3])([fattoreX,fattoreY,fattoreZ]),elemento])
    return elementoDimensionato


def ruota(elemento,dir):

    if(dir>0 and dir < 4):
        c = CUBOID([0.1,0.1,0.1])
        dimensioni = SIZE([1,2])(elemento)
        box = STRUCT([c,elemento])
        box = BOX([1,2,3])(box)
        distance = SIZE([1,2,3])(box)
        posizione = [distance[0]-dimensioni[0],distance[1]-dimensioni[1]]

        elementoRuotato = STRUCT([T([1,2])([-posizione[0],-posizione[1]]),elemento])
        if dir==1:
            elementoRuotato = STRUCT([R([1,2])(PI/2),elementoRuotato])
            elementoRuotato = STRUCT([T([1])(dimensioni[1]),elementoRuotato])
            elementoRuotato = STRUCT([T([1,2])([posizione[0],posizione[1]]),elementoRuotato])
        if dir==2:
            elementoRuotato = STRUCT([R([1,2])(PI),elementoRuotato])
            elementoRuotato = STRUCT([T([1,2])([dimensioni[0],dimensioni[1]]),elementoRuotato])
            elementoRuotato = STRUCT([T([1,2])([posizione[0],posizione[1]]),elementoRuotato])
        if dir==3:
            elementoRuotato = STRUCT([R([1,2])(PI*3/2),elementoRuotato])
            elementoRuotato = STRUCT([T([2])(dimensioni[0]),elementoRuotato])
            elementoRuotato = STRUCT([T([1,2])([position[0],posizione[1]]),elementoRuotato])
        if dir==4:
            elementoRuotato = STRUCT([R([1,2])(PI*2),elementoRuotato])
        return elementoRuotato
    return elemento


def disegnaPianoCasa(muriPerimetrali,muriInterni,porte,finestre,
                  pavimentoCasa,pavimentoBagno,pavimentoCucina,scala,soffitto,numeroPiano):
    
    #Costruiamo i muri esterni, interni, porte e finestre
    esterni = costruisciElemento(muriPerimetrali,"muriPerimetrali")
    interni = costruisciElemento(muriInterni,"muriInterni")
    boxPorte = costruisciElemento(porte,"porte") 
    esterniSenzaPorte = DIFFERENCE([esterni,boxPorte])
    interniSenzaPorte = DIFFERENCE([interni,boxPorte])
    interniSenzaPorte = TEXTURE(["texture/interni.jpg", TRUE, FALSE, 1, 1, 0, 6, 6])(interniSenzaPorte)
    boxFinestre = costruisciElemento(finestre,"finestre")     
    muriSenzaFinestre = DIFFERENCE([esterniSenzaPorte,boxFinestre])    
    muriSenzaFinestre = TEXTURE(["texture/pareti.jpg", TRUE, FALSE, 1, 1, 0, 6, 6])(muriSenzaFinestre)  
    #Inserisco i diversi pavimenti
    pavimento = costruisciElemento(pavimentoCasa,"pavimento")
    pavimento = TEXTURE(["texture/parquet.jpg", TRUE, FALSE, 1, 1, 0, 6, 6])(pavimento)
    pavimentoB = costruisciElemento(pavimentoBagno,"pavimento")
    pavimentoB = TEXTURE(["texture/bagno.jpg", TRUE, FALSE, 1, 1, 0, 6, 6])(pavimentoB)
    pavimentoC = costruisciElemento(pavimentoCucina,"pavimento")
    pavimentoC = TEXTURE(["texture/cucina.jpg", TRUE, FALSE, 1, 1, 0, 6, 6])(pavimentoC)
    pavimenti = STRUCT([pavimento,pavimentoB,pavimentoC])  
    #Inserisco le porte e le finestre
    if numeroPiano == "primoPiano":
        portaIngresso = inserisciElemento(porte, esterni,"porte","muriPerimetrali") 
    porteCasa = inserisciElemento(porte, interni,"porte","muriInterni") 
    finestreCasa = inserisciElemento(finestre,esterni,"finestre","muriPerimetrali")
    if scala != None:
        scalaCasa = inserisciElemento(scala,interni,"scala","muriInterni")
        scalaCasa = TEXTURE(["texture/parquet.jpg", TRUE, FALSE, 1, 1, 0, 6, 6])(scalaCasa)  
    house = STRUCT([muriSenzaFinestre,interniSenzaPorte, pavimenti])    
    #Inserisco il soffitto
    if numeroPiano == "ultimoPiano":
        soffitto = costruisciElemento(soffitto,"pavimento")
        soffitto = T(3)(120)(soffitto)
        house = STRUCT([house,soffitto])
    house = STRUCT([house])
    
    #Scalo l'intera casa
    house = S([1,2,3])([.03,.03,.03])(house)    
    if scala != None and numeroPiano == "primoPiano":
        house = STRUCT([house,porteCasa,portaIngresso,finestreCasa,scalaCasa])
    else:
        house = STRUCT([house,porteCasa,finestreCasa])  
        
    return(house)
    

def disegnaCasa():
    piano1 = disegnaPianoCasa("linesFiles/primoPiano/muriEsterni.lines",
                             "linesFiles/primoPiano/muriInterni.lines",
                             "linesFiles/primoPiano/porte.lines",
                             "linesFiles/primoPiano/finestre.lines",
                             "linesFiles/primoPiano/pavimento.lines",
                             "linesFiles/primoPiano/pavimentoBagno.lines",
                             "linesFiles/primoPiano/pavimentoCucina.lines",
                             "linesFiles/primoPiano/scala.lines",None,"primoPiano")    
    piano2 = disegnaPianoCasa("linesFiles/secondoPiano/muriEsterni.lines",
                             "linesFiles/secondoPiano/muriInterni.lines",
                             "linesFiles/secondoPiano/porte.lines",
                             "linesFiles/secondoPiano/finestre.lines",
                             "linesFiles/secondoPiano/pavimento.lines",
                             "linesFiles/secondoPiano/pavimentoBagno.lines",
                             "linesFiles/secondoPiano/pavimentoCucina.lines",None,
                             "linesFiles/soffitto.lines","ultimoPiano")
    house = STRUCT([piano1,T(3)(3.6)(piano2)])
    misure = getDimAndPos(house)
    tetto = T([1,2])([(misure[1][0]/.03),misure[1][1]/.03])(getVerticiTetto(house))    
    house = STRUCT([house,T(3)(7.2)(tetto)])
    house = STRUCT([house])
    return(house)
