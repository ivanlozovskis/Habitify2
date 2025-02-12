import mysql.connector
import pandas as pd
import json

with open("config.json", "r") as file:
    config = json.load(file)['database']
# all functions to handle database



def get_connection(dbname = config['database_name']):
    return mysql.connector.connect(
        host=config['host'],
        database=dbname,
        user=config['user'],
        password=config['password']
    )

def create_database_if_not_exists():
    try:
        conn = get_connection(None)  # Connect without specifying a database
        cursor = conn.cursor()

        # Check if the database exists
        cursor.execute(f"SHOW DATABASES LIKE '{config['database_name']}'")
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {config['database_name']}")
            print(f"Database '{config['database_name']}' created successfully.")
        else:
            # print(f"Database '{config['database_name']}' already exists.")
            print('all good')

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def initialize_database():
    """Ensure the database exists, then connect and set up tables if needed."""
    create_database_if_not_exists()

    # Now connect to the created database and initialize tables if needed
    conn = get_connection()
    cursor = conn.cursor()

    # Example: Create a sample table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Habit(
        ID int AUTO_INCREMENT,
        Name varchar(15),
        Description varchar(255),
        Frequency varchar(10),
        Stopwatch int DEFAULT False,
        Created timestamp DEFAULT CURRENT_TIMESTAMP,
        Deleted timestamp, 
        PRIMARY KEY (ID)
        );
    """)

    # Example: Create a sample table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Log(
        ID int AUTO_INCREMENT,
        Habit_id int,
        dt timestamp DEFAULT CURRENT_TIMESTAMP,
        TimeSpent time,
        PRIMARY KEY (ID),
        FOREIGN KEY (Habit_id) REFERENCES Habit(ID)
        );
    """)


    # print("Tables checked/created successfully.")



def select(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    df = pd.DataFrame(result, columns=columns)
    return df

def select_one(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()[0]
    return result

def insert_update(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()



def get_active_habits(connection):
    return select(connection, "SELECT * FROM Habit WHERE Deleted is Null;")

def get_latest_check(connection):
    return select(connection, "SELECT Habit_id, MAX(dt) as latest_check FROM Log GROUP BY Habit_id;")

def get_timespent(connection, habit_id):
    result = select_one(connection, f"SELECT sum(TIME_TO_SEC(TimeSpent)) FROM Log WHERE (DATE(dt) = CURDATE()) and (Habit_id = {habit_id});")
    return result if result is not None else 0

def get_log(connection):
    return select(connection,"SELECT l.Habit_id, l.dt, l.TimeSpent, h.Name, h.Description, h.Frequency, h.Stopwatch, h.Created, h.Deleted FROM Log l left join Habit h on l.Habit_id=h.id where h.Deleted is Null union SELECT l.Habit_id, l.dt, l.TimeSpent, h.Name, h.Description, h.Frequency, h.Stopwatch, h.Created, h.Deleted FROM Log l right join Habit h on l.Habit_id=h.id where h.Deleted is Null;")

def get_created(connection):
    return select(connection, "SELECT ID, Created, Deleted from Habit;")

def get_habit_counts(connection):
    return select(connection,"""SELECT 
    COUNT(DISTINCT l.habit_id) AS count, 
    DAYOFYEAR(l.dt) AS doy, 
    YEAR(l.dt) AS year, 
    DATE_FORMAT(l.dt, '%Y-%m-%d') AS dt
    FROM Log l
    JOIN Habit h ON l.habit_id = h.id
    WHERE h.deleted IS NULL OR DATE(h.created) <> DATE(h.deleted)  
    GROUP BY DAYOFYEAR(l.dt), YEAR(l.dt), DATE_FORMAT(l.dt, '%Y-%m-%d');
""")


####needed to have the same habit_id in the class Habit as in Habit table when a habit is created
def iterate_id(connection):
    return select_one(connection, "SELECT MAX(ID) FROM Habit;")


def add_log(connection, habit_id, TimeSpent=None, time=None):

    if time in [None,"'None'",'"None"']:
        if TimeSpent in [None, '"None"', "'None'"]:
            query = f"INSERT INTO Log (Habit_id) VALUES ({habit_id});"
        else:
            query = f"INSERT INTO Log (Habit_id, TimeSpent) VALUES ({habit_id}, {TimeSpent});"
    else:
        if TimeSpent in [None,"'None'",'"None"']:
            query = f"INSERT INTO Log (Habit_id, dt) VALUES ({habit_id}, {time});"
        else:
            query = f"INSERT INTO Log (Habit_id, TimeSpent, dt) VALUES ({habit_id}, {TimeSpent}, {time});"
    insert_update(connection, query)


def add_habit(connection, Name, Description, Frequency, Stopwatch, created=None):
    if created==None:
        insert_update(connection, f"INSERT INTO Habit (Name, Description, Frequency, Stopwatch) VALUES ({Name}, {Description}, {Frequency}, {Stopwatch});")
    else:
        insert_update(connection,
                      f"INSERT INTO Habit (Name, Description, Frequency, Stopwatch, Created) VALUES ({Name}, {Description}, {Frequency}, {Stopwatch}, {created});")


def delete_habit(connection, habit_id, deleted):
    insert_update(connection, f"UPDATE Habit SET Deleted = '{deleted}' WHERE ID = {habit_id};")


def reset(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"Delete from {table_name};")
    connection.commit()


