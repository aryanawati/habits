import customtkinter as ctk
from task import Task
import task
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x600")
        self.grid_columnconfigure((0, 1), weight=1)

        self.tasks = []

        self.CTkEntry = ctk.CTkEntry(self, placeholder_text="Enter task...")
        self.CTkEntry.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.button = ctk.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=0, column=1, padx=20, pady=20, sticky="ew", columnspan=2)

    def createTask(self):
        task = Task(self.CTkEntry.get())
        self.tasks.append(task)
        print(f"Task created: {task.name}")

        self.checkbox = ctk.CTkCheckBox(self, text=f"{task.name}", command=lambda task=task: self.checkbox_callback(task))

        task.checkbox = self.checkbox
        self.tasks.append(task)

        self.checkbox.grid(row=len(self.tasks), column=0, padx=20, pady=(0, 20), sticky="w")

    # def streakUpdate(self, index):
         


    def button_callback(self):
        self.createTask()
        print("button was clicked")
    
    def checkbox_callback(self, task):
        print(f"{task.name} was clicked")

app = App()
app.mainloop()