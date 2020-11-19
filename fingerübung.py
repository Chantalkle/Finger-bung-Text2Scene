# -*- coding: utf-8 -*-
"""

@author: Chantal Klemm

Python3.8
Fingerübung Text2Scene Praktikum
"""
import spacy
import zipfile
import os 
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import networkx as nx

#ordner öffnen und auf daten zugreifen
with zipfile.ZipFile('training.zip','r') as zfile:
    zfile.extractall('training')
    
daten = os.listdir("training")[0]
mehrdaten = "training/"+daten
ordner = os.listdir(mehrdaten) #pfade in ornder auflisten

#variablen die die Häufigkeit zählen
PosTags = []
numPosTags = []
numSpatialEntities = 0
numPlaces = 0
numMotions = 0
numSignals = 0 
numQsLinks = 0
numOLinks = 0
Satzlh = [] 
signalsQs =[]
signalsO = []
typenQs = []
numtypenQs = []
motionVerbs = []
nummotionVerbs =[]

nlp = spacy.load("en_core_web_sm")

x=0
for i in ordner:
    nordner = mehrdaten + "/" + ordner[x]

    if os.path.isdir(nordner): #wenn norndner ein dateipfad ist
        ordnerdaten = os.listdir(nordner)        
        y = 0
        for datei in ordnerdaten: #alle ordnerdaten aufrufen
            dateipfad = nordner + "/" + ordnerdaten[y]
            if os.path.isdir(dateipfad): 
                anderedaten = os.listdir(dateipfad)
                z = 0
                for ndatei in  anderedaten:
                    newdateipfad = dateipfad + "/" + anderedaten[z]
                    if (newdateipfad[-1]) =="l": #überüfen ob die datei eine xml datei ist
                         #baum der xmldatei erstellen
                         tree = ET.parse(newdateipfad)
                         root = tree.getroot()
                         for child in root:
                             if child.tag == 'TEXT':
                                 #den text in der xml datei parsen
                                 atext = nlp(child.text)
                                 satzl = 0
                                 for token in atext:
                                     if token.tag_ == ".": #satzende
                                         if len(Satzlh)>(satzl+1):#wenn die satzlänge schon in der Lsite vertretten, dann erhöhe die anzahl um 1
                                             Satzlh[satzl]=Satzlh[satzl]+1
                                         else: #sonst füge alle satzlängen bis zu dieser satzlänge in die liste ein(mit 0) und diese mit 1
                                             l = len(Satzlh)
                                             while l < satzl:
                                                 Satzlh = Satzlh + [0]
                                                 l = l+1
                                             Satzlh = Satzlh + [1]
                                         satzl = 0 #satzlänge wieder auf 0 setzen, da ein neuer satz beginnt
                                     elif token.pos != 'PUNCT': #wenn kein satzende und es ist kein satzzeichen, dann ist es ein wort und die satzlänge erhöht sich um 1
                                         satzl = satzl+1
                                     #jetzt werden die postags gezählt
                                     if token.tag_ in PosTags:
                                         numPosTags[PosTags.index(token.tag_)] = numPosTags[PosTags.index(token.tag_)] + 1
                                     else: 
                                         PosTags = PosTags + [token.tag_]
                                         numPosTags = numPosTags + [1] 
                             else: #wenn es nicht der text der xml datei ist
                                 for grandchild in child: #unterscheide den typ und zähle die verschiedenen typen
                                     if grandchild.tag == 'SPATIAL_ENTITY':
                                         numSpatialEntities = numSpatialEntities + 1
                                     elif grandchild.tag == 'PLACE':
                                         numPlaces = numPlaces + 1
                                     elif grandchild.tag == 'MOTION':
                                         verb = grandchild.get('text') #motionverben zählen
                                         if verb in motionVerbs:
                                             nummotionVerbs[motionVerbs.index(verb)] = nummotionVerbs[motionVerbs.index(verb)] + 1
                                         else:
                                             motionVerbs = motionVerbs + [verb]
                                             nummotionVerbs = nummotionVerbs + [1]
                                         numMotions = numMotions + 1
                                     elif grandchild.tag == ('SPATIAL_SIGNAL' or 'MOTION_SIGNAL'):
                                         signal = [grandchild.get('id'),grandchild.get('text'),0]
                                         for i in signalsQs: #signale auflisten
                                             if i[1] == signal[1]:
                                                 i[0] = signal[0]
                                             else: 
                                                 signalsQs = signalsQs + [signal]
                                            
                                         for i in signalsO:
                                             if i[1] == signal[1]:
                                                 i[0] = signal[0]
                                             else: 
                                                 signalsO = signalsO + [signal]
                                         numSignals = numSignals + 1
                                     elif grandchild.tag == 'QSLINK':
                                         trigger = grandchild.get('trigger') #trigger der QsLinks zählen
                                         for i in signalsQs:
                                             if i[0] == trigger:
                                                 i[2] = i[2]+1
                                             linktyp = grandchild.get('relType') #linktypen auflisten und zählen
                                             if linktyp in typenQs:
                                                 numtypenQs[typenQs.index(linktyp)] = numtypenQs[typenQs.index(linktyp)] + 1
                                             else: 
                                                 typenQs = typenQs + [linktyp]
                                                 numtypenQs = numtypenQs + [1]
                                         numQsLinks = numQsLinks + 1 
                                         trigger = grandchild.get('trigger')
                                         for i in signalsQs:
                                             if i[0] == trigger:
                                                 i[2] = i[2]+1
                                         linktyp = grandchild.get('relType')
                                         if linktyp in typenQs:
                                             numtypenQs[typenQs.index(linktyp)] = numtypenQs[typenQs.index(linktyp)] + 1
                                         else: 
                                             typenQs = typenQs + [linktyp]
                                             numtypenQs = numtypenQs + [1]
                
                                         numQsLinks = numQsLinks + 1
                                     elif grandchild.tag == 'OLINK':
                                         trigger = grandchild.get('trigger') #trigger der Olinks zählen
                                         for i in signalsO:
                                             if i[0] == trigger:
                                                 i[2] = i[2]+1
                                         numOLinks = numOLinks + 1
                    z = z+1
                    
            else:
                #baum der xmldatei an stelle dateipfad erstellen
                tree = ET.parse(dateipfad)
                root = tree.getroot()
                for child in root:
                    if child.tag == 'TEXT':
                        #den text in der xml datei parsen
                        atext = nlp(child.text)
                        satzl = 0
                        for token in atext:
                            if token.tag_ == ".": #überprüfen ob Satz zu ende
                                if len(Satzlh)>(satzl+1):
                                    Satzlh[satzl]=Satzlh[satzl]+1
                                else:
                                    l = len(Satzlh)
                                    while l < satzl:
                                        Satzlh = Satzlh + [0]
                                        l = l+1
                                    Satzlh = Satzlh + [1] 
                                satzl = 0
                            elif token.pos != 'PUNCT': #sonst wenn kein satzzeichen, satzlänge um 1 erhöhen
                                satzl = satzl+1
                                            
                            if token.tag_ in PosTags: #Pos tags auflisten und zählen
                                numPosTags[PosTags.index(token.tag_)] = numPosTags[PosTags.index(token.tag_)] + 1
                            else: 
                                PosTags = PosTags + [token.tag_]
                                numPosTags = numPosTags + [1] 
                     
                    else: #wenn es kein text ist
                        for grandchild in child: #unterscheide den typ und zähle die verschiedenen typen
                            if grandchild.tag == 'SPATIAL_ENTITY':
                                numSpatialEntities = numSpatialEntities + 1
                            elif grandchild.tag == 'PLACE':
                                numPlaces = numPlaces + 1
                            elif grandchild.tag == 'MOTION':
                                verb = grandchild.get('text') #motion verben zählen
                                if verb in motionVerbs:
                                    nummotionVerbs[motionVerbs.index(verb)] = nummotionVerbs[motionVerbs.index(verb)] + 1
                                else:
                                     motionVerbs = motionVerbs + [verb]
                                     nummotionVerbs = nummotionVerbs + [1]
                                numMotions = numMotions + 1
                            elif grandchild.tag == ('SPATIAL_SIGNAL' or 'MOTION_SIGNAL'):
                                signal = [grandchild.get('id'),grandchild.get('text'),0] #signale auflisten
                                signalsQs = signalsQs + [signal]
                                signalsO = signalsO + [signal]
                                numSignals = numSignals + 1
                            elif grandchild.tag == 'QSLINK':
                                trigger = grandchild.get('trigger') #trigger QsLinks auflisten
                                for i in signalsQs:
                                    if i[0] == trigger:
                                        i[2] = i[2]+1
                                linktyp = grandchild.get('relType')
                                if linktyp in typenQs: #linktypen zählen
                                    numtypenQs[typenQs.index(linktyp)] = numtypenQs[typenQs.index(linktyp)] + 1
                                else: 
                                    typenQs = typenQs + [linktyp]
                                    numtypenQs = numtypenQs + [1]
                                numQsLinks = numQsLinks + 1
                            elif grandchild.tag == 'OLINK':
                                trigger = grandchild.get('trigger') #trigger OLink auflisten
                                for i in signalsO:
                                     if i[0] == trigger:
                                         i[2] = i[2]+1
                                numOLinks = numOLinks + 1
            y = y+1
            
    x = x+1

#Auswertung
print ('Anzahl Motions = '+str(numMotions)+'\n'+'Anzahl SpatialEntities = ' + str(numSpatialEntities))
print( 'Anzahl Places = ' + str(numPlaces) + '\n' + 'Anzahl Signals = ' + str(numSignals))
print('Anzahl QSLinks = ' + str(numQsLinks) + '\n' + 'Anzahl OLinks = ' + str(numOLinks))
print('PoS-Tags und ihre Häufigkeit:')

i= 0
while i< len(PosTags):
    print(str(PosTags[i])+ ' kommt ' + str(numPosTags[i]) + '-mal vor.')
    i = i+1

#doppelte signale zusammenführen
x=0
signalshelp = signalsO
while x <  len(signalsO):
    y = 0
    while y < len(signalsO):
        if signalsO[x][1] == signalsO[y][1]:
            #print(str(signalsO[x][1]) + ' und ' + str(signalsO[y][1]) + ' = ' + str(signalsO[x][1] == signalsO[x][1]))
            signalsO[x][2] = signalsO[x][2] + signalsO[y][2]
            signalshelp[x][2] = signalsO[x][2]
            del signalshelp[y]
        y = y+1
    x = x+1
#ausgabe         
for i in signalsO:
    print('OLink wird ' + str(i[2]) + ' mal von ' + str(i[1]) + ' getriggert')
    
#doppelte signale zusammenführen
x=0
signalshelp = signalsQs
while x <  len(signalsQs):
    y = 0
    while y < len(signalsQs):
        if signalsQs[x][1] == signalsQs[y][1]:
            signalsQs[x][2] = signalsQs[x][2] + signalsQs[y][2]
            signalshelp[x][2] = signalsQs[x][2]
            del signalshelp[y]
        y = y+1
    x = x+1
# ausgabe
for i in signalsQs:
    print('QsLink wird ' + str(i[2]) + ' mal von ' + str(i[1]) + ' getriggert')
    
#typen QsLinks auswerten    
i= 0
while i< len(typenQs):
    if typenQs[i] == "":
        print('Es gibt ' + str(numtypenQs[i]) + ' QsLinks ohne Typ')
    else: 
        print('Es gibt ' + str(numtypenQs[i]) + ' QsLinks vom Typ ' + str(typenQs[i]))
    i = i+1

#die 5 häufigsten MOVEMENT Verben
for i in range(0,5):    
    maxnumverb = max(nummotionVerbs)
    pos = nummotionVerbs.index(maxnumverb)
    verb = motionVerbs[pos]
    print('Eines der 5 häufigsten Motion-Verben ist ' +str(verb)+ '. Es kommt ' + str(maxnumverb) + ' mal vor.')
    del(motionVerbs[pos])
    del(nummotionVerbs[pos])
    

#grafische Darstellung Satzlänge und Häufigkeit
satzlaenge = list(range(0, len(Satzlh)))
haeufigkeit = Satzlh
plt.plot(satzlaenge, haeufigkeit)
plt.show()


#Visualisierung
bicycle = "training/Traning/RFC/Bicycles.xml"
bicyclestree = ET.parse(bicycle)
bicyclesroot = bicyclestree.getroot()

setext = []
seid = []

ptext= []
pid = []

b=nx.Graph()
c=nx.Graph()

for child in bicyclesroot:
    if child.tag != 'TEXT':
        for grandchild in child:
            if grandchild.tag == 'SPATIAL_ENTITY':
                setext = setext + [grandchild.get('text')]
                seid = seid + [grandchild.get('id')]
                b.add_node(grandchild.get('text'))
                
               
                #print(grandchild.get('text'))
            elif grandchild.tag == 'PLACE':
                ptext = ptext + [grandchild.get('text')]
                pid = pid + [grandchild.get('id')]
                c.add_node(grandchild.get('text'))
                
                #print(grandchild.get('text'))
                
            elif grandchild.tag =='METALINK':
                id1 = grandchild.get('objectID1')
                id2 = grandchild.get('objectID2')
                text = grandchild.get('toText')
                
        for grandchild in child: 
            if grandchild.tag == 'QSLINK':
                ver1 = grandchild.get('fromID')
                ver2 = grandchild.get('toID')
                k1 = False
                k2 = False
                if ver1 in seid:
                    k1 = setext[seid.index(ver1)]
                elif ver1 in pid:
                    k1 = ptext[pid.index(ver1)]
                   
                if ver2 in seid:
                    k2 = setext[seid.index(ver2)]
                    isin2 = True
                elif ver1 in pid:
                    k2 = ptext[pid.index(ver2)]
                    isin1 = True
                
                if k1 == False:
                    pass
                elif k2 == False: 
                    pass
                else:
                
                    b.add_edge(k1,k2)
                    c.add_edge(k1,k2)
                    
                
                    
               
            elif grandchild.tag == 'OLINK':
                ver1 = grandchild.get('fromID')
                ver2 = grandchild.get('toID')
                k1 = False
                k2 = False
                if ver1 in seid:
                    k1 = setext[seid.index(ver1)]
                elif ver1 in pid:
                    k1 = ptext[pid.index(ver1)]
                   
                if ver2 in seid:
                    k2 = setext[seid.index(ver2)]
                    isin2 = True
                elif ver1 in pid:
                    if ver2 in pid:
                        k2 = ptext[pid.index(ver2)]
                        isin1 = True
                
                if k1 == False:
                    pass
                elif k2 == False: 
                    pass
                else:
                   
                    b.add_edge(k1,k2)
                    c.add_edge(k1,k2)
            


plt.show()
nx.draw(b, with_labels=True, node_color='green')
nx.draw(c, with_labels=True, node_color='blue')

pradotree = ET.parse("training/Traning/ANC/WhereToMadrid/Highlights_of_the_Prado_Museum.xml")
pradoroot = pradotree.getroot()
b=nx.Graph()
c=nx.Graph()
for child in pradoroot:
    if child.tag != "TEXT":
        for grandchild in child:
            if grandchild.tag == 'SPATIAL_ENTITY':
                b.add_node(grandchild.get('text'))
            elif grandchild.tag == 'PLACE':
                c.add_node(grandchild.get('text'))
                
        for grandchild in child: 
                if grandchild.tag == 'QSLINK':
                    ver1 = grandchild.get('fromID')
                    ver2 = grandchild.get('toID')
                    k1 = False
                    k2 = False
                    if ver1 in seid:
                        k1 = setext[seid.index(ver1)]
                    elif ver1 in pid:
                        k1 = ptext[pid.index(ver1)]
                       
                    if ver2 in seid:
                        k2 = setext[seid.index(ver2)]
                        isin2 = True
                    elif ver1 in pid:
                        if ver2 in pid:
                            k2 = ptext[pid.index(ver2)]
                            isin1 = True
                    
                    if k1 == False:
                        pass
                    elif k2 == False: 
                        pass
                    else:
                       
                        b.add_edge(k1,k2)
                        c.add_edge(k1,k2)
                elif grandchild.tag == 'OLINK':
                    ver1 = grandchild.get('fromID')
                    ver2 = grandchild.get('toID')
                    k1 = False
                    k2 = False
                    if ver1 in seid:
                        k1 = setext[seid.index(ver1)]
                    elif ver1 in pid:
                        k1 = ptext[pid.index(ver1)]
                       
                    if ver2 in seid:
                        k2 = setext[seid.index(ver2)]
                        isin2 = True
                    elif ver1 in pid:
                        if ver2 in pid:
                            k2 = ptext[pid.index(ver2)]
                            isin1 = True
                    
                    if k1 == False:
                        pass
                    elif k2 == False: 
                        pass
                    else:
                       
                        b.add_edge(k1,k2)
                        c.add_edge(k1,k2)
                   

plt.show()
nx.draw(b, with_labels=True, node_color='red')
nx.draw(c, with_labels=True, node_color='yellow')