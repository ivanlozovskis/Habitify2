import tkinter as tk
from dev import calculate_box_coordinates as calc, timepassed
from tkinter import simpledialog
from datetime import datetime
from datetime import timedelta
from tkinter import messagebox, ttk
from Windows import stats
from functional import get_current_streaks
import database as db
import hmtodb




class HabitTrackerGUI:
    def __init__(self, root, habit_manager, db_connection):
        self.root = root
        self.root.title("Habit Tracker")
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)


        #main frame
        button_frame = tk.Frame(root)
        button_frame.pack(side='top', fill='x')

        #filter on periodicity
        self.categories = ['Daily', 'Weekly']
        self.filter_button2 = tk.Button(button_frame, text="Weekly", command=lambda: self.change_categories(['Weekly']))
        self.filter_button2.pack(side='left')
        self.filter_button1 = tk.Button(button_frame, text="Daily",command=lambda: self.change_categories(['Daily']))
        self.filter_button1.pack(side='left')
        self.filter_button = tk.Button(button_frame, text="All", command=lambda: self.change_categories(['Daily', 'Weekly']))
        self.filter_button.pack(side='left')


        #Stats Window
        self.open_analysis_button = tk.Button(button_frame, text="Stats", command=self.open_analysis_window)
        self.open_analysis_button.pack(side='left',padx=10)



        self.habit_manager = habit_manager
        #runnins stopwatches is needed to know which habits running time to upload to database in case of the app closure
        self.running_stopwatches = {}
        self.stopwatch_vars = {}
        self.stopwatch_buttons = {}

        self.db_connection = db_connection
        self.resize_event = None




        self.display_frame = tk.Frame(root,bg='lightgrey', width=480, height=660)
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        self.add_habit_button = tk.Button(root, text="Add Habit", command=self.add_habit)
        self.add_habit_button.pack(pady=10)

        self.missed_habit_button = tk.Button(root, text="Missed Habit", command=self.open_missed_habit_window)
        self.missed_habit_button.pack(pady=10)


        self.habit_check_vars = {}

        self.root.bind("<Configure>", self.on_window_resize)

        self.root.after(200, self.display_habits)


    def change_categories(self, new_categories):
        """Update the categories list and refresh UI if necessary."""
        self.categories = new_categories


    def on_quit(self):
            self.save_data_before_quit()
            self.root.destroy()

    def save_data_before_quit(self):
        habits = self.habit_manager.get_all_habits()

        for habit in habits:
            habit_id = habit.habit_id
            if habit.is_stopwatch:
                if habit_id in self.running_stopwatches and self.running_stopwatches[habit_id]:
                    diff = habit.seconds - habit.timespent
                    timespent = '"' + str(timedelta(seconds=int(diff))) + '"'


                    ###upload habit clock data in case it was not toggled when app was closed
                    if habit.seconds !=0:
                        habit.timespent = habit.seconds
                        hmtodb.done(self.habit_manager, habit, timespent)







    def start_stopwatch(self, habit):
        """whenever stopwatch start/stop button is pressed."""
        habit_id = habit.habit_id
        state = self.habit_check_vars[habit_id].get()


        if habit_id in self.running_stopwatches and self.running_stopwatches[habit_id]:
            self.running_stopwatches[habit_id] = False
            self.stopwatch_buttons[habit_id].config(text="Start")


        else:
            if state:
                self.habit_check_vars[habit_id] = tk.BooleanVar(value=False)
                hours = habit.seconds // 3600
                minutes = (habit.seconds % 3600) // 60
                seconds = habit.seconds % 60
                formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}" if hours > 0 else f"{minutes:02}:{seconds:02}"

                initial_time = tk.StringVar()

                initial_time.set(formatted_time)

                self.stopwatch_vars[habit_id] = initial_time


            self.running_stopwatches[habit_id] = True
            self.stopwatch_buttons[habit_id].config(text="Stop")
            self.update_stopwatch(habit)


    def update_stopwatch(self, habit):
        """Update the stopwatch time for the habit."""
        habit_id = habit.habit_id
        if self.running_stopwatches[habit_id]:
            current_time = self.stopwatch_vars[habit_id].get()


            time_parts = list(map(int, current_time.split(":")))
            if len(time_parts) == 2:
                minutes, seconds = time_parts
                hours = 0
            else:
                hours, minutes, seconds = time_parts

            total_seconds = hours * 3600 + minutes * 60 + seconds
            total_seconds += 1
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60


            formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}" if hours > 0 else f"{minutes:02}:{seconds:02}"
            habit.seconds = total_seconds
            self.stopwatch_vars[habit_id].set(formatted_time)
            self.root.after(1000, lambda: self.update_stopwatch(habit))

    def open_analysis_window(self):
        stats(self.root)




    def deactivate_habit(self, habit):
        self.habit_manager.habits = [h for h in self.habit_manager.habits if h.habit_id != habit.habit_id]
        hmtodb.delete_habit(habit)
        self.display_habits()


    def on_window_resize(self, event):
        """Update the window size label when the window is resized."""
        if self.resize_event:
            self.root.after_cancel(self.resize_event)
        self.resize_event = self.root.after(800, self.display_habits)






    def checkbox_toggled(self, habit):


        habit_id = habit.habit_id
        state = self.habit_check_vars[habit_id].get()

        if state:
            if habit.is_stopwatch:
                if habit_id in self.running_stopwatches and self.running_stopwatches[habit_id]:
                    self.start_stopwatch(habit)
                else:
                    pass

                diff = habit.seconds - habit.timespent
                timespent = '"' + str(timedelta(seconds=int(diff))) + '"'
                habit.timespent = habit.seconds
                hmtodb.done(self.habit_manager, habit, timespent)




            else:
                hmtodb.done(self.habit_manager, habit)

            #if habit is stopwatch and toggled - update streaks
            streaks, days_missed, _, _, _, _, _ = get_current_streaks()
            habit_id = habit.habit_id

            if len(days_missed[days_missed['Habit_id'] == habit_id]['diff']) > 0:
                habit.days_missed = days_missed[days_missed['Habit_id'] == habit_id]['diff'].item()
            if habit_id in streaks['Habit_id'].values:
                habit.current_streak = streaks[streaks['Habit_id'] == habit_id]['max_consecutive_days'].item()

        else:
            #for non-Stopwatch habits - can't click them multiple times
            print("You already did it today!")
            self.habit_check_vars[habit_id].set(True)




    def open_missed_habit_window(self):
        habits = self.habit_manager.get_all_habits()


        if not habits:
            messagebox.showerror("Error", "No habits found!")
            return

        missed_window = tk.Toplevel(self.root)
        missed_window.title("Enter Missed Habit")

        tk.Label(missed_window, text="Select Habit:").pack(pady=5)
        selected_habit = tk.StringVar(missed_window)
        habit_dropdown = ttk.Combobox(missed_window, textvariable=selected_habit)
        habit_dropdown['values'] = [habit.name for habit in habits]
        habit_dropdown.pack(pady=5)


        timespent_label = tk.Label(missed_window, text="Time Spent (example: 00:32:21):")
        timespent_entry = tk.Entry(missed_window)

        def on_habit_select(event):
            selected_name = selected_habit.get()


            for habit in habits:
                if habit.name == selected_name:
                    if habit.is_stopwatch:
                        #show time entry only if the habit is Stopwatch type
                        timespent_label.pack(pady=5)
                        timespent_entry.pack(pady=5)
                    else:
                        timespent_label.pack_forget()
                        timespent_entry.pack_forget()

        habit_dropdown.bind("<<ComboboxSelected>>", on_habit_select)


        def submit_missed_habit():
            habit_name = selected_habit.get()
            for h in habits:
                if habit_name == h.name:
                    habit = h

            timespent = timespent_entry.get() if timespent_entry.winfo_ismapped() else None

            if not habit_name:
                messagebox.showerror("Error", "Please select a habit.")
                return

            try:

                yesterday = datetime.now() - timedelta(days=1)
                timestamp_yesterday = yesterday.strftime('%Y-%m-%d %H:%M:%S')

                all_habits = self.habit_manager.get_all_habits()

                habit_ids = [(int(habit.habit_id), habit.name)  if habit.name == habit_name else None for habit in all_habits]

                for item in habit_ids:
                    if isinstance(item, tuple) and len(item) > 0:
                        selected_id = item[0]

                        break

                hmtodb.done(self.habit_manager, habit, '"'+str(timespent)+'"', str(timestamp_yesterday))
                messagebox.showinfo("Success", f"Missed habit '{habit_name}' logged successfully!")
                missed_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(missed_window, text="Submit", command=submit_missed_habit).pack(pady=10)



    def add_habit(self):
        """Open a dialog to add a new habit with frequency selection."""
        name = simpledialog.askstring("Add Habit", "Enter habit name:")
        description = simpledialog.askstring("Add Habit", "Enter habit description:")

        if name and description:
            frequencies = ["Daily", "Weekly"]
            habit_window = tk.Toplevel(self.root)
            habit_window.title("Add Habit")


            frequency_label = tk.Label(habit_window, text="Select Frequency:")
            frequency_label.pack(pady=5)

            selected_frequency = tk.StringVar()
            selected_frequency.set(frequencies[0])

            frequency_menu = tk.OptionMenu(habit_window, selected_frequency, *frequencies)
            frequency_menu.pack(pady=5)

            is_stopwatch_var = tk.BooleanVar(value=False)
            stopwatch_checkbox = tk.Checkbutton(habit_window, text="Enable Stopwatch", variable=is_stopwatch_var)
            stopwatch_checkbox.pack(pady=5)

            confirm_button = tk.Button(habit_window, text="Confirm",
                                       command=lambda: self.save_habit(name, description, selected_frequency.get(),
                                                                       is_stopwatch_var.get(), habit_window))
            confirm_button.pack(pady=10)

    def save_habit(self, name, description, frequency, is_stopwatch,  window):
        hmtodb.create_habit(self.habit_manager, name, description, frequency, is_stopwatch)
        self.display_habits()
        window.destroy()






    def display_habits(self):
        """Fetch habits from the HabitManager and display them in individual white boxes."""
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        habits = self.habit_manager.get_all_habits()
        frame_x = self.display_frame.winfo_width()
        frame_y = self.display_frame.winfo_height()

        coordinates = calc(frame_x, frame_y, 145, 10, len(habits))
        #next habit coordinates
        if len(habits) > 0:
            x_position = coordinates[0][0]
            y_position = coordinates[0][1]
        else:
            x_position = 0
            y_position = 0

        for i, habit in enumerate(habits):

            if habit.frequency in self.categories:
                habit_id = habit.habit_id
                habit_frame = tk.Frame(self.display_frame, bg="pink", bd=2, relief="groove", width=100, height=100)
                habit_frame.place(x=x_position, y=y_position, width=145, height=135)  # Adjust padding and expand as needed



                habit_name_label = tk.Label(habit_frame, text=f"{habit.name}", fg = "black",bg="pink", anchor="w", font=("Helvetica", 14, "bold"))
                habit_name_label.place(y=15, anchor="w")

                habit_description_label = tk.Label(habit_frame, text=f"{habit.description}", fg = "black",bg="pink", anchor="w", font=("Helvetica", 6, "normal"))
                habit_description_label.place(x=60, y=35, anchor='center')


                habit_frequency_label = tk.Label(habit_frame, text=f"{habit.frequency}", fg = "black",bg="pink", anchor="w", font=("Helvetica", 8, "italic"))
                habit_frequency_label.place(x=110, y=65, anchor="se")



                delete_button = tk.Button(habit_frame, text="x", highlightbackground='pink', fg="red", width=1, padx=1, pady=2, bd=1,font=("", 12),
                                          command=lambda habit=habit: self.deactivate_habit(habit))
                delete_button.place(relx=1.0, rely=0.0, width=22, height=22, anchor="ne")


                if habit.is_stopwatch:
                    if habit_id not in self.stopwatch_vars:
                        hours = habit.seconds // 3600
                        minutes = (habit.seconds % 3600) // 60
                        seconds = habit.seconds % 60
                        formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}" if hours > 0 else f"{minutes:02}:{seconds:02}"


                        self.stopwatch_vars[habit_id] = tk.StringVar(value=formatted_time)
                        self.running_stopwatches[habit_id] = False

                    stopwatch_label = tk.Label(habit_frame, textvariable=self.stopwatch_vars[habit_id], fg="black",
                                               bg="pink", font=("Helvetica", 8))
                    stopwatch_label.place(x=40, y=80, anchor='center')


                    button_text = "Stop" if self.running_stopwatches[habit_id] else "Start"


                    self.stopwatch_buttons[habit_id] = tk.Button(habit_frame, text=button_text,width=2, padx=1, pady=2, bd=1,
                                                 command=lambda habit=habit: self.start_stopwatch(habit))
                    self.stopwatch_buttons[habit_id].place(x=90, y=80, anchor='center')



                was_completed_today = False
                if habit.latest_check:
                    was_completed_today = timepassed(habit)

                if habit.habit_id not in self.habit_check_vars:
                    self.habit_check_vars[habit.habit_id] = tk.BooleanVar(value = was_completed_today)

                checkbox = tk.Checkbutton(
                    habit_frame,
                    text="",
                    variable=self.habit_check_vars[habit.habit_id],
                    font=("", 9),
                    bg = 'pink',
                    fg = 'red',
                    command=lambda habit=habit: self.checkbox_toggled(habit)
                )
                checkbox.place(x=30, y=110, width=20, height=20, anchor="w")

                done = tk.Label(habit_frame, text=f"Done", fg="black", bg="pink", anchor="w",
                                font=("Helvetica", 8, "bold"))
                done.place(y=110, anchor="w")

                """Each habit's last streak is stored. 
                If it also happens that it was checked today it means the streak is active and 🔥 is given.
                If there is only 1 missed day (meaning the habit was last checked yesterday) ⏳ is given and it means the habit's streak is at risk of being over.
                If missed_day value is > 1 😴 is given to show the amount of missed days for the habit."""
                if habit.current_streak > 0:
                    if habit_id in self.habit_check_vars and self.habit_check_vars[habit.habit_id].get():
                        current_streak = tk.Label(habit_frame, text=f'{habit.current_streak}🔥', fg="green", bg="pink",
                                                  anchor="w",
                                                  font=("Helvetica", 8, "normal"))
                        current_streak.place(x=50, y=110, anchor="w")
                    else:
                        current_streak = tk.Label(habit_frame, text=f'{habit.current_streak}⏳', fg="grey", bg="pink",
                                                  anchor="w",
                                                  font=("Helvetica", 8, "normal"))
                        current_streak.place(x=50, y=110, anchor="w")


                if habit.days_missed > 1:
                    days_missed = tk.Label(habit_frame, text=f'{habit.days_missed}😴', fg="red", bg="pink", anchor="w",
                                              font=("Helvetica", 8, "normal"))
                    days_missed.place(x=50, y=110, anchor="w")

            ###calculation for habits coordinates
                if len(habits) > 0:
                    if i < len(habits) -1:
                        coordinates = coordinates[1:]
                        x_position = coordinates[0][0]
                        y_position = coordinates[0][1]

