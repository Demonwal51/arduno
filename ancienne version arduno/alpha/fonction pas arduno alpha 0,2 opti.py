import tkinter as tk
from tkinter import StringVar, OptionMenu, messagebox
import os, platform, datetime, re

FILENAME = "fichier.txt"

# -------------------------
# Utilitaires fichiers
# -------------------------
def write_to_file(content, mode="a"):
    with open(FILENAME, mode, encoding="utf-8") as f:
        f.write(content)

def read_file():
    with open(FILENAME, "r", encoding="utf-8") as f:
        return f.read()

def file_exists():
    return os.path.exists(FILENAME)

# -------------------------
# Fonctions principales
# -------------------------
def save_info():
    nom = name_entry.get().strip()
    desc = description_entry.get("1.0", tk.END).strip()

    if not nom or not desc:
        messagebox.showwarning("Avertissement", "Veuillez entrer un nom et une description.")
        return

    now = datetime.datetime.now()
    header = (
        "/////////////////////////////////////////////////////\n"
        f"//{nom:^51}//\n"
        f"//{desc:^51}//\n"
        f"//{now.strftime('%d-%m-%Y'):^51}//\n"
        f"//{'':^51}//\n"
        "/////////////////////////////////////////////////////\n\n"
    )
    write_to_file(header, "w")

def afficherfichier():
    if not file_exists():
        return messagebox.showerror("Erreur", "Le fichier n'existe pas.")
    if platform.system() == 'Windows':
        os.startfile(FILENAME)
    else:
        os.system(f'open "{FILENAME}"')

def supprimerfichier():
    if file_exists():
        os.remove(FILENAME)
        messagebox.showinfo("Succès", "Le fichier a été supprimé.")
    else:
        messagebox.showerror("Erreur", "Le fichier n'existe pas.")

def fermer_application():
    root.destroy()

# -------------------------
# Bibliothèques
# -------------------------
def ouvrir_bibliotheque():
    global biblio_window
    menu_window.destroy()
    biblio_window = tk.Toplevel()
    biblio_window.title("Choisir des bibliothèques")

    bibliotheque_selectionnee = StringVar(value="Sélectionnez une bibliothèque")
    options = ["RFID", "servomoteur", "RFID et servomoteur"]
    OptionMenu(biblio_window, bibliotheque_selectionnee, *options).pack()

    def enregistrer():
        choix = bibliotheque_selectionnee.get()
        if choix == "RFID":
            write_to_file(
                "#include <SPI.h>\n#include <MFRC522.h>\n"
                "const int SelectSlavePin=10;\nconst int ReStartPin=9;\n"
                "const int mosi=11;\nconst int miso=12;\nconst int sck=13;\n"
                "MFRC522 rfid(SelectSlavePin, ReStartPin);\n"
                "byte ID[4]={252,4,238,23};\nbool RFIDlu=false;\n"
                "void setup(){Serial.begin(9600);\nSPI.begin();}\n\n"
            )

        elif choix == "servomoteur":
            ask_servo_pin(lambda pin: write_to_file(
                f"#include <Servo.h>\nint pinServo={pin};\nServo myServo;\n"
                "void setup(){myServo.attach(pinServo);}\n\n"
            ))

        elif choix == "RFID et servomoteur":
            write_to_file(
                "#include <SPI.h>\n#include <MFRC522.h>\n"
                "const int SelectSlavePin=10;\nconst int ReStartPin=9;\n"
                "const int mosi=11;\nconst int miso=12;\nconst int sck=13;\n"
                "MFRC522 rfid(SelectSlavePin, ReStartPin);\n"
                "byte ID[4]={252,4,238,23};\nbool RFIDlu=false;\n"
                "void setup(){Serial.begin(9600);\nSPI.begin();\n"
            )
            ask_servo_pin(lambda pin: write_to_file(
                f"#include <Servo.h>\nint pinServo={pin};\nServo myServo;\n"
                "myServo.attach(pinServo);}\n\n"
            ))

        else:
            return messagebox.showwarning("Avertissement", "Veuillez sélectionner une bibliothèque.")

    tk.Button(biblio_window, text="Valider", command=enregistrer).pack()
    tk.Button(biblio_window, text="Suivant", command=constantes_const_int).pack()

def ask_servo_pin(callback):
    win = tk.Toplevel()
    win.title("Configuration du servomoteur")
    tk.Label(win, text="Quelle est la pin du servomoteur ?").pack()
    entry = tk.Entry(win)
    entry.pack()

    def valider():
        try:
            pin = int(entry.get())
            callback(pin)
            win.destroy()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre entier.")

    tk.Button(win, text="Valider", command=valider).pack()

# -------------------------
# Constantes
# -------------------------
def constantes_const_int():
    biblio_window.destroy()
    win = create_const_window("Constantes Entières (const int)", "const int")

    def suivant():
        win.destroy()
        constantes_int()

    tk.Button(win, text="Suivant", command=suivant).pack()

def constantes_int():
    win = create_const_window("Variables Entières (int)", "int")

    tk.Button(win, text="Suivant", command=win.destroy).pack()

def create_const_window(title, type_var):
    win = tk.Toplevel(root)
    win.title(title)

    tk.Label(win, text="Nom :").pack()
    nom_entry = tk.Entry(win)
    nom_entry.pack()

    tk.Label(win, text="Valeur :").pack()
    val_entry = tk.Entry(win)
    val_entry.pack()

    def valider():
        nom, val = nom_entry.get(), val_entry.get()
        if not nom or not val:
            return messagebox.showwarning("Erreur", "Champs vides.")
        try:
            contenu = read_file()
            nouveau = re.sub(r"(void setup\(\))", f"{type_var} {nom}={val};\n\\1", contenu)
            write_to_file(nouveau, "w")
            nom_entry.delete(0, tk.END)
            val_entry.delete(0, tk.END)
            messagebox.showinfo("Succès", f"{type_var} ajouté.")
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Créez un projet avant d'ajouter des constantes.")

    tk.Button(win, text="Valider", command=valider).pack()
    return win

# -------------------------
# Menu principal
# -------------------------
def cree_le_project():
    global name_entry, description_entry, inter_window
    inter_window = tk.Toplevel(root)
    inter_window.title("Informations du projet")

    tk.Label(inter_window, text="Nom du projet:").pack()
    name_entry = tk.Entry(inter_window)
    name_entry.pack()

    tk.Label(inter_window, text="Description:").pack()
    description_entry = tk.Text(inter_window, height=5, width=40)
    description_entry.pack()

    tk.Button(inter_window, text="Sauvegarder", command=save_info).pack()
    tk.Button(inter_window, text="Suivant", command=commencer).pack()

def commencer():
    global menu_window
    inter_window.destroy()
    menu_window = tk.Toplevel()
    menu_window.title("Menu")

    carte_options = ["Choisir une carte", "uno"]
    carte_selectionnee = StringVar(value=carte_options[0])
    OptionMenu(menu_window, carte_selectionnee, *carte_options).pack()
    tk.Button(menu_window, text="Ouvrir Bibliothèque", command=ouvrir_bibliotheque).pack()

# -------------------------
# Lancement
# -------------------------
root = tk.Tk()
root.title("Arduino")
root.attributes('-fullscreen', False)

tk.Label(root, text="Interface Arduino", font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=20)
tk.Button(root, text="Commencer à créer le code", command=cree_le_project, width=25, height=2).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
tk.Button(root, text="Afficher le code", command=afficherfichier, width=25, height=2).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
tk.Button(root, text="Supprimer le code", command=supprimerfichier, width=25, height=2).grid(row=2, column=0, padx=5, pady=5, sticky="ew")
tk.Button(root, text="Fermer l'application", command=fermer_application, bg="red", fg="white", width=25, height=2).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

root.mainloop()
