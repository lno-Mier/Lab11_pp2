import psycopg2

conn = psycopg2.connect(
    dbname="lab10",
    user="postgres",
    password="heroes951",
    host="127.0.0.1",
    port="5432"
)

def get_connection():
    return psycopg2.connect(
        dbname="lab10",
        user="postgres",
        password="heroes951",
        host="127.0.0.1",
        port="5432"
    )

def get_record(pattern):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT first_name, last_name, phone_number 
                    FROM phonebook 
                    WHERE first_name LIKE %s OR last_name LIKE %s OR phone_number LIKE %s
                """, (f"%{pattern}%", f"%{pattern}%", f"%{pattern}%"))
                result = cur.fetchall()
                return result
    except (psycopg2.DatabaseError, Exception) as error:
        print("Ошибка при получении данных:", error)

def upsert(first_name, last_name, phone_number):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert(%s, %s, %s)", (first_name, last_name, phone_number))
        print("Успешно!")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Ошибка при вставке данных:", error)

def delete_by_name(first_name, last_name):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_by_name(%s, %s)", (first_name, last_name))
                if conn.notices:
                    for notice in conn.notices:
                        print("Ошибка:", notice.strip())
                else:
                    print("Успешно удалено!")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Ошибка при удалении данных:", error)

def delete_by_phone(phone_number):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_by_phone(%s)", (phone_number,))
                if conn.notices:
                    for notice in conn.notices:
                        print(notice.strip())
                else:
                    print("Успешно удалено!")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Ошибка при удалении данных:", error)

if __name__ == "__main__":
    choose_box = '''
    1. Вставка данных
    2. Поиск данных
    3. Удаление данных
    '''
    print(choose_box)
    n = int(input("Введите номер запроса: "))
    if n == 1:
        first_name = input("Введите имя: ")
        last_name = input("Введите фамилию: ")
        phone_number = input("Введите номер телефона: ")
        upsert(first_name, last_name, phone_number)
    elif n == 2:
        pattern = input("Введите шаблон для поиска: ")
        records = get_record(pattern)
        for record in records:
            print(record)
    elif n == 3:
        choose_box_del = '''
        1. Удалить по имени и фамилии
        2. Удалить по номеру телефона
        '''
        print(choose_box_del)
        
        q = int(input("Введите номер запроса: "))
        
        if q == 1:
            first_name = input("Введите имя: ")
            last_name = input("Введите фамилию: ")
            delete_by_name(first_name, last_name)
        elif q == 2:
            phone_number = input("Введите номер телефона: ")
            delete_by_phone(phone_number)
    else:
        print("Неверный ввод!")