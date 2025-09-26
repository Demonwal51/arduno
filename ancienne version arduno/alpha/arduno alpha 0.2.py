import tkinter as tk
from tkinter import StringVar, OptionMenu, messagebox
import os
import platform
import datetime
import re

def save_info():
    nom_projet = name_entry.get()
    description_projet = description_entry.get("1.0", tk.END).strip()

    if nom_projet and description_projet:
        with open("fichier.txt", "w") as fichier:
            now = datetime.datetime.now()
            fichier.write(f"/////////////////////////////////////////////////////\n")
            fichier.write(f"//{nom_projet:^51}//\n")
            fichier.write(f"//{description_projet:^51}//\n")
            fichier.write(f"//{now.strftime('%d-%m-%Y'):^51}//\n")
            fichier.write(f"//{'':^51}//\n")
            fichier.write(f"/////////////////////////////////////////////////////\n\n")
    else:
        messagebox.showwarning("Avertissement", "Veuillez entrer un nom et une description.")

def commencer():
    global menu_window
    inter_window.destroy()
    menu_window = tk.Toplevel()
    menu_window.title("Menu")

    carte_options = ["Choisir une carte", "uno"]
    carte_selectionnee = StringVar(menu_window)
    carte_selectionnee.set(carte_options[0])

    OptionMenu(menu_window, carte_selectionnee, *carte_options).pack()
    tk.Button(menu_window, text="Ouvrir Bibliothèque", command=ouvrir_bibliotheque).pack()

def ouvrir_bibliotheque():
    global biblio_window
    try:
        menu_window.destroy()
    except AttributeError:
        pass
    biblio_window = tk.Toplevel()
    biblio_window.title("Choisir des bibliothèques")

    bibliotheque_selectionnee = StringVar(biblio_window)
    bibliotheque_selectionnee.set("Sélectionnez une bibliothèque")
    options_bibliotheques = ["RFID", "servomoteur", "RFID et servomoteur"]

    OptionMenu(biblio_window, bibliotheque_selectionnee, *options_bibliotheques).pack()

    def enregistrer_choix_bibliotheque():
        choix = bibliotheque_selectionnee.get()
        if choix != "Sélectionnez une bibliothèque":
            with open("fichier.txt", "a") as fichier:
                if choix == "RFID":
                    fichier.write("#include <SPI.h>\n#include <MFRC522.h>\n")
                    fichier.write("const int SelectSlavePin = 10;\nconst int ReStartPin = 9;\n")
                    fichier.write("const int mosi = 11;\nconst int miso = 12;\nconst int sck = 13;\n")
                    fichier.write("MFRC522 rfid(SelectSlavePin, ReStartPin);\n")
                    fichier.write("byte ID [4]={252,4,238,23};\nbool RFIDlu=false;\n")
                    fichier.write("void setup() { Serial.begin(9600);\nSPI.begin();\n}\n\n")
                elif choix == "servomoteur":
                    def enregistrer_pin_servo():
                        pin = entree_servo.get()
                        try:
                            pin_int = int(pin)
                            with open("fichier.txt", "a") as fichier:
                                fichier.write(f"#include <Servo.h>\nint pinServo = {pin_int};\nServo myServo;\n")
                                fichier.write("void setup() { myServo.attach(pinServo);\n}\n\n")
                            servo_window.destroy()
                        except ValueError:
                            messagebox.showerror("Erreur", "Veuillez entrer un nombre entier pour la broche.")

                    servo_window = tk.Toplevel(biblio_window)
                    servo_window.title("Configuration du servomoteur")
                    tk.Label(servo_window, text="Quelle est la pin du servomoteur ?").pack()
                    entree_servo = tk.Entry(servo_window)
                    entree_servo.pack()
                    tk.Button(servo_window, text="Valider", command=enregistrer_pin_servo).pack()
                elif choix == "RFID et servomoteur":
                    fichier.write("#include <SPI.h>\n#include <MFRC522.h>\n")
                    fichier.write("const int SelectSlavePin = 10;\nconst int ReStartPin = 9;\n")
                    fichier.write("const int mosi = 11;\nconst int miso = 12;\nconst int sck = 13;\n")
                    fichier.write("MFRC522 rfid(SelectSlavePin, ReStartPin);\n")
                    fichier.write("byte ID [4]={252,4,238,23};\nbool RFIDlu=false;\n")
                    fichier.write("void setup() { Serial.begin(9600);\nSPI.begin();\n")

                    def enregistrer_pin_servo_combo():
                        pin = entree_servo_combo.get()
                        try:
                            pin_int = int(pin)
                            with open("fichier.txt", "a") as fichier:
                                fichier.write(f"#include <Servo.h>\nint pinServo = {pin_int};\nServo myServo;\n")
                                fichier.write("myServo.attach(pinServo); }\n\n")
                            servo_window_combo.destroy()
                            biblio_window.destroy()
                        except ValueError:
                            messagebox.showerror("Erreur", "Veuillez entrer un nombre entier pour la broche.")

                    servo_window_combo = tk.Toplevel(biblio_window)
                    servo_window_combo.title("Configuration du servomoteur")
                    tk.Label(servo_window_combo, text="Quelle est la pin du servomoteur ?").pack()
                    entree_servo_combo = tk.Entry(servo_window_combo)
                    entree_servo_combo.pack()
                    tk.Button(servo_window_combo, text="Valider", command=enregistrer_pin_servo_combo).pack()

        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une bibliothèque.")

    tk.Button(biblio_window, text="Valider", command=enregistrer_choix_bibliotheque).pack()
    tk.Button(biblio_window, text="Suivant", command=constantes_const_int).pack()

def afficherfichier():
    try:
        if platform.system() == 'Windows':
            os.startfile('fichier.txt')
        else:
            os.system(f'open fichier.txt')
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Le fichier 'fichier.txt' n'existe pas.")

def supprimerfichier():
    try:
        os.remove('fichier.txt')
        messagebox.showinfo("Succès", "Le fichier 'fichier.txt' a été supprimé.")
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Le fichier 'fichier.txt' n'existe pas.")

def fermer_application():
    root.destroy()

def cree_le_project():
    global name_entry, description_entry, inter_window
    inter_window = tk.Toplevel(root)
    inter_window.title("Informations du projet")

    tk.Label(inter_window, text="Entrez le nom du projet:").pack()
    name_entry = tk.Entry(inter_window)
    name_entry.pack()

    tk.Label(inter_window, text="Entrez une description pour le projet:").pack()
    description_entry = tk.Text(inter_window, height=5, width=40)
    description_entry.pack()

    tk.Button(inter_window, text="Sauvegarder", command=save_info).pack()
    tk.Button(inter_window, text="Suivant", command=commencer).pack()

def constantes_const_int():
    global constantes_const_int_window, nom_constante_entry_const_int, valeur_constante_entry_const_int
    try:
        biblio_window.destroy()
    except AttributeError:
        pass

    constantes_const_int_window = tk.Toplevel(root)
    constantes_const_int_window.title("Constantes Entières (const int)")

    tk.Label(constantes_const_int_window, text="Nom de la constante (ex: ledPin):").pack()
    nom_constante_entry_const_int = tk.Entry(constantes_const_int_window)
    nom_constante_entry_const_int.pack()

    tk.Label(constantes_const_int_window, text="Valeur de la constante (ex: 13):").pack()
    valeur_constante_entry_const_int = tk.Entry(constantes_const_int_window)
    valeur_constante_entry_const_int.pack()

    def valider_constante_const_int():
        nom = nom_constante_entry_const_int.get()
        valeur = valeur_constante_entry_const_int.get()
        try:
            try:
                with open("fichier.txt", "r+") as fichier:
                    contenu = fichier.read()
                    nouveau_contenu = re.sub(r"(void setup\(\))", f"const int {nom} = {valeur};\n\\1", contenu, flags=re.MULTILINE)
                    fichier.seek(0)
                    fichier.write(nouveau_contenu)
                    fichier.truncate()
            except FileNotFoundError:
                messagebox.showerror("Erreur", "Le fichier 'fichier.txt' n'existe pas. Veuillez d'abord créer un projet.")
                return

            nom_constante_entry_const_int.delete(0, tk.END)
            valeur_constante_entry_const_int.delete(0, tk.END)
            messagebox.showinfo("Succès", "Constante ajoutée.")

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

    def suivant_constante_const_int():
        constantes_int()
        constantes_const_int_window.destroy()

    tk.Button(constantes_const_int_window, text="Valider", command=valider_constante_const_int).pack()
    tk.Button(constantes_const_int_window, text="Suivant", command=suivant_constante_const_int).pack()

def constantes_int():
    global constantes_int_window, nom_constante_entry_int, valeur_constante_entry_int
    constantes_int_window = tk.Toplevel(root)
    constantes_int_window.title("Variables Entières (int)")

    tk.Label(constantes_int_window, text="Nom de la variable (ex: compteur):").pack()
    nom_constante_entry_int = tk.Entry(constantes_int_window)
    nom_constante_entry_int.pack()

    tk.Label(constantes_int_window, text="Valeur de la variable (ex: 0):").pack()
    valeur_constante_entry_int = tk.Entry(constantes_int_window)
    valeur_constante_entry_int.pack()

    def valider_constante_int():
        nom = nom_constante_entry_int.get()
        valeur = valeur_constante_entry_int.get()
        try:
            try:
                int(valeur)
            except ValueError:
                messagebox.showwarning("Avertissement", "La valeur entrée contient des lettres.")

            try:
                with open("fichier.txt", "r+") as fichier:
                    contenu = fichier.read()
                    nouveau_contenu = re.sub(r"(void setup\(\))", f"const int {nom} = {valeur};\n\\1", contenu, flags=re.MULTILINE)
                    fichier.seek(0)
                    fichier.write(nouveau_contenu)
                    fichier.truncate()
            except FileNotFoundError:
                messagebox.showerror("Erreur", "Le fichier 'fichier.txt' n'existe pas. Veuillez d'abord créer un projet.")
                return

            nom_constante_entry_const_int.delete(0, tk.END)
            valeur_constante_entry_const_int.delete(0, tk.END)
            messagebox.showinfo("Succès", "Constante ajoutée.")

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

    def suivant_constante_int():
        constantes_int_window.destroy()

    tk.Button(constantes_int_window, text="Valider", command=valider_constante_int).pack()
    tk.Button(constantes_int_window, text="Suivant", command=suivant_constante_int).pack()

root = tk.Tk()
root.title("Arduino")
root.attributes('-fullscreen', False)

tk.Label(root, text="Interface Arduino", font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)

tk.Button(root, text="Commencer à créer le code", command=cree_le_project, width=25, height=2).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
tk.Button(root, text="Afficher le code", command=afficherfichier, width=25, height=2).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
tk.Button(root, text="Supprimer le code", command=supprimerfichier, width=25, height=2).grid(row=2, column=0, padx=5, pady=5, sticky="ew")
tk.Button(root, text="Fermer l'application", command=fermer_application, bg="red", fg="white", width=25, height=2).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

root.mainloop()
