import tkinter as tk
import calendar
import numpy as np
from PIL import Image, ImageTk
from functional import get_current_streaks
import globals
from datetime import datetime
from Graphs import create_activity, year_activity_calendar, monthly_activity_in_minutes
from dev import get_app_data_dir, years, months


def stats(root=None):
    """Stats window layout"""
    from dev import yearly_arrows, monthly_arrows
    from Graphs import all_habits_grid_plot

    analysis_window = tk.Toplevel(root)
    analysis_window.title("Stats")
    analysis_window.geometry("620x500")
    analysis_window.configure(bg="lightgrey")

    canvas = tk.Canvas(analysis_window, bg="lightgrey")
    scrollbar = tk.Scrollbar(analysis_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="lightgrey")


    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )


    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)


    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")



    streaks, _, top, topw, perstats, data, tmps1 = get_current_streaks()

    app_data_dir = get_app_data_dir()
    imagepath = app_data_dir / f"calendar{globals.CURRENT_YEAR1}.png"

    image_path = year_activity_calendar(globals.CURRENT_YEAR1, output_file=imagepath)



    top_frame = tk.Frame(scrollable_frame, bg="lightgrey", height=200)
    top_frame.pack(side="top", fill="x")

    try:
        img = Image.open(image_path)
        tk_image = ImageTk.PhotoImage(img)

        clndr = tk.Label(top_frame, image=tk_image, bg='lightgrey')
        clndr.image = tk_image

        label = tk.Label(top_frame, text="Yearly Activity", bg='lightgrey', fg='black')
        label.pack()

        upper_frame = tk.Frame(top_frame, bg="lightgrey")
        upper_frame.pack(expand=True)

        previous_year, next_year = years(globals.CURRENT_YEAR1)

        globals.YEAR_LABEL = tk.Label(upper_frame, text=globals.CURRENT_YEAR1, bg='lightgrey', font=("Arial", 14))

        if previous_year:
            imagepath = app_data_dir / f"calendar{globals.CURRENT_YEAR1 - 1}.png"
            globals.BTN_LEFT = tk.Button(upper_frame, text="<", highlightbackground='lightgrey', width=2,
                                         command=lambda: yearly_arrows(clndr, imagepath, -1))

        else:
            globals.BTN_LEFT = tk.Button(upper_frame, text="", highlightbackground='lightgrey', width=2)

        globals.BTN_LEFT.pack(side="left", padx=5)

        globals.YEAR_LABEL.pack(side="left", padx=10)
        if next_year:
            imagepath = app_data_dir / f"calendar{globals.CURRENT_YEAR1 + 1}.png"
            globals.BTN_RIGHT = tk.Button(upper_frame, text=">", highlightbackground='lightgrey', width=2,
                                          command=lambda: yearly_arrows(clndr, imagepath, 1))

        else:
            globals.BTN_RIGHT = tk.Button(upper_frame, text="", highlightbackground='lightgrey', width=2)

        globals.BTN_RIGHT.pack(side="left", padx=5)

        clndr.pack()

        imagepath1 = app_data_dir



        flag = monthly_activity_in_minutes(data, get_app_data_dir())
        image_path1 = all_habits_grid_plot(data, month=globals.CURRENT_MONTH, cur_month=globals.CONT_MONTH,
                                           year=globals.CURRENT_YEAR1, output_dir=imagepath1)
        labelim1_state = False
        labelim1 = tk.Label()
        if flag:
            imgm = Image.open(
                f"{app_data_dir}/activity_month_{int(globals.CURRENT_YEAR1)}-{int(globals.CURRENT_MONTH):02d}_combined.png")
            frame_width = int(imgm.size[0] * 0.8)
            frame_height = int(imgm.size[1] * 0.8)

            imgm = imgm.resize((frame_width, frame_height), Image.Resampling.LANCZOS)

            tk_imagem = ImageTk.PhotoImage(imgm)
            labelim1 = tk.Label(top_frame, image=tk_imagem, bg='lightgrey')
            labelim1_state = True
            labelim1.image = tk_imagem

        img1 = Image.open(image_path1)
        tk_image1 = ImageTk.PhotoImage(img1)

        label = tk.Label(top_frame, text="Monthly Activity", bg='lightgrey', fg='black')
        label.pack()
        labelim = tk.Label(top_frame, image=tk_image1, bg='lightgrey')
        labelim.image = tk_image1



        upper_frame1 = tk.Frame(top_frame, bg="lightgrey")
        upper_frame1.pack(expand=True)

        previous_month, next_month, cont_month = months(
            datetime(globals.CURRENT_YEAR, globals.CURRENT_MONTH, 1).strftime("%Y-%m"))

        globals.MONTH_LABEL = tk.Label(upper_frame1,
                                       text=f"{calendar.month_name[globals.CURRENT_MONTH]} {globals.CURRENT_YEAR}",
                                       bg='lightgrey', font=("Arial", 14))

        if previous_month:
            globals.MBTN_LEFT = tk.Button(upper_frame1, text="<", highlightbackground='lightgrey', width=2,
                                          command=lambda: monthly_arrows(labelim, labelim1, app_data_dir, -1, data))

        else:
            globals.MBTN_LEFT = tk.Button(upper_frame1, text="", highlightbackground='lightgrey', width=2)

        globals.MBTN_LEFT.pack(side="left", padx=5)

        globals.MONTH_LABEL.pack(side="left", padx=10)
        if next_month:
            globals.MBTN_RIGHT = tk.Button(upper_frame1, text=">", highlightbackground='lightgrey', width=2,
                                           command=lambda: monthly_arrows(labelim, labelim1, app_data_dir, 1, data))

        else:
            globals.MBTN_RIGHT = tk.Button(upper_frame1, text="", highlightbackground='lightgrey', width=2)

        globals.MBTN_RIGHT.pack(side="left", padx=5)

        labelim.pack()
        if labelim1_state :
            labelim1.pack()

        middle_frame = tk.Frame(scrollable_frame, bg="lightgrey", height=150)
        middle_frame.pack(side="top", fill="x")
        label1 = tk.Label(middle_frame, text='Current Active Streaks', bg='lightgrey', fg='black')
        label1.pack()

        middle_left_frame = tk.Frame(middle_frame, bg="lightgrey", width=400, height=150)
        middle_left_frame.pack(side="left", fill="both", expand=True)

        middle_right_frame = tk.Frame(middle_frame, bg="lightgrey", width=400, height=150)
        middle_right_frame.pack(side="right", fill="both", expand=True)

        label1 = tk.Label(middle_left_frame, text='Daily:', bg='lightgrey', fg='black')
        label1.pack()
        topd = top[top['freq'] == 'Daily']
        streaks1 = streaks[streaks['Name'].isin(topd['Name'])]
        for i, name, n in zip(range(1, len(streaks1) + 1), streaks1['Name'], streaks1['max_consecutive_days']):
            label1 = tk.Label(middle_left_frame, text=f"{name}: {n} Day{'s' if n != 1 else ''}", fg="black", bg="pink",
                              anchor="w",
                              font=("Helvetica", 14, "bold"))
            label1.pack(anchor='w')

        label1 = tk.Label(middle_right_frame, text='Weekly:', bg='lightgrey', fg='black')
        label1.pack()

        for i, name, n in zip(range(1, len(topw) + 1), topw['Name'], topw['max_consecutive_days']):
            label1 = tk.Label(middle_right_frame, text=f"{name}: {n} Week{'s' if n != 1 else ''}", fg="black",
                              bg="pink", anchor="w",
                              font=("Helvetica", 14, "bold"))
            label1.pack(anchor='w')

        bottom_frame = tk.Frame(scrollable_frame, bg="lightgrey", height=150)
        bottom_frame.pack(side="top", fill="x")

        label1 = tk.Label(bottom_frame, text='Historical top Runs', bg='lightgrey', fg='black')
        label1.pack()
        bottom_left_frame = tk.Frame(bottom_frame, bg="lightgrey", width=400, height=150)
        bottom_left_frame.pack(side="left", fill="both", expand=True)

        bottom_right_frame = tk.Frame(bottom_frame, bg="lightgrey", width=400, height=150)
        bottom_right_frame.pack(side="right", fill="both", expand=True)

        label1 = tk.Label(bottom_left_frame, text='Daily:', bg='lightgrey', fg='black')
        label1.pack()
        topd = top[top['freq'] == 'Daily']
        for j, name, n in zip(range(1, len(topd) + 1), topd['Name'], topd['max_consecutive_days']):
            label1 = tk.Label(bottom_left_frame, text=f"{name}: {n} Day{'s' if n != 1 else ''}", fg="black", bg="pink",
                              anchor="w",
                              font=("Helvetica", 14, "bold"))
            label1.pack(anchor='w')

        label1 = tk.Label(bottom_right_frame, text='Weekly:', bg='lightgrey', fg='black')
        label1.pack()
        topw = top[top['freq'] == 'Weekly']
        for j, name, n in zip(range(1, len(topw) + 1), topw['Name'], topw['max_consecutive_days']):
            label1 = tk.Label(bottom_right_frame, text=f"{name}: {n} Week{'s' if n != 1 else ''}", fg="black",
                              bg="pink", anchor="w",
                              font=("Helvetica", 14, "bold"))
            label1.pack(anchor='w')

        bottom_level2_frame = tk.Frame(scrollable_frame, bg="lightgrey", height=150)
        bottom_level2_frame.pack(side="top", fill="both")
        label1 = tk.Label(bottom_level2_frame, text='"Per" stats', bg='lightgrey', fg='black')
        label1.pack(pady=20)

        bottom_level2_left_frame = tk.Frame(bottom_level2_frame, bg="lightgrey", width=400, height=150)
        bottom_level2_left_frame.pack(side="left", fill="both", expand=True)

        bottom_level2_middle_frame = tk.Frame(bottom_level2_frame, bg="lightgrey", width=400, height=150)
        bottom_level2_middle_frame.pack(side="right", fill="both", expand=True)

        label1 = tk.Label(bottom_level2_left_frame, text='Times per Week:', bg='lightgrey', fg='black')
        label1.pack()

        for j, name, n in zip(range(1, len(perstats) + 1), perstats['Name'], perstats['perweek']):
            if perstats[perstats['Name'] == name]['Frequency'].item() != 'Weekly':
                label1 = tk.Label(bottom_level2_left_frame,
                                  text=f"{name}: {np.round(n, 1)} Time{'s' if n != 1 else ''}", fg="black", bg="pink",
                                  anchor="w",
                                  font=("Helvetica", 14, "bold"))
                label1.pack(anchor='w')

        label1 = tk.Label(bottom_level2_middle_frame, text='Weeks Per Month:', bg='lightgrey', fg='black')
        label1.pack()
        perstats = perstats.sort_values(by=['weekspermonth'], ascending=False)
        for j, name, n in zip(range(1, len(perstats) + 1), perstats['Name'], perstats['weekspermonth']):
            label1 = tk.Label(bottom_level2_middle_frame, text=f"{name}: {np.round(n, 1)} Week{'s' if n != 1 else ''}",
                              fg="black", bg="pink",
                              anchor="w",
                              font=("Helvetica", 14, "bold"))
            label1.pack(anchor='w')

        bottom_level3_frame = tk.Frame(scrollable_frame, bg="lightgrey", height=150)
        bottom_level3_frame.pack(side="top", fill="x", )

        bottom_level3_left_frame = tk.Frame(bottom_level3_frame, bg="lightgrey", width=400, height=150)
        bottom_level3_left_frame.pack(side="left", fill="both", expand=True)

        bottom_level3_middle_frame = tk.Frame(bottom_level3_frame, bg="lightgrey", width=400, height=150)
        bottom_level3_middle_frame.pack(side="left", fill="both", expand=True)

        label1 = tk.Label(bottom_level3_left_frame, text='Times per Month:', bg='lightgrey', fg='black')
        label1.pack()
        perstats = perstats.sort_values(by=['permonth'], ascending=False)
        for j, name, n in zip(range(1, len(perstats) + 1), perstats['Name'], perstats['permonth']):
            if perstats[perstats['Name'] == name]['Frequency'].item() != 'Weekly':
                label1 = tk.Label(bottom_level3_left_frame,
                                  text=f"{name}: {np.round(n, 1)} Time{'s' if n != 1 else ''}",
                                  fg="black", bg="pink",
                                  anchor="w",
                                  font=("Helvetica", 14, "bold"))
                label1.pack(anchor='w')

        if 'minutesperday' in perstats.columns:
            label1 = tk.Label(bottom_level3_middle_frame, text='Minutes per Day:', bg='lightgrey', fg='black')
            label1.pack()
            perstats = perstats.sort_values(by=['minutesperday'], ascending=False).dropna()
            for j, name, n in zip(range(1, len(perstats) + 1), perstats['Name'], perstats['minutesperday']):
                label1 = tk.Label(bottom_level3_middle_frame,
                                  text=f"{name}: {np.round(n, 1)} Minute{'s' if n != 1 else ''}",
                                  fg="black", bg="pink",
                                  anchor="w",
                                  font=("Helvetica", 14, "bold"))
                label1.pack(anchor='w')

        flaga, flagb = create_activity(tmps1, of=app_data_dir)

        if flaga:
            label = tk.Label(scrollable_frame, text="Activity Patters", bg='lightgrey', fg='blue')
            label.pack()

            img1 = Image.open(f"{app_data_dir}/activity_combined.png")
            tk_image1 = ImageTk.PhotoImage(img1)
            labela = tk.Label(scrollable_frame, image=tk_image1, bg='lightgrey')
            labela.image = tk_image1
            labela.pack()

        if flagb:
            label = tk.Label(scrollable_frame, text="Activity for Stopwatch Habits", bg='lightgrey', fg='blue')
            label.pack()

            img1 = Image.open(f"{app_data_dir}/activity_minutes_combined.png")

            tk_image1 = ImageTk.PhotoImage(img1)
            labela = tk.Label(scrollable_frame, image=tk_image1, bg='lightgrey')
            labela.image = tk_image1
            labela.pack()


    except Exception as e:
        print(e)
        no_data_label = tk.Label(top_frame, text="No Data", bg='lightgrey', fg='black')
        no_data_label.pack(side="right", padx=5)



