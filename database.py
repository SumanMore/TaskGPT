import pyodbc
import os
import atexit 
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Constants
DATABASE_SERVER = os.getenv("database_server")
DATABASE_NAME = os.getenv("database_name")
DATABASE_USERNAME = os.getenv("database_username")
DATABASE_PASSWORD = os.getenv("database_password")

# Database connection string
connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={DATABASE_SERVER};DATABASE={DATABASE_NAME};UID={DATABASE_USERNAME};PWD={DATABASE_PASSWORD}'

# Establish database connection
def establish_connection():
    connection = pyodbc.connect(connection_string)
    cursor=connection.cursor()
    return connection,cursor

def close_connection(connection, cursor):
    cursor.close()
    connection.close()

# Create a task table if it doesn't exist
def create_task():
    connection,cursor=establish_connection()
    cursor.execute("""
            IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'task')
            BEGIN
                CREATE TABLE task (
                    Defined_task VARCHAR(255),
                    Status VARCHAR(20),
                    Start_Date DATE,
                    End_Date DATE
                )
            END
        """)
    connection.commit()
    close_connection(connection, cursor)

# Insert a task into the database
def insert_task(defined_task, status, start_date, end_date):
    connection,cursor=establish_connection()
    cursor.execute("INSERT INTO task (Defined_task, Status, Start_Date, End_Date) VALUES (?, ?, ?, ?)", (defined_task, status, start_date, end_date))
    connection.commit()
    close_connection(connection, cursor)


# Get all data from the database
def get_all_data():
    connection,cursor=establish_connection()
    cursor.execute("SELECT * FROM task")
    fetch_all_tasks = cursor.fetchall()
    close_connection(connection, cursor)
    return fetch_all_tasks
    

#Get all defined task from database
def get_all_defined_task():
    connection,cursor=establish_connection()
    cursor.execute("Select Defined_task from task")
    fetch_data=cursor.fetchall()
    Task_as_list=[]
    for i in fetch_data:
        Task_as_list.append(i[0])
    close_connection(connection, cursor)
    return Task_as_list
    

# Update a task in the database
def update_task(defined_task, status, start_date, end_date):
    connection,cursor=establish_connection()
    cursor.execute("UPDATE task SET Status=?, Start_Date=?, End_Date=? WHERE Defined_task=?", (status, start_date, end_date, defined_task))
    connection.commit()
    close_connection(connection, cursor)
    
# Delete a task from the database
def delete_task(defined_task):
    connection,cursor=establish_connection()
    cursor.execute("DELETE FROM task WHERE Defined_task=?", (defined_task,))
    connection.commit()
    close_connection(connection, cursor)
    
#Get data of a particular task from the database
def get_task_data(value):
    connection,cursor=establish_connection()
    cursor.execute("Select Status,Start_Date,End_Date from task where Defined_task= ? ",(value))
    fetch_data=cursor.fetchall()
    close_connection(connection, cursor)
    return fetch_data
    
#Get status of a particular task from the database
def get_status(value):
    connection,cursor=establish_connection()
    cursor.execute("Select Status from task where Defined_task= ? ",(value))
    fetch_data=cursor.fetchall()
    close_connection(connection, cursor)
    return fetch_data[0][0]
    


