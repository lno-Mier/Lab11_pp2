import psycopg2

conn = psycopg2.connect(
    dbname="lab10",
    user="postgres",
    password="heroes951",
    host="127.0.0.1",
    port="5432"
)

curr = conn.cursor()

def get_connection():
    return psycopg2.connect(**conn)

def get_record(pattern):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT get_record(%s)", (pattern,))
                result = cur.fetchall()
                return result
    except (psycopg2.DatabaseError, Exception) as error:
        print("Ошибка при получении данных:", error)

def upsert(name, phone):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert(%s, %s)", (name, phone))
        print("Успешно!")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Ошибка при вставке данных:", error)

def delete(name, phone):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL deleting(%s, %s)", (name, phone))
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
        name = input("Введите имя: ")
        phone = input("Введите номер телефона: ")
        upsert(name, phone)
    elif n == 2:
        pattern = input("Введите шаблон для поиска: ")
        records = get_record(pattern)
        for record in records:
            print(record)
    elif n == 3:
        name = input("Введите имя для удаления: ")
        phone = input("Введите номер телефона для удаления: ")
        delete(name, phone)
    else:
        print("Неверный ввод!")
        
    conn.commit()
    curr.close()
    conn.close()