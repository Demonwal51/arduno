import tkinter as tk
from tkinter import StringVar, OptionMenu, messagebox
import os
import platform
import datetime

def commencer():
    """Ouvre la fenêtre de menu de sélection de carte."""
    global menu_window
    inter_window.destroy()
    menu_window = tk.Toplevel()  # Créer une nouvelle fenêtre indépendante
    menu_window.title("Menu")

    options = ["Choisir une carte", "uno"]
    variable = StringVar(menu_window)
    variable.set(options[0])

    OptionMenu(menu_window, variable, *options).pack()

    tk.Button(menu_window, text="Ouvrir Bibliothèque", command=ouvrir_bibliotheque).pack()

def ouvrir_bibliotheque():
    """Ouvre la fenêtre de sélection de bibliothèques."""
    global biblio_window
    try:
        menu_window.destroy()
    except AttributeError:
        pass
    biblio_window = tk.Toplevel()
    biblio_window.title("Choisir des bibliothèques")

    selected_library = StringVar(biblio_window)
    selected_library.set("Sélectionnez une bibliothèque")

    OptionMenu(biblio_window, selected_library, *["RFID", "servomoteur", "RFID et servomoteur"]).pack()

    def enregistrer_choix():
        """Enregistre le choix de la bibliothèque dans le fichier."""
        choix = selected_library.get()
        if choix != "Sélectionnez une bibliothèque":
            with open("fichier.txt", "a") as fichier:
                if choix == "RFID":
                    fichier.write("#include <SPI.h>\n#include <MFRC522.h>\n")
                    fichier.write("const int SelectSlavePin = 10;\nconst int ReStartPin = 9;\n")
                    fichier.write("const int mosi = 11;\nconst int miso = 12;\nconst int sck = 13;\n")
                    fichier.write("MFRC522 rfid(SelectSlavePin, ReStartPin);\n")
                    fichier.write("byte ID [4]={252,4,238,23};\nbool RFIDlu=false;\n")
                    fichier.write("void setup() { Serial.begin(9600);\nSPI.begin();\n\n")
                elif choix == "servomoteur":
                    def enregistrer_pin():
                        pin = entree.get()
                        try:
                            pin_int = int(pin)  # Convertir en entier et vérifier
                            with open("fichier.txt", "a") as fichier:
                                fichier.write(f"#include <Servo.h>\nint pinServo = {pin_int};\nServo myServo;\n")
                                fichier.write("void setup() { myServo.attach(pinServo); \n")
                            servo_window.destroy()
                            biblio_window.destroy() #Ferme aussi la fenêtre biblio window
                        except ValueError:
                            messagebox.showerror("Erreur", "Veuillez entrer un nombre entier pour la broche.")

                    servo_window = tk.Toplevel(biblio_window) #Fenêtre enfant de biblio_window
                    servo_window.title("Configuration du servomoteur")
                    tk.Label(servo_window, text="Quelle est la pin du servomoteur ?").pack()
                    entree = tk.Entry(servo_window)
                    entree.pack()
                    tk.Button(servo_window, text="Valider", command=enregistrer_pin).pack()
                elif choix == "RFID et servomoteur":
                    with open("fichier.txt", "a") as fichier:
                        fichier.write("#include <SPI.h>\n#include <MFRC522.h>\n")
                        fichier.write("const int SelectSlavePin = 10;\nconst int ReStartPin = 9;\n")
                        fichier.write("const int mosi = 11;\nconst int miso = 12;\nconst int sck = 13;\n")
                        fichier.write("MFRC522 rfid(SelectSlavePin, ReStartPin);\n")
                        fichier.write("byte ID [4]={252,4,238,23};\nbool RFIDlu=false;\n")
                        fichier.write("void setup() { Serial.begin(9600);\nSPI.begin();\n\n")
                    def enregistrer_pin():
                        pin = entree.get()
                        try:
                            pin_int = int(pin)  # Convertir en entier et vérifier
                            with open("fichier.txt", "a") as fichier:
                                fichier.write(f"#include <Servo.h>\nint pinServo = {pin_int};\nServo myServo;\n")
                                fichier.write("void setup() { myServo.attach(pinServo); }\n")
                            servo_window.destroy()
                            biblio_window.destroy()
                        except ValueError:
                            messagebox.showerror("Erreur", "Veuillez entrer un nombre entier pour la broche.")

                    servo_window = tk.Toplevel(biblio_window)
                    servo_window.title("Configuration du servomoteur")
                    tk.Label(servo_window, text="Quelle est la pin du servomoteur ?").pack()
                    entree = tk.Entry(servo_window)
                    entree.pack()
                    tk.Button(servo_window, text="Valider", command=enregistrer_pin).pack()
            
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une bibliothèque.")

    tk.Button(biblio_window, text="Valider", command=enregistrer_choix).pack()


def save_info():
    """Sauvegarde les informations du projet dans le fichier."""
    name = name_entry.get()
    description = description_entry.get("1.0", tk.END).strip()

    if name and description:
        with open("fichier.txt", "w") as file:
            now = datetime.datetime.now()
            file.write(f"/////////////////////////////////////////////////////\n")
            file.write(f"//{name:^51}//\n")
            file.write(f"//{description:^51}//\n")
            file.write(f"//{now.strftime('%d-%m-%Y'):^51}//\n")
            file.write(f"//                                                   //\n")
            file.write(f"/////////////////////////////////////////////////////\n\n")
        # inter_window.destroy()  # Suppression de cette ligne pour ne pas fermer inter_window
    else:
        messagebox.showwarning("Avertissement", "Veuillez entrer un nom et une description.")

def afficherfichier():
    """Affiche le contenu du fichier."""
    try:
        if platform.system() == 'Windows':
            os.startfile('fichier.txt')
        else:
            os.system('open fichier.txt')
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Le fichier 'fichier.txt' n'existe pas.")

def supprimerfichier():
    """Supprime le fichier."""
    try:
        os.remove('fichier.txt')
        messagebox.showinfo("Succès", "Le fichier 'fichier.txt' a été supprimé.")
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Le fichier 'fichier.txt' n'existe pas.")

def fermer_application():
    """Ferme l'application."""
    root.destroy()

def inter1():
    """Crée l'interface de saisie des informations du projet."""
    global name_entry, description_entry, inter_window
    inter_window = tk.Toplevel()
    inter_window.title("Informations du projet")

    tk.Label(inter_window, text="Entrez votre nom:").pack()
    name_entry = tk.Entry(inter_window)
    name_entry.pack()

    tk.Label(inter_window, text="Entrez une description:").pack()
    description_entry = tk.Text(inter_window, height=5, width=40)
    description_entry.pack()

    tk.Button(inter_window, text="Sauvegarder", command=save_info).pack()
    tk.Button(inter_window, text="Suivant", command=commencer).pack()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Arduino")
root.attributes('-fullscreen', True)

tk.Label(root, text="Interface Arduino", font=("Arial", 24)).pack(pady=20)
tk.Label(root, text="Application de Demonwal", font=("Arial", 12)).pack(side=tk.BOTTOM, anchor='w', padx=10, pady=10)
tk.Label(root, text="alpha 0.01", font=("Arial", 10)).pack(side=tk.BOTTOM, anchor='w', padx=0, pady=0)

tk.Button(root, text="Commencer à créer le code", command=inter1, width=20, height=2).pack(pady=5)
tk.Button(root, text="Afficher le code", command=afficherfichier, width=20, height=2).pack(pady=5)
tk.Button(root, text="Supprimer le code", command=supprimerfichier, width=20, height=2).pack(pady=5)
tk.Button(root, text="Fermer l'application", command=fermer_application, bg="red", fg="white", width=20, height=2).pack(pady=5)

root.mainloop()