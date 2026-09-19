from tkinter import *

from tkinter import messagebox

from tkinter import ttk
from tkinter.ttk import Combobox

from Addtional_features import myentry

import sqlite3

import sys
import os 
from theme_engine import ThemeEngine

import datetime

import subprocess
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph, LongTable, PageTemplate, SimpleDocTemplate
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import  TA_LEFT, TA_CENTER
from reportlab.lib.units import  cm
from reportlab.platypus import Frame as Frame_rep

sys.path.append(os.path.abspath('../'))

class RSalWindow(ThemeEngine):
    def __init__(self, master):
        ThemeEngine.__init__(self)

        # Creating Top-level window & Setting Window Width and height        
        self.add_prod_win = Toplevel(master)
        win_width, win_height = 1280, 700
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = int((screen_width/2) - (win_width/2))  - 7
        y = int((screen_height/2) - (win_height/2)) - 35
        self.add_prod_win.geometry(f'{win_width}x{win_height}+{x}+{y}')
        self.add_prod_win.resizable(0,0) # Disabling resize
        # Forcing Top-level window to stay on Top
        #self.add_prod_win.attributes('-topmost', 'true')
        # Setting Top Level Window Title
        self.add_prod_win.title("TT Salles")
        
        self.base = sqlite3.connect("UTTMA_FPO.db")
        self.cur = self.base.cursor()
        self.datex=str(datetime.datetime.now().strftime("%d-%m-%Y"))
        # heading
        heading_label = Label(self.add_prod_win, text="---------  SALLE/AMPHI  LIBRE---------",font=('Orbitron',15),bg="black",fg="white")
        heading_label.pack(fill=X)



        black_space = Label(self.add_prod_win, text="\n\n")
        black_space.pack()

        # form Design

        top_frame = Frame(self.add_prod_win,width=600, height=130)
        top_frame.place(x=50,y=50)

        # Name Label
        fname_label = Label(top_frame, text="Jour : ", font=('Orbitron', 20))
        lname_label = Label(top_frame, text="Horaire : ", font=('Orbitron', 20))
        self.dayr = Combobox(top_frame, width=10)
        self.dayr['values'] = ('', 
                           'Lundi',
                           'Mardi',
                           'Mercredi',
                           'Jeudi',
                           'Vendredi',
                           'Samedi')
        self.dayr.current(0)  # set the selected item

        self.timer = Combobox(top_frame, width=10)
        self.timer['values'] = ('', 
                           '09-11',
                           '11-13',
                           '15-17',
                           '17-19')
        self.timer.current(0)  # set the selected item        

        fname_label.grid(row=0, column=0, padx=15, pady=10, sticky=E)
        lname_label.grid(row=1, column=0, padx=15, pady=10, sticky=E)
        self.dayr.grid(row=0, column=1, pady=10, ipady=5, ipadx=60)
        self.timer.grid(row=1, column=1, pady=10, ipady=5, ipadx=60)

        # Proceed Button
        Button(self.add_prod_win, text="PROCEED", width=10, bg="#0000b3", fg='White', font=('ARIAL BLACK', 15),
                    relief=RAISED, command=self.click_proceed).place(x=100,y=180)

        Button(self.add_prod_win, text="Search all", width=10, bg="#0000b3", fg='White', font=('ARIAL BLACK', 15),
                    relief=RAISED, command=self.click_search_all).place(x=100,y=230)

        Button(self.add_prod_win, text="Print", width=10, bg="#0000b3", fg='White', font=('ARIAL BLACK', 15),
                    relief=RAISED, command=self.print).place(x=300,y=230)
        
        mFrame = Frame(self.add_prod_win,width=800, height=600)
        mFrame.place(x=50,y=300)

        scrollbarx = Scrollbar(mFrame, orient=HORIZONTAL)
        scrollbary = Scrollbar(mFrame, orient=VERTICAL)
        self.tree = ttk.Treeview(mFrame, columns=('Jour', 'Horaire', 'Local'), 
        selectmode="browse", height=18,yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=150)
        self.tree.column('#2', stretch=NO, minwidth=0, width=150)
        self.tree.column('#3', stretch=NO, minwidth=0, width=150)
        self.tree.heading('Jour', text="Jour", anchor=W)
        self.tree.heading('Horaire', text="Horaire", anchor=W)
        self.tree.heading('Local', text="Local", anchor=W)
        self.tree.grid(row=1, column=0, sticky="W")
        scrollbary.config(command=self.tree.yview)
        scrollbarx.grid(row=2, column=0, sticky="we")
        scrollbarx.config(command=self.tree.xview)
        scrollbary.grid(row=1, column=1, sticky="ns", pady=30)

    def click_proceed(self):
        self.list_salle=[]
        self.cur.execute("select nom from salle")
        li2=self.cur.fetchall() 
        for ii in li2:
            self.list_salle.append(ii[0])

        self.cur.execute("SELECT local FROM timetable_tp  WHERE jours = ? AND  temps = ?",(self.dayr.get(),self.timer.get()))
        db_rows=self.cur.fetchall()
        if len(db_rows) > 0:
            for row in db_rows:
                #print(row[0])
                if row[0] != 'Salle' and row[0] in self.list_salle:
                    self.list_salle.remove(row[0])

        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        for i in range(len(self.list_salle)):
            self.tree.insert('', 'end', values=(self.dayr.get(),self.timer.get(),self.list_salle[i]))
        
    def click_search_all(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        for day in ['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi']:
            for time in ['09-11','11-13','15-17','17-19']:
                self.list_salle=[]
                self.cur.execute("select nom from salle")
                li2=self.cur.fetchall() 
                for ii in li2:
                    self.list_salle.append(ii[0])
                self.list_salle.remove('AMPHI A Com')
                    
                self.cur.execute("SELECT local FROM timetable_tp  WHERE jours = ? AND  temps = ?",(day,time))
                db_rows=self.cur.fetchall()
                if len(db_rows) > 0:
                    for row in db_rows:
                        if row[0] != 'Salle' and row[0] in self.list_salle:
                            self.list_salle.remove(row[0])
                            
                if day == 'Samedi' and (time == '15-17' or  time =='17-19'):
                    pass
                else:
                    for i in range(len(self.list_salle)):
                        self.tree.insert('', 'end', values=(day,time,self.list_salle[i]))

    def print(self):
       if messagebox.askyesno("Alerte!","Imprimer cette salles?")== True:
            styles = getSampleStyleSheet()
            styleN = styles["BodyText"]
            #used alignment if required
            styleN.alignment = TA_LEFT
            styleBH = styles["Normal"]
            styleBH.alignment = TA_CENTER
            elements = []
            doc = SimpleDocTemplate("emploi/Salles-libre.pdf", pagesize=portrait(A4))
 
            elements.append(Paragraph("FPO le : {}".format(self.datex),styleN))

            elements.append(Paragraph("Salle et Amphi libre:",styleBH))
            
            data = [['Jour', 'Horaire','Salle/Amphi']]
            x=self.tree.get_children()
            for i in x:
                l=self.tree.item(i)
                data.append(l['values'])

            ####
            t = LongTable(data, (3.5*cm,3.5*cm,4*cm))
            t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))
            data_len = len(data)
            
            for each in range(data_len):
                if each == 0:
                    bg_color = colors.lightgrey
                else:
                     bg_color = colors.whitesmoke   
            
                t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))
            
            elements.append(t)
            frame = Frame_rep(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 2 * cm, id='normal')
            template = PageTemplate(id='longtable', frames=frame)
            doc.addPageTemplates([template])
            doc.build(elements)
            ###
            subprocess.Popen(["emploi\Salles-libre.pdf"],shell=True)


