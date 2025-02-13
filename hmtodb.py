from freezegun import freeze_time

import database as db
import pandas as pd
import functional
from datetime import date, datetime
import json

with open("config.json", "r") as file:
    config = json.load(file)['database']
    date_obj = datetime.strptime(config['freeze_time'], "%Y-%m-%d %H:%M:%S")



####these functions were made purely for testing. In reality GUI is pretty much filtering incorrect data. User won't be able to enter tomorrow's date in the log for example
#### However they still ended up useful and were used instead of direct database functions from db.py


def create_habit(hm, name, description, frequency, is_stopwatch, created=None):
    conn = db.get_connection()
    df = db.get_active_habits(conn)
    names = list(df.iloc[:,1])
    if (name != "") & (description != ""):

        if frequency.lower() in ['daily','weekly']:

            if name not in names:
                db.add_habit(conn, '"' + name + '"', '"' + description + '"', '"' + frequency + '"',
                             1 if is_stopwatch else 0, '"'+created+'"' if created != None else None)
                habit_id = db.iterate_id(conn)
                hm.add_habit(habit_id, name, description, frequency, 0, is_stopwatch)
                print(f"Habit '{name}' created successfully.")
                return True
            else:
                print("Already have a Habit with the same name")
                return False
        else:
            print('Wrong Frequency. Type in either "Daily" or "Weekly"')
            return False
    else:
        print("Fill in the fields Name and Description")
        return False

# @freeze_time(config['freeze_time'])
def delete_habit(hm, habit, deleted=None):
    if deleted==None:
        deleted = datetime.now() if config['freeze'] == 0 else date_obj
    hm.habits = [h for h in hm.habits if h.habit_id != habit.habit_id]
    conn = db.get_connection()
    df = db.get_active_habits(conn)
    is_active = df.iloc[:,[0,-1]]
    if habit.habit_id in is_active[is_active['Deleted'].isna()].iloc[:,0].values:

        db.delete_habit(conn, habit.habit_id, deleted)

        return True
    else:
        print("Either Habit_id is wrong or the Habit was already deleted")
        return False


# @freeze_time(config['freeze_time'])
def done(hm, habit, timespent=None, time=None):
    if time == None:

        time = str(datetime.now()) if config['freeze'] == 0 else str(date_obj)

    try:

        pd.to_datetime(time)
        now = datetime.now() if config['freeze'] == 0 else date_obj
        if pd.Timedelta(pd.to_datetime(now)- pd.to_datetime(time)) >= pd.Timedelta(0):

            conn = db.get_connection()
            habit_id = habit.habit_id
            df = db.get_log(conn)
            df = df[df['Name']==habit.name]

            if df['Stopwatch'].unique() == 0:
                if timespent in [None, '"None"',"'None'"]:
                    if len(df.dropna(subset='dt'))>0:
                        if pd.Timestamp(time).strftime('%Y-%m-%d') in [s.strftime('%Y-%m-%d') for s in df['dt']]:
                            print("Already did that!")
                        else:

                            db.add_log(conn, habit_id,None,'"'+time+'"')
                    else:
                        db.add_log(conn, habit_id, None,'"' + time + '"')
                else:
                    print("This Habit is not Stopwatch type to add time here")
            else:
                if timespent != None:
                    db.add_log(conn, habit_id, timespent, '"'+time+'"')
                else:
                    print('timespent is missing')

        else:
            print("Did that habit in the future? Doubt it:D")

    except:
        print('Wrong time Format, must be looking like y-m-d h:m:s')
    finally:
        hm.update_habbits()


def longest_streak(habit=None):
    _, _, longest, _, _, _, _ = functional.get_current_streaks()
    longest = longest[longest['Name']==habit.name]
    if "Daily" in longest['freq'].values:
        print(f"Most Days for Habit {habit.name} in a row : {longest[longest['freq']=='Daily']['max_consecutive_days'].values[0]}")
        return int(longest[longest['freq'] == 'Daily']['max_consecutive_days'].values[0]), int(
            longest[longest['freq'] == 'Weekly']['max_consecutive_days'].values[0])

    print(f"Most Weeks for Habit {habit.name} in a row : {longest[longest['freq']=='Weekly']['max_consecutive_days'].values[0]}")

    return "", int(longest[longest['freq']=='Weekly']['max_consecutive_days'].values[0])


def streaks():
    _, _, longest, _, _, _, _ = functional.get_current_streaks()
    d = longest[longest['freq']=='Daily'].sort_values(by='max_consecutive_days',ascending=False)
    w = longest[longest['freq']=='Weekly'].sort_values(by='max_consecutive_days',ascending=False)
    if len(d)>0:
        print(f"Most Days in a row: {d['Name'].values[0]} - {d['max_consecutive_days'].values[0]}")
    if len(w)>0:
        print(f"Most Weeks in a row: {w['Name'].values[0]} - {w['max_consecutive_days'].values[0]}")

    return longest

