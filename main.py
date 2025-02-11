import tkinter as tk
from classes import HabitManager
from app import HabitTrackerGUI
import database as db


#check for the existence of the db
db.initialize_database()

#initialize
connection = db.get_connection()
root = tk.Tk()
habit_manager = HabitManager()

#get the data
df = db.get_active_habits(connection)

#update the HabitManager data
habit_manager.active_habits(df)
habit_manager.update_habbits()

##GUI
app = HabitTrackerGUI(root, habit_manager, connection)
root.mainloop()

