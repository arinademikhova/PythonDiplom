import sqlite3
import pandas as pd
import datetime
from config import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

def date_to_ms(date_obj):
    #преобразование даты в миллисекунды
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

def load_fund_data(date_from, date_to, hotel=None, sections=None):
    conn = get_connection()
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
            r.room_id,
            '' as client_fio,
            r.name AS item_name,
            s.name AS section_name,
            h.name AS hotel_name
        FROM fund_reserv_list frl
        JOIN fund_reservation fr ON frl.reservation_id = fr.reservation_id
        JOIN rooms r ON fr.room_id = r.room_id
        JOIN sections s ON r.section_id = s.section_id
        JOIN hotels h ON s.hotel_id = h.hotel_id
        WHERE fr.reserv_date BETWEEN ? AND ?
            AND r.enable = 1
            AND r.deleted = 0
    """
    params = [from_ms, to_ms]
    if hotel and hotel != "Все":
        query += " AND h.name = ?"
        params.append(hotel)
    if sections:
        placeholders = ','.join(['?'] * len(sections))
        query += f" AND s.name IN ({placeholders})"
        params.extend(sections)

    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def load_services_data(date_from, date_to, hotel=None, sections=None, service_types=None):
    conn = get_connection()
    from_ms = date_to_ms(date_from)
    to_ms = date_to_ms(date_to) + 24*60*60*1000 - 1

    query = """
        SELECT 
            srl.reservation_id,
            srl.client_id,
            srl.paid,
            srl.realprice,
            sr.reserv_date,
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
        WHERE sr.reserv_date BETWEEN ? AND ?
            AND serv.enable = 1
            AND serv.deleted = 0
    """
    params = [from_ms, to_ms]
    if hotel and hotel != "Все":
        query += " AND h.name = ?"
        params.append(hotel)
    if sections:
        placeholders = ','.join(['?'] * len(sections))
        query += f" AND s.name IN ({placeholders})"
        params.extend(sections)
    if service_types:
        placeholders = ','.join(['?'] * len(service_types))
        query += f" AND st.name IN ({placeholders})"
        params.extend(service_types)

    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

#def get_total_rooms_count():
    conn = get_connection()
    total = pd.read_sql("SELECT COUNT(*) as cnt FROM rooms WHERE deleted = 0", conn).iloc[0]['cnt']
    conn.close()
    return total

def get_total_rooms_count():
    conn = get_connection()
    total = pd.read_sql("SELECT COUNT(*) as cnt FROM rooms WHERE deleted = 0 AND enable = 1", conn).iloc[0]['cnt']
    conn.close()
    return total