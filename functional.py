from datetime import date
from datetime import datetime
import database as db
import pandas as pd
import numpy as np
from freezegun import freeze_time
import globals



### Function that calculates amount of active habits each day
### if a habit was active for less than a day it doesn't count
import json

# from test import missed

with open("config.json", "r") as file:
    config = json.load(file)['database']
    date_obj = datetime.strptime(config['freeze_time'], "%Y-%m-%d %H:%M:%S")

# @freeze_time(config['freeze_time'])
def denom():
    df = db.get_created(db.get_connection())
    df['Created'] = pd.to_datetime(df['Created'])
    df['Deleted'] = pd.to_datetime(df['Deleted'])
    start_date = df['Created'].min().date()
    end_date = datetime.now().date() if config['freeze'] == 0 else date_obj.date()
    date_range = pd.date_range(start=start_date, end=end_date)

    result = pd.DataFrame({'Date': date_range})


    result['Date'] = pd.to_datetime(result['Date'])
    df  = df[df['Created'].dt.strftime('%Y-%m-%d') != df['Deleted'].dt.strftime('%Y-%m-%d')].copy()

    result['Active_Habits'] = result['Date'].apply(
        lambda x: ((pd.to_datetime(df['Created'].dt.strftime('%Y-%m-%d')) <= x.strftime('%Y-%m-%d')) &
                   ((df['Deleted'].isna()) | (df['Deleted'] > x))).sum()
    )


    return result



## Here functional paradigm is being implemented into calculating habit streaks

def filter_habits(df, frequency='Daily'):
    """Filter the DataFrame to include only rows with the specified frequency."""
    return df[df['Frequency'] == frequency].reset_index(drop=True)


# Sort habits by Habit_id and day
def sort_habits(df):
    """Sort the DataFrame by 'Habit_id' and 'dayofyear'."""
    return df.sort_values(by=['Habit_id', 'dayofyear']).reset_index(drop=True)


def drop_dups(df):
    return df.drop_duplicates(subset=['Habit_id', 'weekofyear']).reset_index(drop=True)


#  Identify streaks for every n-day periodicity
def identify_streaks(df, interval=1):

    if interval !=7 :
        df['streak'] = df.groupby('Habit_id')['dayofyear'].diff().ne(interval).cumsum()

    else:
        df['streak'] = df.groupby('Habit_id')['weekofyear'].apply(lambda x: (x.diff().fillna(0) != 1).cumsum()).reset_index()['weekofyear']

    return df



def calculate_max_streak(df):
    """Calculate the maximum streak length for each Habit_id."""
    streak_counts = df.groupby(['Habit_id', 'streak']).size()  # Count days in each streak
    max_streaks = streak_counts.groupby(level=0).max().reset_index(name='max_consecutive_days')
    return max_streaks





def merge_habit_names_recursive(max_streaks, habit_names, index=0, result=None):
    """Recursive function to merge habit names with max streaks."""
    if result is None:
        result = pd.DataFrame(columns=['Habit_id', 'max_consecutive_days', 'Name'])
    if index >= len(max_streaks):
        return result


    habit_id = max_streaks.iloc[index]['Habit_id']
    max_days = max_streaks.iloc[index]['max_consecutive_days']
    name = habit_names[habit_names['Habit_id'] == habit_id]['Name'].values[0]

    if 'result' not in locals() or result.empty:
        result = pd.DataFrame(columns=['Habit_id', 'max_consecutive_days', 'Name'])

    result = result.loc[:, result.notna().any()]
    new_data = pd.DataFrame({'Habit_id': [habit_id], 'max_consecutive_days': [max_days], 'Name': [name]})
    result = pd.concat([result, new_data], ignore_index=True)

    return merge_habit_names_recursive(max_streaks, habit_names, index + 1, result)


def show_top(result):
    return result.sort_values(by='max_consecutive_days', ascending=False)[['Name', 'max_consecutive_days']]



##gets log data
def get_data():
    connection = db.get_connection()
    df = db.get_log(connection)
    if len(df.dropna(subset='Habit_id')) == 0:
        return pd.DataFrame()

    return df



#### The continuous dates are needed due to next year having reset weekdays, day of the year and monthsl.
# @freeze_time(config['freeze_time'])
def continous_dates(df):
    df['date'] = df['dt'].dt.strftime('%Y-%m-%d')
    dates = pd.to_datetime(df['dt'])
    min_date = dates.min().normalize()
    min_date1 = min_date - pd.Timedelta(days=min_date.weekday())
    continuous_weeks = ((dates - min_date1).dt.days // 7) + 1
    continuous_days = (dates - min_date).dt.days + 1
    continuous_months = (dates.dt.year - min_date.year) * 12 + (dates.dt.month - min_date.month)

    df['weekofyear'] = continuous_weeks
    df['dayofyear'] = continuous_days
    df['month'] = continuous_months


    today = pd.Timestamp(date.today()) if config['freeze'] == 0 else pd.Timestamp(date_obj)
    today = date.today() if config['freeze'] == 0 else date_obj
    today = today.strftime("%Y-%m-%d")

    yesterday = date.today() - pd.Timedelta(days=1) if config['freeze'] == 0 else date_obj - pd.Timedelta(days=1)
    yesterday = yesterday.strftime("%Y-%m-%d")

    today1 = pd.Timestamp(date.today()) if config['freeze'] == 0 else pd.Timestamp(date_obj)


    thisweek = ((today1 - min_date).days // 7) + 1
    adjusted_dayofyear = (today1 - min_date).days + 1
    thisdayofyear = adjusted_dayofyear
    this_month = (today1.year - min_date.year) * 12 + (today1.month - min_date.month)
    today_day = date.today().day if config['freeze'] == 0 else date_obj.day

    return df, thisweek, today, yesterday, min_date, thisdayofyear, this_month, today_day

#total time spent for a Stopwatch habit in a day
def sum_timespent(df):
    dfp1 = df.groupby(['Habit_id', 'Name', 'date'])['TimeSpent'].sum().reset_index().sort_values(by=['Habit_id', 'date']).reset_index(drop=True)
    dfp2 = df.drop_duplicates(subset=['Habit_id', 'Name', 'date']).reset_index(drop=True).sort_values(by=['Habit_id', 'date']).reset_index(drop=True)
    dfp2[['Haibit_id', 'Name', 'date', 'TimeSpent']] = dfp1

    return dfp2.sort_values(by='dt')


def fill_with_unique_value(df):
    for c in df[df.isna()].columns:
        unique_values = df[c].dropna().unique()
        if (len(unique_values) == 1)&(c!='TimeSpent'):
            df[c] = df[c].fillna(unique_values[0])

    return df


# @freeze_time(config['freeze_time'])
def get_current_streaks():
    """Function that calculates everything.
    Streaks, Missed days, Data for different plots(ones that starts from
    the first day of the month and those that start from the first toggled day of the month)."""


    df = get_data()
    if df.empty:
        return None, None, None, None, None, None, None

    df, thisweek, today, yesterday, min_date, thisdayofyear, this_month, today_day = continous_dates(df)
    df_merged = sum_timespent(df)


    ress = pd.DataFrame()
    cats = ['Daily', 'Weekly']
    pers = [1, 7]



    for cat, per in zip(cats, pers):
        df_filtered = filter_habits(df_merged, frequency=cat)
        df_sorted = sort_habits(df_filtered)
        df_with_streaks = identify_streaks(df_sorted, interval=per)

        if cat != 'Weekly':
            streaks = df_with_streaks[df_with_streaks['date'] == today]['streak']
            streaksy = df_with_streaks[df_with_streaks['date'] == yesterday]['streak']
        else:
            streaks = df_with_streaks[df_with_streaks['weekofyear'] == thisweek]['streak']
            streaksy = df_with_streaks[df_with_streaks['weekofyear'] == (thisweek - 1)]['streak']


        dff1 = df_with_streaks[df_with_streaks['streak'].isin(streaks)].groupby(['Habit_id']).size().reset_index(name='max_consecutive_days')
        dff1['done'] = 1
        dff2 = df_with_streaks[df_with_streaks['streak'].isin(streaksy)].groupby(['Habit_id']).size().reset_index(name='max_consecutive_days')
        dff2['done'] = 0
        dff2 = dff2[~dff2['Habit_id'].isin(dff1['Habit_id'])]
        dff3 = pd.concat([dff1, dff2])
        ress = pd.concat([ress, dff3])

    current_streaks_days = pd.merge(ress, df_merged[['Habit_id', 'Name']].drop_duplicates(), on='Habit_id',how='left')
    current_streaks_days = current_streaks_days.sort_values(by='max_consecutive_days', ascending=False)





    lastcheck = df_merged.groupby('Habit_id')['dt'].max().reset_index(name='last')
    weeklies = df_merged[df_merged['Frequency']=='Weekly']['Habit_id'].unique()
    dailies = df_merged[df_merged['Frequency']=='Daily']['Habit_id'].unique()
    weeklies_lastcheck = lastcheck[lastcheck['Habit_id'].isin(weeklies)].copy()
    dailies_lastcheck = lastcheck[lastcheck['Habit_id'].isin(dailies)].copy()



    weeklies_lastcheck['week'] = ((lastcheck['last'] - min_date).dt.days // 7) + 1
    weeklies_lastcheck['diff'] = thisweek - weeklies_lastcheck['week'] - 1


    dailies_lastcheck['last'] = dailies_lastcheck['last'].dt.strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d") if config['freeze'] == 0 else date_obj.strftime("%Y-%m-%d")
    dailies_lastcheck['diff'] = (pd.to_datetime(now) - pd.to_datetime(dailies_lastcheck['last'])).dt.days
    dailies_lastcheck['diff'] = dailies_lastcheck['diff'].apply(lambda x: x - 1 if x > 0 else x)

    missed_days_or_weeks = pd.concat([weeklies_lastcheck[['Habit_id','diff']], dailies_lastcheck[["Habit_id", "diff"]]])
    missed_days_or_weeks.dropna(subset='Habit_id', inplace=True)

    missed_days_or_weeks['Name'] = missed_days_or_weeks['Habit_id'].apply(
        lambda x: df_merged[df_merged['Habit_id'] == x]['Name'].unique()[0])

    ##both in weeks and days(except for weekly habits)
    longest_streaks = pd.DataFrame()
    cats = ['Daily', 'Weekly']
    pers = [1, 7]

    for cat, per in zip(cats, pers):
        if per == 7:
            df_filtered = df_merged[df_merged['Deleted'].isna()]
        else:
            df_filtered = filter_habits(df_merged[df_merged['Deleted'].isna()], frequency=cat)

        if per == 7:
            df_sorted = sort_habits(df_filtered)
            df_sorted = df_sorted.drop_duplicates(subset=['Habit_id', 'weekofyear']).reset_index(drop=True)


        else:
            df_sorted = sort_habits(df_filtered)
        df_with_streaks = identify_streaks(df_sorted, interval=per)
        max_streaks = calculate_max_streak(df_with_streaks)
        result = merge_habit_names_recursive(max_streaks, df_merged)
        res1 = show_top(result)
        res1['freq'] = cat
        res1 = res1.loc[:, res1.notna().any()]
        if not res1.empty:
            longest_streaks = pd.concat([longest_streaks, res1], ignore_index=True)



    current_streaks_in_weeks = pd.DataFrame()
    cats = ['Daily', 'Weekly']
    pers = [7, 7]


    for cat, per in zip(cats, pers):
        df_filtered = filter_habits(df_merged[df_merged['Deleted'].isna()], frequency=cat)
        df_sorted = sort_habits(df_filtered)
        df_sorted = df_sorted.drop_duplicates(subset=['Habit_id', 'weekofyear']).reset_index(drop=True)
        df_with_streaks = identify_streaks(df_sorted, interval=per)
        df_with_streaks['streak'] = df_with_streaks['Habit_id'].astype(str)+"_"+df_with_streaks['streak'].astype(str)
        streaks = df_with_streaks[df_with_streaks['weekofyear'] == thisweek]['streak']
        dff1 = df_with_streaks[df_with_streaks['streak'].isin(streaks)].groupby(['Habit_id']).size().reset_index(
            name='max_consecutive_days')
        current_streaks_in_weeks = pd.concat([current_streaks_in_weeks, dff1])


    current_streaks_in_weeks = merge_habit_names_recursive(current_streaks_in_weeks, df_merged)
    current_streaks_in_weeks = current_streaks_in_weeks.sort_values(by='max_consecutive_days', ascending=False)


    globals.CONT_MONTH = this_month



    ds = df_merged[df_merged['Deleted'].isna()]
    ds = ds.groupby(['Habit_id', 'Name', 'date', 'weekofyear']).size().reset_index(name='count').groupby(['Habit_id', 'Name', 'weekofyear']).size().reset_index(name='count')  # .groupby(['Habit_id','Name'])['count'].mean()
    min_max_weeks = ds.groupby("Habit_id")["weekofyear"].agg(["min", "max"]).reset_index()
    min_max_weeks['max'] = thisweek

    all_weeks = []
    for _, row in min_max_weeks.iterrows():
        all_weeks.extend([(row["Habit_id"], week) for week in range(int(row["min"]), int(row["max"]) + 1)])

    all_weeks_df = pd.DataFrame(all_weeks, columns=["Habit_id", "weekofyear"])
    result = all_weeks_df.merge(ds, on=["Habit_id", "weekofyear"], how="left").fillna({"count": 0})
    result["count"] = result["count"].astype(int)
    result1 = result.groupby(['Habit_id'])['count'].mean().reset_index(name='mean')
    res = pd.merge(result1, df_merged[['Habit_id', 'Name']].drop_duplicates(), on='Habit_id')
    res.apply(lambda x: f"{x['Name']}: {np.round(x['mean'], 2)}", axis=1)
    res['perweek'] = res['mean']
    df_merged['month1'] = df_merged['dt'].dt.month

    ds = df_merged[df_merged['Deleted'].isna()]
    ds = ds.groupby(['Habit_id', 'Name', 'date', 'month']).size().reset_index(name='count').groupby(['Habit_id', 'Name', 'month']).size().reset_index(name='count')  # .groupby(['Habit_id','Name'])['count'].mean()
    res5 = ds.groupby(['Habit_id', 'Name'])['count'].mean().reset_index()
    res5.apply(lambda x: f"{x['Name']}: {np.round(x['count'], 2)}", axis=1)
    res5['permonth'] = res5['count']
    res1 = pd.merge(res, res5, on=['Habit_id', 'Name'])
    ds = df_merged[df_merged['Deleted'].isna()]
    ds.groupby(['Habit_id', 'Name', 'date', 'month'])
    ds = ds.groupby(['Habit_id', 'Name', 'month', 'weekofyear']).size().reset_index().groupby(['Habit_id', 'Name', 'month']).size().reset_index(name='weekspermonth')
    ds = ds.groupby(['Habit_id', 'Name'])['weekspermonth'].mean().reset_index()
    res2 = pd.merge(res1, ds, on=['Habit_id', 'Name'])

    df2 = df_merged[df_merged['Stopwatch'] == 1]
    if len(df2.dropna(subset='dt'))>0:

        df22 = df2.groupby(['Habit_id', 'dayofyear'])['TimeSpent'].sum().reset_index(name='sum')
        res = pd.merge(df22, df_merged[['Habit_id', 'Name']].drop_duplicates(), on='Habit_id')
        min_max_weeks = res.groupby("Habit_id")["dayofyear"].agg(["min", "max"]).reset_index()
        min_max_weeks['max'] = thisdayofyear
        all_weeks = []
        for _, row in min_max_weeks.iterrows():
            all_weeks.extend([(row["Habit_id"], week) for week in range(int(row["min"]), int(row["max"]) + 1)])

        all_weeks_df = pd.DataFrame(all_weeks, columns=["Habit_id", "dayofyear"])


        result = all_weeks_df.merge(res, on=["Habit_id", "dayofyear"], how="left").fillna({"sum": pd.to_timedelta("0 days 00:00:00")})
        result1 = result.groupby(['Habit_id'])['sum'].mean().reset_index(name='mean')
        result1['mean1'] = result1['mean'].apply(lambda x: np.round(x.total_seconds() / 60, 1))

        res = pd.merge(result1, df_merged[['Habit_id', 'Name']].drop_duplicates(), on='Habit_id')
        res.apply(lambda x: f"{x['Name']}: {np.round(x['mean1'], 2)}", axis=1)
        res['minutesperday'] = np.round(res['mean'].dt.total_seconds() / 60, 1)
        res3 = pd.merge(res2, res, on=['Habit_id', 'Name'], how='left')
        per_stats = res3.sort_values(by='perweek', ascending=False)[['Habit_id', 'Name', 'perweek', 'permonth', 'weekspermonth', 'minutesperday']]
        per_stats = pd.merge(per_stats, df_merged[['Habit_id', 'Frequency']].drop_duplicates(), on='Habit_id', how='left')
    else:
        per_stats = res2.sort_values(by='perweek', ascending=False)[['Habit_id', 'Name', 'perweek', 'permonth', 'weekspermonth']]
        per_stats = pd.merge(per_stats, df_merged[['Habit_id', 'Frequency']].drop_duplicates(), on='Habit_id', how='left')




    ff = sort_habits(df_merged.reset_index(drop=True))
    ff['year'] = pd.to_datetime(ff['date']).dt.year
    ff['TimeSpent'] = pd.to_timedelta(ff['TimeSpent'])

    ## data for the all_habits_grid_plot() plot
    plot_data_first_day_1 = pd.DataFrame()

    for name in ff['Name'].unique():
        tmp = ff[ff['Name'] == name]
        first = tmp['month'].min()

        stopwatch = tmp['Stopwatch'].unique()
        pd.options.mode.chained_assignment = None

        if (globals.CONT_MONTH not in tmp['month'].unique()) & (name in df_merged[(df_merged['Deleted'].isna())&(df_merged['Frequency']=='Daily')]['Name'].unique()):
            tmp1 = pd.DataFrame({"Habit_id":[tmp['Habit_id'].unique()[0]], "Name":[name], "year":[globals.CURRENT_YEAR1], "month":[globals.CONT_MONTH], "day":[1], "done":[0], 'TimeSpent':[pd.to_timedelta("0 days 00:00:00'")]})
            tmp1 = pd.merge(tmp1, pd.Series(range(1, today_day + 1), name='day'), on='day', how='right')
            tmp1['TimeSpent'] = tmp1['TimeSpent'].fillna(pd.to_timedelta("0 days 00:00:00'"))
            tmp1['done'] = 0
            tmp1['Name'] = name
            tmp1['month'] = globals.CONT_MONTH
            tmp1['month1'] = globals.CURRENT_MONTH
            tmp1['year'] = globals.CURRENT_YEAR1
            tmp1 = fill_with_unique_value(tmp1)

            plot_data_first_day_1 = pd.concat([plot_data_first_day_1, tmp1[['Habit_id', 'Name', 'year', 'month', 'month1','day', 'done', 'TimeSpent']]])


        for month, month1 in zip(tmp['month'].unique(), tmp['month1'].unique()):
            tmp1 = tmp[tmp['month'] == month]
            tmp1.loc[:, 'day'] = tmp1['dt'].dt.day
            tmp1.loc[:,'year'] = tmp1['dt'].dt.year
            lastday = (tmp1['dt'].values[0] + pd.offsets.MonthEnd(0)).day
            if stopwatch == 0:
                tmp1['TimeSpent'] += pd.Timedelta(minutes=1)

            if (first == this_month)|(month == this_month):
                b = today_day+1
            else:
                b = lastday+1

            tmp1 = pd.merge(tmp1, pd.Series(range(1, b), name='day'), on='day', how='right')
            tmp1['TimeSpent'] = tmp1['TimeSpent'].fillna(pd.to_timedelta("0 days 00:00:00'"))
            tmp1['done'] = tmp1['TimeSpent'].apply(lambda x: 1 if x.total_seconds() > 0 else 0)
            tmp1 = fill_with_unique_value(tmp1)

            plot_data_first_day_1 = pd.concat([plot_data_first_day_1, tmp1[['Habit_id', 'Name', 'year', 'month','month1', 'day', 'done', 'TimeSpent']]])



    fix = plot_data_first_day_1[['year','month1','day']]
    fix['month'] = fix['month1'].astype(int)

    plot_data_first_day_1['date'] = pd.to_datetime(fix[['year','month','day']])
    plot_data_first_day_1['Stopwatch'] = plot_data_first_day_1['Habit_id'].apply(lambda x: x in df_merged[df_merged['Stopwatch'] == 1]['Habit_id'].unique())
    plot_data_first_day_1['dow'] = plot_data_first_day_1['date'].dt.dayofweek  # Numerical representation (0=Monday)
    plot_data_first_day_1['dow_name'] = plot_data_first_day_1['date'].dt.day_name()

    ## data for the monthly_activity_in_minutes() plot
    plot_data_first_day_x = pd.DataFrame()


    for name in ff['Name'].unique():
        tmp = ff[ff['Name'] == name]
        first = tmp['month'].min()
        stopwatch = tmp['Stopwatch'].unique()



        for month in tmp['month'].unique():
            tmp1 = tmp[tmp['month'] == month]
            tmp1['day'] = tmp1['dt'].dt.day
            tmp1['year'] = tmp1['dt'].dt.year
            firstday = tmp1['day'].min()
            lastday = (tmp1['dt'].values[0] + pd.offsets.MonthEnd(0)).day


            if stopwatch == 0:
                tmp1['TimeSpent'] += pd.Timedelta(minutes=1)

            if first == this_month:
                a = firstday
                b = today_day+1
            elif month == first:
                a,b = firstday, lastday+1
            elif month == this_month:
                a,b = 1, today_day+1
            else:
                a,b = 1, lastday+1

            tmp1 = pd.merge(tmp1, pd.Series(range(a, b), name='day'), on='day', how='right')
            tmp1['TimeSpent'] = tmp1['TimeSpent'].fillna(pd.to_timedelta("0 days 00:00:00'"))
            tmp1['done'] = tmp1['TimeSpent'].apply(lambda x: 1 if x.total_seconds() > 0 else 0)
            tmp1 = fill_with_unique_value(tmp1)

            years = ff.groupby(['year','month']).size().reset_index()[['year','month']]
            tmp1 = tmp1.drop(columns='year')
            tmp1 = pd.merge(tmp1, years, how='left',on='month')
            plot_data_first_day_x = pd.concat([plot_data_first_day_x, tmp1[['Habit_id', 'Name', 'year', 'month', 'month1','day', 'done', 'TimeSpent']]])

        fix = plot_data_first_day_x[['year', 'month1', 'day']]
        fix['month'] = fix['month1'].astype(int)


        plot_data_first_day_x['date'] = pd.to_datetime(fix[['year', 'month', 'day']])

        plot_data_first_day_x['dow'] = plot_data_first_day_x['date'].dt.dayofweek
        plot_data_first_day_x["weekday"] = plot_data_first_day_x["date"].dt.strftime("%A")
        plot_data_first_day_x['Stopwatch'] = plot_data_first_day_x['Habit_id'].apply(lambda x: x in df_merged[df_merged['Stopwatch']==1]['Habit_id'].unique())
        plot_data_first_day_x = plot_data_first_day_x[plot_data_first_day_x['Habit_id'].isin(df_merged[df_merged['Frequency']=='Daily']['Habit_id'].unique())]
        plot_data_first_day_x= plot_data_first_day_x[plot_data_first_day_x['Habit_id'].isin(df_merged[df_merged['Deleted'].isna()]['Habit_id'].unique())]
        plot_data_first_day_x['Name'] = plot_data_first_day_x['Habit_id'].apply(lambda x: df_merged[df_merged['Habit_id']==x]['Name'].unique()[0])


    return current_streaks_days, missed_days_or_weeks, longest_streaks, current_streaks_in_weeks, per_stats, plot_data_first_day_1, plot_data_first_day_x



