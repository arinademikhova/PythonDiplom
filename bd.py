import sqlite3
import pandas as pd
import datetime
from config import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

def date_to_ms(date_obj):
    dt = datetime.datetime.combine(date_obj, datetime.time.min)
    return int(dt.timestamp() * 1000)

def get_list_hotels():
    conn = get_connection()
    df = pd.read_sql("SELECT name FROM hotels ORDER BY name", conn)
    conn.close()
    return df['name'].tolist()

def get_list_sections():
    conn = get_connection()
    df = pd.read_sql("SELECT name FROM sections WHERE deleted = 0 ORDER BY name", conn)
    conn.close()
    return df['name'].tolist()

def get_list_service_types():
    conn = get_connection()
    df = pd.read_sql("SELECT name FROM services_type WHERE deleted = 0 ORDER BY name", conn)
    conn.close()
    return df['name'].tolist()

def get_total_rooms_count():
    conn = get_connection()
    total = pd.read_sql("SELECT COUNT(*) as cnt FROM rooms WHERE deleted = 0", conn).iloc[0]['cnt']
    conn.close()
    return total