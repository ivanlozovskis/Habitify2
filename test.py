from datetime import datetime

import database as db
import functional
from classes import HabitManager
import hmtodb
import pandas as pd

connection = db.get_connection()
habit_manager = HabitManager()
df = db.get_active_habits(connection)
# print(df)
habit_manager.active_habits(df)
habit_manager.update_habbits()

# assert hmtodb.create_habit(habit_manager, "", "To stuff","deely",0) == False
# assert hmtodb.create_habit(habit_manager, "Habit1", "To stuff","Daily",0) == False
# assert hmtodb.create_habit(habit_manager, "Habit6", "To stuff","Daily",0) == "Habit 'Habit6' created successfully."
# print(hmtodb.delete_habit())
# print(habit_manager)


# hmtodb.create_habit(habit_manager, "Running", "to Run", "Daily", 1)
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[1], '"01:11:03"', time='2025-01-20 14:05:03')

# db.reset(connection, "Log")
# db.reset(connection, "Habit")


# print(datetime.today())
#

# print(habit_manager)




#40 days data
#
# hmtodb.create_habit(habit_manager, "Running", "to Run 10 km", "Weekly", 0, created='2024-12-01 07:05:03')
# hmtodb.create_habit(habit_manager, "Chess", "Do the chess routine", "Weekly", 0, created='2024-12-01 07:05:03')
# hmtodb.create_habit(habit_manager, "Gym", "Go to the Gym", "Daily", 0, created='2024-12-01 07:05:03')
# hmtodb.create_habit(habit_manager, "Study", "Uni/Languages", "Daily", 1,created='2024-12-01 07:05:03')
# hmtodb.create_habit(habit_manager, "Stretching", "Do the Stretching", "Daily", 0, created='2024-12-01 07:05:03')

# db.delete_habit(connection, 15, deleted='"2025-01-22 07:05:03"')


# hmtodb.create_habit(habit_manager, "Running", "to Run", "Daily", 1)
# print(habit_manager.get_all_habits()[2].name)
#
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-01 14:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-02 15:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-03 16:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-07 07:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-09 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-10 14:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-11 15:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-17 16:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-18 07:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-19 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-20 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-21 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-24 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-27 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2025-01-01 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2025-01-07 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2025-01-11 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2025-01-12 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2025-01-13 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2025-01-19 08:05:03')
# # # for h in habit_manager.get_all_habits():
# # #     print(h.name)
# # # print(habit_manager)
#
# #
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[0], time='2024-12-01 14:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[0], time='2024-12-15 15:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[0], time='2024-12-27 16:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[0], time='2025-01-05 07:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[0], time='2025-01-16 08:05:03')
#
#
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[1], time='2025-01-10 14:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[1], time='2025-01-17 15:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[1], time='2025-01-21 16:05:03')

# #
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:45:22"', time='2024-12-31 07:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:15:17"', time='2025-01-01 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:06:11"',time='2025-01-02 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:11:33"', time='2025-01-03 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:27:55"', time='2025-01-04 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:59:51"', time='2025-01-05 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:09:00"', time='2025-01-06 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"02:56:07"', time='2025-01-07 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"00:16:15"', time='2025-01-07 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"00:55:47"', time='2025-01-11 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:05:03"', time='2025-01-12 08:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:44:46"', time='2025-01-13 08:05:03')

#
#
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-01 13:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-02 12:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-07 06:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-09 07:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-10 15:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-11 14:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-17 15:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-19 07:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-20 07:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2025-01-07 06:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2025-01-11 09:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2025-01-12 05:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2025-01-13 07:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2025-01-19 10:05:03')
# hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2025-01-27 10:05:03')

# print(hmtodb.streaks())
#
# print(functional.denom())
# print(habit_manager)

# print(hmtodb.longest_streak(habit_manager.get_all_habits()[0]))
# print(hmtodb.longest_streak(habit_manager.get_all_habits()[1]))
# print(hmtodb.longest_streak(habit_manager.get_all_habits()[2]))
# print(db.get_created(connection))