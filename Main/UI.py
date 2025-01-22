from tkinter import IntVar, mainloop, W, StringVar, Toplevel, PhotoImage
from venv import create

import customtkinter
from customtkinter import *
from tkinter import messagebox


#from Main.User import User


#from Main.Main import generate_graphs

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

    def clear(self):
        for checkbox in self.checkboxes:
            checkbox.deselect()

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

    def clear(self):
        self.variable.set("")

class MySliderFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, from_, to, steps=None):
        super().__init__(master)
        self.title = title

        self.title_label = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title_label.pack(pady=5, padx=5)

        self.value_label = customtkinter.CTkLabel(self, text=" ", fg_color="gray20", corner_radius=6)
        self.value_label.pack(pady=5, padx=5)

        self.slider = customtkinter.CTkSlider(
            self, from_=from_, to=to, number_of_steps=steps, command=self.update_label
        )
        self.slider.pack(pady=8, padx=8)

    def update_label(self, value):
        self.value_label.configure(text=f"{int(value)}")

    def get(self):
        return self.slider.get()

    def set(self, value):
        self.slider.set(value)
        self.update_label(value)

    def clear(self):
        self.slider.set(0)
        self.value_label.configure(text="0")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("900x1200")
        self.title("LocateYourself")
        icon = PhotoImage(file="../Images/icon.png")
        self.iconphoto( True, icon)
        self.grid_columnconfigure((0, 1), weight=1)
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        # name
        self.entryName = customtkinter.CTkEntry(self, placeholder_text="Enter your name")
        self.entryName.pack(pady=8, padx=8)

        #age
        self.sliderAgeFrame = MySliderFrame(self, "Age", from_=0, to=100)
        self.sliderAgeFrame.pack(pady=8, padx=8)

        #smoker status
        self.checkbox_frame = MyCheckboxFrame(self,"Check the box if you are a smoker", values=["I smoke"])
        self.checkbox_frame.pack(pady=8, padx=8)

        #sex
        self.radiobutton_frame = MyRadiobuttonFrame(self, "Sex",values=["Male", "Female", "Other"])
        self.radiobutton_frame.pack(pady=8, padx=8)

        #sleep per day
        self.sliderSleepHoursFrame = MySliderFrame(self, "Hours of sleep per day", from_=0, to=24, steps=24)
        self.sliderSleepHoursFrame.pack(pady=8, padx=8)

        #time in bed
        self.sliderTimeInBedFrame = MySliderFrame(self, "Time spent in bed (hours)", from_=0, to=24, steps=24)
        self.sliderTimeInBedFrame.pack(pady=8, padx=8)

        #caffein
        self.entryCaffeine = customtkinter.CTkEntry(self, placeholder_text="Caffeine consumption (mg/day)")
        self.entryCaffeine.pack(pady=8, padx=8)
        self.labelInfo= customtkinter.CTkLabel(self, text="(One coffee around 65mg)")
        self.labelInfo.pack(pady=8, padx=8)


        #exercise
        self.sliderExerciseFrequencyFrame = MySliderFrame(self, "Exercise frequency per week (times)", from_=0, to=14,steps=14)
        self.sliderExerciseFrequencyFrame.pack(pady=8, padx=8)

        #times woke up during the day
        self.sliderWakeUpTimesFrame = MySliderFrame(self, "How many times you woke up during the night", from_=0, to=10,steps=10)
        self.sliderWakeUpTimesFrame.pack(pady=8, padx=8)

        #submit button
        self.button = customtkinter.CTkButton(self, text="Submit", fg_color="#5a65d6",hover_color="#c8cade",text_color="white",command=self.check_data)
        self.button.pack(pady=12, padx=10)

        #clear button
        self.button = customtkinter.CTkButton(self, text="Clear",fg_color="#5a65d6",hover_color="#c8cade",text_color="white", command=self.clear)
        self.button.pack(pady=12, padx=10)

        #generate garph button
        self.button = customtkinter.CTkButton(self, text="Generate Graphs",fg_color="#5a65d6",hover_color="#c8cade",text_color="white", command=self.generate_graphs)
        self.button.pack(pady=12, padx=10)


    def button_callback(self):
        print("checked checkboxes:", self.checkbox_frame.get())
        print("radiobutton_frame:", self.radiobutton_frame.get())

    # def slider_callback(self, value):
    #     self.labelAge.configure(text=int(value))

    def check_data(self):
        if self.entryName.get() and self.radiobutton_frame.get():
            messagebox.showinfo("Success", "Your data has been entered")
            #tutaj będzie ładowanie tyvh danych ale idk jak to zrobic jeszcze
            #app.create_user()
        if not self.entryName.get():
            messagebox.showerror("Error", "Please enter your name")
        if not self.radiobutton_frame.get():
            messagebox.showerror("Error", "Please enter sex")
        if not self.sliderAge.get():
            messagebox.showerror("Error", "Please enter age")
        if not self.checkbox_frame.get() and not self.radiobutton_frame.get() and not self.sliderAge.get():
            messagebox.showerror("Error", "Please enter your data")

    def clear(self):
        self.entryName.delete(0, "end")
        self.checkbox_frame.clear()
        self.radiobutton_frame.clear()
        self.sliderAge.set(0)
        self.sliderTimeInBed.set(0)
        self.sliderSleepHours.set(0)
        self.entryCaffeine.delete(0, "end")
        self.sliderExerciseFrequency.set(0)
        self.sliderWakeUpTimes.set(0)

    def generate_graphs(self):
        new_window=customtkinter.CTk()
        new_window.title("Graphs")


    # def create_user(self):
    #     return User(self.entryName.get(),self.sliderAge.get(), self.checkbox_frame.get(), self.radiobutton_frame.get())

if __name__ == "__main__":
    app=App()
    app.mainloop()

