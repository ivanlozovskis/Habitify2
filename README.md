# Habitify

**Habitify** is a habit-tracking application that helps users build and maintain good habits. The app provides a simple interface for tracking habits, viewing progress, and analyzing habit consistency over time.

## Features

- **Track Habits:** Add, edit, and remove habits easily.
- **Progress Analysis:** View habit statistics and streaks.
- **Data Persistence:** Stores habit data in a **local MySQL database**.
- **GUI Interface:** User-friendly graphical interface for easy navigation.



## Installation (Mac)

#### Prerequisites
#### Ensure you have the following installed:

- Python 3.9
- MySQL Server (started with initialized database)
- Required Python libraries (see requirements.txt)
#### Steps
1. Clone the Repository:

```bash
git clone https://github.com/ivanlozovskis/Habitify2.git
cd habitify2
```
2. Install Dependencies:

```bash
pip install -r requirements.txt
```
3. Set Up MySQL Database:
 

- Ensure MySQL server is running.
- DB will be created automatically
- **in the config.json change the "password" to the password to your mysql server**

4. Run testing:

```bash
   python test.py
   ```
**After testing you can switch "freeze" in config.json from 1 to 0 to exit the testing mode (the today's date is set to "2025-01-27 20:05:03")**

If you want to reset the app data you can run:
```bash
   python reset.py
   ```




5. Run the Application:



```bash
   python main.py
   ```



## Usage

1. **Launch the application**
2. **Add new habits** by entering a name, description and selecting a frequency & clock usage.
3. **Track progress** by marking habits as completed ("Done" Checkbox, after starting the clock if the habit is "Stopwatch" type).
Weekly habits streaks are in weeks and Daily habits streaks are in days. "🔥" stands for days/weeks in a row. "⏳" stands for a habit at risk of being lost (ends tomorrow/next week). "😴" stands for amount of days/weeks in a row without checking the habit.
4. **Fill missed data if missed any in the previous day**.
5. **View statistics** in the stats window.
6. **delete habits** as needed.





## Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new feature branch.
3. Commit and push changes.
4. Submit a pull request.


## Contact

For questions or feedback, reach out via GitHub Issues.

