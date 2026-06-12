import customtkinter as ctk
from task import Task
from datetime import datetime
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x600")
        self.grid_columnconfigure((0, 1), weight=1)

        self.tasks = []

        self.CTkEntry = ctk.CTkEntry(self, placeholder_text="Enter task...")
        self.CTkEntry.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.button = ctk.CTkButton(self, text="Add Task", command=self.button_callback)
        self.button.grid(row=0, column=1, padx=20, pady=20, sticky="ew", columnspan=2)

        self.CTkEntry.bind("<Return>", self.enter_pressed)

    def createTask(self):
        task = Task(self.CTkEntry.get())
        self.tasks.append(task)
        print(f"Task created: {task.name}")

        self.checkbox = ctk.CTkCheckBox(self, text=f"{task.name}", command=lambda task=task: self.checkbox_callback(task))
        self.streaklabel = ctk.CTkLabel(self, text=f" Streak: {task.streak}")
        self.streakImg = ctk.CTkImage(light_image=Image.open(r"images\fire.png"),dark_image=Image.open(r"images\fire.png"),size=(30,30))
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