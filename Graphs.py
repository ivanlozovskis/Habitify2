import calendar
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import database as db
import functional
import pandas as pd


##All plots are here


try:
    resampling_filter = Image.Resampling.LANCZOS  # Pillow >= 7.0
except AttributeError:
    resampling_filter = Image.ANTIALIAS


def all_habits_grid_plot(data, cur_month,month, year, output_dir="", file_prefix="habit_plot"):
    tmp = data[data['month']==cur_month]
    month_name = calendar.month_name[month]

    if len(tmp[tmp['done']!=0]) > 0:
        days_in_month = tmp['day'].max()
        data = [list(tmp[tmp['Name'] == x]['done'].values) for x in tmp['Name'].unique()]
        hab_names = [x.encode("ascii", "ignore").decode("ascii") for x in tmp['Name'].unique()] #Had problems with showcasing emojies in the plot title
        data = np.array(data)
        weekend_mask = tmp['dow'][:data.shape[1]] >= 5
        weekend_mask = weekend_mask.values
        darkened_data = data.astype(float)
        for habit_idx in range(darkened_data.shape[0]):
            darkened_data[habit_idx, weekend_mask & (darkened_data[habit_idx, :] == 0)] += 0.2

        fig = Figure(figsize=(8, 4), dpi=80, facecolor="lightgrey")
        ax = fig.add_subplot(111)
        cmap = plt.cm.Greens
        ax.imshow(darkened_data, cmap=cmap, aspect='equal')

        for i in range(data.shape[0] + 1):
            ax.axhline(i - 0.5, color='black', linewidth=1)
        for j in range(days_in_month + 1):
            ax.axvline(j - 0.5, color='black', linewidth=1)

        ax.set_xticks(range(days_in_month))
        ax.set_xticklabels(range(1, days_in_month + 1))
        ax.set_yticks(range(data.shape[0]))
        ax.set_yticklabels(hab_names)
    else:
        fig, ax = plt.subplots(figsize=(8, 3), facecolor='lightgrey')
        ax.set_facecolor('lightgrey')
        ax.text(0.5, 0.5, "No Data Available", ha='center', va='center', fontsize=12, color='grey')
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    ax.set_title(f"Habit Tracking - {month_name} {year}", fontsize=16)

    output_file = f"{output_dir}/{file_prefix}_{year}-{month:02d}.png"
    fig.savefig(output_file, bbox_inches='tight')
    plt.close(fig)

    return output_file


#
def year_activity_calendar(year, output_file=""):
    """each cell color is a percentage of done habits to all active habits in that day"""
    connection = db.get_connection()
    df = (db.get_habit_counts(connection))
    if len(df) == 0:
        return False
    df1 = functional.denom()
    df1['Date'] = df1['Date'].dt.strftime('%Y-%m-%d')
    df = pd.merge(df, df1, how='left', left_on='dt', right_on='Date')
    df['perc'] = df['count'] / df['Active_Habits']
    df['perc'] = (df['perc'] * 4).astype(int) + 1


    streaks, _, top, topw, perstats, data, tmps1 = functional.get_current_streaks()
    df = df[df['year'] == year]


    days_total = pd.to_datetime(data[data['year']==year]['date']).dt.dayofyear.max()
    full_days = pd.DataFrame({'doy': range(1, days_total + 1)})

    merged_df = pd.merge(full_days, df, on='doy', how='left')
    merged_df.fillna({'perc': 0}, inplace=True)

    contribution_data = np.array(merged_df['perc'].astype(int))




    colors = ["#808080", "#9be9a8", "#40c463", "#30a14e", "#216e39", "#FFD700"] #the "perfect day"(all habits were checked) will be colored gold

    cell_size = 8
    cell_padding = 2
    border_padding = 20
    y_label_padding = 5

    first_day_of_year = datetime(year, 1, 1).weekday()
    empty_days = (first_day_of_year + 1) % 7 - 1
    empty_days = (first_day_of_year + 1) % 7 - 1

    weeks_in_year = (len(contribution_data) + empty_days + 6) // 7

    width = (cell_size + cell_padding) * weeks_in_year - cell_padding + (2 * border_padding)
    height = (cell_size + cell_padding) * 7 - cell_padding + (2 * border_padding)

    days_of_week = ["M", "T", "W", "T", "F", "S", "S"]

    try:
        font = ImageFont.truetype("arial.ttf", 10)
    except:
        font = ImageFont.load_default()


    image = Image.new("RGB", (width, height), "lightgrey")
    draw = ImageDraw.Draw(image)


    for i, day in enumerate(days_of_week):
        x = border_padding
        y = border_padding + i * (cell_size + cell_padding) + (cell_size // 2)
        draw.text((x - y_label_padding, y), day, fill="black", font=font, anchor="mm")


    day_of_year = 0

    for column in range(weeks_in_year):
        for row in range(7):
            if column == 0 and row < empty_days:
                continue
            if day_of_year < len(contribution_data):

                color = colors[contribution_data[day_of_year]]

                x0 = border_padding + column * (cell_size + cell_padding)
                y0 = border_padding + row * (cell_size + cell_padding)
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                draw.rectangle([x0, y0, x1, y1], fill=color)

                day_of_year += 1


    image.save(output_file)
    return output_file



def monthly_activity_in_minutes(tmps, of=""):
    stopwatches = tmps[tmps['Stopwatch'] == 1]['Habit_id'].unique()
    if len(stopwatches) > 0:
        for m, m1 in zip(tmps['month'].unique(), tmps['month1'].unique()):
            if m in tmps['month'].unique():
                thism = tmps[tmps['month'] == m]
                thism = thism[thism['Habit_id'].isin(stopwatches)]
                ln = len(thism[thism['done']>0]['Name'].unique())


                if ln > 1:
                    fig, axs = plt.subplots(figsize=(8, 3 * ln), ncols=1, nrows=ln, facecolor='lightgrey')
                    axs = axs if ln > 1 else [axs]

                    for i, h in enumerate(thism[thism['done']>0]['Name'].unique()):
                        tmp = thism[thism['Name'] == h]
                        axs[i].set_facecolor('lightgrey')
                        axs[i].bar(tmp['day'].values, tmp['TimeSpent'].dt.total_seconds() / 60, color='pink')
                        axs[i].set_xticks(tmp['day'])
                        axs[i].set_title(f"{h.encode('ascii', 'ignore').decode('ascii')} : {calendar.month_name[int(m1)]} {int(thism['year'].unique()[0])}")
                        for spine in axs[i].spines.values():
                            spine.set_visible(False)
                        axs[i].grid()


                elif ln == 1:
                    fig, axs = plt.subplots(figsize=(8, 3), facecolor='lightgrey')
                    h = thism[thism['done']==1]['Name'].unique()[0]
                    tmp = thism[thism['Name'] == h]
                    axs.set_facecolor('lightgrey')
                    axs.bar(tmp['day'].values, tmp['TimeSpent'].dt.total_seconds() / 60, color='pink')
                    axs.set_xticks(tmp['day'])
                    axs.set_title(f"{h.encode('ascii', 'ignore').decode('ascii')} : {calendar.month_name[int(m1)]} {int(thism['year'].unique()[0])}")
                    for spine in axs.spines.values():
                        spine.set_visible(False)
                    axs.grid()
                else:
                    fig, axs = plt.subplots(figsize=(8, 3), facecolor='lightgrey')
                    axs.set_facecolor('lightgrey')


                    axs.set_title(f"{calendar.month_name[int(m1)]} {int(thism['year'].unique()[0])}")

                    axs.text(0.5, 0.5, "No Data Available", ha='center', va='center', fontsize=12, color='grey')
                    axs.set_xticks([])
                    axs.set_yticks([])

                    for spine in axs.spines.values():
                        spine.set_visible(False)
                    axs.grid()



                plt.tight_layout()
                output_file = f"{of}/activity_month_{int(thism['year'].unique()[0])}-{int(m1):02d}_combined.png"
                fig.savefig(output_file, bbox_inches='tight')
                plt.close(fig)
        return True
    else:
        return False






def create_activity(tmps, of=""):
    """Create activity patterns for both Stopwatch and Non-Stopwatch Habits"""
    stopwatches = tmps[tmps['Stopwatch'] == 1]['Habit_id'].unique()
    n_stopwatches = len(stopwatches)


    rows = (n_stopwatches + 1) // 2
    cols = 2
    flaga = False
    flagb = False
    if rows >0:
        fig, axes = plt.subplots(rows, cols, figsize=(10, 5 * rows), dpi=60, facecolor='lightgrey')
        axes = axes.flatten()
        fig.subplots_adjust(hspace=0.5, wspace=0.3)

        for idx, s in enumerate(stopwatches):
            ax = axes[idx]


            patterns = tmps[tmps['Habit_id'] == s].groupby(['weekday', 'dow'])['TimeSpent'].mean().reset_index()
            patterns = patterns.sort_values(by='dow')
            patterns['minutes'] = patterns['TimeSpent'].dt.total_seconds() / 60


            ax.set_facecolor('lightgrey')
            ax.bar(patterns['weekday'], patterns['minutes'], color='mistyrose')
            ax.set_xticks(patterns['weekday'])
            ax.set_xticklabels(patterns['weekday'], rotation=45)


            habit_name = tmps[tmps['Habit_id'] == s]['Name'].unique()[0].encode("ascii", "ignore").decode("ascii")
            ax.set_title(f"Minutes per day: {habit_name}")

            for spine in ax.spines.values():
                spine.set_visible(False)


        for ax in axes[len(stopwatches):]:
            ax.set_visible(False)


        output_file = f"{of}/activity_minutes_combined.png"

        fig.savefig(output_file, bbox_inches='tight')
        plt.close(fig)
        flaga = True
    else:
        flaga = False


    habit_ids = list(set(tmps['Habit_id'].unique()) - set(stopwatches))
    n_habits = len(habit_ids)
    rows = (n_habits + 1) // 2
    cols = 2

    if n_habits>0:

        fig, axes = plt.subplots(rows, cols, figsize=(10, 5 * rows), dpi=60, facecolor='lightgrey')
        axes = axes.flatten()
        fig.subplots_adjust(hspace=0.5, wspace=0.3)

        for idx, s in enumerate(habit_ids):
            ax = axes[idx]

            patterns = tmps[(tmps['Habit_id'] == s) & (tmps['done'] == 1)].groupby(['weekday', 'dow']).size().reset_index(
                name='count')
            patterns = patterns.sort_values(by='dow')

            ax.set_facecolor('lightgrey')

            ax.bar(patterns['weekday'], patterns['count'], color='mistyrose')
            ax.set_xticks(patterns['weekday'])
            ax.set_xticklabels(patterns['weekday'], rotation=45)

            habit_name = tmps[tmps['Habit_id'] == s]['Name'].unique()[0].encode("ascii", "ignore").decode("ascii")
            ax.set_title(f"Activity pattern: {habit_name}")

            ax.set_yticks([])

            for spine in ax.spines.values():
                spine.set_visible(False)


        for ax in axes[n_habits:]:
            ax.set_visible(False)


        output_file = f"{of}/activity_combined.png"
        fig.savefig(output_file, bbox_inches='tight')
        plt.close(fig)
        flagb = True
    else:
        flagb = False

    return flagb,flaga
