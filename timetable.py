# importing modules
from tkinter import *

from tkinter import messagebox

from tkinter import ttk
from tkinter.ttk import Combobox

#from openpyxl import load_workbook
from Addtional_features import mycombobox, myentry
import sqlite3


import time
import os
import sys
import database as db
# print(sys.path)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main_menu as main_menu

from theme_engine import ThemeEngine
from enseignants import EnsWindow
from salles import SalWindow
from distribution import DistWindow
from res_salles import RSalWindow
from TT_FSG import TTFWindow
from TT_Prof import TTPWindow
from TT_Salle import TTSWindow
from modules import ModWindow
from profs import ProfWindow    
    
class TTWindow(Frame, ThemeEngine):
    """Inventory Window to Update or Delete Inventories and to add New product"""
    
    def __init__(self, master):
        Frame.__init__(self, master)
        # Initializing Theme Engine
        ThemeEngine.__init__(self)
        self.master = master
        #===== Main Background Frame / Master Frame ===============

        self.master.title("FACULTY MANAGEMENT")
        self.master.geometry("1000x600")
        self.base = sqlite3.connect("UTTMA_FPO.db")
        self.cur = self.base.cursor()

        self.db_obj = db.Database()
        self.mainframe = LabelFrame(master, width=999, height=33)#,bg="#f7f7f7"
        self.mainframe.place(x=0, y=0)         

        
        self.buve1 = Menubutton(self.mainframe,  text="Edition",font="roboto 12", compound='top')#,
        self.buve1.place(x=20, y=0)
         # Create pull down menu
        self.buve1.menu = Menu(self.buve1, tearoff = 0)
        self.buve1["menu"] = self.buve1.menu 
        self.buve1.menu.add_separator()
        self.buve1.menu.add_command(label="Ressource Humaine",command=lambda : EnsWindow(self))
        self.buve1.menu.add_command(label="Professeurs",command=lambda : ProfWindow(self))
        self.buve1.menu.add_command(label="Locaux",command=lambda : SalWindow(self))
        #self.buve1.menu.add_command(label="Étudiants")
        self.buve1.menu.add_command(label="Distribution",command=lambda : DistWindow(self))
        self.buve1.menu.add_command(label="Modules",command=lambda : ModWindow(self))
        #self.buve1.menu.add_command(label="Quitter",command=lambda: controller.qExit())
        
        self.buve2 = Menubutton(self.mainframe,  text="Recherche",font="roboto 12", compound='top')#,
        self.buve2.place(x=220, y=0)
         # Create pull down menu
        self.buve2.menu = Menu(self.buve2, tearoff = 0)
        self.buve2["menu"] = self.buve2.menu
        self.buve2.menu.add_separator()
        self.buve2.menu.add_command(label="Recherche la salle libre",command=lambda : RSalWindow(self))
        
        # Buttons
        cin_button = Button(master, text="Emplois des filières", bg='#000000', fg='white', font=('Orbitron', 20, 'bold'), width=30,
                        command=self.filier)
        cin_button.place(x=300,y=100)
        cot_button = Button(master, text="Emplois des professeurs", bg='#1a1a1a', fg='white', font=('Orbitron', 20, 'bold'), width=30,
                        command=self.prof)
        cot_button.place(x=300,y=200)
        rd_button = Button(master, text="Emplois des salles", bg='#404040', fg='white', font=('Orbitron', 20, 'bold'), width=30,
                       command=self.sall)
        rd_button.place(x=300,y=300)
        cd_button = Button(master, text="Rattrapage, annulation et réservation", bg='#666666', fg='white', font=('Orbitron', 20, 'bold'), width=30,
                       command=self.even)
        cd_button.place(x=300,y=400) 
        
        
    def filier(self): 
        self.NewWindow = Toplevel() 
        self.NewWindow.title("Filières TT") 
        self.NewWindow.geometry('1000x650')          
        mFrame11 = LabelFrame(self.NewWindow, text = ' Choix de la filière, semestre, section et groupe ',width=940, height=200)
        mFrame11.place(x=50,y=50)
        
        Label(mFrame11, text = 'Filière: ', font=('Orbitron', 15)).place(x=10, y=10,height = 30)
        self.filiere=mycombobox(mFrame11,  width=10,   font=('Arial', 15))
        self.filiere.place(x=100, y=10,height = 30)
        self.cur.execute("select filiere from distribution")
        li = self.cur.fetchall()    
        a = []
        for i in range(0, len(li)):
            if li[i][0] not in a:
                a.append(li[i][0])
        self.filiere.set_completion_list(a)
        self.filiere.bind("<<ComboboxSelected>>", self.callback)
        Label(mFrame11, text = 'Semestre: :', font=('Orbitron', 15)).place(x=280, y=10,height = 30)
        self.semestre = mycombobox(mFrame11,   width=10,   font=('Arial', 15))
        self.semestre.place(x=400, y=10,height = 30)         
        self.semestre.bind("<<ComboboxSelected>>", self.callback2)
        
        Label(mFrame11, text = 'Section:', font=('Orbitron', 15)).place(x=10, y=60,height = 30)
        self.section = mycombobox(mFrame11,   width=10,  font=('Arial', 15))
        self.section.place(x=100, y=60,height = 30) 
        self.section.bind("<<ComboboxSelected>>", self.callback3)

        Label(mFrame11, text = 'Groupe TD:', font=('Orbitron', 15)).place(x=280, y=60,height = 30)
        self.groupe = mycombobox(mFrame11,   width=10,   font=('Arial', 15))
        self.groupe.place(x=400, y=60,height = 30)
        self.groupe.bind("<<ComboboxSelected>>", self.callback4)

        Label(mFrame11, text = 'Groupe TP:', font=('Orbitron', 15)).place(x=540, y=60,height = 30)
        self.groupe_tp = mycombobox(mFrame11,   width=10,   font=('Arial', 15))
        self.groupe_tp.place(x=660, y=60,height = 30)
        
        Button(mFrame11, text='Time Table',activeforeground='blue',activebackground='red',bg="#66ff66", command=lambda : TTFWindow(self)).place(x=10, y=120,height = 30)
        Button(mFrame11, text='Clear',activeforeground='blue',activebackground='red', bg="pink", command=self.clear).place(x=110, y=120,height = 30)
        Button(mFrame11, text='Supprimer',activeforeground='blue',activebackground='red', bg="pink", command=self.delet_emploi).place(x=210, y=120,height = 30)
        Button(mFrame11, text="Exit", bg="#ff0000", fg="white", width=10, command=self.tExit, font=('Orbitron', 10, 'bold')).place(x=310, y=120,height = 30)
        #Button(mFrame11, text="Update TP", bg="#ff0000", fg="white", width=10, command=self.update_tp, font=('Orbitron', 10, 'bold')).place(x=410, y=120,height = 30)

            
        mFrame = Frame(self.NewWindow,width=800, height=600)
        mFrame.place(x=50,y=250)
        
        scrollbarx = Scrollbar(mFrame, orient=HORIZONTAL)
        scrollbary = Scrollbar(mFrame, orient=VERTICAL)
        self.tree = ttk.Treeview(mFrame, columns=('Filière', 'Semestre','Section','Groupe','Groupe_tp'), 
        selectmode="browse", height=18,yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=100)
        self.tree.column('#2', stretch=NO, minwidth=0, width=100)
        self.tree.column('#3', stretch=NO, minwidth=0, width=100)
        self.tree.column('#4', stretch=NO, minwidth=0, width=100)
        self.tree.column('#5', stretch=NO, minwidth=0, width=100)
        #self.tree.heading('id', text="Id", anchor=W)
        self.tree.heading('Filière', text="Filière", anchor=W)
        self.tree.heading('Semestre', text="Semestre", anchor=W)
        self.tree.heading('Section', text="Section", anchor=W)
        self.tree.heading('Groupe', text="Groupe TD", anchor=W)
        self.tree.heading('Groupe_tp', text="Groupe TP", anchor=W)
        self.tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=self.tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=self.tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=40)
        self.getfiliere()
        self.tree.bind("<<TreeviewSelect>>", self.clicktable)

    def callback(self,eventObject):
        self.cur.execute("select semestre from distribution where filiere = ?",(self.filiere.get(),))#, very important
        li = self.cur.fetchall()    
        a = []
        for i in range(0, len(li)):
           a.append(li[i][0])
        self.semestre.set_completion_list(a)
        
    def callback2(self,eventObject):
        self.cur.execute("SELECT section FROM distribution  WHERE filiere = ? AND  semestre = ?",(self.filiere.get(),self.semestre.get()))
        li = self.cur.fetchall()    
        a = []
        sec_max = li[0][0]
        if sec_max == 1:
            a.append('')
        if sec_max == 2:
            a.append('A')
            a.append('B')
        if sec_max == 3:
            a.append('A')
            a.append('B')
            a.append('C')            
        self.section.set_completion_list(a)
        
    def callback3(self,eventObject):
        self.cur.execute("SELECT groupe FROM distribution  WHERE filiere = ? AND  semestre = ?",(self.filiere.get(),self.semestre.get()))
        li = self.cur.fetchall()    
        a = []
        sec_max = li[0][0]
        if sec_max == 1:
            a.append('')
        if sec_max > 1:
            for i in range(1, sec_max+1):
               a.append('G'+str(i))
        self.groupe.set_completion_list(a)

    def callback4(self,eventObject):
        self.cur.execute("SELECT groupetp FROM distribution  WHERE filiere = ? AND  semestre = ?",(self.filiere.get(),self.semestre.get()))
        li = self.cur.fetchall()    
        a = []
        sec_max = li[0][0]
        if sec_max == 0:
            a.append('None')
        if sec_max > 1 and self.groupe.get()=='G1':
            a.append('G1')
            a.append('G2')
        if sec_max > 1 and self.groupe.get()=='G2':
            a.append('G3')
            a.append('G4')
        if sec_max > 1 and self.groupe.get()=='G3':
            a.append('G5')
            a.append('G6')            
        self.groupe_tp.set_completion_list(a)
        
    def clicktable(self, event):
        cur = self.tree.selection()
        cur = self.tree.item(cur)
        li = cur['values']
        if (len(li) >= 4):
            self.filiere.set((li[0]))
            self.semestre.set((li[1]))
            self.section.set((li[2]))
            self.groupe.set((li[3]))
            self.groupe_tp.set((li[4]))

    def clear(self):
        self.filiere.set('')
        self.semestre.set('')
        self.section.set('')
        self.groupe.set('')
        self.groupe_tp.set('')
        self.getfiliere()
            

        
    def getfiliere(self):
         records = self.tree.get_children()
         for element in records:
            self.tree.delete(element)

         sallelist = self.db_obj.get_timetable_tp_value()
         an=[]
         for i in sallelist:
             if i not in an:
                 an.append(i)
                 self.tree.insert('', 'end', values=(i))
                 
    def delet_emploi(self):
        if self.filiere.get()=='' or self.semestre.get() =='' :
            messagebox.showinfo("Alerte!", "Sélectionner l'emploi !")
            return
        if messagebox.askyesno('Alerte!',"Voulez-vous supprimer l'emploi  sélectionner?") == True:
            self.base = sqlite3.connect("UTTMA_FPO.db")
            self.cur = self.base.cursor()
            self.cur.execute("SELECT * FROM timetable_tp  WHERE filiere = ? AND  semestre = ? AND section = ? AND groupe = ? AND groupetp = ?",
                         (self.filiere.get(),self.semestre.get(), self.section.get(), self.groupe.get(), self.groupe_tp.get()))
            sallelist = self.cur.fetchall()
            while len(sallelist)>0:
                self.cur.execute("DELETE  FROM timetable_tp  WHERE filiere = ? AND  semestre = ? AND section = ? AND groupe = ? AND groupetp = ?",
                         (self.filiere.get(),self.semestre.get(), self.section.get(), self.groupe.get(), self.groupe_tp.get()))
                self.base.commit()
                self.cur.execute("SELECT * FROM timetable_tp  WHERE filiere = ? AND  semestre = ? AND section = ? AND groupe = ? AND groupetp = ?",
                         (self.filiere.get(),self.semestre.get(), self.section.get(), self.groupe.get(), self.groupe_tp.get()))
                sallelist = self.cur.fetchall()                
            self.getfiliere()
            messagebox.showinfo("Alerte!", "l'emploi est supprimé")
            
    def update_tp(self):
        '''
        if self.filiere.get()=='' and self.semestre.get() =='' and self.groupe_tp.get()=='':
            messagebox.showinfo("Alerte!", "Sélectionner l'emploi !")
            return
        '''
        if messagebox.askyesno('Alerte!',"Do you want update TP groupe?") == True:
            self.base = sqlite3.connect("dataFPO.db")
            self.cur = self.base.cursor()
            self.cur.execute("UPDATE timetable SET groupetp = ?",
                         ('CM',))
            self.base.commit()
                
            self.getfiliere()
            messagebox.showinfo("Alerte!", "TT are update")
        
    def tExit(self):
        self.NewWindow.destroy() 
          
    def prof(self):  
        self.NewWindow = Toplevel() 
        self.NewWindow.title("DMG TT") 
        self.NewWindow.geometry('300x300')         
        mFrame1 = LabelFrame(self.NewWindow, text = "Informations sur l'Emplois des professeurs",width=600, height=200)
        mFrame1.place(x=50,y=50)

              
        Label(mFrame1, text = 'Prof: ').grid(row=8,column=1)
        self.proff = mycombobox(mFrame1, width=15,   font=('Arial', 15))
        self.cur.execute("select prof from profs")
        li = self.cur.fetchall()    
        a = []
        for i in range(0, len(li)):
            if li[i][0] not in a:
                a.append(li[i][0])
        self.proff.set_completion_list(a)

        self.proff.grid(row=8,column=2)
        
        button2 = Button(mFrame1, text='Import',activeforeground='blue',activebackground='red',bg="pink",command=lambda : TTPWindow(self))
        button2.grid(row=12,column=2) 
         
    def sall(self):
        self.NewWindow = Toplevel() 
        self.NewWindow.title("EMAIC TT") 
        self.NewWindow.geometry('300x300')          
        mFrame1 = LabelFrame(self.NewWindow, text = "Informations sur l'Emplois des salles",width=600, height=200)
        mFrame1.place(x=50,y=50)        
        
        self.left_salle=[]
        self.cur.execute("select nom from salle")
        li2=self.cur.fetchall() 
        for i in li2:
            if i[0] not in self.left_salle:
                self.left_salle.append(i[0])    
        
        Label(mFrame1, text = 'Salle: ').grid(row=10,column=1)
        self.sall = Combobox(mFrame1, width=15)
        list_sall = ['']
        for ii in range(len(self.left_salle)):
            list_sall.append(self.left_salle[ii])
        self.sall['values'] = tuple(list_sall)
        self.sall.current(0)  # set the selected item
        self.sall.grid(row=10,column=2)
        ###

        button2 = Button(mFrame1, text='Import',activeforeground='blue',activebackground='red',bg="pink",command=lambda : TTSWindow(self))
        button2.grid(row=12,column=2)  
        
    def even(self): 
        self.NewWindow = Toplevel() 
        self.NewWindow.title("EMAIC TT") 
        self.NewWindow.geometry('800x650')          
        mFrame11 = LabelFrame(self.NewWindow, text = 'Informations sur rattrapage, annulation et réservation',width=700, height=200)
        mFrame11.place(x=50,y=50)
        
        Label(mFrame11, text = 'Nom : ', font=('Orbitron', 15)).place(x=10, y=10,height = 30)
        self.nom = StringVar()
        x1=myentry(mFrame11, textvariable=self.nom,  width=23, bd=5, bg="#ccefff", fg='blue', font=('Arial', 15))
        x1.place(x=110, y=10,height = 30)
        self.cur.execute("select prof from profs")
        li = self.cur.fetchall()    
        a = []
        for i in range(0, len(li)):
           a.append(li[i][0])
        x1.set_completion_list(a)
        Label(mFrame11, text = 'Tel :', font=('Orbitron', 15)).place(x=330, y=10,height = 30)
        self.tel = StringVar()
        Entry(mFrame11, textvariable=self.tel, width=18, bd=5, bg="#ccefff", fg='blue', font=('Arial', 15)).place(x=375, y=10,height = 30) 
        Label(mFrame11, text = 'Date :', font=('Orbitron', 15)).place(x=10, y=60,height = 30)
        self.specialite = StringVar()
        Entry(mFrame11, textvariable=self.specialite,  width=23, bd=5, bg="#ccefff", fg='blue', font=('Arial', 15)).place(x=110, y=60,height = 30)
        Label(mFrame11, text = 'Heures :', font=('Orbitron', 15)).place(x=10, y=110,height = 30)
        self.specialite = StringVar()
        Entry(mFrame11, textvariable=self.specialite,  width=23, bd=5, bg="#ccefff", fg='blue', font=('Arial', 15)).place(x=110, y=110,height = 30)
        Label(mFrame11, text = 'Lieu :', font=('Orbitron', 15)).place(x=360, y=60,height = 30)
        self.grade = Combobox(mFrame11, width=10)
        self.grade['values'] = ('',
                                    'Salle',
                                    'Amphi',
                                    'Studio',
                                    'AUTRE')
        self.grade.current(0)  # set the selected item
        self.grade.place(x=440, y=60,height = 30)     
        Label(mFrame11, text = 'Type :', font=('Orbitron', 15)).place(x=360, y=110,height = 30)
        self.grade = Combobox(mFrame11, width=10)
        self.grade['values'] = ('',
                                    'Annulation',
                                    'Rattrapage',
                                    'Réservation',
                                    'AUTRE')
        self.grade.current(0)  # set the selected item
        self.grade.place(x=440, y=110,height = 30)   


        mFrame = Frame(self.NewWindow,width=800, height=600)
        mFrame.place(x=50,y=250)
        
        scrollbarx = Scrollbar(mFrame, orient=HORIZONTAL)
        scrollbary = Scrollbar(mFrame, orient=VERTICAL)
        self.tree = ttk.Treeview(mFrame, columns=('id',
         'Nom', 'tel','Date','Heures','Lieu','Type'), 
        selectmode="browse", height=18,yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=40)
        self.tree.column('#2', stretch=NO, minwidth=0, width=150)
        self.tree.column('#3', stretch=NO, minwidth=0, width=150)
        self.tree.column('#4', stretch=NO, minwidth=0, width=70)
        self.tree.column('#5', stretch=NO, minwidth=0, width=70)
        self.tree.column('#6', stretch=NO, minwidth=0, width=120)                 
        self.tree.column('#7', stretch=NO, minwidth=0, width=120)
        self.tree.heading('id', text="Id", anchor=W)
        self.tree.heading('Nom', text="Nom", anchor=W)
        self.tree.heading('tel', text="Tel", anchor=W)
        self.tree.heading('Date', text="Date", anchor=W)
        self.tree.heading('Heures', text="Heures", anchor=W)
        self.tree.heading('Lieu', text="Lieu", anchor=W)
        self.tree.heading('Type', text="Type", anchor=W)
        self.tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=self.tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=self.tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)
        #self.getprof()
        #self.tree.bind("<<TreeviewSelect>>", self.clicktable)
    
    

        
'''        
        #========================  Title Frame  ==========================

        title_frame = ttk.Frame(bg_frame)
        title_frame.place(x=20, y=20, relwidth=0.97)
        # Back Button
        self.back_btn_img = tk.PhotoImage(file='images/back_button.png')
        back_btn = tk.Button(title_frame, image=self.back_btn_img, bd=0,
                            bg=self.button_bg, activebackground=self.button_bg,
                            command=lambda: master.switch_frame(main_menu.MainMenuWindow, bg_frame))
        back_btn.pack(side="left", padx=50)
        # Title Label
        title_label = ttk.Label(title_frame, text="البيانات",
                                font="Arial 60 bold", foreground='#22d3fe')
        title_label.pack(side="left", padx=240)
        # Time Label
        date_string = time.strftime("%a,%d/%b/%y")
        time_string = time.strftime("%I:%M %p")
        date_label = ttk.Label(title_frame, text=date_string, font="Arial 18 bold")
        date_label.place(x=1030, y=15)
        time_label = ttk.Label(title_frame, text=time_string, font="Arial 18 bold")
        time_label.place(x=1060, y=50)

        
'''

        
        

