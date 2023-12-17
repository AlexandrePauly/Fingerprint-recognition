# Initialisation de variables#!/usr/bin/env python3
"""! @brief Programme Python de reconnaissance d'empreintes digitales."""
##
# @file cryptage.py
#
# @brief Fonction pour décrypter une image à l'aide de la méthode de Fernet.
#
# EXPLICATION : 
#   -- Les données sont encryptées pour assurer leur sécurité (données = empreintes digitales).
#   -- Et dans l'optique d'assurer leur sécurité sur le temps, elles sont décrypées, puis réencryptées régulièrement avec newEncryption() (de façon fictive, mais il est imaginable qu'un programme pourrait effectuer cette démarche à une périodicité fixée) avec une nouvelle clé. 
#   -- Ici l'initialisation est déjà faite, mais encryption() permet de mettre cela en place pour une nouvelle BDD.
#
# @section Description
# Cryptage/Décryptage réalisé avec la librairie Fernet
#
# @section Notes
# - [...]
#
##
#
# @section Libraries/Modules
# - Fernet extern library (https://cryptography.io/en/latest/fernet/)
# - os standard library (https://docs.python.org/3/library/os.html?highlight=os#module-os)
# - base64 standard library (https://docs.python.org/3/library/base64.html?highlight=base64#module-base64)
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

from cryptography.fernet import Fernet
import os, base64, shutil

def writeFile(path, key):
    """! Écriture dans un fichier

    Fonction pour écrire dans un fichier.

    @param path: Chemin du fichier
    @type path: String

    @param key: Clé de chiffrement
    @type key: bytes

    """

    # Ouverte du fichier en mode écriture s'il existe, sinon création, puis ouverture en écriture
    with open(path, 'w') as f:
        f.write(base64.urlsafe_b64encode(key).decode('utf-8')) # Transformation de la clé en string pour la stocker dans un fichier txt

def readFile(path):
    """! Lecture dans un fichier

    Fonction pour lire dans un fichier.

    @param path: Chemin du fichier
    @type path: String

    @return: Clé de chiffrement
    @rtype: String

    """

    # Ouverture du fichier en mode lecture
    with open(path, 'r') as f:
        # Lecture du contenu du fichier
        contenu = f.read()

        return contenu

# Générer une clé pour le chiffrement
def generateKey():
    """! Génération d'une clé de chiffrement

    Génération d'une clé de chiffrement à l'aide de la librairie Fernet.

    @return: Clé de chiffrement
    @rtype: bytes

    """

    return Fernet.generate_key()

def encryptionImage(key, img_to_encrypt, bool):
    """! Cryptage d'une image

    Fonction pour crypter une image à l'aide de la méthode de Fernet.

    @param key: Clé de chiffrement
    @type key: String

    @param img_to_encrypt: Chemin de l'image à crypter
    @type img_to_encrypt: String

    """

    if bool == True:
        # Ouverture de l'image en mode de lecture binaire
        with open(img_to_encrypt, 'rb') as input_file:
            # Lecture de l'image non cryptée
            image_data = input_file.read()

        # Décodage de la clé encodée en base64 et création d'une suite de chiffrement de Fernet
        cipher_suite = Fernet(base64.urlsafe_b64decode(key))

        # Cryptage des données de l'image à l'aide de la suite de chiffrement de Fernet
        encrypted_image = cipher_suite.encrypt(image_data)

        # Ouverture de l'image en mode d'écriture binaire
        with open(img_to_encrypt, 'wb') as encrypted_file:
            # Sauvegarde de l'image encryptée
            encrypted_file.write(encrypted_image)
    else: 
        new_key = generateKey() # Nouvelle clé de cryptage

        # Sauvegarde de la nouvelle clé dans le fichier déterminé par FILE
        writeFile(FILE, new_key)

        key = readFile(FILE) # Clé à utiliser

        # Ouverture de l'image en mode de lecture binaire
        with open(img_to_encrypt, 'rb') as input_file:
            # Lecture de l'image non cryptée
            image_data = input_file.read()

        # Décodage de la clé encodée en base64 et création d'une suite de chiffrement de Fernet
        cipher_suite = Fernet(base64.urlsafe_b64decode(key))

        # Cryptage des données de l'image à l'aide de la suite de chiffrement de Fernet
        encrypted_image = cipher_suite.encrypt(image_data)

        # Ouverture de l'image en mode d'écriture binaire
        with open(img_to_encrypt, 'wb') as encrypted_file:
            # Sauvegarde de l'image encryptée
            encrypted_file.write(encrypted_image)

def decryptionImage(key, img_to_decrypt):
    """! Décryptage d'une image

    Fonction pour décrypter une image à l'aide de la méthode de Fernet.

    @param key: Clé de chiffrement
    @type key: String

    @param img_to_decrypt: Chemin de l'image à décrypter
    @type img_to_decrypt: String

    """

    # Ouverture de l'image encryptée en mode de lecture binaire
    with open(img_to_decrypt, 'rb') as encrypted_file:
        # Lecture de l'image cryptée
        encrypted_image = encrypted_file.read()

    # Décodage de la clé encodée en base64 et création d'une suite de chiffrement de Fernet
    cipher_suite = Fernet(base64.urlsafe_b64decode(key))

    # Décryptage des données de l'image à l'aide de la suite de chiffrement de Fernet
    decrypted_image = cipher_suite.decrypt(encrypted_image)

    # Ouverture de l'image décryptée en mode d'écriture binaire
    with open(img_to_decrypt, 'wb') as output_file:
        # Sauvegarde de l'image décryptée
        output_file.write(decrypted_image)

def encryption(folder, file):
    """! Encryptage des données

    Fonction pour crypter une image à l'aide de la méthode de Fernet.

    @param folder: Dossier contenant les images à crypter
    @type folder: String

    @param file: Fichier contenant la clé de cryptage
    @type file: String

    """

    # Initialisation de variables
    key = generateKey() # Nouvelle clé de cryptage

    # Sauvegarde de la nouvelle clé dans le fichier déterminé par file
    writeFile(file, key)
    
    for path, dirs, files in os.walk(folder):
        # Pour chaque élément du dossier défini par folder, un décryptage et décryptage sera effectué
        for filename in files:
            if filename != "DB.csv":
                # Encryptage des données
                encryptionImage(readFile(file), f'{folder}/{filename}', True)

def newEncryption():
    """! Renouvellement de l'encryptage des données

    Fonction pour renouveler le cryptage d'un dossier d'images à l'aide de la méthode de Fernet.

    """

    # Initialisation de variables
    old_key = readFile(FILE) # Ancienne clé de cryptage
    new_key = generateKey()  # Nouvelle clé de cryptage
    
    for path, dirs, files in os.walk(FOLDER_PATH):
        # Pour chaque élément du dossier défini par FOLDER_PATH, un décryptage et décryptage sera effectué
        for filename in files:
            if filename != "DB.csv":
                # Décryptage des données
                decryptionImage(old_key, f'{FOLDER_PATH}/{filename}')

                # Sauvegarde de la nouvelle clé dans le fichier déterminé par FILE
                writeFile(FILE, new_key)

                # Encryptage des données
                encryptionImage(readFile(FILE), f'{FOLDER_PATH}/{filename}', True)

# Initialisation de variables
FOLDER_PATH = "DB" # Dossier contenant la BDD
FILE = 'key.txt'  # Fichier contenant la clé de cryptage