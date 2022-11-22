import tkinter
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from tkinter import filedialog
import customtkinter
import randfacts
from deep_translator import GoogleTranslator
import time


customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

#Horloge
curtime = ''
def tick( ):
    global curtime
    newtime = time.strftime('%H:%M:%S')
    if newtime != curtime:
        curtime = newtime
        clock.configure(text=curtime)
    clock.after(200, tick)

def afficher_info():
    #Aller chercher une info
    info = randfacts.get_fact()

    #Traduire l'info en français
    traduire = GoogleTranslator(source="auto", target="fr").translate(info)

    #Affichez l'info
    message_info.config(text=traduire)

def fonction_recherche():
    resultat.delete(0, "end")
    resultat.insert("end",f"########Les évènements de l'année {entry_recherche.get()}########")
    resultat.insert("end","")
    # Rubrique Monde
    page_actu = requests.get(f"https://fr.wikipedia.org/wiki/{entry_recherche.get()}")
    bs_actu = BeautifulSoup(page_actu.text, "html.parser")
    resultat.insert("end",f"########{entry_recherche.get()} 'Monde'########")
    try:
        monde = bs_actu.find(name="h3", string="Monde")
        monde_list = monde.find_next(name="ul")
        monde_list_li = monde_list.find_all(name="li")
        for element in monde_list_li:
            resultat.insert("end",element.text)
    except:
        resultat.insert("end","***La rubrique 'Monde' n'existe pas pour cette année !")
    # Rubrique en Musique
    page_musique = requests.get(f"https://fr.wikipedia.org/wiki/{entry_recherche.get()}_en_musique")
    bs_musique = BeautifulSoup(page_musique.text, "html.parser")
    resultat.insert("end","")
    resultat.insert("end",f"########{entry_recherche.get()} 'Musique'########")
    try:
        musique = bs_musique.find_all(name="h3")
        musique_list = musique[1].find_next(name="ul")
        musique_list_li = musique_list.find_all(name="li")
        for element in musique_list_li:
            resultat.insert("end",element.text)
    except:
        resultat.insert("end","***La rubrique 'Musique' n'existe pas pour cette année !")
    # Rubrique Box-Office
    page_cine = requests.get(f"https://fr.wikipedia.org/wiki/Box-office_France_{entry_recherche.get()}")
    bs_cine = BeautifulSoup(page_cine.text, "html.parser")
    resultat.insert("end","")
    resultat.insert("end",f"########{entry_recherche.get()} 'Box Office'########")

    try:
        cine = bs_cine.find_all(name="tr")
        for film in cine[1:6]:
            affichage = list(film)
            formatage = " ".join([affichage[1].text, affichage[3].text])
            resultat.insert("end", formatage)
    except:
        resultat.insert("end","***La rubrique 'Box Office' n'existe pas pour cette année !")

def deselection():
    selection = resultat.curselection()
    for element in selection:
        resultat.selection_clear(0, "end")

def effacer():
    selection = resultat.curselection()
    for element in selection[::-1]:
        resultat.delete(element)

def modifier():

    def sauver_modif():
        resultat.delete(indice)
        resultat.insert(indice, text.get(1.0,'end'))
        top1.destroy()
    #messagebox
    nb_selection = len(resultat.curselection())
    if nb_selection != 1:
        if nb_selection<1:
            message = "Vous devez selectionner un élément à modifier !"
        else:
            message = "Vous ne devez selectionner qu'un seul élément !"
        messagebox.showwarning("Impossible de modifier",message,parent=fenetre)
    else:
        top1 = tkinter.Toplevel()
        top1.title("Apprenez la webradio")
        top1.geometry("600x400")

        for indice in resultat.curselection():
            indice = indice
            texte = resultat.get(indice)


        label_top1 = tkinter.Label(top1, text="Modifier: ")
        text = tkinter.Text(top1, height=5)
        text.insert("end",texte)

        btn_sauve = tkinter.Button(top1, text="Sauvegarder", command=sauver_modif)

        label_top1.pack(pady=15)
        text.pack(pady=15)
        btn_sauve.pack(pady=15)

def enregistrer():
    fichier = filedialog.asksaveasfilename(title="Enregistrer sous", filetypes=[("Fichier texte",".txt")], defaultextension=".txt")
    if fichier:
        ecrire_fichier = open(fichier, "w")
        liste_lignes = list(resultat.get(0, "end"))
        for ligne in liste_lignes:
            ecrire_fichier.write(ligne+"\n")
        ecrire_fichier.close()
    else:
        messagebox.showinfo("Sauvegarder sous","Annulation de la sauvegarde", parent=fenetre)

def ouvrir():
    fichier = filedialog.askopenfilename(title="Ouverture d'un fichier", filetypes=[("Fichier texte",".txt")], defaultextension=".txt")
    if fichier:
        resultat.delete(0,"end")
        ouvrir_fichier = open(fichier, "r")
        lecture = ouvrir_fichier.readlines()
        for ligne in lecture:
            resultat.insert("end",ligne)
        ouvrir_fichier.close()
    else:
        messagebox.showinfo("Ouvrir","Annulé", parent=fenetre)


fenetre = customtkinter.CTk()
fenetre.title("Apprenez la webradio")
fenetre.geometry("1250x900")

canva_titre=tkinter.Canvas(fenetre, width=100, height=450, highlightthickness=0, bg="#212325")
canva_titre.create_text(55,225, text="GRATAIJE", font=("OMEGLE",64), angle=90, fill="silver")
frame_programme=customtkinter.CTkFrame(fenetre, corner_radius=20)
label_recherche = customtkinter.CTkLabel(frame_programme, text="Recherche", text_font=("Helvetica", 16))

entry_recherche = customtkinter.CTkEntry(frame_programme, width=540, height=30, border_width=1)
btn_rechercher = customtkinter.CTkButton(frame_programme, text="Rechercher", command = fonction_recherche)

#Zone de ListBox
frame_resultat = customtkinter.CTkFrame(frame_programme, corner_radius=20)
sb = customtkinter.CTkScrollbar(frame_resultat, orientation="horizontal")
resultat = tkinter.Listbox(frame_resultat,height = 28, width=90, font=("Comic Sans MS", 10),selectmode="multiple", activestyle="dotbox", highlightthickness=0, bg="#343638", fg="#f2f2f2", border=0, xscrollcommand=sb.set)
sb.configure(command=resultat.xview)
btn_nouvelle_info = customtkinter.CTkButton(frame_programme, text="Afficher une nouvelle info", command=afficher_info)
message_info = tkinter.Message(frame_programme, relief="sunken", width=650, anchor='center', font=(14))
frame_btn = tkinter.Frame(frame_resultat, bg="#343638")
btn_deselectionner = customtkinter.CTkButton(frame_btn, text="Déselectionner", command=deselection)
btn_effacer = customtkinter.CTkButton(frame_btn, text="Effacer", command=effacer)
btn_modifier = customtkinter.CTkButton(frame_btn, text="Modifier", command=modifier)
clock = customtkinter.CTkLabel(frame_programme, text_font=("Arial", 16))
btn_ouvrir = customtkinter.CTkButton(frame_programme, text="Ouvrir", command=ouvrir)
btn_enregistrer = customtkinter.CTkButton(frame_programme, text="Enregistrer sous", command=enregistrer)

#Placement des widgets
canva_titre.grid(row=0, column=0, padx=(10,25))
frame_programme.grid(row=0, column=1, pady=25, padx=15)

label_recherche.grid(row=2, column=0, pady=15)
entry_recherche.grid(row=2, column=1, sticky="w", pady=10)
btn_rechercher.grid(row=2, column=2, padx=20)
btn_nouvelle_info.grid(row=1, column=0, padx=20)
message_info.grid(row=1, column=1, sticky="w", pady=10)
frame_resultat.grid(row=0, column=0, columnspan=2, padx=25, pady=25)
resultat.pack(padx=25, pady=(25,0))
sb.pack(fill="x", pady=(5,25), padx=(25,25))

frame_btn.pack(pady=(0,15))
btn_deselectionner.grid(row=0, column=2, padx=10)
btn_effacer.grid(row=0, column=1, padx=10)
btn_modifier.grid(row=0, column=3, padx=10)
clock.grid(row=0, column=2, sticky='n', pady=100)
btn_ouvrir.grid(row=0, column=2, sticky="n", pady=200)
btn_enregistrer.grid(row=0, column=2, sticky="n", pady=300)

tick()
fenetre.mainloop()