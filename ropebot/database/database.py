import sqlite3
import logging

#перед продом удалить все пути!!!
logger = logging.getLogger(__name__)

def _create_connection_and_cursor():
    conn = sqlite3.connect("/Users/User/PycharmProjects\pythonProject5/ropebot/database/ropebot_database.db")
    cursor = conn.cursor()

    return conn, cursor


def create_a_table():
    conn, cursor = _create_connection_and_cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS ropebot_database (
    admin_name TEXT NOT NULL,
    station TEXT NOT NULL,
    ff_group INTEGER 
);
    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks_and_order (
        id INTEGER NOT NULL,
        order TEXT NOT NULL,
        tasks TEXT NOT NULL 
    );
        ''')

    cursor.execute('INSERT INTO tasks_and_order (id, order, tasks) VALUES (?, ?, ?)', (admin_name, station, group))

    conn.commit()
    conn.close()


def get_conntact():
    conn, cursor = _create_connection_and_cursor()
    return conn, cursor

def get_tasks():
    conn, cursor = _create_connection_and_cursor()

    cursor.execute()
def set_data(admin_name: str, station: str, group: int):
    conn, cursor = _create_connection_and_cursor()

    cursor.execute('INSERT INTO ropebot_database (admin_name, station, ff_group) VALUES (?, ?, ?)', (admin_name, station, group))

    conn.commit()
    conn.close()

def get_data():
    conn, cursor = _create_connection_and_cursor()

    cursor.execute('SELECT * FROM ropebot_database')
    data = cursor.fetchall()

    conn.close()

    return data

def delete_a_table():
    conn, cursor = _create_connection_and_cursor()

    try:
        cursor.execute('DROP TABLE ropebot_database')
        cursor.execute('DROP TABLE tasks_and_order')
    except:
        pass

    conn.commit()
    conn.close()
def set_group(ff_group: int, admin_name: str):
    conn, cursor = _create_connection_and_cursor()

    cursor.execute("UPDATE ropebot_database SET ff_group = ? WHERE admin_name = ?", (ff_group, admin_name))

    conn.commit()
    conn.close()


#убрать при выходе в прод - позволяет тестировать
delete_a_table()