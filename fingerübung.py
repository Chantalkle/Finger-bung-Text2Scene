# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 11:34:48 2020

@author: Chantal Klemm
"""
import spacy
#import numpy
import zipfile
import os 
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt


with zipfile.ZipFile('training.zip','r') as zfile:
    zfile.extractall('training')
    
daten = os.listdir("training")[0]
mehrdaten = "training/"+daten
ordner = os.listdir(mehrdaten)

#variablen die die Häufigkeit zählen
PosTags = []
numPosTags = []
numSpatialEntities = 0
numPlaces = 0
numMotions = 0
numSignals = 0 
numQsLinks = 0
numOLinks = 0


    

Satzlh = [] #Tupel: Stelle 1 Satzlänge, Stelle 2 Häufigkeit


x=0
for i in ordner:
    nordner = mehrdaten + "/" + ordner[x]
    nlp = spacy.load("en_core_web_sm")

    if os.path.isdir(nordner):
        ordnerdaten = os.listdir(nordner)
        #print(ordnerdaten)
        
        #die einzelnen xml dateien durchegehen:
        y = 0
        for datei in ordnerdaten:
            dateipfad = nordner + "/" + ordnerdaten[y]
            if os.path.isdir(dateipfad):
                anderedaten = os.listdir(dateipfad)
                z = 0
                for ndatei in  anderedaten:
                    newdateipfad = dateipfad + "/" + anderedaten[z]
                    #print(newdateipfad)
                    if (newdateipfad[-1]) =="l":
                        #datei an stelle newdateipfad tokenisiern und pos
                         tree = ET.parse(newdateipfad)
                         root = tree.getroot()
                         #print(root.tag)
                        # print(root.attrib)
                         for child in root:
                           #  print(child.tag,child.attrib)
                             if child.tag == 'TEXT':
                                 #hier text parsen und stazlängen zählen
                                 atext = nlp(child.text)
                                 satzl = 0
                                 for token in atext:
                                     if token.tag_ == ".":
                                         if len(Satzlh)>(satzl+1):
                                             Satzlh[satzl]=Satzlh[satzl]+1
                                         else:
                                             l = len(Satzlh)
                                             while l < satzl:
                                                 Satzlh = Satzlh + [0]
                                                 l = l+1
                                             Satzlh = Satzlh + [1]
                                         satzl = 0
                                     elif token.pos != 'PUNCT':
                                         satzl = satzl+1
                                            
                                             
                                     if token.tag_ in PosTags:
                                         numPosTags[PosTags.index(token.tag_)] = numPosTags[PosTags.index(token.tag_)] + 1
                                     else: 
                                         PosTags = PosTags + [token.tag_]
                                         numPosTags = numPosTags + [1] 
                                 #print(child)
                             else:
                                 for grandchild in child:
                                     if grandchild.tag == 'SPATIAL_ENTITY':
                                         numSpatialEntities = numSpatialEntities + 1
                                     elif grandchild.tag == 'PLACE':
                                         numPlaces = numPlaces + 1
                                     elif grandchild.tag == 'MOTION':
                                         numMotions = numMotions + 1
                                     elif grandchild.tag == ('SPATIAL_SIGNAL' or 'MOTION_SIGNAL'):
                                         numSignals = numSignals + 1
                                     elif grandchild.tag == 'QSLINK':
                                         numQsLinks = numQsLinks + 1
                                     elif grandchild.tag == 'OLINK':
                                         numOLinks = numOLinks + 1
                    z = z+1
                    
            else:
                # datei an stelle dateipfad tokenisieren und pos
                #doc = open(dateipfad)
               # print(ordnerdaten[y])
                tree = ET.parse(dateipfad)
                root = tree.getroot()
               # print(root.tag)
               # print(root.attrib)
                for child in root:
                 #   print(child.tag,child.attrib)
                    if child.tag == 'TEXT':
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
                                            
                            if token.tag_ in PosTags:
                                numPosTags[PosTags.index(token.tag_)] = numPosTags[PosTags.index(token.tag_)] + 1
                            else: 
                                PosTags = PosTags + [token.tag_]
                                numPosTags = numPosTags + [1] 
                           
                        
                        
                         #hier text parsen und stazlängen zählen
                        pass
                     #   print(child)
                     
                    else: 
                        for grandchild in child:
                            if grandchild.tag == 'SPATIAL_ENTITY':
                                numSpatialEntities = numSpatialEntities + 1
                            elif grandchild.tag == 'PLACE':
                                numPlaces = numPlaces + 1
                            elif grandchild.tag == 'MOTION':
                                numMotions = numMotions + 1
                            elif grandchild.tag == ('SPATIAL_SIGNAL' or 'MOTION_SIGNAL'):
                                numSignals = numSignals + 1
                            elif grandchild.tag == 'QSLINK':
                                numQsLinks = numQsLinks + 1
                            elif grandchild.tag == 'OLINK':
                                numOLinks = numOLinks + 1
                                
                        
                                
                #baum = dom.parse(dateipfad)

            y = y+1
            
    x = x+1

print ('Anzahl Motions = '+str(numMotions)+'\n'+'Anzahl SpatialEntities = ' + str(numSpatialEntities))
print( 'Anzahl Places = ' + str(numPlaces) + '\n' + 'Anzahl Signals = ' + str(numSignals))
print('Anzahl QSLinks = ' + str(numQsLinks) + '\n' + 'Anzahl OLinks = ' + str(numOLinks))
print('PoS-Tags und ihre Häufigkeit:')
i= 0
while i< len(PosTags):
    print(str(PosTags[i])+ ' kommt ' + str(numPosTags[i]) + '-mal vor.')
    i = i+1

satzlaenge = list(range(0, len(Satzlh)))
# die Y-Werte:
haeufigkeit = Satzlh
plt.plot(satzlaenge, haeufigkeit)
plt.show()

