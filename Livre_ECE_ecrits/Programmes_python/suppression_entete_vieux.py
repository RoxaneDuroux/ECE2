#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 16:10:40 2018

@author: ajobin
"""
import os
import re

#######
# Fixer le répertoire courant
#######
os.chdir('../')
# Pour Roxane : commenter la ligne précédente et décommenter celle-ci
# os.chdir('/home/roxane/Dropbox/ECE2/ECE2_Carnot/Extraction_exos')

#######
# Début du programme pour remplacer les entêtes
#######

# supprime les chaines d'un texte connaissant les positions de début de ces chaines
# on regroupe chaque bout du texte "troué" dans une liste

def suppListe(Lchaine, lDeb, texte) :
    L1 = [0] + [lDeb[k] + len(Lchaine[k]) for k in range(len(lDeb))]
    L2 = lDeb + [-1]
    Ltexte = [texte[L1[k]:L2[k]] for k in range(len(L1))]
    Ltexte[-1] = Ltexte[-1] + texte[-1]
    return Ltexte

# supprimer toutes les occurrences de la même chaîne

def suppChaineUnique(chaine, lDeb, texte) :
    Lchaine = [chaine for n in lDeb]
    Ltexte = suppListe(Lchaine, lDeb, texte)
    return Ltexte

# supprime tout ce qui se situe avant %%DEBUT (inclus) et remplace par \chapter*{ECRICOME 2016 : le sujet / le corrigé}
def remplaceEntete(nomAnnale, sujCorr, contenu) :
    # remplacer l'entete du doc cible par la nouvelle entete
    regBD = re.compile("%%DEBUT")
    # récupérer la place de \begin{document} dans le document cible
    posBD = [m.start() for m in re.finditer(regBD, contenu)]
    # suppresion de tout ce qui précède %%DEBUT => le fichier est scindé en 2 : tout ce qui précède %%DEBUT et tout ce qui suit
    Ltexte = suppChaineUnique("%%DEBUT", posBD, contenu)
    fichierTeX = "\\chapter*{" + nomAnnale + " : le " + sujCorr + "}" + "\n  " + "\n%" + Ltexte[1]
    ###
    return fichierTeX

### ESSAI ###
#fichier_lecture = "ECRICOME_2016_correction.tex"
#mon_fichier_source = open(fichier_lecture, "r")
#strSource = mon_fichier_source.read()
#mon_fichier_source.close()
#cont = remplaceEntete("ECRICOME 2016", "sujet", strSource)
#mon_fichier_ecriture = open("ECRICOME_2016_correction_entete.tex", "w")
#mon_fichier_ecriture.write(cont)
#mon_fichier_ecriture.close()

def remplaceTouteEntete(annee) :
    listeNomGenAnnale = ["ECRICOME"] #, "EDHEC", "EML", "ESSEC-I", "ESSEC-II", "HEC"]
    # une première passe pour tous les corrigés
    for nomAnnale in listeNomGenAnnale :
        fichier_lecture = nomAnnale + "_" + annee + "_correction.tex"
        mon_fichier_source = open(annee + "/" + fichier_lecture, "r")
        strSource = mon_fichier_source.read()
        mon_fichier_source.close()
        cont = remplaceEntete(nomAnnale + " " + annee, "corrigé", strSource)
        mon_fichier_ecriture = open(annee + "_sans_entete/" + nomAnnale + "_" + annee + "_correction_sans_entete.tex", "w")
        mon_fichier_ecriture.write(cont)
        mon_fichier_ecriture.close()
    # une deuxième passe pour tous les sujets
    for nomAnnale in listeNomGenAnnale :
        fichier_lecture = nomAnnale + "_" + annee + ".tex"
        mon_fichier_source = open(annee + "/" + fichier_lecture, "r")
        strSource = mon_fichier_source.read()
        mon_fichier_source.close()
        cont = remplaceEntete(nomAnnale + " " + annee, "sujet", strSource)
        mon_fichier_ecriture = open(annee + "_sans_entete/" + nomAnnale + "_" + annee + "_sans_entete.tex", "w")
        mon_fichier_ecriture.write(cont)
        mon_fichier_ecriture.close()
    return print("WELL DONE, les fichiers ont bien été copiés dans " + annee + "_sans_entete")

#######
# Début du programme pour virer les proof
#######

# la fonction permettant de supprimer d'un texte tous les \begin{chaine}...\end{chaine}

def supprimeBE(texte, chaine) :
    regBeg = re.compile("\\\\begin{" + chaine + "}")
    listeDebBeg = [m.start() for m in re.finditer(regBeg, texte)]
    ###
    regEnd = re.compile("\\\\end{" + chaine + "}")
    listeDebEnd = [m.start() for m in re.finditer(regEnd, texte)]
    ##
    # L2 : liste des positions des début des \begin{chaine}
    # L1 : liste des positions des fins des \end{chaine}
    L1 = [0] + [debEnd + 6 + len(chaine) for debEnd in listeDebEnd] 
    L2 = listeDebBeg + [-1]
    Ltexte = [texte[L1[k]:L2[k]] for k in range(len(L1))]
    Ltexte[-1] = Ltexte[-1] + texte[-1]
    texteRes = ""
    for elmt in Ltexte :
        texteRes += elmt
    return texteRes

def supprimeRemProof(fichier, remProof, dossierSource, dossierCible) :
    ajoutNom = "_sans_" + remProof + ".tex"
    fichier_lecture = fichier
    mon_fichier_source = open(dossierSource + "/" + fichier_lecture, "r")
    strSource = mon_fichier_source.read()
    mon_fichier_source.close()
    if remProof == "remark" :
        cont = supprimeBE(strSource, "remark")
        cont = supprimeBE(cont, "remarkL")
    elif remProof == "proof" :        
        cont = supprimeBE(strSource, "proof")
        # on supprime les proof mais aussi les remark hors proof !
        cont = supprimeBE(cont, "remark")
        cont = supprimeBE(cont, "remarkL")
    j = 0
    fichierTeX = ''
    while j < len(cont) :
        # virer les \newpage
        if cont[j:j+8] == "\\newpage" :
            fichierTeX += "%\\newpage"
            j = j+8        
        else :
            fichierTeX += cont[j]
            j = j+1
    mon_fichier_ecriture = open(dossierCible + "/" + fichier[0:-4] + ajoutNom, "w")
    mon_fichier_ecriture.write(fichierTeX)
    mon_fichier_ecriture.close()
    return print("WELL DONE : " + fichier[0:-4] + ajoutNom + " créé")

# supprimeRem("programme_python/essai.tex")

def supprimeTouteRemProof(annee, remProof) :
    listeNomGenAnnale = ["ECRICOME", "EML"] #, "EDHEC", "EML", "ESSEC-I", "ESSEC-II", "HEC"]
    dossierSource = annee
    dossierCible = annee #+ "_sans_" + remProof
    for nomAnnale in listeNomGenAnnale :
        supprimeRemProof(nomAnnale + "_" + annee + "_correction.tex", remProof, dossierSource, dossierCible)
    return print("WELL DONE ! Les fichiers ont bien été copiés dans " + annee + "_sans_" + remProof)

listeAnnee = ["2018"]
[remplaceTouteEntete(annee) for annee in listeAnnee]
[supprimeTouteRemProof(annee, "remark") for annee in listeAnnee]
[supprimeTouteRemProof(annee, "proof") for annee in listeAnnee]




