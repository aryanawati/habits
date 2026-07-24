import customtkinter as ctk
import tkinter as tk
from task import Task
from datetime import datetime
from PIL import Image
import schedule
import sys
import os
import getpass
import random

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("habits")
        self.geometry("400x650")
        self.grid_columnconfigure((0, 1), weight=1)

        username = getpass.getuser()

        self.tasks = []
        self.intromessages = [
            f"I've been waiting, {username}.",
            f"Welcome back... {username}.",
            f"Let's make today better than yesterday.",
            f"Ready to continue where we left off?",
            f"Today is a fresh start.",
            f"Consistency beats motivation, {username}!"
        ]

        self.titleframe = ctk.CTkFrame(self)
        self.titleframe.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        self.titlelabel = ctk.CTkLabel(self.titleframe, text=f"Habits", font=("SF Pro Display", 28, "bold"))
        self.titlelabel.grid(row=0, column=0, padx=20, pady=(20,10), sticky="w")
        self.namelabel = ctk.CTkLabel(self.titleframe, text=f"{random.choice(self.intromessages)}", font=("SF Pro Display", 14))
        self.namelabel.grid(row=1,column=0, padx=20, pady=(5,20), sticky="w")

        self.grid_rowconfigure(0, weight=0)  # title
        self.grid_rowconfigure(1, weight=0)  # add habit
        self.grid_rowconfigure(2, weight=1) # task frame expands

        self.entryframe = ctk.CTkFrame(self)
        self.entryframe.grid(row=1, column=0, padx=20, pady=(1,20), sticky="ew", columnspan=2)

        self.entryframe.grid_columnconfigure(0, weight=1, minsize=220)
        self.entryframe.grid_columnconfigure(1, weight=0, minsize=80)

        self.addHabitFrame = ctk.CTkFrame(self.entryframe)
        self.addHabitFrame.grid(row=0, column=0, padx=10, pady =(10,0), sticky="ew", columnspan=2)
        self.addHabitLabel = ctk.CTkLabel(self.addHabitFrame, text=f"Add a Habit", font=("SF Pro Display", 12), anchor="center")
        self.addHabitLabel.grid(row=0, column=0, padx=10, pady=5)
        self.addHabitFrame.grid_columnconfigure(0, weight=1)

        self.CTkEntry = ctk.CTkEntry(self.entryframe, placeholder_text="Enter task...", width=250, height=20, font=("SF Pro Display", 20))
        self.CTkEntry.grid(row=1, column=0, padx=(10,10), pady=(20,20), sticky="ew")

        self.button = ctk.CTkButton(self.entryframe, text="Add Task", command=self.button_callback, width=20, height=20 , font=("SF Pro Display", 20))
        self.button.grid(row=1, column=1, padx=(10,10), pady=(20,20), sticky="e")
        self.CTkEntry.bind("<Return>", self.enter_pressed)

        self.streaklistFrame = ctk.CTkScrollableFrame(self, scrollbar_button_color="gray25", scrollbar_button_hover_color="gray35")
        self.streaklistFrame.grid(row=2, column=0, padx=20, pady=(1,20), sticky="nsew", columnspan=2)
        self.noHabitsLabel = ctk.CTkLabel(self.streaklistFrame, text=f"No Habits Yet.. Add One?", font=("SF Pro Display", 12), anchor="center")
        self.noHabitsLabel.grid(row=0, column=0, padx = 20, pady = 20, sticky="ew")
        self.streaklistFrame.grid_columnconfigure(0, weight=1)
        self.streaklistFrame.grid_rowconfigure(2, weight=1)

    def createTask(self):
        task = Task(self.CTkEntry.get())
        self.tasks.append(task)
        print(f"Task created: {task.name}")

        self.taskframe = ctk.CTkFrame(self.streaklistFrame, fg_color=("white", "#191919"))
        self.noHabitsLabel.grid_remove()

        fire_path = resource_path(os.path.join("images", "fire.png"))
        notfire_path = resource_path(os.path.join("images", "grayfire.png"))
        self.checkbox = ctk.CTkCheckBox(self.taskframe, text="", command=lambda task=task: self.checkbox_callback(task), width=24)
        self.checkboxlabel = ctk.CTkLabel(self.taskframe, text=f"{task.name}", font=("SF Pro Display", 20), anchor="w", justify="left", wraplength=180)
        self.streaklabel = ctk.CTkLabel(self.taskframe, text=f"{task.streak}", font=("SF Pro Display", 20))
        self.streakImg = ctk.CTkImage(light_image=Image.open(fire_path),dark_image=Image.open(fire_path),size=(30,30))
        self.streakImgLabel = ctk.CTkLabel(self.taskframe, image=self.streakImg, text="")
        self.streakImgNot = ctk.CTkImage(light_image=Image.open(notfire_path),dark_image=Image.open(notfire_path),size=(30,30))
        self.streakImgNotLabel = ctk.CTkLabel(self.taskframe, image=self.streakImgNot, text="")

        task.checkbox = self.checkbox
        task.streaklabel = self.streaklabel
        task.streakImgLabel = self.streakImgLabel
        task.streakImgNotLabel = self.streakImgNotLabel
        task.row = len(self.tasks)

        self.taskframe.grid(row=len(self.tasks) + 1, column=0, padx=10, pady=5, sticky="ew", columnspan=2)
        self.checkbox.grid(row=0, column=0, padx=(15,10), pady=15, sticky="w")
        self.checkboxlabel.grid(row=0, column=1, padx=5, pady=15, sticky="w")
        self.streaklabel.grid(row=0, column=4, padx=(10, 15), pady=15, sticky="e")
        self.streakImgNotLabel.grid(row=0, column=3, padx=0, pady=0, sticky="e")

        self.taskframe.grid_columnconfigure(0, weight=0) #Checkbox
        self.taskframe.grid_columnconfigure(1, weight=0) #Task Name
        self.taskframe.grid_columnconfigure(2, weight=1) #Spacer
        self.taskframe.grid_columnconfigure(3, weight=0) #Fire
        self.taskframe.grid_columnconfigure(4, weight=0) #Streak Number




        
    def streakUpdate(self, task):
        if task.checkbox.get():
            if task.streak == 0:
                task.streakStartDate = datetime.now()
                task.streak = 1
            else:
                task.streak = (datetime.now() - task.streakStartDate).days + 1    
            task.streakImgNotLabel.grid_remove()
            task.streakImgLabel.grid(row=0, column=3, padx=0, pady=0, sticky="e")
        else:
            if task.streak != 0:
                task.streak -=1
                task.streakImgNotLabel.grid(row=0, column=3, padx=0, pady=0, sticky="e")  
            task.streakImgLabel.grid_remove()
            task.streakImgNotLabel.grid(row=0, column=3, padx=0, pady=0, sticky="e") 
        task.streaklabel.configure(text=f"{task.streak}")   


    def button_callback(self):
        if self.CTkEntry.get().strip() != "":
            self.createTask()
        self.CTkEntry.delete(0, ctk.END)

    def checkbox_callback(self, task):
        print(f"{task.name} was clicked")
        self.streakUpdate(task)

    def enter_pressed(self, event):
        self.button_callback()

app = App()
app.mainloop()