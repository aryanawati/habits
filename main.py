import customtkinter as ctk
from task import Task
from datetime import datetime
from PIL import Image
import schedule
import sys
import os

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
        self.geometry("400x600")
        self.grid_columnconfigure((0, 1), weight=1)

        self.tasks = []

        self.entryframe = ctk.CTkFrame(self)
        self.entryframe.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.entryframe.grid_columnconfigure(0, weight=1, minsize=220)
        self.entryframe.grid_columnconfigure(1, weight=0, minsize=80)

        self.CTkEntry = ctk.CTkEntry(self.entryframe, placeholder_text="Enter task...", width=250)
        self.CTkEntry.grid(row=0, column=0, padx=(10,10), pady=1, sticky="ew")

        self.button = ctk.CTkButton(self.entryframe, text="Add Task", command=self.button_callback, width=50)
        self.button.grid(row=0, column=1, padx=(10,10), pady=1, sticky="e")

        self.CTkEntry.bind("<Return>", self.enter_pressed)

    def createTask(self):
        task = Task(self.CTkEntry.get())
        self.tasks.append(task)
        print(f"Task created: {task.name}")

        self.checkbox = ctk.CTkCheckBox(self, text=f"{task.name}", command=lambda task=task: self.checkbox_callback(task))
        self.streaklabel = ctk.CTkLabel(self, text=f" Streak: {task.streak}")
        self.streakImg = ctk.CTkImage(light_image=Image.open(resource_path(r"images\fire.png")),dark_image=Image.open(resource_path(r"images\fire.png")),size=(30,30))
        self.streakImgLabel = ctk.CTkLabel(self, image=self.streakImg, text="")

        task.checkbox = self.checkbox 
        task.streaklabel = self.streaklabel
        task.streakImgLabel = self.streakImgLabel
        task.row = len(self.tasks)

        self.checkbox.grid(row=len(self.tasks), column=0, padx=20, pady=(0, 20), sticky="w")
        self.streaklabel.grid(row=len(self.tasks), column=2, padx=20, pady=(0, 20), sticky="e")
        
    def streakUpdate(self, task):
        if task.streak == 0:
            task.streakStartDate = datetime.now()
            task.streak = 1
        else:
            task.streak = (datetime.now() - task.streakStartDate).days + 1
        task.streaklabel.configure(text=f"Streak: {task.streak}")
        task.streakImgLabel.grid(row=task.row, column=1, padx=20, pady=(0, 20), sticky="e")        

    def button_callback(self):
        if self.CTkEntry.get().strip() != "":
            self.createTask()
        self.CTkEntry.delete(0, ctk.END)
        print("button was clicked")

    def checkbox_callback(self, task):
        print(f"{task.name} was clicked")
        self.streakUpdate(task)

    def enter_pressed(self, event):
        self.button_callback()

app = App()
app.mainloop()