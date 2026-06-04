from bd import get_connection, get_list_hotels

conn = get_connection()
if conn:
    print("Подключение успешно!")
    hotels = get_list_hotels()
    print(f"Найдено отелей: {len(hotels)}")
    conn.close()
else:
    print("Не удалось подключиться")