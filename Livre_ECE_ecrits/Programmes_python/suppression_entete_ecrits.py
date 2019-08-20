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
    cont = "\\chapter*{" + nomAnnale + " : le " + sujCorr + "}" + "\n  " + "\n%" + Ltexte[1]
    
    j = 0
    fichierTeX = ''
    while j < len(cont) :
        if cont[j:j+13] == "\\end{document" :
            fichierTeX += ""
            j = j+len(cont)
        else :
            fichierTeX += cont[j]
            j = j+1

    ###
    return fichierTeX 

### ESSAI ###
#fichier_lecture = "2016/ECRICOME_2016_correction.tex"
#mon_fichier_source = open(fichier_lecture, "r")
#strSource = mon_fichier_source.read()
#mon_fichier_source.close()
#cont = remplaceEntete("ECRICOME 2016", "sujet", strSource)
#mon_fichier_ecriture = open("ECRICOME_2016_correction_sans_entete.tex", "w")
#mon_fichier_ecriture.write(cont)
#mon_fichier_ecriture.close()

# listeNomGenAnnale = = ["ECRICOME", "EDHEC", "EML", "ESSEC-I", "ESSEC-II", "HEC"]

#def remplaceTouteEntete(annee, listeNomGenAnnale) :
#    # listeNomGenAnnale = ["ECRICOME", "EDHEC", "EML", "ESSEC-I", "ESSEC-II", "HEC"]
#    # une première passe pour tous les corrigés
#    for nomAnnale in listeNomGenAnnale :
#        print(nomAnnale)
#        fichier_lecture = nomAnnale + "_" + str(annee) + "_correction.tex"    
#        # ESSAI 
#        if os.path.exists(str(annee) + "/" + fichier_lecture) :
#            # le if devrait suffire, pas besoin de l'exception car pas d'erreur je pense (?)
#            with open(str(annee) + "/" + fichier_lecture, 'r') as mon_fichier_source : 
#                try : 
#                    strSource = mon_fichier_source.read()
#                    mon_fichier_source.close()
#                    cont = remplaceEntete(nomAnnale + " " + str(annee), "corrigé", strSource)
#                    # DANS LE MEME DOSSIER !
#                    # mon_fichier_ecriture = open(annee + "_sans_entete/" + nomAnnale + "_" + annee + "_correction_sans_entete.tex", "w")
#                    mon_fichier_ecriture = open(str(annee) + "/" + nomAnnale + "_" + str(annee) + "_correction_sans_entete.tex", "w")
#                    mon_fichier_ecriture.write(cont)
#                    mon_fichier_ecriture.close()
#                    return print("WELL DONE, fichier " + str(annee) + "/" + nomAnnale + "_" + str(annee) + "_correction_sans_entete.tex" + " créé")
#                except :
#                   print("ATTENTION : erreur lors du traitement du fichier " + str(annee) + "/" + nomAnnale + "_" + str(annee) + "_correction_sans_entete.tex")
#        else :
#            print("ATTENTION : fichier " + str(annee) + "/" + fichier_lecture + " non trouvé !")
#    # une deuxième passe pour tous les sujets
#    for nomAnnale in listeNomGenAnnale :
#        fichier_lecture = nomAnnale + "_" + str(annee) + ".tex"
#        # ESSAI 
#        if os.path.exists(str(annee) + "/" + fichier_lecture) :
#            # le if devrait suffire, pas besoin de l'exception car pas d'erreur je pense (?)
#            with open(str(annee) + "/" + fichier_lecture, 'r') as mon_fichier_source : 
#                try :             
#                    mon_fichier_source = open(str(annee) + "/" + fichier_lecture, "r")
#                    strSource = mon_fichier_source.read()
#                    mon_fichier_source.close()
#                    cont = remplaceEntete(nomAnnale + " " + str(annee), "sujet", strSource)
#                    # DANS LE MEME DOSSIER !
#                    # mon_fichier_ecriture = open(str(annee) + "_sans_entete/" + nomAnnale + "_" + annee + "_sans_entete.tex", "w")
#                    mon_fichier_ecriture = open(str(annee) + '/' + nomAnnale + "_" + str(annee) + "_sans_entete.tex", "w")
#                    mon_fichier_ecriture.write(cont)
#                    mon_fichier_ecriture.close()
#                    return print("WELL DONE, fichier " + str(annee) + "/" + nomAnnale + "_" + str(annee) + "_sans_entete.tex" + " créé")
#                except :
#                   print("ATTENTION : erreur lors du traitement du fichier " + str(annee) + "/" + nomAnnale + "_" + str(annee) + "_sans_entete.tex")
#        else :
#            return print("ATTENTION : fichier " + str(annee) + "/" + fichier_lecture + " non trouvé !")


# SAUVEGARDE
def remplaceTouteEntete(annee, listeNomGenAnnale) :
    # listeNomGenAnnale = ["ECRICOME", "EDHEC", "EML", "ESSEC-I", "ESSEC-II", "HEC"]
    # une première passe pour tous les corrigés
    for nomAnnale in listeNomGenAnnale :
        fichier_lecture = nomAnnale + "_" + str(annee) + "_correction.tex"    
        mon_fichier_source = open(str(annee) + "/" + fichier_lecture, "r")
        strSource = mon_fichier_source.read()
        mon_fichier_source.close()
        cont = remplaceEntete(nomAnnale + " " + str(annee), "corrigé", strSource)
        # DANS LE MEME DOSSIER !
        # mon_fichier_ecriture = open(annee + "_sans_entete/" + nomAnnale + "_" + annee + "_correction_sans_entete.tex", "w")
        mon_fichier_ecriture = open(str(annee) + "/" + nomAnnale + "_" + str(annee) + "_correction_sans_entete.tex", "w")
        mon_fichier_ecriture.write(cont)
        mon_fichier_ecriture.close()
        print("OK pour " + nomAnnale + " corrigé")
    # une deuxième passe pour tous les sujets
    for nomAnnale in listeNomGenAnnale :
        fichier_lecture = nomAnnale + "_" + str(annee) + ".tex"
        mon_fichier_source = open(str(annee) + "/" + fichier_lecture, "r")
        strSource = mon_fichier_source.read()
        mon_fichier_source.close()
        cont = remplaceEntete(nomAnnale + " " + str(annee), "sujet", strSource)
        # DANS LE MEME DOSSIER !
        # mon_fichier_ecriture = open(annee + "_sans_entete/" + nomAnnale + "_" + annee + "_sans_entete.tex", "w")
        mon_fichier_ecriture = open(str(annee) + "/" + nomAnnale + "_" + str(annee) + "_sans_entete.tex", "w")
        mon_fichier_ecriture.write(cont)
        mon_fichier_ecriture.close()
        print("OK pour " + nomAnnale + " sujet")
    return print("WELL DONE, les fichiers ont bien été copiés dans " + str(annee) + "_sans_entete")

def remplaceTouteEnteteAnneeDebAnneeFin(anneeDeb, anneeFin, listeNomGenAnnale) :
    # listeNomGenAnnale = ["ECRICOME", "EML", "EDHEC", "EML", "ESSEC-I", "ESSEC-II", "HEC"]
    listeAnnee = [i for i in range(anneeDeb, anneeFin + 1)]
    [remplaceTouteEntete(annee, listeNomGenAnnale) for annee in listeAnnee]
    return print("WELL DONE ! Tous les dossiers ont bien été traités et le fichiers DESentêtés.")

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
    # quand on vire les remark on le fait figurer dans le nom, quand on vire les proof (sous-entendu après les remark !), on n'ajoute pas d'extension
    if remProof == "remark" :                                                                                   
        ajoutNom = "_sans_" + remProof + ".tex"
        num = 4 # on vire le .tex (4 caractères) avant d'ajouter l'extension
    else : 
        ajoutNom = ".tex"
        num = 15 # on vire le _correction.tex (16 caractères) avant d'ajouter l'extension
    fichier_lecture = fichier
    # ESSAI 
    if os.path.exists(dossierSource + "/" + fichier_lecture) :
        # le if devrait suffire, pas besoin de l'exception car pas d'erreur je pense (?)
        with open(dossierSource + "/" + fichier_lecture, "r") as mon_fichier_source : 
            try : 
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
                    # virer les \newpage : on garde ceux qui sont commentés et on commente ceux qui ne le sont pas
                    if cont[j:j+9] == "%\\newpage" :
                        fichierTeX += cont[j:j+9]
                        j = j+9
                    elif cont[j:j+8] == "\\newpage" :
                        fichierTeX += "%\\newpage"
                        j = j+8        
                    else :
                        fichierTeX += cont[j]
                        j = j+1
                mon_fichier_ecriture = open(dossierCible + "/" + fichier[0:-num] + ajoutNom, "w")
                mon_fichier_ecriture.write(fichierTeX)
                mon_fichier_ecriture.close()                
                return print("WELL DONE : " + fichier[0:-num] + ajoutNom + " créé")
            except :
                return print("ATTENTION : fichier " + dossierSource + "/" + fichier_lecture + " non trouvé !")
    else :
        return print("ATTENTION : fichier " + dossierSource + "/" + fichier_lecture + " non trouvé !")
    
# SAUVEGARDE
#def supprimeRemProof(fichier, remProof, dossierSource, dossierCible) :
#    ajoutNom = "_sans_" + remProof + ".tex"
#    fichier_lecture = fichier
#    mon_fichier_source = open(dossierSource + "/" + fichier_lecture, "r")
#    strSource = mon_fichier_source.read()
#    mon_fichier_source.close()
#    if remProof == "remark" :
#        cont = supprimeBE(strSource, "remark")
#        cont = supprimeBE(cont, "remarkL")
#    elif remProof == "proof" :        
#        cont = supprimeBE(strSource, "proof")
#        # on supprime les proof mais aussi les remark hors proof !
#        cont = supprimeBE(cont, "remark")
#        cont = supprimeBE(cont, "remarkL")
#    j = 0
#    fichierTeX = ''
#    while j < len(cont) :
#        # virer les \newpage
#        if cont[j:j+8] == "\\newpage" :
#            fichierTeX += "%\\newpage"
#            j = j+8        
#        else :
#            fichierTeX += cont[j]
#            j = j+1
#    mon_fichier_ecriture = open(dossierCible + "/" + fichier[0:-4] + ajoutNom, "w")
#    mon_fichier_ecriture.write(fichierTeX)
#    mon_fichier_ecriture.close()
#    return print("WELL DONE : " + fichier[0:-4] + ajoutNom + " créé")

# supprimeRem("programme_python/essai.tex")
# listeNomGenAnnale = ["ECRICOME", "EML", "EDHEC", "EML", "ESSEC-I", "ESSEC-II", "HEC"]

def supprimeTouteRemProof(annee, remProof, listeNomGenAnnale) :
    # listeNomGenAnnale = ["ECRICOME", "EML", "EDHEC", "EML", "ESSEC-I", "ESSEC-II", "HEC"]
    dossierSource = str(annee)
    dossierCible = str(annee) #+ "_sans_" + remProof
    for nomAnnale in listeNomGenAnnale :
        supprimeRemProof(nomAnnale + "_" + str(annee) + "_correction.tex", remProof, dossierSource, dossierCible)
    # return print("WELL DONE ! Les fichiers ont bien été copiés dans " + str(annee) + "_sans_" + remProof)

# la même mais pour les annales de anneeDeb à anneFin

def supprimeTouteRemProofAnneeDebAnneeFin(anneeDeb, anneeFin, listeNomGenAnnale) :
    # listeNomGenAnnale = ["ECRICOME", "EML", "EDHEC", "EML", "ESSEC-I", "ESSEC-II", "HEC"]
    listeAnnee = [i for i in range(anneeDeb, anneeFin + 1)]
    [supprimeTouteRemProof(annee, "remark", listeNomGenAnnale) for annee in listeAnnee]
    [supprimeTouteRemProof(annee, "proof", listeNomGenAnnale) for annee in listeAnnee]
    return print("WELL DONE ! Tous les dossiers ont bien été traités.")

#listeAnnee = ["2018"]
#listeAnnale = ["ECRICOME", "EDHEC", "EML", "ESSEC-I", "ESSEC-II", "HEC"]
#[remplaceTouteEntete(annee, listeAnnale) for annee in listeAnnee]
#[supprimeTouteRemProof(annee, "remark", listeAnnale) for annee in listeAnnee]
#[supprimeTouteRemProof(annee, "proof", listeAnnale) for annee in listeAnnee]




