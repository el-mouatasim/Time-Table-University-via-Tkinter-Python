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

class TTPWindow(ThemeEngine):
    def __init__(self, master):
        ThemeEngine.__init__(self)
        self.base = sqlite3.connect("UTTMA_FPO.db")
        self.cur = self.base.cursor() 
        #self.cur.execute("select * from get")
        #li=self.cur.fetchall()
        #self.gfilier = li[-1][1]

        self.master = master
        self.profg = master.proff.get()
        #print(self.profg)
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
        self.add_prod_win.title("Emploi du Prof. {}".format(self.profg))

      
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
        #self.buve.menu.add_command(label="Quitter",command=lambda: controller.qExit())
        
        
        
    def  voir_timetable_db(self):
        
        self.cur.execute("SELECT * FROM timetable_tp  WHERE prof =?", (self.profg,))
        dbrows=self.cur.fetchall()
        ll = list(dbrows)
        
        #print('db',len(list(self.db_rows))) not work
        #print('ll',len(ll))#work سبحان الله
        
        if len(ll)>0:
            self.timetabling()
            for row in ll:
                #for j in range(1,6):
                clet = '({},{})'.format(row[1],row[2])
                #print('clet',clet)
                z =self.dict[clet]
                #print('z',z)
                if (row[1]%3==1):#(j !=3) and
                        self.cr_vars[z].set(row[-3])
                if (row[1]%3==2):
                    if row[-1]=='CM':
                        self.cr_vars[z].set('{0}-{1}-{2}-{3}'.format(row[3],row[4],row[5],row[6]))
                    else:
                        self.cr_vars[z].set('{0}-{1}-TD {3}-TP {4}'.format(row[3],row[4],row[5],row[6],row[-1]))
                if (row[1]%3==0):
                        self.cr_vars[z].set(row[-2])            
        else: 
            messagebox.showinfo("Validation info", "Emplois de Prof {} n'est pas existe".format(self.profg))
            return
        
               
            
            #print(self.cr_vars[z].get())
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
        
        self.cur.execute("SELECT module FROM timetable_tp  WHERE prof =?", (self.profg,))
        mod=self.cur.fetchall()
        if len(list(mod))!=0:
            for i in mod:
                #print(i[0])
                self.tasks.append(i[0])
                #self.left_course.append(i[0])
                
        self.cur.execute("SELECT filiere, semestre, section, groupe FROM timetable_tp  WHERE prof =?", (self.profg,))
        fss=self.cur.fetchall()
        if len(list(fss))!=0:
            for i in fss:
                #print(i[0])
                self.tasks.append('{0}-{1}-{2}-{3}'.format(i[0],i[1],i[2],i[3]))               
        
        self.left_course.append('Module -') 
        self.Day = ['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi']
        self.Time = ['09-11','11-13','15-17','17-19']         
                                        
                                    
        self.cr_vars = []
        self.dic ={}
        self.dict ={}
        z = 0
        

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
                self.left_salle.append('Salle')
                
                self.left_prof = []

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
                    self.cur.execute("SELECT filiere, semestre, section, groupe, module, prof, local FROM timetable_tp  WHERE jours = ? AND  temps = ?",
                         (Jours,temp))
                    db_rows=self.cur.fetchall()
                    try :
                        for row in db_rows:
                            if (row[5] == self.profg):
                                self.cr_vars[z].set(row[4])
                                color = self.colouring[row[4]]
                                self.w.config(bg=color)             
                    except:
                        pass

                    
                if(i%3 == 2):
                    self.cr_vars[z].set("Filière")
                    Jours = self.Day[(i-1)//3]
                    self.w = OptionMenu(self.NewWindow, self.cr_vars[z], *self.left_prof)
                    
                    
                    self.cur.execute("SELECT filiere, semestre, section, groupe, module, prof, local, groupetp FROM timetable_tp  WHERE jours = ? AND  temps = ?",
                         (Jours,temp))
                    db_rows=self.cur.fetchall()

                    for row in db_rows:
                        try:
                            if (row[5] == self.profg):
                                if row[-1]=='CM':
                                    self.cr_vars[z].set('{0}-{1}-{2}-{3}'.format(row[0],row[1],row[2],row[3]))
                                else:
                                    self.cr_vars[z].set('{0}-{1}-{2}-TD {3}-TP {4}'.format(row[0],row[1],row[2],row[3],row[-1]))
                                color = self.colouring['{0}-{1}-{2}-{3}'.format(row[0],row[1],row[2],row[3])]
                                self.w.config(bg=color)
                        except:
                            pass

                    self.w.config(width=20,height=1)
                    if(j != 3) :
                        self.w.grid(row=i,column=j)
                        
                
                if(i%3 == 0):
                    self.cr_vars[z].set("Salle")
                    self.w = OptionMenu(self.NewWindow, self.cr_vars[z], *self.left_salle)
                    Jours = self.Day[(i-1)//3]
                    self.cur.execute("SELECT filiere, semestre, section, groupe, module, prof, local FROM timetable_tp  WHERE jours = ? AND  temps = ?",
                         (Jours,temp))
                    db_rows=self.cur.fetchall()
                    
                    for row in db_rows:
                        try:
                            if (row[5] == self.profg):
                                self.w = OptionMenu(self.NewWindow, self.cr_vars[z], *self.left_salle)
                            if (row[5] == self.profg):
                                self.cr_vars[z].set(row[6])
                                color = self.colouring[row[6]]
                                self.w.config(bg=color)                                
                        except:
                            pass

                    self.w.config(width=20,height=1)
                    if(j != 3) :
                        self.w.grid(row=i,column=j)

                z = z + 1


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
                canv = canvas.Canvas("emploi/Prof. {}.pdf".format(self.profg), pagesize=landscape(A4))
                canv.setLineWidth(.3)
                canv.setFont('Helvetica', 13)
                canv.drawImage('./images/FPO.png', 50, 530, width=290, height=60)
                canv.line(50, 515,800 ,515) #coordinate sequence: (x_start, y_start, x_end, y_end)
                canv.drawString(600, 500, "Année universitaire {}".format('2021-2022'))
                canv.drawString(50, 490, "Emploi du Temps  : Prof {}".format(self.profg))
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
                        if cr == 'Module -' or cr == 'Prof' or cr == 'Salle' or cr =='Filière':
                            cr = ''
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
                subprocess.Popen(["emploi/Prof. {}.pdf".format(self.profg)],shell=True)  
  
 
                    
