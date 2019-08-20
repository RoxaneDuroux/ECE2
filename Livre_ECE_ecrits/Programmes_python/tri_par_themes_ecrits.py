# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 16:10:40 2018

@author: ajobin
"""
import os
import re

######
## La balise a repéré en tout premier lieu est %%% EPR %%% HEC
######

#######
# Fixer le répertoire courant : on prend celui au-dessus du dossier contenant les .py
#######
#os.chdir('../')
# Pour Roxane : commenter la ligne précédente et décommenter celle-ci
# os.chdir('/home/roxane/Dropbox/ECE2/ECE2_Carnot/Extraction_exos')

# On repère dans le fichier toutes les balises %%% EPR %%% HEC
# Pour chaque balise, on extrait le contenu situé entre "%%% EPR %%% HEC" et le \begin{exercice...} (exclu)
# Le résultat est texteRes (chaîne de caractère)

def extraitContenuT(texte) :
#    regBeg = re.compile('\\\subsection')
#    listeDebC1 = [m.start() for m in re.finditer(regBeg, texte)]
#    Lsub = []
#    for i in listeDebC1 :
#        j = i
#        texteSub = ''
#        while texte[j] != '}' :
#            texteSub += texte[j]
#            j += 1
#        texteSub += '}\n\n'
#        Lsub += [texteSub]
    ##
    regBeg = re.compile("%%% EPR %%%")
    listeDebCont = [m.start() for m in re.finditer(regBeg, texte)]
    texteRes = ''
#    unDeux = 1
#    k = 0
    for i in listeDebCont :
        j = i
#        unDeux = (1 + unDeux) % 2
#        if unDeux == 0 :
#            texteRes += Lsub[k]
#            k += 1
        while j+5 < len(texte) and texte[j:j+6] != "\\begin" :
            texteRes += texte[j]
            j += 1
        texteRes += "\n"    
    return texteRes

# CE QUI EST COMMENTÉ : si on le décommente, on obtient dans le fichier des contenus \subsection*{Sujet E...} => c'est surtout pertinent dans le fichier d'exos trouvés!
#annee = 2017
#fichier_lecture = "oraux_HEC_" + str(annee) + ".tex"
#with open(str(annee) + "/" + fichier_lecture, 'r') as mon_fichier_source :      
#    texte = mon_fichier_source.read()
#    # print(texte)
#    mon_fichier_source.close()
#    tRes = extraitContenuT(texte)    
#print(tRes)

# On appelle la fonction précédente sur le fichier oraux_HEC_annee.tex du dossier annee
# Le résultat est copié dans un fichier oraux_HEC_annee_contenu.tex créé dans le dossier annee

def extraitContenuF(annee) :
    fichier_lecture = "oraux_HEC_" + str(annee) + ".tex"
    if os.path.exists(str(annee) + "/" + fichier_lecture) :
        with open(str(annee) + "/" + fichier_lecture, 'r') as mon_fichier_source :         
            strSource = mon_fichier_source.read()
            mon_fichier_source.close()
            cont = extraitContenuT(strSource)
            mon_fichier_ecriture = open(str(annee) + "/" + "oraux_HEC_" + str(annee) + "_contenu.tex", "w")
            mon_fichier_ecriture.write(cont)
            mon_fichier_ecriture.close()
            return print("WELL DONE, le fichier " + "oraux_HEC_" + str(annee) + "_contenu.tex" + " a bien été créé dans le répertoire " + str(annee))
    else :
        return print("ATTENTION : le fichier " + str(annee) + "/" + fichier_lecture + " n'existe pas.")

# extraitContenuF(2017)

# On considère les dossiers annee pour annee dans listeAnnee
# On parcourt tous les fichiers d'énoncés .tex et on en extrait le contenu grâce à la fonction précédente
# Le résultat est copié dans un fichier oraux_HEC_annee_contenu.tex créé pour chaque dossier annee

def extraitToutContenu(listeAnnee) :
    for annee in listeAnnee :
        extraitContenuF(str(annee))
    return print("WELL DONE : tous les fichiers de contenu ont été créés.")

# listeA = [2017-i for i in range(10)]
# extraitToutContenu(listeA)

# Sans supposer que tous les contenus ont été extraits année par année
# => ils sont extraits à la volée par cette fonction et le fichier contenu est créé dans chaque dossier annee correspondant (non nécessaire)
# On construit la concaténation des contenus et on écrit le fichier dans Contenu/contenu_anneeDeb_anneeFin.tex
# C'EST LA FONCTION À UTILISER !

def contAnneeDebAnneFin(anneeDeb, anneeFin) :
    listeAnnee = [i for i in range(anneeDeb, anneeFin + 1)]
    contenu = ''
    for annee in listeAnnee :
        fichier_lecture = "oraux_HEC_" + str(annee) + ".tex"
        #
        anneeProb = ''
        if os.path.exists(str(annee) + "/" + fichier_lecture) :
            with open(str(annee) + "/" + fichier_lecture, 'r') as mon_fichier_source :
                strSource = mon_fichier_source.read()
                mon_fichier_source.close()
                cont = extraitContenuT(strSource)
                mon_fichier_volee = open(str(annee) + "/" + "oraux_HEC_" + str(annee) + "_contenu.tex", "w")
                mon_fichier_volee.write(cont)
                mon_fichier_volee.close()
                contenu += cont
                if anneeDeb == anneeFin :
                    nom_annee = str(anneeDeb)
                else :
                    nom_annee = str(anneeDeb) + "_" + str(anneeFin)
        else : 
            anneeProb += str(annee) + ', '
    mon_fichier_ecriture = open("Contenu" + "/" + "contenu_" + nom_annee + ".tex", "w")
    mon_fichier_ecriture.write(contenu)
    mon_fichier_ecriture.close()
    if anneeProb == '':
        return print("WELL DONE, le fichier des contenus de " + str(anneeDeb) + " à " + str(anneeFin) + " a bien été généré dans le dossier Contenu")
    else :
        return print("ATTENTION : les fichiers " + str(annee) + "/" + "oraux_HEC_" + anneeProb[:-2] + " n'existent pas.")


#contAnneeDebAnneFin(2005, 2017)


################################################################################################################


####################
### Extraction des thèmes 
####################

# Récupérer les caractères jusqu'au symbole de fin de ligne ";" 
# Les symboles non considérés [' ', ':', '%', '\n', '\r'] ne sont pas récupérés

def recupereLigne(chaine, symboleFinLigne, symbolesNonConsideres) :
    ligne = ''
    k = 0
    for s in chaine :
        if s in symbolesNonConsideres :
            k = k+1
        elif (s != symboleFinLigne) :
            ligne += s
            k = k+1
        else :
            break    
    return (ligne, k)

# Retirer les espaces initiaux d'une chaîne de caractère (plus propre)

def retireEspaceInit(chaine) :
    k = 0
    for s in chaine :
        if s == ' ' :
            k = k + 1
        else :
            break
    return chaine[k:]

# On considère la chaîne de caractères et on repère les balises ['ECR', 'EDH', 'EML', 'ESS', 'HEC', 'ESC'] 
# On coupe suivant ces balises à l'aide de la fonction split. Cela permet de récupérer une liste contenant les débuts de description 

def splitChaine(chaine, symbolesEntree) :
    L = chaine.split(symbolesEntree)
    Lret = []
    for elmt in L :
        if elmt[:3] in ['ECR', 'EDH', 'EML', 'ESS', 'HEC', 'ESC'] :
            Lret += [elmt]
    return Lret

# On considère une description et on récupère les mots après la balise % theme (on les range dans une liste)

def extraitListeTheme(description, symboleFinLigne) :
    j = 0
    while j < len(description) :
        if (description[j:j+5] == 'theme') | (description[j:j+5] == 'thème') :
            (theme, k) = recupereLigne(description[j+5:], symboleFinLigne, [' ', ':', '%', '\n', '\r']) 
            break
        else :
            j += 1
    return theme.split(',')
      
# On considère une liste de thème issue d'une description
# On considère une liste de contraintes (liste de thèmes)
# Si l'un de ces thèmes contrainte est dans la liste des thèmes, on renvoie Vrai et Faux sinon

def verifUneContrainte(Lcontraintes, Ltheme) :
    bool = False
    for elmt in Lcontraintes :
        if elmt in Ltheme :
            bool = True
            break
    return bool

# Extraire les infos d'une description
# On crée une chaîne de caractères annale qui contient la description un peu mieux présentée

def extraitInfo(description, symboleFinLigne) :
    j = 0
    annale = ''
    (titre, k) = recupereLigne(description, symboleFinLigne, [' ', ':', '%', '\n', '\r']) 
    annale += titre + '-'
    j = j + k
    while j < len(description) :
        if (description[j:j+5] == 'annee') : # ATTENTION: probleme en utf-8 ! | (description[j:j+5] == 'année') :
            (session, k) = recupereLigne(description[j+5:], symboleFinLigne, [' ', ':', '%', '\n', '\r']) 
            annale += session + ', '
            j = j + k
        elif description[j:j+4] == 'type' :
            (exo, k) = recupereLigne(description[j+4:], symboleFinLigne, [' ', ':', '%', '\n', '\r']) 
            annale += exo
            j = j + k
        elif description[j:j+7] == 'interro' :
            (DS, k) = recupereLigne(description[j+7:], symboleFinLigne, [' ', ':', '%', '\n', '\r']) 
            if DS == '' :
                annale += '\n' + '=> jamais donné'
            else :
                annale += '\n' + '=> donné en ' + DS
            j = j + k
        elif (description[j:j+12] == 'commentaires') : # ATTENTION: probleme en utf-8 !| (description[j:j+12] == 'commentaire'):
            (comm, k) = recupereLigne(description[j+12:], symboleFinLigne, [':', '%', '\n', '\r']) 
            annale += '\n' + '=> ' + retireEspaceInit(comm)
            j = j + k
        elif (description[j:j+5] == 'theme') : # ATTENTION: probleme en utf-8 !| (description[j:j+5] == 'thème') :
            (theme, k) = recupereLigne(description[j+5:], symboleFinLigne, [':', '%', '\n', '\r']) 
            annale += '\n' + '=> ' + 'theme : ' + retireEspaceInit(theme)
            j = j + k
        else :
            j = j + 1
    return annale
  
# Extraire les infos d'une description si le thème est trouvé

def extraitInfoSiContrainte(Lcontraintes, description, symboleFinLigne) :
    annale = ''
    Ltheme = extraitListeTheme(description, symboleFinLigne)
    if verifUneContrainte(Lcontraintes, Ltheme) :
        annale = extraitInfo(description, symboleFinLigne)
    return annale

# Extraire la liste des descriptions du fichier
# On part d'un fichier contenuExos (typiquement oraux_HEC_annee.tex) et on extrait deux listes : 
# 1) la liste des descriptions de chaque exo
# 2) la liste des exos correspondants

def extraitListeDescriptionExo(contenuExos) :
    # ATTENTION '%%% EPR %%% ' et pas '%%% EPR %%%'
    Lch = splitChaine(contenuExos, '%%% EPR %%% ')
    listeDesc = []
    listeExo = []
    for ch in Lch :
        Laux = ch.split("\\begin{exercice")
        listeDesc += [Laux[0]]
        #### pour récupérer le texte entre \begin{exercice..} et \end{exrcice..}
        # on récupère d'abord ce qui commence par \begin{exercice
        texte = Laux[1]
        # on récupère ensuite le type d'exo AP / SP ou rien si c'est un {exercice}        
        typeExo = ''
        if texte[0:2] == "AP" or texte[0:2] == "SP" :
            typeExo = texte[0:2]    
        # on récupère tout le texte de l'exo jusqu'à \end{exercice
        texteExo = ''
        j = 0     
        while j+6 < len(texte) and texte[j:j+13] != "\\end{exercice" :
            texteExo += texte[j]
            j += 1
        texteExo = "\\begin{exercice" + texteExo + "\\end{exercice" + typeExo + "} \n" 
        # ATTENTION ! Remplacer la ligne suivante par :
        # listeExo += [texteExo]
        # si on ne veut pas transporter les descriptions dans le fichier .tex généré
        # ATTENTION '%%% EPR %%% ' et pas '%%% EPR %%%'
        listeExo += ['%%% EPR %%% ' + Laux[0] + texteExo]
    return (listeDesc, listeExo)

# Extraire les (descriptions, exo) de chaque annale dont le thème est trouvé dans le fichier de contenu (typiquement oraux_HEC_annee.tex)

def extraitAnnales(Lcontraintes, contenuExos, symboleFinLigne) :
    listeDescription, listeExo = extraitListeDescriptionExo(contenuExos)
    annales = ''
    fichierExo = ''
    for i in range(len(listeDescription)) :
        ann = extraitInfoSiContrainte(Lcontraintes, listeDescription[i], symboleFinLigne)
        if ann != '' :
            annales += ann + '\n\n'
            fichierExo += listeExo[i] + '\n\n'
    return (annales, fichierExo)

# Extraire les (descriptions, exo) de chaque annale dont le thème est trouvé dans le dossier annee (typiquement oraux_HEC_annee.tex)
# ATTENTION le nom du fichier .tex est codé en dur ici !

def extraitAnnalesAnnee(Lcontraintes, annee, symboleFinLigne) :
    fichier_contenu = str(annee) + '/oraux_HEC_' + str(annee) + '.tex'
    #
    if os.path.exists(fichier_contenu) :
        with open(fichier_contenu, 'r') as mon_fichier_CE :
            contenuExos = mon_fichier_CE.read()
            mon_fichier_CE.close()
            #
            (annales, fichierExo) = extraitAnnales(Lcontraintes, contenuExos, symboleFinLigne)
            if annales != '' :
                fichierExo = '\subsection*{Exercices oraux HEC ' + str(annee) + '}' + '\n\n' + fichierExo
            return (annales, fichierExo)
    else :
        return print("ATTENTION : le fichier " + fichier_contenu + " n'existe pas.")

# Extraire les (descriptions, exo) de chaque annale dont le thème est trouvé dans les dossiers anneeDeb...annneFin (typiquement oraux_HEC_annee.tex)

def extraitAnnalesAnneeDebAnneeFin(Lcontraintes, anneeDeb, anneeFin, symboleFinLigne) :
    listeAnnee = [i for i in range(anneeDeb, anneeFin + 1)]
    annalesDF = ''
    exosDF = ''
    for annee in listeAnnee :
        (annales, fichierExo) = extraitAnnalesAnnee(Lcontraintes, annee, symboleFinLigne)        
        annalesDF += annales
        exosDF += fichierExo
    return (annalesDF, exosDF)

#######
# Fonction permettant de lancer l'extraction
#######

# Extraire les (descriptions, exo) de chaque annale dont le thème est trouvé dans le dossier source
# On prend en paramètre la liste des contraintes et les années de début et de fin
# On code en dur le nom des fichiers résultats

def trouveAnnales(Lcontraintes, anneeDeb, anneeFin, symboleFinLigne) :
    (annalesDF, exosDF) = extraitAnnalesAnneeDebAnneeFin(Lcontraintes, anneeDeb, anneeFin, symboleFinLigne)
    ### def correcte des noms
    if anneeDeb == anneeFin :
        nom_annee = str(anneeDeb)
    else :
        nom_annee = str(anneeDeb) + "_" + str(anneeFin)
    fichResTxt = "annales_" + nom_annee + "_" + '_'.join(Lcontraintes) + ".txt"
    fichResTeX = "exercices_" + nom_annee + "_" + '_'.join(Lcontraintes) + ".tex"
    #
    fichier_ecriture_txt = 'Extraction/' + fichResTxt
    fichier_ecriture_TeX = 'Extraction/' + fichResTeX
    ###
    mon_fichier_ecriture_txt = open(fichier_ecriture_txt, "w") # 'w' pour écraser le fichier à chaque fois, 'a' sinon
    mon_fichier_ecriture_TeX = open(fichier_ecriture_TeX, "w") # 'w' pour écraser le fichier à chaque fois, 'a' sinon
    ###
    # extraction des annales à considérer 
    (annales, fichierExo) = extraitAnnalesAnneeDebAnneeFin(Lcontraintes, anneeDeb, anneeFin, symboleFinLigne)
    ### écriture du fichier des résultats
    # pour l'affichage
    contraintes = ", ".join(Lcontraintes)
    phraseInit = 'Voici les annales contenant l\'un des thèmes suivants : ' + contraintes + '.\n\n'
    # écriture du fichier txt
    mon_fichier_ecriture_txt.write(phraseInit + annales)
    mon_fichier_ecriture_txt.close()
    # écriture du fichier TeX
    mon_fichier_ecriture_TeX.write(fichierExo)
    mon_fichier_ecriture_TeX.close()
    ###
    print("\nDONE : programme exécuté avec succès.\nLes fichiers résultats ont été enregistré dans :\n" \
                  + fichier_ecriture_txt + " et " + fichier_ecriture_TeX)
    return (annales, fichierExo) # on peut virer cette ligne. Renvoyer le fichier obtenu permet de faire des tests dessus


# liste_contraintes = ['vaGumbel', 'vaDiscrete', 'suites', 'vaMax']
# trouveAnnales(liste_contraintes, 2005, 2017, ';')


################################################################################################################


####################
### TriAlpha des thèmes 
####################

# L'odre lexico est implémenté de base en python
# Il suffit donc de coder un tri fusion (par exemple)
# Gaffe quand même : l'existence de majuscules influe l'ordre lexico => lower() !

# fusion (fonciton récursive) permet de réaliser la fusion de 2 listes triées
                                                                             
def fusion(Lmot1, Lmot2) :
    if Lmot1 == [] :
        LmotFusion = Lmot2
    elif Lmot2 == [] :
        LmotFusion = Lmot1
    elif Lmot1[0].lower() < Lmot2[0].lower() :
        LmotFusion = [Lmot1[0]] + fusion(Lmot1[1:], Lmot2)
    else :
        LmotFusion = [Lmot2[0]] + fusion(Lmot1, Lmot2[1:])
    return LmotFusion

# triFusion est l'implémentation du tri fusion

def triFusion(listeMots) :
    n = len(listeMots)
    if (n == 0) | (n == 1) :
        L = listeMots
    else :
        L = fusion(triFusion(listeMots[:n//2]), triFusion(listeMots[n//2:]))
    return L

# trouver la place d'un mot dans une liste triée de mot (dichotomie)

def dichotoAux(mot, liste, posMot) :
    pos = posMot
    n = len(liste)
    if n == 0 :
        return -1
    elif mot.lower() < liste[n//2].lower() :
        m = len(liste[:n//2])
        nouvPosMot = posMot - m//2 - m % 2
        pos = dichotoAux(mot, liste[:n//2], nouvPosMot)
    elif mot.lower() > liste[n//2].lower() :
        m = len(liste[n//2+1:])
        nouvPosMot = posMot + m//2 + 1
        pos = dichotoAux(mot, liste[n//2+1:], nouvPosMot)
    return pos

def posMotListe(mot, liste) :
    n = len(liste)
    pos = dichotoAux(mot, liste, n//2)
    return pos

#######
# Partie comparaison des thèmes
#######

# Extraire d'un fichier contenant des descriptions (comme contenus_anneeDeb_anneeFin.tex) la liste (et non pas l'ensemble pour compter les occurences) des thèmes

def extraitListeDescription(contDesc) :
    # ATTENTION '%%% EPR %%% ' et pas '%%% EPR %%%'
    Ldescription = splitChaine(contDesc, '%%% EPR %%% ')
    return Ldescription

# Extraire de la liste des descriptions (du fichier theme) la liste des thèmes

def extraitListeIntegraleTheme(desc, symboleFinLigne) :
    Ldesc = extraitListeDescription(desc)
    LintTheme = []
    for d in Ldesc :
        LintTheme += extraitListeTheme(d, symboleFinLigne)
    return LintTheme

# LthemeExos est la liste de tous les themes trouvées
# LthemeDesc est la liste des themes autorisés

def compteOccurrences(LthemeExosTriee, LthemeDescTriee) :
    Loccurrence = [0 for _ in LthemeDescTriee]
    themesNonPermis = ''
    for theme in LthemeExosTriee :
        k = posMotListe(theme, LthemeDescTriee)
        if k == -1 :
            themesNonPermis += theme + ", "
        else :
            Loccurrence[k] += 1
    themesNonPermis = themesNonPermis[:-2]
    return (Loccurrence, themesNonPermis)


#######
# Partie écriture du fichier résultat
#######

# Le fichier des descriptions se nomme fichDesc (avec l'extension !) et est présent dans le dossier nomDossierSource
# Le fichier des thèmes se nomme fichTheme (avec l'extension !) et est présent dans le même dossier
# Le fichier généré se nomme fichResultat (avec l'extension !) et se trouve dans le dossier nomDossierCible

def gestionThemes(fichDesc, fichTheme, fichResultat, nomDossierSource, nomDossierCible, symboleFinLigne) :
    ### def correcte des noms
    fichier_lecture_description = nomDossierSource + '/' + fichDesc
    fichier_lecture_theme = nomDossierSource + '/' + fichTheme
    fichier_ecriture = nomDossierCible + '/' + fichResultat
    ###
    mon_fichier_description = open(fichier_lecture_description, "r")
    strSourceDesc = mon_fichier_description.read()
    #
    mon_fichier_theme = open(fichier_lecture_theme, "r")
    strSourceTheme = mon_fichier_theme.read()
    ###
    # extraction de la liste des thèmes autorisés : ceux contenus dans le fichier des thèmes
    LthemeDesc = triFusion(extraitListeTheme(strSourceTheme, symboleFinLigne))
    #
    mon_fichier_description.close()
    mon_fichier_theme.close()
    ###
    # strThemeTrie = '\n'.join(LthemeTrie) + '\n\n'
    # phraseInitThemeTrie = 'Voici la liste des thèmes autorisés par le fichier des thèmes : ' + '\n\n'
    # Pour récupérer la liste intégrale des thèmes du fichier contenu_exos
    LintTheme = triFusion(extraitListeIntegraleTheme(strSourceDesc, symboleFinLigne))
    ###
    # On vérifie que les thèmes du fichier description sont bien dans les thèmes autorisés et on compte les occurences d'apparition
    (Locc, themesNP) = compteOccurrences(LintTheme, LthemeDesc)
    LthemeOcc = [LthemeDesc[k] + ' (' + str(Locc[k]) + ')' for k in range(len(LthemeDesc))]
    strThemeOcc = '\n'.join(LthemeOcc) + '\n\n'
    # Phrase pour affichage
    phraseInitThemeOcc = "Voici la liste des thèmes présents (avec occurrence associée) dans le fichier des descriptions : " \
                        + "\n\n"
    if themesNP == '' : 
        phraseThemesNP = "Tous les thèmes du fichier de descriptions sont bien autorisés par le fichier des thèmes." \
                        + '\n' + 'Joie.' + '\n'
    else :
        phraseThemesNP = "Dans le fichier de descriptions, on trouve le(s) thème(s) suivant(s), " \
                        + "non autorisé(s) par le fichier des thèmes : " + themesNP + '.' + '\n' + "Tristesse." \
                        + '\n' + "Vérifiez l'orthographe ou rajoutez le(s) thème(s) au fichier des thèmes." + '\n'   
    phraseFin = 'Allez prendre un café, vous êtes entre de bonnes mains.' + '\n'                                                         
    mon_fichier_ecriture = open(fichier_ecriture, "w") # 'w' pour écraser le fichier à chaque fois, 'a' sinon
    ###
    # écriture du fichier des thèmes 
    #mon_fichier_ecriture.write(phraseInitThemeTrie + strThemeTrie)
    mon_fichier_ecriture.write(phraseInitThemeOcc + strThemeOcc + phraseThemesNP + '\n' + phraseFin)
    mon_fichier_ecriture.close()
    ###
    print("\nDONE : programme exécuté avec succès.\nLe fichier résultat est enregistré dans :\n" \
                  + fichier_ecriture)
    return strThemeOcc # on peut virer cette ligne. Renvoyer le fichier obtenu permet de faire des tests dessus
  
# On appelle la fonction précédente avec les bons arguments
# On crée contenu_anneeDeb_anneeFin.tex
# On crée theme_tries.txt
# => C'EST LA FONCTION À UTILISER

def gestionThemesAnnee(anneeDeb, anneeFin) :
    # on commence par créer le fichier des contenus qui est enregistré dans contenu_anneeDeb_anneeFin.tex dans le fichier Contenu 
    contAnneeDebAnneFin(anneeDeb, anneeFin)
    # pour récupérer ce fichier de contenu dans le dossier Contenu
    dossier_source = "Contenu"
    if anneeDeb == anneeFin :
        nom_annee = str(anneeDeb)
    else :
        nom_annee = str(anneeDeb) + "_" + str(anneeFin)
    fichier_desc = "contenu_" + nom_annee + ".tex"
    fichier_theme = "theme.tex" # placé dans le dossier Contenu => fichier qui contient tous les thèmes
    # pour extraire dans le dossier Extraction
    dossier_resultat = "Extraction"    
    fichier_resultat = "theme_tries.txt"
    symbole_fin_ligne = ';'
    contenu = gestionThemes(fichier_desc, fichier_theme, fichier_resultat, dossier_source, dossier_resultat, symbole_fin_ligne)
    return contenu

###############
## UTILISATION
###############

# 1) Pour trouver les annales qui contiennent au moins un élément d'une liste de contraintes données 
# liste_contraintes = ['vaGumbel', 'vaDiscrete', 'suites', 'vaMax']
# trouveAnnales(liste_contraintes, 2017, 2017, ';')

# 2) Pour générer la liste des thèmes avec occurrences sur une période donnée
# gestionThemesAnnee(2005, 2017)


















# POUBELLE A VIRER

################
### Exemple d'utilisation
################
#
#fichier_desc = "contenu_2005_2016.tex"
#fichDesc = ""
#
#fichier_theme = "theme.tex"
#
#fichier_resultat = "annales_trouvees.txt"
#fichResultat = "annales_trouvees.txt"
#
#dossier_source = "Contenu"
#nomDossierSource = "2017"
#
#dossier_resultat = "Resultats"
#
#nomDossierCible = "Resultats"
#
#liste_contraintes = ['vaGumbel', 'vaDiscrete', 'suites', 'vaMax']
#
#Lcontraintes = ['vaGumbel', 'vaDiscrete', 'suites', 'vaMax']
#symbole_fin_ligne = ';'
#symboleFinLigne = ';'
#
#### def correcte des noms
#fichier_lecture_description = nomDossierSource + '/' + fichDesc
#fichier_ecriture = nomDossierCible + '/' + fichResultat
#    ###
#mon_fichier_description = open(fichier_lecture_description, "r")
#strSourceDesc = mon_fichier_description.read()
#mon_fichier_description.close()
#    ###
#mon_fichier_ecriture = open(fichier_ecriture, "w") # 'w' pour écraser le fichier à chaque fois, 'a' sinon
#    ###
#    # extraction des annales à considérer 
#(annales, fichierExo) = extraitAnnales(Lcontraintes, strSourceDesc, symboleFinLigne)
#    ### écriture du fichier des résultats
#    # pour l'affichage
#contraintes = ' '.join(Lcontraintes)
#phraseInit = 'Voici les annales contenant l\'un des thèmes suivants : ' + contraintes + '\n\n'
#    # écriture
#mon_fichier_ecriture.write(phraseInit + annales)
#mon_fichier_ecriture.close()
#    ###
#print("\nDONE : programme exécuté avec succès.\nLe fichier résultat est enregistré dans :\n" \
#                  + fichier_ecriture)
#(annales, fichierExo) # on peut virer cette ligne. Renvoyer le fichier obtenu permet de faire des tests dessus



#contenu = trouveAnnales(fichier_desc, fichier_resultat, liste_contraintes, dossier_source, dossier_resultat, symbole_fin_ligne)










#anneeDeb = 2017
#anneeFin = 2017
#if anneeDeb == anneeFin :
#    nom_annee = str(anneeDeb)
#else :
#    nom_annee = str(anneeDeb) + "_" + str(anneeFin)
#fichier_desc = "Contenu/contenu_" + nom_annee + ".tex"
#fichier_theme = "Contenu/theme.tex" # placé dans le dossier Contenu => fichier qui contient tous les thèmes
#
#mon_fichier_description = open(fichier_desc, "r")
#strSourceDesc = mon_fichier_description.read()
##
#mon_fichier_theme = open(fichier_theme, "r")
#strSourceTheme = mon_fichier_theme.read()
####
## extraction de la liste des thèmes autorisés : ceux contenus dans le fichier des thèmes
#LthemeDesc = triFusion(extraitListeTheme(strSourceTheme, ";"))
##
#mon_fichier_description.close()
#mon_fichier_theme.close()
####
## tri des thèmes autorisés
## strThemeTrie = '\n'.join(LthemeTrie) + '\n\n'
## phraseInitThemeTrie = 'Voici la liste des thèmes autorisés par le fichier des thèmes : ' + '\n\n'
## Pour récupérer la liste intégrale des thèmes du fichier contenu_exos
#LthemeTrie = triFusion(extraitListeIntegraleTheme(strSourceDesc, ";"))
#(Locc, themesNP) = compteOccurrences(LthemeTrie, LthemeDesc)






# SAUVEGARDE 



# Extraire les (descriptions, exo) de chaque annale dont le thème est trouvé dans le dossier source
# On prend en paramètre tous les noms de dossiers / fichiers qui seront précisés dans la fonction suivante

#def trouveAnnales(fichSourceTeX, fichResTeX, fichResTxt, Lcontraintes, nomDossierSource, nomDossierCible, symboleFinLigne) :
#    ### def correcte des noms
#    fichier_lecture_description = nomDossierSource + '/' + fichSourceTeX
#    fichier_ecriture_txt = nomDossierCible + '/' + fichResTxt
#    fichier_ecriture_TeX = nomDossierCible + '/' + fichResTeX
#    ###
#    mon_fichier_description = open(fichier_lecture_description, "r")
#    strSourceDesc = mon_fichier_description.read()
#    mon_fichier_description.close()
#    ###
#    mon_fichier_ecriture_txt = open(fichier_ecriture_txt, "w") # 'w' pour écraser le fichier à chaque fois, 'a' sinon
#    mon_fichier_ecriture_TeX = open(fichier_ecriture_TeX, "w") # 'w' pour écraser le fichier à chaque fois, 'a' sinon
#    ###
#    # extraction des annales à considérer 
#    (annales, fichierExo) = extraitAnnales(Lcontraintes, strSourceDesc, symboleFinLigne)
#    ### écriture du fichier des résultats
#    # pour l'affichage
#    contraintes = ", ".join(Lcontraintes)
#    phraseInit = 'Voici les annales contenant l\'un des thèmes suivants : ' + contraintes + '.\n\n'
#    # écriture du fichier txt
#    mon_fichier_ecriture_txt.write(phraseInit + annales)
#    mon_fichier_ecriture_txt.close()
#    # écriture du fichier TeX
#    mon_fichier_ecriture_TeX.write(fichierExo)
#    mon_fichier_ecriture_TeX.close()
#    ###
#    print("\nDONE : programme exécuté avec succès.\nLes fichiers résultats ont été enregistré dans :\n" \
#                  + fichier_ecriture_txt + " et " + fichier_ecriture_TeX)
#    return (annales, fichierExo) # on peut virer cette ligne. Renvoyer le fichier obtenu permet de faire des tests dessus



# On appelle la fonction précédente avec les bons arguments notamment le numéro de l'année
# On extrait les (annales, fichierExo) du dossier annee
# On crée dans le dossier Extraction un fichier annales_contrainte1_contrainte2_..._contrainteN.txt pour afficher une description des annales vérifiant les contraintes
# On crée dans le dossier Extraction un fichier exercices_contrainte1_contrainte2_..._contrainteN.tex qui contient les exos correspondants
# => C'EST LA FONCTION À UTILISER

#def trouveAnnalesAnnee(annee, Lcontraintes) :
#    fichTeX = "oraux_HEC_" + str(annee) + ".tex"
#    fichResTxt = "annales_" + str(annee) + "_" + '_'.join(Lcontraintes) + ".txt"
#    fichResTex = "exercices_" + str(annee) + "_" + '_'.join(Lcontraintes) + ".tex"
#    nomDossierSource = str(annee)
#    nomDossierCible = "Extraction"
#    symboleFinLigne = ';'
#    trouveAnnales(fichTeX, fichResTex, fichResTxt, Lcontraintes, nomDossierSource, nomDossierCible, symboleFinLigne)

