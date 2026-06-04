#import sqlite3
import pandas as pd
import datetime
#from config import DB_PATH
import pymysql
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

#def get_connection():
    #return sqlite3.connect(DB_PATH)

def get_connection():
    try:
        conn = pymysql.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        st.error(f"Ошибка подключения к MySQL: {e}")
        return None


def date_to_ms(date_obj):
    dt = datetime.datetime.combine(date_obj, datetime.time.min)
    return int(dt.timestamp() * 1000)

def get_list_hotels():
    try:
        conn = get_connection()
        if conn is None:
            return []
        df = pd.read_sql("SELECT name FROM hotels ORDER BY name", conn)
        conn.close()
        return df['name'].tolist()
    except Exception as e:
        st.error(f"Ошибка загрузки списка отелей: {e}")
        return []

def get_list_sections():
    try:
        conn = get_connection()
        if conn is None:
            return []
        df = pd.read_sql("SELECT name FROM sections WHERE deleted = 0 ORDER BY name", conn)
        conn.close()
        return df['name'].tolist()
    except Exception as e:
        st.error(f"Ошибка загрузки списка секций: {e}")
        return []

def get_list_service_types():
    try:
        conn = get_connection()
        if conn is None:
            return []
        df = pd.read_sql("SELECT name FROM services_type WHERE deleted = 0 ORDER BY name", conn)
        conn.close()
        return df['name'].tolist()
    except Exception as e:
        st.error(f"Ошибка загрузки типов услуг: {e}")
        return []

def load_fund_data(date_from, date_to, hotel=None, sections=None):
    try:
        conn = get_connection()
        if conn is None:
            return pd.DataFrame()
        from_ms = date_to_ms(date_from)
        to_ms = date_to_ms(date_to) + 24*60*60*1000 - 1

        query = """
            SELECT 
                frl.reservation_id,
                frl.client_id,
                frl.paid,
                frl.realprice,
                frl.howadult,
                frl.howteenager,
                frl.howchild,
                fr.reserv_date,
                fr.time,
                r.room_id,
                r.name AS item_name,
                s.name AS section_name,
                h.name AS hotel_name
            FROM fund_reserv_list frl
            JOIN fund_reservation fr ON frl.reservation_id = fr.reservation_id
            JOIN rooms r ON fr.room_id = r.room_id
            JOIN sections s ON r.section_id = s.section_id
            JOIN hotels h ON s.hotel_id = h.hotel_id
            WHERE fr.reserv_date BETWEEN %s AND %s
                AND r.enable = 1
                AND r.deleted = 0
        """
        params = [from_ms, to_ms]
        if hotel and hotel != "Все":
            query += " AND h.name = %s"
            params.append(hotel)
        if sections:
            placeholders = ','.join(['%s'] * len(sections))
            query += f" AND s.name IN ({placeholders})"
            params.extend(sections)

        df = pd.read_sql(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Ошибка загрузки данных размещения: {e}")
        return pd.DataFrame()

def load_services_data(date_from, date_to, hotel=None, sections=None, service_types=None):
    try:
        conn = get_connection()
        if conn is None:
            return pd.DataFrame()
        from_ms = date_to_ms(date_from)
        to_ms = date_to_ms(date_to) + 24*60*60*1000 - 1

        query = """
            SELECT 
                srl.reservation_id,
                srl.client_id,
                srl.paid,
                srl.realprice,
                sr.reserv_date,
                sr.timefrom,
                '' as client_fio,
                serv.name AS item_name,
                st.name AS service_type_name,
                s.name AS section_name,
                h.name AS hotel_name
            FROM service_reserv_list srl
            JOIN service_reservation sr ON srl.reservation_id = sr.reservation_id
            JOIN services serv ON sr.service_id = serv.service_id
            JOIN services_type st ON serv.service_type_id = st.service_type_id
            JOIN sections s ON serv.section_id = s.section_id
            JOIN hotels h ON s.hotel_id = h.hotel_id
            WHERE sr.reserv_date BETWEEN %s AND %s
                AND serv.enable = 1
                AND serv.deleted = 0
        """
        params = [from_ms, to_ms]
        if hotel and hotel != "Все":
            query += " AND h.name = %s"
            params.append(hotel)
        if sections:
            placeholders = ','.join(['%s'] * len(sections))
            query += f" AND s.name IN ({placeholders})"
            params.extend(sections)
        if service_types:
            placeholders = ','.join(['%s'] * len(service_types))
            query += f" AND st.name IN ({placeholders})"
            params.extend(service_types)

        df = pd.read_sql(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Ошибка загрузки данных услуг: {e}")
        return pd.DataFrame()

def get_all_sections_with_room_count():
    try:
        conn = get_connection()
        if conn is None:
            return pd.DataFrame()
        query = """
            SELECT s.name as section_name, COALESCE(COUNT(r.room_id), 0) as total_rooms
            FROM sections s
            LEFT JOIN rooms r ON s.section_id = r.section_id AND r.deleted = 0 AND r.enable = 1
            WHERE s.deleted = 0
            GROUP BY s.section_id
            ORDER BY s.name
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Ошибка подсчёта комнат: {e}")
        return pd.DataFrame()

def get_sections_by_hotel(hotel_name):
    try:
        conn = get_connection()
        if conn is None:
            return []
        if hotel_name == "Все":
            query = "SELECT name FROM sections WHERE deleted = 0 ORDER BY name"
            df = pd.read_sql(query, conn)
        else:
            # Заменили ? на %s
            query = """
                SELECT s.name
                FROM sections s
                JOIN hotels h ON s.hotel_id = h.hotel_id
                WHERE h.name = %s AND s.deleted = 0
                ORDER BY s.name
            """
            df = pd.read_sql(query, conn, params=(hotel_name,))
        conn.close()
        return df['name'].tolist()
    except Exception as e:
        st.error(f"Ошибка загрузки секций по отелю: {e}")
        return []
