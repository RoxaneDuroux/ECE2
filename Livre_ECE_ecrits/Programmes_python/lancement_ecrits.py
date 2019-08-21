#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 26 01:22:15 2018

@author: ajobin
"""

import os 

import suppression_entete_ecrits as supp 
# Les deux fichiers modifient le dossier courant. Pas très malin...
# Gaffe : on définit les dir dans des fichiers qu'on charge
#os.chdir('../')
#import tri_par_themes_ecrits as tri

###############
## UTILISATION
###############

# I. Pour créer les fichiers sans entete, sans proof, sans remark
## OBLIGATOIRE D'EXECUTER CECI EN PREMIER !
anneeDeb = 2016
anneeFin = 2018
# listeAnnale = ["oraux_HEC"] 
listeAnnale = ["ECRICOME", "EDHEC", "EML", "ESSEC-I", "ESSEC-II", "HEC"] # pour les écrits !

supp.supprimeTouteRemProofAnneeDebAnneeFin(anneeDeb, anneeFin, listeAnnale) 
supp.remplaceTouteEnteteAnneeDebAnneeFin(anneeDeb, anneeFin, listeAnnale) 

#supp.remplaceTouteEntete(2016, listeAnnale)

# II. Pour la gestion des thèmes et la récupération des exercices liés aux thèmes souhaités

# 1) Pour trouver les annales qui contiennent au moins un élément d'une liste de contraintes données 
# liste_contraintes = ['estimBiais', 'estimConv', 'estimation', 'inegBT']
# tri.trouveAnnales(liste_contraintes, anneeDeb, anneeFin, ';')

# 2) Pour générer la liste des thèmes avec occurrences sur une période donnée
# tri.gestionThemesAnnee(anneeDeb, anneeFin)
