from tkinter import *

from tkinter import messagebox

from tkinter import ttk
from tkinter.ttk import Combobox

import sqlite3
from itertools import cycle


import subprocess
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import portrait, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import  TA_LEFT, TA_CENTER
from reportlab.lib.units import  cm

import sys
import os 
from theme_engine import ThemeEngine
from res_salles import RSalWindow
import database as db

sys.path.append(os.path.abspath('../'))

grid_colours = [
    '#%02x%02x%02x' % (0x1C, 0x77, 0xC3),
    '#%02x%02x%02x' % (0x39, 0xA9, 0xDB),
    '#%02x%02x%02x' % (0x40, 0xBC, 0xD8),
    '#%02x%02x%02x' % (0xE3, 0x92, 0x37),
    '#%02x%02x%02x' % (0xD6, 0x32, 0x30),
    '#%02x%02x%02x' % (0x1D, 0xD3, 0xB0),
    '#%02x%02x%02x' % (0xAF, 0xFC, 0x41),
    '#%02x%02x%02x' % (0xB2, 0xfF, 0x9E),
    '#%02x%02x%02x' % (0x6D, 0x72, 0xC3),
    "red",
    "green",
    "blue",
    "cyan",
    "yellow",
    "magenta"
]

class TTFWindow(ThemeEngine):
    def __init__(self, master):
        ThemeEngine.__init__(self)
        self.db_obj = db.Database()
        
        self.base = sqlite3.connect("UTTMA_FPO.db")
        self.cur = self.base.cursor()
        
        self.gfilier = master.filiere.get()
        self.gsemestre = master.semestre.get()
        self.gsection = master.section.get()
        self.ggroup = master.groupe.get()
        self.ggroup_tp = master.groupe_tp.get()
        self.master = master

        # Creating Top-level window & Setting Window Width and height        
        self.add_prod_win = Toplevel(master)
        win_width, win_height = 1200, 650
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = int((screen_width/2) - (win_width/2))  - 7
        y = int((screen_height/2) - (win_height/2)) - 35
        self.add_prod_win.geometry(f'{win_width}x{win_height}+{x}+{y}')
        self.add_prod_win.resizable(0,0) # Disabling resize
        # Setting Top Level Window Title
        if self.ggroup_tp == 'None' or self.ggroup_tp == '':
            self.add_prod_win.title("Filièr {}-{} {} TD {}".format(self.gfilier,self.gsemestre,self.gsection,self.ggroup))
        else:
            self.add_prod_win.title("Filièr {}-{} {} TD {} TP {}".format(self.gfilier,self.gsemestre,self.gsection,self.ggroup,self.ggroup_tp))
            
        self.voir_timetable_db()
        
        self.mainframe = LabelFrame(self.add_prod_win, width=1200, height=33)#,bg="#f7f7f7"
        self.mainframe.place(x=0, y=0)         
        self.buve = Menubutton(self.mainframe,  text="Fichier",font="roboto 12", compound='top')#,
        self.buve.place(x=20, y=0)
         # Create pull down menu
        self.buve.menu = Menu(self.buve, tearoff = 0)
        self.buve["menu"] = self.buve.menu 
        self.buve.menu.add_separator()
        self.buve.menu.add_command(label="Imprimer-pdf",command=self.makeprint_emploi)
        self.buve.menu.add_command(label="Claire l'emploi",command=self.clear_matrix)
        #self.buve.menu.add_command(label="Quitter",command=lambda: controller.qExit())
        
        self.buve1 = Menubutton(self.mainframe,  text="Edition",font="roboto 12", compound='top')#,
        self.buve1.place(x=120, y=0)
         # Create pull down menu
        self.buve1.menu = Menu(self.buve1, tearoff = 0)
        self.buve1["menu"] = self.buve1.menu 
        self.buve1.menu.add_separator()
        #self.buve1.menu.add_command(label="Enregistrer l'emploi TP",command=self.save_in_db_table_tp)
        self.buve1.menu.add_command(label="Enregistrer l'emploi",command=self.save_in_db_table)
        self.buve1.menu.add_command(label="Mise à jour l'emploi",command=self.update_in_db_table)
        
        
        self.buve2 = Menubutton(self.mainframe,  text="Recherche",font="roboto 12", compound='top')#,
        self.buve2.place(x=220, y=0)
        # Create pull down menu
        self.buve2.menu = Menu(self.buve2, tearoff = 0)
        self.buve2["menu"] = self.buve2.menu
        self.buve2.menu.add_separator()
        self.buve2.menu.add_command(label="Recherche la salle libre", command=lambda : RSalWindow(master))

     
    def clear_matrix(self):
        z = 0
        for i in range(1,19):
            for j in range(1,6):
                if(i%3 == 1):  
                    self.cr_vars[z].set("Module - ")
                if(i%3 == 2): 
                    self.cr_vars[z].set("Prof")
                if(i%3 == 0): 
                    self.cr_vars[z].set("Salle")
                self.butt.config(bg='lightgray')
                z += 1              
      
        
    def  voir_timetable_db(self):

        self.cur.execute("SELECT * FROM timetable_tp  WHERE filiere = ? AND  semestre = ? AND section = ? AND groupe =? AND groupetp =?",
            (self.gfilier, self.gsemestre, self.gsection, self.ggroup, self.ggroup_tp))            
        dbrows=self.cur.fetchall()
        ll = list(dbrows)
           
        
        if len(ll)>0:
            self.timetabling()
            for row in ll:
                #for j in range(1,6):
                clet = '({},{})'.format(row[1],row[2])
                #print('clet',clet)
                z =self.dict[clet]
                #print('z',z)
                if (row[1]%3==1):#(j !=3) and
                        self.cr_vars[z].set(row[-4])
                if (row[1]%3==2):
                        self.cr_vars[z].set(row[-3])
                if (row[1]%3==0):
                        self.cr_vars[z].set(row[-2])            
        else: 
            messagebox.showinfo("Validation info", "Ajouter l'emplois de {}-{}  {}  {} {}".format(self.gfilier,self.gsemestre,self.gsection,self.ggroup,self.ggroup_tp))
            self.timetabling()
        
               
    def timetabling(self):
        self.NewWindow = LabelFrame(self.add_prod_win, width=1200, height=600)#,bg="#f7f7f7"
        self.NewWindow.place(x=50, y=40) 
        # -----------------
        # START DATE LABEL
        Label(self.NewWindow,width=25,height=2, text='09 - 11', relief="solid",bg='white').grid(row=0,column=1)
        Label(self.NewWindow,width=25,height=2, text='11 - 13', relief="solid",bg='pink').grid(row=0,column=2)
        Label(self.NewWindow,width=20,height=2, text='13 - 15', relief="solid",bg='green').grid(row=0,column=3)
        Label(self.NewWindow,width=25,height=2, text='15 - 17', relief="solid",bg='yellow').grid(row=0,column=4)
        Label(self.NewWindow,width=25,height=2, text='17 - 19', relief="solid",bg='orange').grid(row=0,column=5)
        Label(self.NewWindow,width=20,height=6, text='Lundi', relief="solid",bg='orange').grid(row=1,rowspan=3)
        Label(self.NewWindow,width=20,height=6, text='Mardi', relief="solid",bg='blue').grid(row=4,rowspan=3)
        Label(self.NewWindow,width=20,height=6, text='Mercredi', relief="solid",bg='green').grid(row=7,rowspan=3)
        Label(self.NewWindow,width=20,height=6, text='Jeudi', relief="solid",bg='yellow').grid(row=10,rowspan=3)
        Label(self.NewWindow,width=20,height=6, text='Vendredi', relief="solid",bg='pink').grid(row=13,rowspan=3)
        Label(self.NewWindow,width=20,height=6, text='Samedi', relief="solid",bg='white').grid(row=16,rowspan=3)        
        self.left_course = []
        self.tasks = []
        self.cur.execute("select nom from module where filiere = ? and semestre = ?",
                         (self.gfilier, self.gsemestre))
        li1=self.cur.fetchall()
        if len(list(li1))!=0:
            for i in li1:
                self.left_course.append(i[0]+' - Cours')
                self.left_course.append(i[0]+' - TD')
                if self.gsemestre != 'S1' or self.gsemestre != 'S2':
                    self.left_course.append(i[0]+' - TP')  
                self.tasks.append(i[0])
        #add commun cours for section
        self.cur.execute("select commun from distribution where filiere = ? and semestre = ?",
                         (self.gfilier, self.gsemestre))
        lic=self.cur.fetchall()
        self.co_co = []
        if len(list(lic))!=0:
            for i in lic:
                if i[0] != None:
                    self.co_co.append(i[0]+' - Cours')        
        self.left_course.append('Module -') 
        self.Day = ['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi']
        self.Time = ['09-11','11-13','15-17','17-19']
        # THIS SECTION DEFINES THE ALGORITHM TO UPDATE THE OPTIONS IN THE GUI
        def update_options(var,butt,indi,indj,dictio):  
            cr = self.cr_vars[var].get()
            self.butt = butt
            if (cr=='Module - ' or cr=='Prof' or cr=='Salle'):
                return
            else:
                self.butt.config(bg="cyan")
        	
            try:
                sp=(str(cr)).split(' - ')
                cr = sp[0]
            except:
                pass
            color = self.colouring[cr]
            self.butt.configure(bg=color)          
                                        
                                    
        self.cr_vars = []
        self.dic ={}
        self.dict ={}
        z = 0
        
        self.cur.execute("select prof from profs")
        li=self.cur.fetchall()
        for i in li:
            self.tasks.append(i[0])

        self.cur.execute("select nom from salle")
        li2=self.cur.fetchall() 
        for i in li2:
            self.tasks.append(i[0])
                    
        self.colouring = dict(zip(sorted(self.tasks), cycle(grid_colours)))
        self.colouring["Module -"] = "#A4A9AD"
        self.colouring["Prof"] = "#A4A9AD"
        self.colouring["Salle"] = "#A4A9AD"
        
        for i in range(1,19):
            for j in range(1,6):
                self.left_salle=[]
                self.cur.execute("select nom from salle")
                li2=self.cur.fetchall() 
                for ii in li2:
                    self.left_salle.append(ii[0])
                self.left_salle.append('Salle')
                
                self.left_prof = []
                self.cur.execute("SELECT prof FROM profs  WHERE filiere = ? AND  semestre = ?",(self.gfilier, self.gsemestre))
                li=self.cur.fetchall()
                for ii in li:
                    self.left_prof.append(ii[0])
                self.left_prof.append('Prof')
                
                self.cr_vars.append(StringVar(self.NewWindow))
                cle = '{}'.format(z)
                self.dic[cle] = (i,j)
                clet = '({},{})'.format(i,j)
                self.dict[clet] = z
                
                if (j <3):
                    temp = self.Time[j-1]
                if (j >3):
                    temp = self.Time[j-2] 
   
                if(i%3 == 1): 
                    self.cr_vars[z].set("Module -")
                    self.w = OptionMenu(self.NewWindow, self.cr_vars[z], *self.left_course)
                    self.w.config(width=20,height=1)
                    if(j != 3) :
                        self.w.grid(row=i,column=j)

                    Jours = self.Day[(i-1)//3]
                    
                    self.cur.execute("SELECT filiere, semestre, section, groupe, module, prof, local, groupetp FROM timetable_tp  WHERE jours = ? AND  temps = ?",
                         (Jours,temp))
                    db_rows=self.cur.fetchall()
                    try :
                        for row in db_rows:
                            sp=(str(row[4])).split(' - ')
                            if (row[0] == self.gfilier and row[1] == self.gsemestre and  row[2] == self.gsection and self.ggroup != 'G1' and sp[1] =='Cours'):
                                self.cr_vars[z].set(row[4])
                                color = self.colouring[sp[0]]
                                self.w.config(bg=color)
                            if (row[0] == self.gfilier and row[1] == self.gsemestre and  row[2] == self.gsection and self.ggroup == 'G1' and (self.ggroup_tp == 'G1' or self.ggroup_tp == 'G2')):
                                self.cr_vars[z].set(row[4])
                                color = self.colouring[sp[0]]
                                self.w.config(bg=color)
                            if (row[0] == self.gfilier and row[1] == self.gsemestre and  row[2] == self.gsection and self.ggroup == 'G2' and (self.ggroup_tp == 'G3' or self.ggroup_tp == 'G4')):
                                self.cr_vars[z].set(row[4])
                                color = self.colouring[sp[0]]
                                self.w.config(bg=color)                                
                    except:
                        pass

                    self.cr_vars[z].trace("w", lambda *_, var=z, butt=self.w, indi=i, indj=j, dictio=self.dic: update_options(var,butt,indi,indj,dictio))
                    
                if(i%3 == 2):
                    self.cr_vars[z].set("Prof")
                    Jours = self.Day[(i-1)//3]
                    self.w = OptionMenu(self.NewWindow, self.cr_vars[z], *self.left_prof)
                    
                    
                    self.cur.execute("SELECT filiere, semestre, section, groupe, module, prof, local, groupetp FROM timetable_tp  WHERE jours = ? AND  temps = ?",
                         (Jours,temp))
                    db_rows=self.cur.fetchall()

                    for row in db_rows:
                        try:
                            sp=(str(row[4])).split(' - ') #or (row[7]!=self.ggroup_tp and sp[1] !='TD')
                            if (row[5] != 'Prof' and row[5] != '') and (row[5] in self.left_prof) and (row[4] not in self.co_co):
                                if  (row[0] != self.gfilier or row[1] != self.gsemestre or  row[2] != self.gsection ):
                                    self.left_prof.remove(row[5])
                                    self.w = OptionMenu(self.NewWindow, self.cr_vars[z], *self.left_prof)
                                if  (row[0] == self.gfilier and row[1] == self.gsemestre and row[2] == self.gsection and row[3] != self.ggroup and sp[1] !='Cours'):
                                    self.left_prof.remove(row[5])
                                    self.w = OptionMenu(self.NewWindow, self.cr_vars[z], *self.left_prof)
                                
                                if  (row[0] == self.gfilier and row[1] == self.gsemestre and row[2] == self.gsection and row[3] == self.ggroup and row[7]!=self.ggroup_tp and sp[1] !='Cours' and sp[1] !='TD'):
                                    self.left_prof.remove(row[5])
                                    self.w = OptionMenu(self.NewWindow, self.cr_vars[z], *self.left_prof)
                                
                            if (row[0] == self.gfilier and row[1] == self.gsemestre and  row[2] == self.gsection and self.ggroup != 'G1' and sp[1] =='Cours') and (row[5] != 'Prof' and row[5] != ''):
                                self.cr_vars[z].set(row[5])
                                color = self.colouring[row[5]]
                                self.w.config(bg=color)
                            if (row[0] == self.gfilier and row[1] == self.gsemestre and  row[2] == self.gsection and self.ggroup == 'G1' and (self.ggroup_tp == 'G1' or self.ggroup_tp == 'G2')) and (row[5] != 'Prof' and row[5] != ''):
                                self.cr_vars[z].set(row[5])
                                color = self.colouring[row[5]]
                                self.w.config(bg=color)
                            if (row[0] == self.gfilier and row[1] == self.gsemestre and  row[2] == self.gsection and self.ggroup == 'G2' and (self.ggroup_tp == 'G3' or self.ggroup_tp == 'G4')) and (row[5] != 'Prof' and row[5] != ''):
                                self.cr_vars[z].set(row[5])
                                color = self.colouring[row[5]]
                                self.w.config(bg=color)                                
                        except:
                            pass

                    self.w.config(width=20,height=1)
                    if(j != 3) :
                        self.w.grid(row=i,column=j)                       
                    self.cr_vars[z].trace("w", lambda *_, var=z, butt=self.w, indi=i, indj=j, dictio=self.dic: update_options(var,butt,indi,indj,dictio))
                
                if(i%3 == 0):
                    self.cr_vars[z].set("Salle")
                    self.w = OptionMenu(self.NewWindow, self.cr_vars[z], *self.left_salle)
                    Jours = self.Day[(i-1)//3]
                    self.cur.execute("SELECT filiere, semestre, section, groupe, module, prof, local, groupetp FROM timetable_tp  WHERE jours = ? AND  temps = ?",
                         (Jours,temp))
                    db_rows=self.cur.fetchall()
                    
                    for row in db_rows:
                        try:
                            sp=(str(row[4])).split(' - ')
                            if (row[6] != 'Salle' and row[6] != '') and (row[6] in self.left_salle) and (row[4] not in self.co_co):
                                if  (row[0] != self.gfilier or row[1] != self.gsemestre or  row[2] != self.gsection ):
                                    self.left_salle.remove(row[6])
                                    self.w = OptionMenu(self.NewWindow, self.cr_vars[z], *self.left_salle) 
                                if  (row[0] == self.gfilier and row[1] == self.gsemestre and row[2] == self.gsection and row[3] != self.ggroup and sp[1] !='Cours'):
                                    self.left_salle.remove(row[6])
                                    self.w = OptionMenu(self.NewWindow, self.cr_vars[z], *self.left_salle) 
                                
                                if  (row[0] == self.gfilier and row[1] == self.gsemestre and row[2] == self.gsection and row[3] == self.ggroup and row[7]!=self.ggroup_tp and sp[1] !='Cours' and sp[1] !='TD'):
                                    self.left_salle.remove(row[6])
                                    self.w = OptionMenu(self.NewWindow, self.cr_vars[z], *self.left_salle) 
                              
                            if (row[0] == self.gfilier and row[1] == self.gsemestre and  row[2] == self.gsection and self.ggroup != 'G1' and sp[1] =='Cours') and (row[6] != '' and  row[6] != 'Salle'):
                                self.cr_vars[z].set(row[6])
                                color = self.colouring[row[6]]
                                self.w.config(bg=color)
                            if (row[0] == self.gfilier and row[1] == self.gsemestre and  row[2] == self.gsection and self.ggroup == 'G1' and (self.ggroup_tp == 'G1' or self.ggroup_tp == 'G2')) and (row[5] != 'Prof' and row[5] != ''):
                                self.cr_vars[z].set(row[6])
                                color = self.colouring[row[6]]
                                self.w.config(bg=color)
                            if (row[0] == self.gfilier and row[1] == self.gsemestre and  row[2] == self.gsection and self.ggroup == 'G2' and (self.ggroup_tp == 'G3' or self.ggroup_tp == 'G4')) and (row[5] != 'Prof' and row[5] != ''):
                                self.cr_vars[z].set(row[6])
                                color = self.colouring[row[6]]
                                self.w.config(bg=color)                                 
                        except:
                            pass

                    self.w.config(width=20,height=1)
                    if(j != 3) :
                        self.w.grid(row=i,column=j)
                    self.cr_vars[z].trace("w", lambda *_, var=z, butt=self.w, indi=i, indj=j, dictio=self.dic: update_options(var,butt,indi,indj,dictio))

                z = z + 1

        
    def save_in_db_table(self):
        self.cur.execute("SELECT * FROM timetable_tp  WHERE filiere = ? AND  semestre = ? AND section = ? AND groupe =? AND groupetp =?",
             (self.gfilier,self.gsemestre,self.gsection,self.ggroup,self.ggroup_tp)) 
        db_rows=self.cur.fetchall()
     
        if len(list(db_rows))!=0:
            messagebox.showinfo("Validation info", "TT {} - {}  {}  {} exist in db, so it well update".format(self.gfilier,self.gsemestre,self.gsection,self.ggroup,self.ggroup_tp))
            self.update_in_db_table()
            return        
        z = 0
        self.cours = ['','','','','']
        self.prof = ['','','','','']
        for i in range(1,19):
            Jours = self.Day[(i-1)//3]
            for j in range(1,6):
                if (j <3):
                    temp = self.Time[j-1]
                if (j >3):
                    temp = self.Time[j-2]
                if (j !=3) and (i%3 == 1):
                    self.cours[j-1]=self.cr_vars[z].get()
                    self.cur.execute("INSERT INTO timetable_tp VALUES(NULL,?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?)",
                        (i,j,self.gfilier,self.gsemestre,self.gsection,self.ggroup, Jours, temp,self.cours[j-1], '','',self.ggroup_tp))                    
                    self.base.commit()  
                if (j !=3) and (i%3 == 2):
                    self.prof[j-1]=self.cr_vars[z].get()
                    self.cur.execute("INSERT INTO timetable_tp VALUES(NULL,?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?)",
                       (i,j,self.gfilier,self.gsemestre,self.gsection,self.ggroup, Jours, temp,self.cours[j-1], self.prof[j-1],'',self.ggroup_tp))                        
                    self.base.commit()
                if (j !=3) and (i%3 == 0):
                    local=self.cr_vars[z].get()
                    self.cur.execute("INSERT INTO timetable_tp VALUES(NULL,?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?)",
                        (i,j,self.gfilier,self.gsemestre,self.gsection,self.ggroup, Jours, temp,self.cours[j-1], self.prof[j-1],local,self.ggroup_tp))                        
                    self.base.commit()
                z += 1                         
        messagebox.showinfo("Validation info", "SAVED SUCCESSFULLY to db of TP")
        self.master.getfiliere()         

    def update_in_db_table(self):
        self.cur.execute("SELECT * FROM timetable_tp  WHERE filiere = ? AND  semestre = ? AND section = ? AND groupe =? AND groupetp =?",
             (self.gfilier,self.gsemestre,self.gsection,self.ggroup,self.ggroup_tp))            
        db_rows=self.cur.fetchall()
        
        if len(list(db_rows))==0:
            messagebox.showinfo("Validation info", "TT {} - {} {} {} {} not exist in db, but well saved ".format(self.gfilier,self.gsemestre,self.gsection,self.ggroup,self.ggroup_tp))
            self.save_in_db_table()
            return        
        z = 0
        cours = ['','','','','']
        prof = ['','','','','']
        for i in range(1,19):
            Jours = self.Day[(i-1)//3]
            for j in range(1,6):
                if (j <3):
                    temp = self.Time[j-1]
                if (j >3):
                    temp = self.Time[j-2]
                if (j !=3) and (i%3 == 1):
                    cours[j-1]=self.cr_vars[z].get()
                    self.db_obj.update_timetable_tp_table(Jours, temp,cours[j-1], '','',i,j, self.gfilier,self.gsemestre,self.gsection,self.ggroup,self.ggroup_tp)                   
                if (j !=3) and (i%3 == 2):
                    prof[j-1]=self.cr_vars[z].get()
                    self.cur.execute("UPDATE timetable_tp SET jours =?, temps=?, module=?, prof=?, local=?  WHERE indi=? AND indj=? AND filiere=? AND semestre=? AND section =? AND groupe=? AND groupetp =?",
                        ( Jours, temp,cours[j-1], prof[j-1],'',i,j, self.gfilier,self.gsemestre,self.gsection,self.ggroup,self.ggroup_tp))                        
                    self.base.commit()
                if (j !=3) and (i%3 == 0):
                    local=self.cr_vars[z].get()
                    self.cur.execute("UPDATE timetable_tp SET jours =?, temps=?, module=?, prof=?, local=?  WHERE indi=? AND indj=? AND filiere=? AND semestre=? AND section =? AND groupe=? AND groupetp =?",
                           ( Jours, temp,cours[j-1], prof[j-1],local,i,j, self.gfilier, self.gsemestre, self.gsection,self.ggroup,self.ggroup_tp))                        
                    self.base.commit()                

                z += 1                         
        messagebox.showinfo("Validation info", "UPDATE SUCCESSFULLY to db")
                    
    def makeprint_emploi(self):
           if messagebox.askyesno("Alerte!","Imprimer cette emploi ?")== True:
                styles = getSampleStyleSheet()
                styleN = styles["BodyText"]
                #used alignment if required
                styleN.alignment = TA_LEFT
                styleBH = styles["Normal"]
                styleBH.alignment = TA_CENTER
                #add mekdir folder
                os.makedirs('./emploi', exist_ok = True)
                if self.ggroup_tp == 'CM':
                    canv = canvas.Canvas("emploi/{}-{}{}TD{}.pdf".format(self.gfilier,self.gsemestre,self.gsection,self.ggroup), pagesize=landscape(A4))
                else:
                    canv = canvas.Canvas("emploi/{}-{}{}TD{}TP{}.pdf".format(self.gfilier,self.gsemestre,self.gsection,self.ggroup,self.ggroup_tp), pagesize=landscape(A4))
                canv.setLineWidth(.3)
                canv.setFont('Helvetica', 13)
                canv.drawImage('./images/FPO.png', 50, 530, width=290, height=60)
                canv.line(50, 515,800 ,515) #coordinate sequence: (x_start, y_start, x_end, y_end)
                canv.drawString(600, 500, "Année universitaire {}".format('2021-2022'))
                if self.gsection != '' and self.ggroup_tp == 'CM':
                    canv.drawString(50, 490, "Emploi du Temps  : Filière {} - Semestre {} - Section {} - Groupe TD {}".format(self.gfilier,self.gsemestre,self.gsection,self.ggroup))
                if self.gsection != '' and self.ggroup_tp != 'CM':
                    canv.drawString(50, 490, "Emploi du Temps  : Filière {} - Semestre {} - Section {} - Groupe TD {} - Groupe TP {}".format(self.gfilier,self.gsemestre,self.gsection,self.ggroup,self.ggroup_tp))
                if self.gsection == '' and self.ggroup_tp == 'CM':
                    canv.drawString(50, 490, "Emploi du Temps  : Filière {} - Semestre {} - Groupe TD {}".format(self.gfilier,self.gsemestre,self.ggroup))
                if self.gsection == '' and self.ggroup_tp != 'CM':
                    canv.drawString(50, 490, "Emploi du Temps  : Filière {} - Semestre {} - Groupe TD {} - Groupe TP {}".format(self.gfilier,self.gsemestre,self.ggroup,self.ggroup_tp))
                    
                #canv.setFont('Helvetica-Bold', 32)
                data = [['','09-11','11-13','13-15','15-17','17-19']]

                z = 0
                for i in range(1,19):
                    a =[]
                    if i%3 == 2:
                        a.append(self.Day[i//3])
                    else:
                        a.append('')
                    
                    for j in range(1,6):
                        cr = self.cr_vars[z].get()
                        if cr == 'Module -' or cr == 'Prof' or cr == 'Salle':
                            cr = ''
                        if (j !=3) and (i%3 == 2) and cr != '':
                            cr = 'Prof. '+ cr
                        if j==3:
                            a.append('')
                        else:  
                            a.append(cr)
                        
                            
                        z += 1
                    data.append(a)
                              
                t = Table(data, (1.85*cm,6*cm,6*cm,1.65*cm,6*cm,6*cm))
                t.setStyle(TableStyle([
                                    ('GRID', (1,0), (-1,-1), 1, colors.red, 1, None, 1),
                                    ('FONTNAME', (0,0), (0,-1), 'Courier-Bold'),
                                    ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
                                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                                   #('LINEABOVE', (0,1), (2,1), 1 ,colors.blue, None, (5,3,1,3)),
                                   ('LINEABOVE', (0,1), (-1,1), 0.25 ,colors.blue, None, None, None, 4, 0.5),
                                   ('LINEABOVE', (0,4), (-1,4), 2 ,colors.blue, 1),
                                   ('LINEABOVE', (0,7), (-1,7), 2 ,colors.blue, 1),
                                   ('LINEABOVE', (0,10), (-1,10), 2 ,colors.blue, 1),
                                   ('LINEABOVE', (0,13), (-1,13), 2 ,colors.blue, 1),
                                   ('LINEABOVE', (0,16), (-1,16), 2 ,colors.blue, 1)
                                   #('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)
                                   ]))   
                aW = 400
                aH = 450
                
                w, h = t.wrap(aW, aH)
                t.drawOn(canv, 50, aH-h)
                
                canv.showPage()
                canv.save()
                
                if self.ggroup_tp == 'CM':
                    subprocess.Popen(["emploi\{}-{}{}TD{}.pdf".format(self.gfilier,self.gsemestre,self.gsection,self.ggroup)],shell=True)
                else:
                    subprocess.Popen(["emploi\{}-{}{}TD{}TP{}.pdf".format(self.gfilier,self.gsemestre,self.gsection,self.ggroup,self.ggroup_tp)],shell=True)

