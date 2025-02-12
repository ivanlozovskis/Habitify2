import database as db



connection = db.get_connection()


db.reset(connection, "Log")
db.reset(connection, "Habit")