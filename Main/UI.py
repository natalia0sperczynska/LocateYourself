import tkinter as tk
from tkinter import IntVar, mainloop, W, StringVar, Toplevel, PhotoImage, ttk
from tkinter.ttk import Scrollbar, Frame, Notebook
import customtkinter
from tkinter import messagebox
from firebase_admin import db
from matplotlib import pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


from Graphs.Main import open_file, distribution, graph_male_female, age_distribution_sleep_efficiency1, \
    graph_caffeine_influence_awakenings,graph_smoking_influence_sleep_efficiency
from User.User import User
from firebase.firebase import initialize_firebase


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

class VerticalScrolledFrame(ttk.Frame):
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                                yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=self.canvas.yview)

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.interior = ttk.Frame(self.canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=tk.NW)
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)

    def _configure_interior(self, event):
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, root, tabControl):
        super().__init__(root)
        self.root = root
        self.generatedTabs = 0
        self.tabControl=tabControl

        # name
        self.entryName = customtkinter.CTkEntry(self, placeholder_text="Enter your name")
        self.entryName.pack(pady=8, padx=8)

        # age
        self.sliderAge = MySliderFrame(self, "Age", from_=0, to=100)
        self.sliderAge.pack(pady=8, padx=8)

        # smoker status
        self.checkbox_frame = MyCheckboxFrame(self, "Check the box if you are a smoker", values=["I smoke"])
        self.checkbox_frame.pack(pady=8, padx=8)

        # sex
        self.radiobutton_frame = MyRadiobuttonFrame(self, "Sex", values=["Male", "Female"])
        self.radiobutton_frame.pack(pady=8, padx=8)


        # sleep per day
        self.sliderSleepHours = MySliderFrame(self, "Hours of sleep per day", from_=0, to=24, steps=24)
        self.sliderSleepHours.pack(pady=8, padx=8)

        # time in bed
        self.sliderTimeInBed = MySliderFrame(self, "Time spent in bed (hours)", from_=0, to=24, steps=24)
        self.sliderTimeInBed.pack(pady=8, padx=8)

        # caffein
        self.entryCaffeine = customtkinter.CTkEntry(self, placeholder_text="Caffeine consumption (mg/day)")
        self.entryCaffeine.pack(pady=8, padx=8)
        self.labelInfo = customtkinter.CTkLabel(self, text="(One coffee around 65mg)")
        self.labelInfo.pack(pady=8, padx=8)

        # exercise
        self.sliderExerciseFrequency = MySliderFrame(self, "Exercise frequency per week (times)", from_=0, to=14,
                                                     steps=14)
        self.sliderExerciseFrequency.pack(pady=8, padx=8)

        # times woke up during the day
        self.sliderWakeUpTimes = MySliderFrame(self, "How many times you woke up during the night", from_=0, to=10,
                                               steps=10)
        self.sliderWakeUpTimes.pack(pady=8, padx=8)

        # submit button
        self.button = customtkinter.CTkButton(self, text="Submit", fg_color="#5a65d6", hover_color="#c8cade",
                                              text_color="white", command=self.check_data)
        self.button.pack(pady=12, padx=10)

        # clear button
        self.button = customtkinter.CTkButton(self, text="Clear", fg_color="#5a65d6", hover_color="#c8cade",
                                              text_color="white", command=self.clear)
        self.button.pack(pady=12, padx=10)

        # generate garph button
        self.button = customtkinter.CTkButton(self, text="Generate Graphs", fg_color="#5a65d6", hover_color="#c8cade",
                                              text_color="white", command=self.generate_graphs)
        self.button.pack(pady=12, padx=10)

        #light or dar mode because why not
        toggle_button = customtkinter.CTkButton(
            self, text="Change Theme",fg_color="#5a65d6", hover_color="#c8cade",text_color="white", command=self.toggle_theme
        )
        toggle_button.pack(pady=8, padx=8)

    def toggle_theme(self):
        current_theme = customtkinter.get_appearance_mode().lower()
        if current_theme == "dark":
            customtkinter.set_appearance_mode("light")
            customtkinter.set_default_color_theme("blue")
        else:
            customtkinter.set_appearance_mode("dark")
            customtkinter.set_default_color_theme("dark-blue")

    def check_data(self):
        if self.entryName.get() and self.radiobutton_frame.get():
            messagebox.showinfo("Success", "Your data has been entered")
            self.get_data()
        if not self.entryName.get():
            messagebox.showerror("Error", "Please enter your name")
        if not self.radiobutton_frame.get():
            messagebox.showerror("Error", "Please enter sex")
        if not self.sliderAge.get():
            messagebox.showerror("Error", "Please enter age")
        if not self.checkbox_frame.get() and not self.radiobutton_frame.get() and not self.sliderAge.get():
            messagebox.showerror("Error", "Please enter your data")

            user = self.get_data()
            self.save_to_firebase(user)

# nowe zmieione
    def get_data(self):
        """Collect user input into a User object."""
        try:
            user = User(
                name=self.entryName.get(),
                age=int(self.sliderAge.get()),
                sleep_efficeincy=float(self.sliderSleepHours.get() / self.sliderTimeInBed.get()),
                smoking_status=self.checkbox_frame.get(),
                exercise=int(self.sliderExerciseFrequency.get()),
                coffein_consumption=int(self.entryCaffeine.get()) if self.entryCaffeine.get() else 0,
                waking_up_during_night=int(self.sliderWakeUpTimes.get()),
                sex=self.radiobutton_frame.get()
            )
            return user
        except Exception as e:
            messagebox.showerror("Error", f"Invalid data: {e}")
            return None

    def clear(self):
        self.entryName.delete(0, "end")
        self.checkbox_frame.clear()
        self.radiobutton_frame.clear()
        self.sliderAge.clear()
        self.sliderTimeInBed.clear()
        self.sliderSleepHours.clear()
        self.entryCaffeine.delete(0, "end")
        self.sliderExerciseFrequency.clear()
        self.sliderWakeUpTimes.clear()

    def generate_graphs(self):
        path_data_sleep_efficiency = "../Data/Sleep_Efficiency.csv"
        data = open_file(path_data_sleep_efficiency)
        if data is None:
            messagebox.showerror("Error", "No data available to generate graphs.")
            return
        self.generatedTabs += 1
        plotsFrame = customtkinter.CTkFrame(self.tabControl)
        plotsFrame.pack(expand=True, fill="both")
        self.tabControl.add(plotsFrame, text=f"Graphs{self.generatedTabs}")

        fig, axs = plt.subplots(3,2,figsize=(12, 10))
        fig.tight_layout(pad=5.0)

        ax1, ax2= axs[0]
        ax3, ax4= axs[1]
        ax5, ax6 = axs[2]
        user=self.get_data()

        distribution(data,user,ax=ax1)
        graph_male_female(data,user, ax=ax2)
        age_distribution_sleep_efficiency1(data, ax=ax3)
        graph_caffeine_influence_awakenings(data, ax=ax4)
        graph_smoking_influence_sleep_efficiency(data, ax=ax5)
        graph_caffeine_influence_awakenings(data, ax=ax6)

        canvas = FigureCanvasTkAgg(fig, master=plotsFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, plotsFrame)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    # nowe
    def save_to_firebase(self, user):

        try:
            ref = db.reference("/users")
            ref.push({
                "name": user.name,
                "age": user.age,
                "sleep_efficiency": user.sleep_efficeincy,
                "smoking_status": user.smoking_status,
                "exercise": user.exercise,
                "caffeine_consumption": user.coffein_consumption,
                "waking_up_during_night": user.waking_up_during_night,
            })
            messagebox.showinfo("Success", "Your data has been saved to Firebase")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data to Firebase: {e}")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x1000")
        self.title("LocateYourself")
        customtkinter.set_default_color_theme("blue")
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        icon = PhotoImage(file="../Images/icon.png")
        self.iconphoto(True, icon)
        self.grid_columnconfigure((0, 1), weight=1)

        self.tabControl = ttk.Notebook(self)
        self.tabControl.pack(expand=True, fill="both")

        scrollable_frame = VerticalScrolledFrame(self.tabControl)
        scrollable_frame.pack(expand=True, fill="both")

        input_frame = MyFrame(scrollable_frame.interior, self.tabControl)
        input_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.tabControl.add(scrollable_frame, text="Input")


if __name__ == "__main__":
    #initialize_firebase()

    app=App()
    app.mainloop()

