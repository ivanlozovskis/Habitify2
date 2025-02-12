import numpy as np
import pandas as pd
from functional import get_current_streaks
from pathlib import Path
from database import  get_connection
import database as db
from PIL import Image, ImageTk
import globals
import tkinter as tk
from tkinter import messagebox
from Graphs import all_habits_grid_plot, year_activity_calendar
import os
import sys
from datetime import datetime
import calendar
from dateutil.relativedelta import relativedelta
from freezegun import freeze_time

import json

from hmtodb import date_obj

with open("config.json", "r") as file:
    config = json.load(file)['database']
    date_obj = datetime.strptime(config['freeze_time'], "%Y-%m-%d %H:%M:%S")




def get_app_data_dir(app_name="HabitifyApp"):
    """Get or create the application support directory for the plots."""
    base_dir = Path.home() / "Library" / "Application Support" / app_name
    base_dir.mkdir(parents=True, exist_ok=True)

    return base_dir

# @freeze_time(config['freeze_time'])
def timepassed(habit):
    """Calculates whether the habit was done yesterday/last week"""
    today = datetime.now().date()  if config['freeze'] == 0 else date_obj.date()
    latestcheck = habit.latest_check.date()
    if habit.frequency == "Daily":
        if today == latestcheck:
            return True
    elif habit.frequency == "Weekly":
        current_week = today.isocalendar()[1]
        latestcheck_week = latestcheck.isocalendar()[1]

        current_year = today.isocalendar()[0]
        latestcheck_year = latestcheck.isocalendar()[0]

        if current_week == latestcheck_week and current_year == latestcheck_year:
            return True




def calculate_box_coordinates(frame_width, frame_height, box_size, padding, box_count):
    """figuring out each habit box placement"""
    coordinates = []
    x_position = padding
    y_position = padding

    # Calculate how many boxes fit in one row
    boxes_per_row = (frame_width - padding) // (box_size + padding)

    for i in range(box_count):
        # Add the current box's coordinates
        coordinates.append((x_position, y_position))

        # Update x_position for the next box
        x_position += box_size + padding

        # If we've reached the end of the row, reset x_position and move to the next row
        if (i + 1) % boxes_per_row == 0:
            x_position = padding
            y_position += box_size + padding

    return coordinates



def years(year):
    """This function calculates whether there are data in the previous and in the next year to show the correct arrows above year calendar"""
    left = right = None
    connection = get_connection()
    df = db.get_log(connection)
    unique_years = df.dropna(subset='dt')['dt'].dt.year.unique()
    if np.where(unique_years == year)[0] > 0:
        left = year - 1
    if np.where(unique_years == year)[0] < len(unique_years)-1:
        right = year + 1
    return left, right

# @freeze_time(config['freeze_time'])
def months(month):
    """this function calculates whether there are data in the previous and in the next month and also gives out the continous number of the month (starting from the first date in log)"""
    left = right = None
    _, _, _, _, _, data, _ = get_current_streaks()

    data['dt'] = pd.to_datetime(data['date'])
    data['date'] = data['dt'].dt.strftime("%Y-%m")
    data = data.drop_duplicates(subset='date')
    df_sorted = data.sort_values(by='date')['date'].values


    cont_months = {}
    for i, m in enumerate(df_sorted):
        cont_months[m] = i


    target_month = datetime(globals.CURRENT_YEAR, globals.CURRENT_MONTH, 1).strftime("%Y-%m")
    dates = sorted(datetime.strptime(k, "%Y-%m") for k in cont_months.keys())
    start_date = dates[0]
    end_date = datetime.now() if config['freeze'] == 0 else date_obj
    target_date = datetime.strptime(target_month, "%Y-%m")
    month_number = (target_date.year - start_date.year) * 12 + (target_date.month - start_date.month)

    if target_date > end_date:
        end_date = target_date

    filled_dict = {}
    current_date = start_date
    while current_date <= end_date:
        formatted_month = current_date.strftime("%Y-%m")
        filled_dict[formatted_month] = (current_date.year - start_date.year) * 12 + (
                    current_date.month - start_date.month)
        current_date += relativedelta(months=1)


    df_sorted = np.array([s for s in filled_dict.keys()])
    if np.where(df_sorted == month)[0] > 0:
        left = df_sorted[np.where(df_sorted == month)[0] - 1][0]
    if np.where(df_sorted == month)[0] < len(df_sorted) - 1:
        right = df_sorted[np.where(df_sorted == month)[0] + 1][0]

    return left, right, month_number





def get_output_dir():
    if hasattr(sys, "_MEIPASS"):  # PyInstaller's temporary folder for resources
        return os.path.abspath(sys._MEIPASS)
    return os.path.abspath(".")



try:
    resampling_filter = Image.Resampling.LANCZOS  # Pillow >= 7.0
except AttributeError:
    resampling_filter = Image.ANTIALIAS  # Older Pillow versions



def display_plot_in_frame(frame, filename="habit_plot.png"):
    for widget in frame.winfo_children():
        widget.destroy()


    img = Image.open(filename)
    fixed_size = (600, 300)
    padded_img = img.resize(fixed_size, resampling_filter)


    canvas_img = Image.new("RGBA", (fixed_size[0] + 20, fixed_size[1] + 20), (255, 255, 255, 255))
    canvas_img.paste(padded_img, (10, 10))


    img_tk = ImageTk.PhotoImage(canvas_img)
    label = tk.Label(frame, image=img_tk, bg="lightgrey")
    label.image = img_tk
    label.pack(pady=10)





def debug_popup(message):
    messagebox.showerror("Debug Info", message)



# @freeze_time(config['freeze_time'])
def monthly_arrows(label, label1,output_dir, switch, data):
    globals.MBTN_LEFT.pack_forget()
    globals.MBTN_RIGHT.pack_forget()
    globals.MONTH_LABEL.pack_forget()

    previous_month, next_month, cont_month = months(datetime(globals.CURRENT_YEAR, globals.CURRENT_MONTH, 1).strftime("%Y-%m"))
    yr, mn = (previous_month.split("-")) if switch < 0 else next_month.split("-")
    globals.CURRENT_YEAR=int(yr)
    globals.CURRENT_MONTH = int(mn)
    previous_month, next_month, cont_month = months(datetime(globals.CURRENT_YEAR, globals.CURRENT_MONTH, 1).strftime("%Y-%m"))

    output_file = all_habits_grid_plot(
        data=data,
        month=int(mn),
        cur_month= cont_month,
        year=int(yr),
        output_dir=output_dir
    )

    new_image = Image.open(output_file)
    tk_image = ImageTk.PhotoImage(new_image)


    label.config(image=tk_image)
    label.image = tk_image


    new_image1 = Image.open(
        f"{output_dir}/activity_month_{int(yr)}-{int(mn):02d}_combined.png")
    frame_width = int(new_image1.size[0] * 0.8)
    frame_height = int(new_image1.size[1] * 0.8)

    new_image1 = new_image1.resize((frame_width, frame_height), Image.Resampling.LANCZOS)

    tk_image1 = ImageTk.PhotoImage(new_image1)

    label1.config(image=tk_image1)
    label1.image = tk_image1



    app_data_dir = get_app_data_dir()


    globals.MONTH_LABEL.config(text=f"{calendar.month_name[int(mn)]} {int(yr)}")

    if previous_month:
        imagepath = app_data_dir
        globals.MBTN_LEFT.config(text="<",command = lambda: monthly_arrows(label, label1, imagepath, -1, data))

    else:
        globals.MBTN_LEFT.config(text="", command = lambda: None)

    globals.MBTN_LEFT.pack(side="left", padx=5)
    globals.MONTH_LABEL.pack(side="left", padx=10)

    if next_month:
        imagepath = app_data_dir
        globals.MBTN_RIGHT.config(text=">", command=lambda: monthly_arrows(label, label1, imagepath, 1, data))

    else:
        globals.MBTN_RIGHT.config(text="", command = lambda: None)
    globals.MBTN_RIGHT.pack(side="left", padx=5)



### Arrows above yearly calendar
def yearly_arrows(label,output_dir, switch):

    globals.BTN_LEFT.pack_forget()
    globals.BTN_RIGHT.pack_forget()
    globals.YEAR_LABEL.pack_forget()


    image_path = year_activity_calendar(globals.CURRENT_YEAR1 + switch , output_file=output_dir)
    new_image = Image.open(image_path)
    tk_image = ImageTk.PhotoImage(new_image)

    label.config(image=tk_image)
    label.image = tk_image
    globals.CURRENT_YEAR1 += switch


    app_data_dir = get_app_data_dir()

    previous_year, next_year = years(globals.CURRENT_YEAR1)


    globals.YEAR_LABEL.config(text=globals.CURRENT_YEAR1)

    if previous_year:
        imagepath = app_data_dir / f"calendar{globals.CURRENT_YEAR1 - 1}.png"
        globals.BTN_LEFT.config(text="<",command = lambda: yearly_arrows(label, imagepath, -1))

    else:
        globals.BTN_LEFT.config(text="", command = lambda: None)

    globals.BTN_LEFT.pack(side="left", padx=5)
    globals.YEAR_LABEL.pack(side="left", padx=10)

    if next_year:
        imagepath = app_data_dir / f"calendar{globals.CURRENT_YEAR1 + 1}.png"
        globals.BTN_RIGHT.config(text=">", command=lambda: yearly_arrows(label, imagepath, 1))

    else:
        globals.BTN_RIGHT.config(text="", command = lambda: None)
    globals.BTN_RIGHT.pack(side="left", padx=5)



