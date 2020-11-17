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

with zipfile.ZipFile('training.zip','r') as zfile:
    zfile.extractall('training')
    
daten = os.listdir("training")[0]
mehrdaten = "training/"+daten
ordner = os.listdir(mehrdaten)

#variablen die die Häufigkeit zählen
PoS_tags = []
numSpatialEntities = 0
numPlaces = 0
numMotions = 0
numSignals = 0 
numQsLinks = 0
numOLinks = 0

Satzlh = [(0,0)] #Tupel: Stelle 1 Satzlänge, Stelle 2 Häufigkeit

nlp = spacy.load("en_core_web_sm")

x=0
for i in ordner:
    nordner = mehrdaten + "/" + ordner[x]
    if os.path.isdir(nordner):
        ordnerdaten = os.listdir(nordner)
        print(ordnerdaten)
        
        #die einzelnen xml dateien durchegehen:
        y = 0
        for datei in ordnerdaten:
            dateipfad = nordner + "/" + ordnerdaten[y]
            if os.path.isdir(dateipfad):
                anderedaten = os.listdir(dateipfad)
                z = 0
                for ndatei in  anderedaten:
                    newdateipfad = dateipfad + "/" + anderedaten[z]
                    if (anderedaten[z])[-1] =="l" and (anderedaten[-2]) == "m" and (anderedaten[-3] == "x"):
                        #datei an stelle newdateipfad tokenisiern und pos
                         tree = ET.parse(newdateipfad)
                         root = tree.getroot()
                         print(root.tag)
                         print(root.attrib)
                         for child in root:
                             print(child.tag,child.attrib)
                             if child.tag == 'TEXT':
                                 print(child)
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
                print(ordnerdaten[y])
                tree = ET.parse(dateipfad)
                root = tree.getroot()
                print(root.tag)
                print(root.attrib)
                for child in root:
                    print(child.tag,child.attrib)
                    if child.tag == 'TEXT':
                        print(child)
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





