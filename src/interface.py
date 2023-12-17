# Initialisation de variables#!/usr/bin/env python3
"""! @brief Programme Python de reconnaissance d'empreintes digitales."""
##
# @file interface.py
#
# @brief Interface pour effectuer la reconnaissance d'une empreinte digitale.
#
# @section Description
# Interface Python réalisée avec la libraire Tkinter.
#
# @section Libraries/Modules
# - tkinter extern library (https://docs.python.org/fr/3/library/tkinter.html)
# - PIL extern library (https://he-arc.github.io/livre-python/pillow/index.html)
# - matplotlib.pyplot extern library (https://matplotlib.org/stable/)
# - numpy extern library (https://numpy.org/)
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

import tkinter as tk
from tkinter import Menu, ttk, filedialog, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np

# Import des autres fichiers
import project
import cryptage

# Définition de variables globales
file_path = None # Chemin de l'image à traiter
image_tk = None 
result = None    # Personne détectée

def showRoot():
    """! Affichage de l'interface

    Fonction pour afficher l'interface graphique de reconnaissance d'empreintes digitales.
    
    """

    def on_menu_click(menu_item):
        """! Actions du menu

        Fonction pour effectuer les actions du menu en fonction de l'élément cliqué.

        @param menu_item: Élément du menu cliqué
        @type menu_item: String

        """

        # Action en fonction de l'élément du menu sélectionné
        if menu_item == "Nouveau":
            # Création d'une nouvelle fenêtre
            showRoot()
        elif menu_item == "Ouvrir":
            # Choix de l'image à traiter
            charger_image()
        elif menu_item == "Quitter":
            # Fermeture de la fenêtre
            root.destroy()
        elif menu_item == "Renouveler le cryptage":
            # Renouvellement du cryptage de données
            cryptage.newEncryption()
        elif menu_item == "Plein écran":
            # Redimensionnement de la fenêtre en plein écran
            root.attributes('-fullscreen', True)
        elif menu_item == "Mode normal":
            # Redimensionnement de la fenêtre en petit
            root.attributes('-fullscreen', False)
        elif menu_item == "Mode sombre":
            # Modification de l'élément du menu 
            menu_affichage.entryconfig(2, label="Mode clair", command=lambda: on_menu_click("Mode clair"))

            # Thème de couleurs de l'interface en sombre
            header_color = "#11131e"
            leftCol_color = "#11131e"
            leftCol_border_color = "white"
            border_color = "#f9f9f9"
            rightCol_color = "#11131e"
            text_color = "#f9f9f9"
            buttonActivated_color = "#5372F0"
            button_color = "#6C757D"
        elif menu_item == "Mode clair":
            # Modification de l'élément du menu 
            menu_affichage.entryconfig(2, label="Mode sombre", command=lambda: on_menu_click("Mode sombre"))

            # Thème de couleurs de l'interface en clair
            header_color = "#cccccc"
            leftCol_color = "#cccccc"
            leftCol_border_color = "black"
            border_color = "black"
            rightCol_color = "#cccccc"
            text_color = "black"
            buttonActivated_color = "lightgrey"
            button_color = "lightgrey"
            
        if menu_item == "Mode sombre" or menu_item == "Mode clair":
            # Redéfinition des styles de l'interface
            root.config(bg=header_color)
            barre_menu.config(bg=header_color, foreground=text_color)
            menu_fichier.config(bg=header_color, foreground=text_color)
            menu_edition.config(bg=header_color, foreground=text_color)
            menu_affichage.config(bg=header_color, foreground=text_color)
            menu_aide.config(bg=header_color, foreground=text_color)
            leftCol.config(bg=leftCol_color)
            leftCol_title.config(bg=leftCol_color, foreground=text_color)
            leftCol_content_border.config(bg=leftCol_border_color)
            leftCol_content.config(bg=leftCol_color)
            binarisation_frame.config(bg=leftCol_color)
            binarisation_label.config(bg=leftCol_color, foreground=text_color)
            skeletonize_frame.config(bg=leftCol_color)
            skeletonize_label.config(bg=leftCol_color, foreground=text_color)
            nbMinutiae_frame.config(bg=leftCol_color)
            nbMinutiae_label.config(bg=leftCol_color, foreground=text_color)
            minutiae_slider.config(bg=leftCol_color, foreground=text_color)
            minutiae_label.config(bg=leftCol_color, foreground=text_color)
            button_filter.configure(bg=buttonActivated_color)
            border.config(bg=border_color)
            rightCol.config(bg=rightCol_color)
            style.configure("TNotebook.Tab", bg=header_color, foreground=text_color, padding=[10, 5])
            style.map("TNotebook.Tab", background=[("selected", rightCol_color)])
            tab1.configure(bg=rightCol_color)
            canvas.configure(bg=rightCol_color)
            button_frame.configure(bg=rightCol_color)
            download_button.configure(bg=buttonActivated_color)
            reset_button.configure(bg=button_color)
            data_button.configure(bg=button_color)

    def on_shortcut_click(event):
        """! Actions du menu

        Fonction pour effectuer les actions du menu en fonction du raccourcis clavier.

        @param menu_item: Évènement liés à l'interface
        @type menu_item: Event
        
        """

        if event.keysym == 'n':
            on_menu_click("Nouveau")
        elif event.keysym == 'o':
            on_menu_click("Ouvrir")
        elif event.keysym == 'w':
            on_menu_click("Quitter")
        elif event.keysym == 'equal':
            on_menu_click("Plein écran")
        elif event.keysym == 'Escape':
            on_menu_click("Mode normal")

    def charger_image():
        """! Chargement de l'image à traiter

        Fonction pour charger l'image à reconnaître.

        """

        # Déclaration de variables globales pour stocker le chemin de l'image à traiter
        global file_path, image_tk

        # Choix de l'image à traiter
        file_path = filedialog.askopenfilename()

        # Ouverture de l'image
        image_pil = Image.open(file_path)

        # Convertion de l'image PIL en PhotoImage (format Tkinter)
        image_tk = ImageTk.PhotoImage(image_pil)

        # Affichage de l'image dans le Canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)

        # Mise à jour de la taille du canvas en fonction de la taille de l'image
        canvas.config(width=image_pil.width, height=image_pil.height)

        # Activation d'éléments après avoir importée l'image à traiter
        binarisation_combobox.config(state="normal") 
        skeletonize_combobox.config(state="normal")
        minutiae_slider.config(state="normal")
        minutiae_slider.set(12) # 12 par rapport à la législation française
        reset_button.config(state="normal")

    def on_select_filter(event):
        """! Valeur des filtres à appliquer

        Fonction pour récupérer et actualiser la valeur du slider et des combobox.

        @param menu_item: Évènement liés à l'interface
        @type menu_item: Event

        """

        # VInitialisation de variables
        binarisation_value = binarisation_combobox.get() # Valeur de la combobox pour la méthode de binarisation
        skeletonize_value = skeletonize_combobox.get()   # Valeur de la combobox pour la méthode de squelettisation
        value = minutiae_slider.get()                    # Valeur du slider pour le nombre de minuties

        # Si l'utilisateur a choisi une méthode de binarisation et de squelettisation
        if binarisation_value != "" and skeletonize_value != "" :
            # Affichage du bouton pour appliquer les filtres
            button_filter.config(state="normal")

    def recognition():
        """! Reconnaissance d'empreinte digitale

        Fonction pour appeler le code afin d'effectuer la reconnaissance d'empreinte digitale à partir des méthodes du fichier project.py

        """

        global result

        # Appel de la fonction pour effectuer la reconnaissance d'empreintes
        result = project.main(file_path, binarisation_combobox.get(), skeletonize_combobox.get(), minutiae_slider.get())

        # Activation du bouton pour analyser les résultats
        data_button.config(state="normal")

        if not result:
            messagebox.showinfo("Avertissement", "Aucun résultat n'a aboutit avec la reconnaissance.")
        else:
            messagebox.showinfo("Avertissement", "Une reconnaissance a été trouvée. Allez voir dans 'Analyse'")

    def data_recognition():
        """! Affichage des données concernant la reconnaissance

        Fonction pour afficher une interface permettant d'analyser les données relatives au traitement de la reconnaissance.

        """

        global result

        if not result:
            # Tableau d'images
            images_data = [
                {"title": "Image originale", "text": "", "data": np.array(Image.open(file_path))},
                {"title": "Image binarisée", "text": f"Temps d'exécution : {project.binarized_time}", "data": project.binarized_image},
                {"title": "Image squelettisée", "text": f"Temps d'exécution : {project.skeleton_time}", "data": project.skeleton_image},
                {"title": "Minuties de l'empreinte", "text": f"Temps d'exécution : {project.minutiae_time}\nNombre de minuties détectées : {project.minutiae_number}\nNombre de bifurcations : {project.bifurcation_number}", "data": project.minutiae_image}
            ]

            # Initialisation de variables
            num_rows = 1 # Nombre de lignes
            num_cols = 4 # Nombre de colonnes
        else:
            # Tableau d'images
            images_data = [
                {"title": "Image originale", "text": "", "data": np.array(Image.open(file_path))},
                {"title": "Image binarisée", "text": f"Temps d'exécution : {project.binarized_time}", "data": project.binarized_image},
                {"title": "Image squelettisée", "text": f"Temps d'exécution : {project.skeleton_time}", "data": project.skeleton_image},
                {"title": "Minuties de l'empreinte", "text": f"Temps d'exécution : {project.minutiae_time}\nNombre de minuties détectées : {project.minutiae_number}\nNombre de bifurcations : {project.bifurcation_number}", "data": project.minutiae_image},
                {"title": "Empreinte détectée", "text": f"Temps d'exécution : {project.detection_time}\nPersonne détectée : {result[0]}", "data": result[1]}
            ]

            # Initialisation de variables
            num_rows = 1 # Nombre de lignes
            num_cols = 5 # Nombre de colonnes

        # Création du subplot avec son titre
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5))
        fig.suptitle("Analyse de la reconnaissance d'empreintes digitales", fontsize=16) 

        # Parcours des données et affichage des images
        for i, data in enumerate(images_data):
            ax = axes[i]

            # Plot de l'image
            ax.imshow(data["data"], cmap='gray')

            # Titre de l'image
            ax.set_title(data["title"])

            # Texte de l'image en-dessous
            ax.text(0.5, -0.15, data["text"], horizontalalignment='center', verticalalignment='top', transform=ax.transAxes)

        # Ajustement des espacements entre les sous-plots
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        # Affichage du plot
        plt.show()

    def reset_root():
        """! Réinitialisation de l'interface

        Fonction pour réinitialiser certains statut de l'interface.

        """

        # Mise à jour des variables globales du fichier project.py
        project.binarized_image = None # Image binarisée
        project.skeleton_image = None # Image squeletisée
        project.minutiae_image = None # Minuties sur l'image squeletisée
        project.binarized_time = None # Temps d'exéciton pour la binarisation
        project.skeleton_time = None # Temps d'exéciton pour la squelettisation
        project.minutiae_time = None # Temps d'exéciton pour la recherche des minuties
        project.minutiae_number = None # Nombre de minuties détectées
        project.bifurcation_number = None # Nombre de minuties de type bifurcation

        # Mise à jour des éléments de l'interface
        canvas.delete("all")
        binarisation_combobox.config(state="disabled")
        skeletonize_combobox.config(state="disabled")
        minutiae_slider.config(state="disabled")
        reset_button.config(state="disabled")
        data_button.config(state="disabled")

    # Création de la fenêtre avec son titre
    root = tk.Tk()
    root.title("Reconnaissance d'empreinte digitale")

    # Définition de la largeur et de la hauteur de la fenêtre
    width = 1000
    height = 700

    # Récupérer les dimensions de l'écran
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcul des coordonnées pour centrer la fenêtre
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Définir la position et les dimensions de la fenêtre
    root.geometry(f"{width}x{height}+{x}+{y}")

    # Création d'une barre de menu
    barre_menu = Menu(root)

    # Création du menu Fichier avec ses éléments
    menu_fichier = Menu(barre_menu, tearoff=0)
    menu_fichier.add_command(label="Nouveau", command=lambda: on_menu_click("Nouveau"), accelerator="Ctrl+N")
    menu_fichier.add_command(label="Ouvrir", command=lambda: on_menu_click("Ouvrir"))
    menu_fichier.add_command(label="Enregistrer", command=lambda: on_menu_click("Enregistrer"))
    menu_fichier.add_separator()
    menu_fichier.add_command(label="Quitter", command=root.destroy, accelerator="Ctrl+W")
    barre_menu.add_cascade(label="Fichier", menu=menu_fichier)

    # Création du menu Édition avec ses éléments
    menu_edition = Menu(barre_menu, tearoff=0)
    menu_edition.add_command(label="Renouveler le cryptage", command=lambda: on_menu_click("Renouveler le cryptage"))
    # menu_edition.add_command(label="Choisir base de données", command=lambda: on_menu_click("Choisir base de données"))
    barre_menu.add_cascade(label="Édition", menu=menu_edition)

    # Création du menu Affichage avec ses éléments
    menu_affichage = Menu(barre_menu, tearoff=0)
    menu_affichage.add_command(label="Plein écran", command=lambda: on_menu_click("Plein écran"), accelerator="Ctrl++")
    menu_affichage.add_command(label="Mode normal", command=lambda: on_menu_click("Mode normal"), accelerator="Esc")
    menu_affichage.add_command(label="Mode sombre", command=lambda: on_menu_click("Mode sombre"))
    barre_menu.add_cascade(label="Affichage", menu=menu_affichage)

    # Création du menu Aide avec ses éléments
    menu_aide = Menu(barre_menu, tearoff=0)
    menu_aide.add_command(label="A propos", command=lambda: on_menu_click("A propos"))
    barre_menu.add_cascade(label="Aide", menu=menu_aide)

    root.config(menu=barre_menu)

    # Raccoucis clavier
    root.bind('<Control-n>', on_shortcut_click)
    root.bind('<Control-o>', on_shortcut_click)
    root.bind('<Control-w>', on_shortcut_click)
    root.bind('<Escape>', on_shortcut_click)
    root.bind('<Control-KeyPress-equal>', on_shortcut_click)

    # Création de la partie gauche de l'interface
    leftCol = tk.Frame(root, width=200, padx=8, pady=8, relief=tk.SOLID)
    leftCol.pack(side=tk.LEFT, anchor="n")

    # Création d'une frame pour imiter une bordure
    leftCol_content_border = tk.Frame(leftCol, padx=2, pady=2, relief=tk.SOLID, bg="black")
    leftCol_content_border.pack(side=tk.LEFT, anchor="n", pady=1)

    # COntenu de la partie gauche
    leftCol_content = tk.Frame(leftCol_content_border, padx=2, pady=2, relief=tk.SOLID)
    leftCol_content.pack(side=tk.LEFT, anchor="n", pady=1)

    # Titre de la partie gauche de l'interface
    leftCol_title = tk.Label(leftCol_content, text="Filtres", font=("Helvetica", 12))
    leftCol_title.pack(pady=10)
    
    # Placer binarisation_frame en haut
    binarisation_frame = tk.Frame(leftCol_content)
    binarisation_frame.pack(side=tk.TOP, anchor="n")

    # Création d'un label
    binarisation_label = tk.Label(binarisation_frame, text="Binarisation :", font=("Helvetica", 10))
    binarisation_label.grid(row=0, column=0, columnspan=2, padx=2, pady=(0, 0), sticky="w")

    # Création de la boîte de sélection (combobox)
    options = ["Méthode d'Otsu", "Moyenne adaptative", "Gaussienne adaptative"]
    selected_option = tk.StringVar()
    binarisation_combobox = ttk.Combobox(binarisation_frame, textvariable=selected_option, values=options, state="disabled")
    binarisation_combobox.grid(row=1, column=0, columnspan=1, padx=3, pady=(0, 10), sticky="ew")
        
    # Associer la fonction on_select à l'événement de sélection
    binarisation_combobox.bind("<<ComboboxSelected>>", on_select_filter)

    # Configuration des propriétés de la colonne
    binarisation_frame.columnconfigure(0, weight=1)
    binarisation_frame.columnconfigure(1, weight=1)

    # Placer skeletonize_frame en-dessous de binarisation_frame
    skeletonize_frame = tk.Frame(leftCol_content)
    skeletonize_frame.pack(side=tk.TOP, anchor="n")

    # Création d'un label
    skeletonize_label = tk.Label(skeletonize_frame, text="Squelettisation :", font=("Helvetica", 10))
    skeletonize_label.grid(row=0, column=0, columnspan=1, pady=(0, 0), sticky="w")

    # Création de la boîte de sélection (combobox)
    options_skeletonize = ["Filtre Laplacien"]
    selected_option_skeletonize = tk.StringVar()
    skeletonize_combobox = ttk.Combobox(skeletonize_frame, textvariable=selected_option_skeletonize, values=options_skeletonize, state="disabled")
    skeletonize_combobox.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")

    # Définir une option par défaut (facultatif)
    skeletonize_combobox.set("")
        
    # Associer la fonction on_select à l'événement de sélection
    skeletonize_combobox.bind("<<ComboboxSelected>>", on_select_filter)

    # Placer nbMinutiae_frame en-dessous de skeletonize_frame
    nbMinutiae_frame = tk.Frame(leftCol_content)
    nbMinutiae_frame.pack(side=tk.TOP, anchor="n")

    # Création d'un label
    nbMinutiae_label = tk.Label(nbMinutiae_frame, text="Nombre de minuties :", font=("Helvetica", 10))
    nbMinutiae_label.grid(row=0, column=0, columnspan=1, pady=0, sticky="w")

    # Variable de contrôle pour le Slider
    slider_var = tk.IntVar()

    # Création du Slider pour le choix du nombre de minuties à extraire
    minutiae_slider = tk.Scale(nbMinutiae_frame, from_=8, to=17, variable=slider_var, orient=tk.HORIZONTAL, command=on_select_filter, state=tk.DISABLED)
    minutiae_slider.grid(row=1, column=0, columnspan=2, pady=0, sticky="ew")

    # Étiquette pour afficher la valeur actuelle
    label_var = tk.StringVar()
    minutiae_label = tk.Label(nbMinutiae_frame, textvariable=label_var)
    minutiae_label.grid(row=2, column=0, columnspan=2, pady=0, sticky="ew")

    button_filter = tk.Button(leftCol_content, text="Appliquer", cursor="hand2", state="disabled", command=recognition)
    button_filter.pack(side=tk.LEFT, padx=50, pady=(0,10))

    # Création d'une Frame pour simuler une bordure
    border = tk.Frame(root, relief=tk.SOLID, bg="black")
    border.pack(side=tk.LEFT, fill=tk.Y)

    # Création de la partie droite de l'interface
    rightCol = tk.Frame(root)
    rightCol.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=0, pady=(10, 0))
    
    # Définir un style pour le Notebook
    style = ttk.Style()
    style.configure("TNotebook.Tab", padding=[10, 5])

    tabs = ttk.Notebook(rightCol, style="TNotebook")
    tabs.pack(expand=True, fill=tk.BOTH)

    tab1 = tk.Frame(tabs)
    tabs.add(tab1, text="Nouvel Onglet")
    tabs.bind("<<NotebookTabChanged>>")

    # Ajout d'une Frame pour l'image en haut
    image_frame = tk.Frame(tab1, bg="black")
    image_frame.pack(side="top", fill="both", expand=True)
    image_frame.place(relx=0.5, rely=0.45, anchor="center")

    # Ajout d'un Canvas pour afficher l'image
    canvas = tk.Canvas(image_frame)
    canvas.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")
    canvas.create_image(0, 0, anchor=tk.NW)

    # Associer l'image_tk au canvas pour éviter la collecte des déchets
    canvas.image = image_tk

    # Ajout d'une Frame pour les boutons en bas
    button_frame = tk.Frame(tab1)
    button_frame.pack(side="top", fill="both", expand=True)
    button_frame.place(relx=0.5, rely=0.9, anchor="center")

    download_button = tk.Button(button_frame, text="Importer Image", command=charger_image, cursor="hand2")
    download_button.grid(row=1, column=0, pady=(0, 10), padx=(0, 10), sticky="s")

    reset_button = tk.Button(button_frame, text="Réinitialiser", command=reset_root, cursor="hand2", state=tk.DISABLED)
    reset_button.grid(row=1, column=1, pady=(0, 10), padx=10, sticky="s")

    data_button = tk.Button(button_frame, text="Analyse", command=data_recognition, cursor="hand2", state=tk.DISABLED)
    data_button.grid(row=1, column=2, pady=(0, 10), padx=(10, 0), sticky="s")

    # Configuration des colonnes pour le centrage
    tab1.columnconfigure(0, weight=1)
    tab1.columnconfigure(1, weight=1)

    root.mainloop()

# Exécute la fonction main
if __name__ == "__main__":
    showRoot()