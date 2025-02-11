# Habitify

**Habitify** is a habit-tracking application that helps users build and maintain good habits. The app provides a simple interface for tracking habits, viewing progress, and analyzing habit consistency over time.

## Features

- **Track Habits:** Add, edit, and remove habits easily.
- **Progress Analysis:** View habit statistics and streaks.
- **Data Persistence:** Stores habit data in a **local MySQL database**.
- **GUI Interface:** User-friendly graphical interface for easy navigation.
- **Standalone Executable:** Run the app without needing Python or dependencies.

1.

   ```bash
   python main.py
   ```

## Installation

#### Prerequisites
#### Ensure you have the following installed:

- Python 3.9
- MySQL Server (started with initialized database)
- Required Python libraries (see requirements.txt)
#### Steps
1. Clone the Repository:

```bash
git clone https://github.com/ivanlozovskis/Habitify.git
cd habitify
```
2. Install Dependencies:

```bash
pip install -r requirements.txt
```
3. Set Up MySQL Database:

- Ensure MySQL is running.
- Create a new database:
```bash
CREATE DATABASE Habitify;
```
- Configure database settings in database.py.
4. Run the Application:



```bash
   python main.py
   ```



## Usage

1. **Launch the application**
2. **Add new habits** by entering a name and selecting a frequency.
3. **Track progress** by marking habits as completed.
4. **View statistics** in the analysis window.
5. **Modify or delete habits** as needed.


## Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new feature branch.
3. Commit and push changes.
4. Submit a pull request.


## Contact

For questions or feedback, reach out via GitHub Issues.

