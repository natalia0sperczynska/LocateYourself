import tkinter as tk
from tkinter import PhotoImage, ttk
import customtkinter
from tkinter import messagebox
from firebase_admin import db
from matplotlib import pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pygame
pygame.mixer.init()
from Graphs.Graph import open_file, graph_distribution, graph_male_female, \
    graph_caffeine_influence_awakenings, graph_smoking_influence_sleep_efficiency, graph_sleep_efficiency_age, \
    graph_exercise_sleep_efficiency
from User.User import User


class MyCheckboxFrame(customtkinter.CTkFrame):
    """
    This is custom frame containing multiple checkboxes
    """
    def __init__(self, master,title,values):
        """
        This function initialize the checkbox frame.
        Arguments:
            master (tk.Widget): Parent widget
            title (str): Title of the frame
            values (list): List of checkbox labels
        """
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
        """
        This function gets the list of selected checkboxes.

        Returns:
            list: List of selected checkbox texts.
        """
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

    def clear(self):
        """
        This function deselects all checkboxes.
        """
        for checkbox in self.checkboxes:
            checkbox.deselect()

class MyRadiobuttonFrame(customtkinter.CTkFrame):
    """
    This represents custom frame containing multiple radio buttons.
    """
    def __init__(self, master, title, values):
        """
        Function Initialize the radio button frame.

        Arguments:
            master (tk.Widget): Parent widget.
            title (str): Title displayed at the top of the frame.
            values (list): List of values for the radio buttons.
        """
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
        """
        This function gets the list of selected radio buttons values.

        Returns:
            str: The selected value.
        """
        return self.variable.get()

    def set(self, value):
        """
        This function sets the value of the radio button group.

        Arguments:
            value (str): The selected value.
        """
        self.variable.set(value)

    def clear(self):
        """
        This function clear the selected value.
        """
        self.variable.set("")

class MySliderFrame(customtkinter.CTkFrame):
    """
    This is custom frame containing a slider with a little value display.
    """
    def __init__(self, master, title, from_, to, steps=None):
        """
        Function initialize the slider frame.
        
        Arguments:
            master (tk.Widget): Parent widget.
            title (str): Title displayed above the slider.
            from_ (float): Minimum value of the slider.
            to (float): Maximum value of the slider.
            steps (int, optional): Number of steps on the slider.
        """
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
        """
        This function updates the value of the slider.
        
        Arguments:
            value (str): Current slider value.
        """
        self.value_label.configure(text=f"{int(value)}")

    def get(self):
        """
        Function gets current value of the slider.
        
        Returns:
            float: Current value of the slider.
        """
        return self.slider.get()

    def set(self, value):
        """
        This function sets the value of the slider.
        
        Arguments:
            value (float): Value to set
        """
        self.slider.set(value)
        self.update_label(value)

    def clear(self):
        """
        FUnction resets the slider to its default position.
        """
        self.slider.set(0)
        self.value_label.configure(text="0")

class VerticalScrolledFrame(ttk.Frame):
    """
    This is frame with vertical scrollbar.
    """
    def __init__(self, parent, *args, **kw):
        """
        FUnction initialize the vertically scrollable frame.
        
        Arguments:
            parent: Parent widget.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
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
        """
        Function adjusts the scroll region when the interior is realized.

        Arguments:
            event: The event object.
        """
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        """
        Function adjusts the interior width to match the canvas width.

        Arguments:
             event: The event object.
        """

        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())

class MyFrame(customtkinter.CTkFrame):
    """
    Custom frame that gathers user input for various health and lifestyle parameters.
    """
    def __init__(self, root, tabControl):
        """
        Function initializes the frame and creates all input widgets.

        Arguments:
            root (customtkinter.CTk): Parent widget.
            tabControl (ttk.Notebook): The notebook widget to manage tabs.
        """
        super().__init__(root)
        self.root = root
        self.generatedTabs = 0
        self.tabControl=tabControl

        # name
        self.entryName = customtkinter.CTkEntry(self, placeholder_text="Enter your name")
        self.entryName.pack(pady=8, padx=8)

        # age
        self.sliderAge = MySliderFrame(self, "Age", from_=0, to=80)
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
        # music because why not
        music_button=customtkinter.CTkButton(self, text='Music', fg_color="#5a65d6", hover_color="#c8cade",text_color="white", command=self.music)
        music_button.pack(pady=8, padx=8)

    def music(self):
        """
        Function lets play a music file using pygame.
        """
        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.play(loops=0)

    def toggle_theme(self):
        """
        Function toggles the application's appearance mode between light and dark themes.
        """
        current_theme = customtkinter.get_appearance_mode().lower()
        if current_theme == "dark":
            customtkinter.set_appearance_mode("light")
            customtkinter.set_default_color_theme("blue")
        else:
            customtkinter.set_appearance_mode("dark")
            customtkinter.set_default_color_theme("dark-blue")

    def check_data(self,show_success=True):
        """
        Function validates the user input data and displays appropriate messages.

        Arguments:
            show_success (bool): Whether to show a success message on valid input.
        Returns:
            bool: True if data is valid, False otherwise.
        """
        missing_fields = []
        invalid_fields = []

        if not self.entryName.get():
            missing_fields.append("name")
        if not self.radiobutton_frame.get():
            missing_fields.append("sex")
        if self.sliderAge.get()==0:
            missing_fields.append("age")
        if self.sliderSleepHours.get()==0:
            missing_fields.append("sleep hours")
        if self.sliderTimeInBed.get()==0:
            missing_fields.append("time in bed")
        if not self.entryCaffeine.get():
            missing_fields.append("caffeine consumption")
        else:
            try:
                int(self.entryCaffeine.get())
            except ValueError:
                invalid_fields.append('caffeine consumption')

        if self.sliderSleepHours.get()>self.sliderTimeInBed.get():
            messagebox.showerror("Error", "Time in bed cannot be smaller than sleep hours")
            return False
        elif missing_fields or invalid_fields:
            error_message = ""
            if missing_fields:
                error_message += f"Missing fields: {', '.join(missing_fields)}\n"
            if invalid_fields:
                error_message += f"Invalid fields: {', '.join(invalid_fields)}"
            messagebox.showerror("Error", error_message)
            return False
        else:
            if show_success:
                messagebox.showinfo("Success", "Your data has been entered successfully!")
            return True

    def get_data(self):
        """
        Function collects and structures user input data into User object.

        Returns:
            User: An object containing the user's input data, or None if invalid.
        """
        try:
            user = User(
                name=self.entryName.get(),
                age=int(self.sliderAge.get()),
                sleep_efficiency=float(self.sliderSleepHours.get() / self.sliderTimeInBed.get()),
                smoking_status=self.checkbox_frame.get(),
                exercise=int(self.sliderExerciseFrequency.get()),
                coffein_consumption=int(self.entryCaffeine.get()),
                waking_up_during_night=int(self.sliderWakeUpTimes.get()),
                sex=self.radiobutton_frame.get()
            )
            return user
        except Exception as e:
            messagebox.showerror("Error", f"Invalid data: {e}")
            return None

    def clear(self):
        """
        Function clears all input fields and resets widgets to their default states.
        """
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
        """
        Function validates input data and generates graphs based on user input and loaded data.
        """
        if not self.check_data(show_success=False):
            messagebox.showinfo("Required data", "To see the graphs, please enter the required data.")
            return
        path_data_sleep_efficiency = "../Data/Sleep_Efficiency.csv"
        try:
            data=open_file(path_data_sleep_efficiency)
            data=data.dropna()
            if data is None:
                messagebox.showerror("Error", "No data available to generate graphs.")
                return
            self.generatedTabs += 1
            plotsFrame = customtkinter.CTkFrame(self.tabControl)
            plotsFrame.pack(expand=True, fill="both")
            self.tabControl.add(plotsFrame, text=f"Graphs{self.generatedTabs}")

            fig, axs = plt.subplots(3,2,figsize=(11, 11))
            fig.tight_layout(pad=5.0)

            ax1, ax2= axs[0]
            ax3, ax4= axs[1]
            ax5, ax6 = axs[2]
            user=self.get_data()

            graph_distribution(data, user, ax=ax1)
            graph_male_female(data,user, ax=ax2)
            graph_sleep_efficiency_age(data, user,ax=ax3)
            graph_caffeine_influence_awakenings(data, user,ax=ax4)
            graph_smoking_influence_sleep_efficiency(data, user,ax=ax5)
            graph_exercise_sleep_efficiency(data,user,ax=ax6)

            canvas = FigureCanvasTkAgg(fig, master=plotsFrame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            toolbar = NavigationToolbar2Tk(canvas, plotsFrame)
            toolbar.update()
            toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate graphs: {e}")

    def save_to_firebase(self, user):
        """
        Function saves user's data to Firebase database.'

        Arguments:
            user (User): The user data to be saved.
        """
        try:
            ref = db.reference("/users")
            ref.push({
                "name": user.name,
                "age": user.age,
                "sleep_efficiency": user.sleep_efficiency,
                "smoking_status": user.smoking_status,
                "exercise": user.exercise,
                "caffeine_consumption": user.coffein_consumption,
                "waking_up_during_night": user.waking_up_during_night,
            })
            messagebox.showinfo("Success", "Your data has been saved to Firebase")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data to Firebase: {e}")

class App(customtkinter.CTk):
    """
    Main application class for creating and managing the tkinter GUI.
    """
    def __init__(self):

        """
        Function initializes the application window, layout and tabs.
        """
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

