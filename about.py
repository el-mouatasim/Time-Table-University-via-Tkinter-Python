# importing modules
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import time
import os
import sys
from tkinter import WORD
# print(sys.path)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main_menu as main_menu
from theme_engine import ThemeEngine


class AboutWindow(ttk.Frame, ThemeEngine):
    """Settings / Extras Page"""
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        # Initializing Theme Engine
        ThemeEngine.__init__(self)

        self.master = master
        # Setting Window Title
        master.title("Management System\ About")  
        
        #=========================  Main Background Frame =====================#
        
        win_width, win_height = 1200, 500
        self.bg_frame = ttk.Frame(master, width=win_width, height=win_height,
                                 style="mainframe.TFrame")
        self.bg_frame.place(x=0, y=0)

        #========================  Title Frame  ===============================#

        title_frame = ttk.Frame(self.bg_frame)
        title_frame.place(x=20, y=20, relwidth=0.97)
        # Back Button
        self.back_btn_img = tk.PhotoImage(file='images/back_button.png')
        back_btn = tk.Button(title_frame, image=self.back_btn_img, bd=0,
                             bg=self.button_bg, activebackground=self.button_bg,
                            command=lambda: master.switch_frame(main_menu.MainMenuWindow, self.bg_frame))
        back_btn.place(relwidth=0.15, relheight=1)
        # Title Label
        title_label = ttk.Label(title_frame, text="About us", font="Arial 60 bold",
                                 foreground='#22d3fe')
        title_label.pack()
        # Date and Time Label
        date_string = time.strftime("%a,%d/%b/%y")
        time_string = time.strftime("%I:%M %p")
        date_label = ttk.Label(title_frame, text=date_string, font="Arial 18 bold")
        date_label.place(x=900, y=15)
        time_label = ttk.Label(title_frame, text=time_string, font="Arial 18 bold")
        time_label.place(x=950, y=50)



        #===============  Entry Frame / Down Frame 2 =======================#

        ch_entry_frame = ttk.Frame(self.bg_frame)
        ch_entry_frame.place(x=20, y=120,  height=350, relwidth=0.97)
        
        
        # Heading Label
        heading_label2 = ttk.Label(ch_entry_frame, text="Informations", 
                                 font="Arial 20 bold", foreground='#4eacfe')
        heading_label2.pack(side='top', pady=10)
        

        message ='''
        This is a version 1 of Karama application created by Prof. Dr. Abdelkrim El Mouatasim, for more informations please visite:\n
        https://www.researchgate.net/profile/Abdelkrim-El-Mouatasim\n
        https://github.com/el-mouatasim\n
        Email: a.mouatasim@gmail.com
        '''

        text_box = tk.Text(ch_entry_frame, wrap='word', height=300, width=200)
        text_box.pack(expand=True)
        text_box.insert('end', message)
        text_box.config(state='disabled')        
        
if __name__ == "__main__":
    master = tk.Tk()
    # Setting Window Width and height        
    win_width, win_height = 1340, 680
    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()
    x = int((screen_width/2) - (win_width/2))
    y = int((screen_height/2) - (win_height/2)) - 15
    master.geometry(f'{win_width}x{win_height}+{x}+{y}')
    master.resizable(0,0) # Disabling resize
    
    frame = ExtrasWindow(master).pack()
    master.mainloop()
