import database as db
import functional
import pandas as pd




class Habit:
    def __init__(self, habit_id, name, description, frequency, timespent, is_stopwatch = False, seconds=0, is_completed=False, latest_check = None, days_missed=0):
        self.habit_id = habit_id
        self.name = name
        self.description = description
        self.frequency = frequency
        self.latest_check = latest_check
        self.timespent = timespent
        self.is_stopwatch = is_stopwatch
        self.is_completed = is_completed
        self.seconds = seconds
        self.current_streak = 0
        self.days_missed = 0




class HabitManager:
    def __init__(self):
        self.habits = []

    def active_habits(self, df):
        """gets habits from Habit table into Habit class"""
        for i in range(len(df)):

            self.add_habit(df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 2], df.iloc[i, 3], 0, df.iloc[i, 4], 0)



    def add_habit(self, habit_id, name, description, frequency, timespent, is_stopwatch, seconds=0):
        """Adds a single habit to the class"""
        habit = Habit(habit_id, name, description, frequency, timespent, is_stopwatch, seconds)
        self.habits.append(habit)



    def update_habbits(self):

        streaks, misses, _, _, _, _, _ = functional.get_current_streaks()
        #update habits timespent, current_steak and days_missed
        if type(misses)==type(pd.DataFrame()):
            for habit in self.habits:
                habit_id = habit.habit_id
                timespent = db.get_timespent(db.get_connection(), habit_id)
                #####timespent = seconds here because it is set as a starting point so that clock won't be 00:00 everytime the app is closed.
                ##### Then the difference between seconds and timespent is uploaded to the log
                habit.timespent = timespent
                habit.seconds = timespent

                if len(misses[misses['Habit_id'] == habit_id]['diff']) > 0:
                    habit.days_missed = misses[misses['Habit_id'] == habit_id]['diff'].item()
                if habit_id in streaks['Habit_id'].values:
                    habit.current_streak = streaks[streaks['Habit_id'] == habit_id]['max_consecutive_days'].item()
                latest_check = db.get_latest_check(db.get_connection())
                if habit_id in latest_check['Habit_id'].values:
                    habit.latest_check = latest_check[latest_check['Habit_id'] == habit_id]['latest_check'].item()

    def get_all_habits(self):
        return self.habits

    def __str__(self):
        s=""
        for habit in self.habits:
            s += f"Name: {habit.name}, Streak: {habit.current_streak}, Missed: {habit.days_missed}\n"
        return s