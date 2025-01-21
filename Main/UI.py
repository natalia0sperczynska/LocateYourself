from tkinter import IntVar, mainloop, W, StringVar, Toplevel
from venv import create

#Gówno dla mnie bo python nie umiał znaleźć biblioteki wykomentujcie
import os
os.environ['TCL_LIBRARY'] = r'C:/Users/tomek/AppData/Local/Programs/Python/Python313/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = r'C:/Users/tomek/AppData/Local/Programs/Python/Python313/tcl/tk8.6'


import customtkinter
from customtkinter import *
from tkinter import messagebox
from FirestoreIntegration import initialize_firestore, write_user_to_firestore

# Initialize Firestore globally
db = initialize_firestore()

class MyCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master,title,values):
        super().__init__(master)
        self.values = values
        self.title=title
        self.checkboxes = []

        self.title_label = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title_label.pack(pady=9, padx=9)

        for i, value in enumerate(self.values):
            checkbox= customtkinter.CTkCheckBox(self, text=value)
            checkbox.pack(pady=(10, 8))
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

class MyRadiobuttonFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value="")

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = customtkinter.CTkLabel(self, text="Hello user!")
        self.label.pack(pady=12, padx=10)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("800x600")
        self.title("LocateYourself")
        self.grid_columnconfigure((0, 1), weight=1)
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.label = customtkinter.CTkLabel(self, text="Age")
        self.label.pack(pady=5, padx=5)
        self.sliderAge = customtkinter.CTkSlider(self, command=self.slider_callback, from_=0, to=100)
        self.sliderAge.pack(pady=8, padx=8)
        self.sliderAge.set(0)
        self.labelAge = customtkinter.CTkLabel(self, text="")
        self.labelAge.pack(pady=8, padx=8)

        self.my_frame1= MyFrame(self)
        self.my_frame1.pack(pady=10, padx=10)
        self.my_frame1.configure(fg_color="transparent")

        self.entryName = customtkinter.CTkEntry(self, placeholder_text="Enter your name")
        self.entryName.pack(pady=8, padx=8)

        self.checkbox_frame = MyCheckboxFrame(self,"Check the box if you are a smoker", values=["I smoke"])
        self.checkbox_frame.pack(pady=8, padx=8)

        self.radiobutton_frame = MyRadiobuttonFrame(self, "Sex",values=["Male", "Female", "Other"])
        self.radiobutton_frame.pack(pady=8, padx=8)

        self.button = customtkinter.CTkButton(self, text="Submit", command=self.check_data)
        self.button.pack(pady=12, padx=10)

        self.button = customtkinter.CTkButton(self, text="Clear", command=self.clear)
        self.button.pack(pady=12, padx=10)

        self.button = customtkinter.CTkButton(self, text="Generate Graphs", command=self.button_callback)
        self.button.pack(pady=12, padx=10)

    def button_callback(self):
        print("checked checkboxes:", self.checkbox_frame.get())
        print("radiobutton_frame:", self.radiobutton_frame.get())

    def slider_callback(self, value):
        self.labelAge.configure(text=int(value))

    def check_data(self):
        if self.entryName.get() and self.radiobutton_frame.get():
            messagebox.showinfo("Success", "Your data has been entered")
            user = self.create_user()
            user_data = {
                "name": user.name,
                "age": user.age,
                "smoking_status": user.smoking_status,
                "exercise": user.exercise,
                "coffein_consumption": user.coffein_consumption,
                "waking_up_during_night": user.waking_up_during_night,
                "sleep_efficiency": user.sleep_efficiency_calculator(),
            }
            # Save to Firestore
            write_user_to_firestore(db, user_data)
        if not self.entryName.get():
            messagebox.showerror("Error", "Please enter your name")
        if not self.radiobutton_frame.get():
            messagebox.showerror("Error", "Please enter sex")
        if not self.sliderAge.get():
            messagebox.showerror("Error", "Please enter age")
        if not self.checkbox_frame.get() and not self.radiobutton_frame.get() and not self.sliderAge.get():
            messagebox.showerror("Error", "Please enter your data")

    def generate_graphs(self):
        print("Graphs")
        graph_window = Toplevel(app)
        graph_window.title("Graphs")

    def clear(self):
        self.labelAge.configure(text="")
        self.sliderAge.set(0)
        self.entryName.delete(0, END)

    def click(self):
        pass

    #def create_user(self):
    #   return User(self.entryName.get(),self.sliderAge.get(), self.checkbox_frame.get(), self.radiobutton_frame.get())

if __name__ == "__main__":
    app=App()
    app.mainloop()
