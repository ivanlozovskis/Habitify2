from datetime import datetime

import database as db
import functional
from classes import HabitManager
import hmtodb
import pandas as pd
import functional


connection = db.get_connection()
habit_manager = HabitManager()
df = db.get_active_habits(connection)
habit_manager.active_habits(df)
habit_manager.update_habbits()


###Create habits


### empty name|description when create habit
assert hmtodb.create_habit(habit_manager, "", "To stuff","deely",0) == False

### create habit, all should be good
assert hmtodb.create_habit(habit_manager, "Habit1", "To stuff","Daily",0) == True
#
# ### can't create habit with the same name
assert hmtodb.create_habit(habit_manager, "Habit1", "To stuff","Daily",0) == False
#
# ### habit deletion
assert hmtodb.delete_habit(habit_manager, habit_manager.get_all_habits()[-1]) == True





#40 days data


####Create habits



hmtodb.create_habit(habit_manager, "Running", "to Run 10 km", "Weekly", 0, created='2024-12-01 07:05:03')
hmtodb.create_habit(habit_manager, "Chess", "Do the chess routine", "Weekly", 0, created='2024-12-01 07:05:03')
hmtodb.create_habit(habit_manager, "Gym", "Go to the Gym", "Daily", 0, created='2024-12-01 07:05:03')
hmtodb.create_habit(habit_manager, "Study", "Uni/Languages", "Daily", 1,created='2024-12-01 07:05:03')
hmtodb.create_habit(habit_manager, "Stretching", "Do the Stretching", "Daily", 0, created='2024-12-01 07:05:03')

##no habits have been checked - should be no_data

assert functional.get_current_streaks() == (None, None, None, None, None, None, None)

#
#

###Running Weekly data, max streak should be 2

hmtodb.done(habit_manager, habit_manager.get_all_habits()[0], time='2024-12-01 14:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[0], time='2024-12-15 15:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[0], time='2024-12-27 16:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[0], time='2025-01-05 07:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[0], time='2025-01-16 08:05:03')




###Gym data, max streak is 5


hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-01 14:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-02 15:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-03 16:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-07 07:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-09 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-10 14:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-11 15:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-17 16:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-18 07:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-19 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-20 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-21 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-24 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2024-12-27 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2025-01-01 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2025-01-07 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2025-01-11 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2025-01-12 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2025-01-13 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[2], time='2025-01-19 08:05:03')


### Chess data, max streak is 2
hmtodb.done(habit_manager, habit_manager.get_all_habits()[1], time='2025-01-10 14:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[1], time='2025-01-17 15:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[1], time='2025-01-21 16:05:03')


##Study data, max streak is 8
hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:45:22"', time='2024-12-31 07:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:15:17"', time='2025-01-01 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:06:11"',time='2025-01-02 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:11:33"', time='2025-01-03 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:27:55"', time='2025-01-04 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:59:51"', time='2025-01-05 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:09:00"', time='2025-01-06 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"02:56:07"', time='2025-01-07 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"00:16:15"', time='2025-01-07 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"00:55:47"', time='2025-01-11 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:05:03"', time='2025-01-12 08:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[3], timespent= '"01:44:46"', time='2025-01-13 08:05:03')
#


##Stretching data, the only one with current steak of 4, max streak is 4
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-01 13:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-02 12:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-07 06:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-09 07:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-10 15:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-11 14:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-17 15:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-19 07:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2024-12-20 07:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2025-01-07 06:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2025-01-11 09:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2025-01-12 05:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2025-01-13 07:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2025-01-19 10:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2025-01-24 10:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2025-01-25 10:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2025-01-26 10:05:03')
hmtodb.done(habit_manager, habit_manager.get_all_habits()[4], time='2025-01-27 10:05:03')



streaks, missed, historical, _, _, _, _ = functional.get_current_streaks()





#running current streak is 1 week, althugh it hasn't been checked this week
assert int(streaks[streaks['Name']=='Running']['max_consecutive_days'].values[0])==1

#that is why missed value should be 1 (user is going to lose the streak the next day)
assert int(missed[missed['Name']=='Running']['diff'].values[0])==1


#running best streak was 2 weeks
assert int(historical[historical['Name']=='Running']['max_consecutive_days'].values[0]) == 2
#not tracking days streaks in weekly habits
assert hmtodb.longest_streak(habit_manager.get_all_habits()[0]) == ("",2)



#Stretching current streak is 4 days
assert int(streaks[streaks['Name']=='Stretching']['max_consecutive_days'].values[0])==4
#Stretching best streak was 2 weeks
assert int(historical[historical['Name']=='Stretching']['max_consecutive_days'].values[0]) == 4



#Gym hasn't been done for 7 days
assert int(missed[missed['Name']=='Gym']['diff'].values[0])==7
#Gym  best streak was 5 days
assert int(historical[historical['Name']=='Gym']['max_consecutive_days'].values[0]) == 5

#5 days in a row top historical streak, 8 weeks in a row top historical streak in weeks
assert hmtodb.longest_streak(habit_manager.get_all_habits()[2]) == (5, 8)





# db.reset(connection, "Log")
# db.reset(connection, "Habit")