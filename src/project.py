#!/usr/bin/env python3
"""! @brief Programme Python de reconnaissance d'empreintes digitales."""
##
# @mainpage project.py
#
# @section Description
# Ensemble des fonctions du projet.
#
# @section Notes
# - [...]
#
##
# @file cryptage.py
#
# @brief Fonction pour décrypter une image à l'aide de la méthode de Fernet.
#
# @section Description
# Cryptage/Décryptage réalisé avec la librairie Fernet
#
##
# @file interface.py
#
# @brief Interface pour effectuer la reconnaissance d'une empreinte digitale
#
# @section Description
# Interface Python réalisée avec la libraire Tkinter.
#
# @section Libraries/Modules
# - cv2 extern library (https://pypi.org/project/opencv-python/)
# - numpy extern library (https://numpy.org/)
# - signal standard library (https://docs.python.org/3/library/signal.html#module-signal)
# - imageio extern library (https://pypi.org/project/imageio/)
# - time standard library (https://docs.python.org/3/library/time.html)
# - Fernet extern library (https://cryptography.io/en/latest/fernet/)
# - os standard library (https://docs.python.org/3/library/os.html?highlight=os#module-os)
# - base64 standard library (https://docs.python.org/3/library/base64.html?highlight=base64#module-base64)
# - tkinter extern library (https://docs.python.org/fr/3/library/tkinter.html)
# - PIL extern library (https://he-arc.github.io/livre-python/pillow/index.html)
# - matplotlib.pyplot extern library (https://matplotlib.org/stable/)
# - ast standard library (https://docs.python.org/3/library/ast.html?highlight=ast#module-ast)
# - csv standard library (https://docs.python.org/3/library/csv.html?highlight=csv#module-csv)
# - shutil standard library (https://docs.python.org/3/library/shutil.html?highlight=shutil#module-shutil)
#
# @section todo_doxygen_example TODO
# - [...]
#
# @section Auteurs
# - GANZHORN Octave
# - GOUTH Thomas
# - PAULY Alexandre
# - SABADIE Laura
##

# Import des bibliothèques nécessaires
import cv2
import numpy as np
from scipy import signal
import imageio
import time, os, csv, ast, base64, shutil
from matplotlib import pyplot as plt
from cryptography.fernet import Fernet

# Import des autres fichiers
import cryptage
import interface

# Définition de variables globales
binarized_image = None # Image binarisée
skeleton_image = None # Image squeletisée
minutiae_image = None # Minuties sur l'image squeletisée
detection_image = None # Empreinte détectée lors de la reconnaissance
binarized_time = None # Temps d'exécution pour la binarisation
skeleton_time = None # Temps d'exécution pour la squelettisation
minutiae_time = None # Temps d'exécution pour la recherche des minuties
detection_time = None # Temps d'exécution pour la reconnaissance
minutiae_number = None # Nombre de minuties détectées
bifurcation_number = None # Nombre de minuties de type bifurcation

def binarize_image(image, method):
    """! Binarisation d'image

    Fonction pour binariser une image en noir et blanc en utilisant une méthode spécifiée.

    @param image: Image à binariser
    @type image: String (Adresse de l'image)

    @param method: Méthode de binarisation (otsu, adaptive_mean ou adaptive_gaussian)
    @type method: String

    @return: Image binarisée
    @rtype: Image

    """
    
    # Chargement de l'image en niveau de gris
    original_image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    
    # Application de la méthode de binarisation spécifiée (Correspond à un seuillage)
    if method == "Méthode d'Otsu":
        _, binary_image = cv2.threshold(original_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif method == "Moyenne adaptative":
        binary_image = cv2.adaptiveThreshold(original_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    elif method == "Gaussienne adaptative":
        binary_image = cv2.adaptiveThreshold(original_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    else:
        raise ValueError("Méthode de binarisation non reconnue.")
    
    # Retourne l'image binarisée
    return binary_image

def skeletonize_image(image, method):
    """! Squeletisation d'image

    Fonction pour squelettiser une image selon une méthode spécifiée

    @param image: Image binarisée à squelettiser
    @type image: Image

    @param method: Méthode de squelettisation (zhang_suen, guo_hall ou morphology)
    @type method: String

    @return: Image squelettisation
    @rtype: Image

    """
    
    # Choix de la méthode de squelettisation
    if method == "Filtre Laplacien":
        # Motif de convolution avec le filtre Laplacien
        M = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]])
        # M = np.array([[-1,-1,-1],[-1,8,-1],[-1,-2,-1]])
        # M = np.array([[1,-2,1],[-2,4,-2],[1,-2,1]])

        # Produit de convolution A*M (mode='same' permet d'obtenir un r\'esultat de m\^eme taille que A).
        skeleton = signal.convolve2d(image, M, mode='same')
    elif method == "Filtre Sobel": 
        # Motif de convolution avec le filtre de Sobel
        M = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])/4
        M = np.transpose(M)

        # Produit de convolution A*M (mode='same' permet d'obtenir un résultat de mêeme taille que A).
        skeleton = signal.convolve2d(image, M, mode='same')
    elif method == "zhang_suen":
        # Application de la squelettisation Zhang-Suen
        skeleton = cv2.ximgproc.thinning(image, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
    elif method == "guo_hall":
        # Application de la squelettisation Guo-Hall
        skeleton = cv2.ximgproc.thinning(image, thinningType=cv2.ximgproc.THINNING_GUOHALL)
    elif method == "morphology":
        # Application d'une opération de fermeture suivie d'une soustraction pour simuler la squelettisation
        skeleton = cv2.morphologyEx(image, cv2.MORPH_CLOSE, np.ones((3,3), np.uint8))
        skeleton = cv2.subtract(skeleton, image)
    else:
        # Lever une exception si la méthode spécifiée n'est pas reconnue
        raise ValueError("Méthode de squelettisation non reconnue.")
    
    # On ramène les valeurs entre 0 et 255 (ici les images sont codées sur 8 bits)
    skeleton[skeleton > 255] = 255
    skeleton[skeleton < 0] = 0

    # Inversement des couleurs pour avoir des contours noirs sur fond blanc
    skeleton = 255 - skeleton
    
    # Retourne l'image squeletisée
    return skeleton

def add_minutiae(file_path, image, minutiaes):
    """! Ajout des minuties dans un fichier

    Fonction pour ajouter les minuties trouvées dans le fichier DB.csv.

    EXPLICATION :
    -- L'intérêt de les écrire dans ce fichier va permettre d'alléger les calculs lors de la recherche de minuties.
    -- Elles seront par la suite comparées avec celles de l'image à traiter.
    -- Initialisation déjà faite.

    @param file_path: Fichier à traiter
    @type file_path: String (Adresse du fichier)

    @param image: Image à laquelle appartiennent les minuties
    @type image: String

    @param minutiaes: Tableau de coordonnées des minuties
    @rtype minutiaes: Tableau de Tableau à 2 dimensions

    """

    try:
        # Ouverture de fichier CSV en mode lecture/écriture
        with open(file_path, 'r', newline='') as file:
            reading = csv.reader(file, delimiter=';')
            data = list(reading)

            # Recherche de la ligne correspondante à l'image
            for elt in data:
                if elt and elt[0] == image:
                    # Ajout des coordonnées de la minutie
                    elt.append(minutiaes)

                    break

        # Écriture des lignes mises à jour dans le fichier
        with open(file_path, 'w', newline='') as file:
            writing = csv.writer(file, delimiter=';')
            writing.writerows(data)

    # Gestion des erreurs
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

def crossing_number(image):
    """! Calcul du crossing number d'un pixel

    Fonction pour calculer le nombre de croisements pour un contour donné dans une image binaire.
    
    EXPLICATION : 
    -- L'image est traitée en considérant une bordure de 5 pixels sur chacun de ses côtés pour éviter de traiter des minuties coupées par la dimension de l'image.
    -- Seuls les minuties de type bifurcation sont conservées de par leur complexité. En effet, lorsqu'elles seront comparées par la suite avec les images de la BDD, il est plus facile de reconnaître des bifurcations que des terminaisons. Ce qui par ailleurs réduira le coût des calculs de par l'effectif amoindri de ces dernières.

    @param image: Image squelettisée
    @type image: Tableau d'image

    @param cpt : Compteur du nombre de minuties
    @type cpt : int

    """

    # Initialisation de variable
    rows, cols = image.shape # Nombre de lignes et de colonnes de l'image
    cpt_minutiae = 0         # Compteur du nombre de minuties
    cpt_bifurcation = 0      # Compteur du nombre de minuties de type bifurcation
    i = 5                    # Indice de ligne
    tab_minutiae = []        # Tableau contenant les minuties

    # Parcours des lignes de l'image
    while i < rows - 5:
        # Initialisation de variables
        j = 5                     # Indice de colonne
        minutiae_detected = False # Booléen (prend vrai lorsqu'une minutie a été trouvée sur la ligne)

        # Parcours des colonnes de l'image
        while j < cols - 5:
            # Vérification du nombre de croisements (division par 255 car l'image est en niveau de noir = 255 et non 1)
            p0 = image[i, j] / 255
            p1 = image[i, j + 1] / 255
            p2 = image[i - 1, j + 1] / 255
            p3 = image[i - 1, j] / 255
            p4 = image[i - 1, j - 1] / 255
            p5 = image[i, j - 1] / 255
            p6 = image[i + 1, j - 1] / 255
            p7 = image[i + 1, j] / 255
            p8 = image[i + 1, j + 1] / 255

            # Calcul du crossing number (nombre de croisements) pour ce pixel
            crossing = 0.5 * (abs(p1 - p2) + abs(p2 - p3) + abs(p3 - p4) + abs(p4 - p5) + abs(p5 - p6) + abs(p6 - p7) + abs(p7 - p8))

            # S'il s'agit d'une terminaison (crossing = 1) ou d'une bifurcation (crossing = 3), on augmente le compteur de minuties
            if (crossing == 1 or crossing == 3):
                # Appel de fonction pour récupérer la minutie détectée
                if(crossing == 3):
                    # minutiae_detection(image, i, j)
                    tab_minutiae.append((j,i))
                    cv2.rectangle(image, (j-5,i-5), (j+5,i+5), (0, 0, 255), 2)
                    cpt_bifurcation += 1 # Compteur du nombre de minuties de type bifurcation

                # Mise à jour de variables
                cpt_minutiae += 1        # Compteur du nombre de minuties
                j += 4                   # Indice de colonne (prend +5 pour éviter de détecter une autre minutie à proximité de celle-ci)
                minutiae_detected = True # Booléen (prend vrai car'une minutie a été trouvée sur la ligne)
            # Sinon si aucune minutie n'a été détectée
            else:
                # Mise à jour de variables
                j += 1 # Indice de colonne

        # Si une minutie a été détectée
        if not minutiae_detected:
            i += 1 # Indice de ligne (prend +5 pour éviter de détecter une autre minutie à proximité de celle-ci)
        # Sinon si aucune minutie n'a été détectée
        else:
            i += 4 # Indice de ligne

    # Retourne le nombre de minuties
    return cpt_minutiae, cpt_bifurcation, tab_minutiae

def variance_calculation(data):
    """! Calcul d'une variance

    Fonction pour calculer la variance d'un échantillon.

    @param data: Echantillon de données
    @type data: Tableau de réels

    @return: Variance
    @rtype: Réel

    """

    n = len(data)
    moyenne = np.mean(data)
    variance = np.sum((data - moyenne)**2) / (n - 1)

    return variance

def match_template(image, template):
    """! Reherche de la présence d'une template dans une image

    Fonction pour rechercher la présence d'une template dans une image.

    EXPLICATIN :
    -- Grâce à la fonction de match template, il est possible de retrouver une minutie (template) sur une image avec plusieurs méthodes.
    -- L'idée est de combiner les méthodes pour obtenir différents résultats et les comparer.
    -- Etant donné que la minutie appartienne ou non à l'image, la fonction renverra une matrice comme résultat. 
    -- Nous allons récupérer ces résultats et calculer pour chacun la valeur moyenne des pixels de l'image de retour pour par la suite en calculer la variance afin de connaître la variabilité du résultat car lorsque la template appartient à l'image, le retour sera très proche du noir. À l'inverse, il sera proche du blanc lorsqu'il ne sera pas correcte.

    @param image: Image sur laquelle on recherche la minutie
    @type image: Matrice d'une image

    @param template: Minutie à retrouver
    @type template: Matrice d'une image

    @return: tabMoy
    @rtype: Tableau contenant la valeur moyenne des pixels de l'image retournée par matchTemplate pour chaque méthode

    """

    # Initialisation de variables
    w, h = template.shape[::-1]                                                                                         # Dimensions de la template
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED'] # Méthodes à utiliser
    tabMoy = []                                                                                                         # Tableau de la couleur moyennes de chaque pixel

    # Boucle sur les méthodes de correspondance
    for meth in methods:
        # Conversion de la méthode de correspondance en une fonction OpenCV
        method = eval(meth)
        
        # Application de la correspondance de modèle en utilisant la méthode actuelle
        result = cv2.matchTemplate(image,template,method)

        # Recherche des valeurs minimales et maximales dans le résultat de la correspondance
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # Si la méthode est TM_SQDIFF ou TM_SQDIFF_NORMED, prendre la position minimale
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        # Sinon prendre la position maximale
        else:
            top_left = max_loc

        # Calcul de la position du coin inférieur droit du rectangle délimitant la correspondance 
        bottom_right = (top_left[0] + w, top_left[1] + h)

        np.set_printoptions(threshold=np.inf)
        
        # Dessin d'un rectangle autour de la zone de correspondance dans l'image
        # cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)

        region_delimitee = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        moyenne_pixels = np.mean(region_delimitee)
        tabMoy.append(moyenne_pixels)

    return tabMoy

def fingerprint_recognition(skeleton_image, binarization_methods, skeletonize_methods, nb_minutiae):
    """! Comparaison d'empreinte digitale

    Fonction pour effectuer la comparaison de l'empreinte digitale à traiter avec celles de la BDD.

    @param image_path: Squelette de l'image à traiter
    @type image_path: Matrice binaire

    @param binarization_methods : Méthode de binarisaiton
    @type binarization_methods : String

    @param skeletonize_methods : Méthode de squelettisation
    @type skeletonize_methods : String

    @param nb_minutiae : Nombre de minuties à prélever
    @type nb_minutiae : int

    """

    # global detection_image

    # Initialisation de variables
    folder_db = "DB"                            # Dossier contenant la BDD des empreintes cryptées
    file_db = "DB.csv"                          # Fichier contenant la BDD des informations des empreintes (Image (= empreinte), Personne associée et minuties de l'empreinte)
    file = 'key.txt'                            # Fichier contenant la clé de cryptage
    old_key = cryptage.readFile(file)           # Ancienne clé de cryptage
    skeleton_image_copy = skeleton_image.copy() # Copie de l'image squeletisée à traiter
    result = []                                 # Tableau contenant les personnes reconnues par le traitement

    # Lecture d'un dossier
    files_in_folder = os.listdir(folder_db)

    # Filtrer pour ne conserver que les fichiers (pas les sous-dossiers)
    files = [f for f in files_in_folder if os.path.isfile(os.path.join(folder_db, f))]

    # Parcours de chaque fichier dans le dossier
    for filename in files:
        if filename != file_db:
            # Décryptage des données
            cryptage.decryptionImage(old_key, f'{folder_db}/{filename}')
    
    try:
        # Ouverture de fichier CSV en mode lecture
        with open(f"{folder_db}/{file_db}", 'r', newline='') as file:
            reading = csv.reader(file, delimiter=';')
            data = list(reading)

            # Recherche de la ligne correspondante à l'image
            for elt in data:
                # Affectation de variables
                img = elt[0]    # Non de l'image
                person = elt[1] # Nom de la personne
                # Association des minuties en fonction de la méthode de binarisation utilisée
                if binarization_methods == "Méthode d'Otsu":
                    minuties = elt[2] # Minuties associées
                elif binarization_methods == "Moyenne adaptative":
                    minuties = elt[3] # Minuties associées
                elif binarization_methods == "Gaussienne adaptative":
                    minuties = elt[4] # Minuties associées

                # Transformation du tableau de minuties récupéré en string en un tableau de points de coordonnées
                minuties = ast.literal_eval(minuties)

                # Image de la BDD à comparer avec celle à traiter
                imageDB = f'{folder_db}/{img}'

                # Prétraitement de l'image de la BDD
                binarized_image_bdd = binarize_image(imageDB, binarization_methods)
                skeleton_image_bdd = skeletonize_image(binarized_image_bdd, skeletonize_methods)
                skeleton_image_bdd = cv2.convertScaleAbs(skeleton_image_bdd)

                # Initialisation de variables
                cpt = 0 # Compteur du nombre de correspondance entre l'image de la BDD et celle à traiter
                i = 0   # Indice de boucle

                # Tant que le nombre de match de minuties à chercher n'est pas trouvé et qu'il y a des minuties à tester
                while cpt < nb_minutiae and i < len(minuties):
                    # Récupération des points de coordonnées de la minutie
                    minutiae = minuties[i]
                    
                    # Extraction de la minutie (11 x 11 autour de ses coordonnées) sur chacune des images
                    minutiae_image_bdd = skeleton_image_bdd[minutiae[1]-5:minutiae[1]+6, minutiae[0]-5:minutiae[0]+6]
                    minutiae_image = skeleton_image[minutiae[1]-5:minutiae[1]+6, minutiae[0]-5:minutiae[0]+6]

                    # Recherche d'une correspondance entre l'image à traiter et la minutie extraite sur l'image de la bdd et sur l'image à traiter
                    match_minutiae_bdd = match_template(skeleton_image,minutiae_image_bdd)
                    match_minutiae = match_template(skeleton_image,minutiae_image)

                    # Calcul de la variance sur chacun de ses matchs
                    variance_minutiae_bdd = variance_calculation(match_minutiae_bdd)
                    variance_minutiae = variance_calculation(match_minutiae)

                    # Si les variances sont nulles, alors la correspondance est bonne
                    if(variance_minutiae_bdd == 0 and variance_minutiae == 0): # Ici la variance vaut 0, mais sur une applicaiton plus importante, il faudrait que la variance soit comparée à un intervalle de confiance
                        # Incrémentation d'un compteur
                        cpt += 1

                        # Dessin d'un rectangle autour de la zone de correspondance dans l'image
                        cv2.rectangle(skeleton_image, (minutiae[0]-5,minutiae[1]-5), (minutiae[0]+5,minutiae[1]+5), (0, 0, 255), 2)
                        cv2.rectangle(skeleton_image_bdd, (minutiae[0]-5,minutiae[1]-5), (minutiae[0]+5,minutiae[1]+5), (0, 0, 255), 2)

                    # Incrémentation de l'indice de boucle
                    i += 1
                
                # Si le nombre de minuties à rechercher a été trouvé, alors on conserve le nom de la personne
                if cpt >= nb_minutiae:
                    detection_image = cv2.imread(imageDB, cv2.IMREAD_GRAYSCALE)
                    result.append(person)
                    result.append(detection_image)

                # Réinitialisation de la valeur de l'image à traiter car des rectangles ont été dessinés dessus
                skeleton_image = skeleton_image_copy.copy()
                
    # Gestion des erreurs
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    # Parcours de chaque fichier dans le dossier
    for filename in files:
        if filename != file_db:
            # Encryptage des données
            cryptage.encryptionImage("", f'{folder_db}/{filename}', False)

    return result

def main(image_path, binarization_methods, skeletonize_methods, nb_minutiae):
    """! Reconnaissance d'empreinte digitale

    Fonction principale pour effectuer toutes les étapes de reconnaissance d'empreintes digitales.
    
    @param image_path: Image à traiter
    @type image_path: String

    @param binarization_methods : Méthode de binarisaiton
    @type binarization_methods : String

    @param skeletonize_methods : Méthode de squelettisation
    @type skeletonize_methods : String

    @param nb_minutiae : Nombre de minuties à prélever
    @type nb_minutiae : int

    """

    # Déclaration de variables globales pour stocker les résultats du traitement
    global binarized_image, skeleton_image, minutiae_image
    global binarized_time, skeleton_time, minutiae_time, detection_time
    global minutiae_number, bifurcation_number
    
    # Enregistrement du temps de début du traitement
    start = time.time() 
    
    # Binarisation de l'image à traiter et sauvagarde de l'image binarisée
    binarized_image = binarize_image(image_path, binarization_methods)
    
    # Enregistrement du temps de fin du traitement
    end = time.time()

    # Calcul du temps pris par la binarisation
    binarized_time = str(round(float(end - start), 4))

    # Réinitialisation du compteur de temps
    start = time.time()
    
    # Squelettisation de l'image à traiter et sauvagarde de l'image squelettisée
    skeleton_image = skeletonize_image(binarized_image, skeletonize_methods)
    skeleton_image = cv2.convertScaleAbs(skeleton_image)
    minutiae_image = cv2.convertScaleAbs(skeleton_image)
    
    # Enregistrement du temps de fin du traitement
    end = time.time() 

    # Calcul du temps pris par la squelettisation
    skeleton_time = str(round(float(end-start),4))

    # Réinitialisation du compteur de temps
    start = time.time() 
    
    # Appel de la fonction pour calculer le nombre de minuties, puis affichage et sauvegarde de l'image avec les minuties
    minutiae_number, bifurcation_number, tab_minutiae = crossing_number(minutiae_image)

    # Enregistrement du temps de fin du traitement
    end = time.time() 

    # Calcul du temps pris par la recherche des minuties
    minutiae_time = str(round(float(end-start),4))

    # Réinitialisation du compteur de temps
    start = time.time() 
    
    # Reconnaissance de l'image à tester parmi les empreintes digitales de la BDD
    result = fingerprint_recognition(skeleton_image, binarization_methods, skeletonize_methods, nb_minutiae)

    # Enregistrement du temps de fin du traitement
    end = time.time() 

    # Calcul du temps pris par la recherche des minuties
    detection_time = str(round(float(end-start),4))

    try:
        shutil.rmtree("DB")
        shutil.copytree("DB_original", "DB")
        cryptage.encryption("DB", "key.txt")
        cryptage.newEncryption()
    except FileNotFoundError:
        print(f"Le dossier n'existe pas.")
    except Exception as e:
        print(f"--Une erreur s'est produite : {e}")

    return result

# Exécute la fonction main
if __name__ == "__main__":
    # Initialisation de variables
    file_path = "DB_original/101_1.tif"                                                      # Image à traiter
    binarization_methods = ["Méthode d'Otsu", "Moyenne adaptative", "Gaussienne adaptative"] # Tableau des méthodes de binarisation
    skeletonize_methods = ["Filtre Laplacien", "zhang_suen", "guo_hall", "morphology"]       # Tableau des méthodes de quelettisation
    
    # Appel de la fonction pour effectuer la reconnaissance d'empreintes digitales
    personne = main(file_path, binarization_methods[0], skeletonize_methods[0], 10)
    print("id = ", personne)