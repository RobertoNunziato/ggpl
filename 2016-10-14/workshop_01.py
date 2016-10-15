from pyplasm import *
"""Funzione che disegna una struttura piana di travi e colonne
"""
def draw(beamSection,pillarSection,distPillar,interstoryHeight):
	px = pillarSection[0]
	py = pillarSection[1]
	bx = beamSection[0]
	bz = beamSection[1]
	"""Definisco tre liste relative alle dimensioni lungo x,y e z
	   dei pilastri e delle travi
	"""
	xPillar = []
	yPillar = []
	zPillar = []
	xBeam = []
	yBeam = []
	zBeam = []	
	distance = 0	#valore per il calcolo della distanze tra i pilastri
	"""Ciclo le distanza passate in input alla funzione e costruisco
	   i pilastri della struttura
	"""
	for i in distPillar:
		xPillar = [px]
		yPillar = yPillar + [py,-i]
		distance = distance + i + py   #Calcolo la distanze tra i pilastri
	yPillar = yPillar + [py]	#Aggiungo un'altra colonna
	"""Ciclo le altezze passate in input e costruisco le travi
	"""
	for i in interstoryHeight:
		zPillar = zPillar + [i,-bz] #Itero in altezza i pilastri
		xBeam = [bx]
		yBeam = [distance+py]	#Assegno alla trave la stessa sezione del pilastro
		zBeam = zBeam + [-i,bz]

	pilTemp = PROD([QUOTE(xPillar),QUOTE(yPillar)])
	pillar = PROD([pilTemp,QUOTE(zPillar)])
	traTemp = PROD([QUOTE(xBeam),QUOTE(yBeam)])
	beam = PROD([traTemp,QUOTE(zBeam)])

	model = STRUCT([pillar,beam])
	VIEW(model)

draw((.3,.3),(.3,.3),[4,4,4,4],[3,3,3,3])
