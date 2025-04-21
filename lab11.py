import psycopg2

conn = psycopg2.connect(
    dbname="lab10",
    user="postgres",
    password="heroes951",
    host="127.0.0.1",
    port="5432"
)

curr = conn.cursor()

def find(st):
    ptr = f"%{st}%"
    curr.execute(
        "SELECT * FROM phonebook WHERE first_name ILIKE %s OR phone ILIKE %s", (ptr, ptr)
    )
    return curr.fetchall()

def ins_upd(name, phone):
    curr.execute(
        "SELECT * FROM phonebook WHERE first_name = %s", (name,)
    )
    exx = curr.fetchone()

    if exx:
        curr.execute(
            "UPDATE phonebook SET phone = %s WHERE first_name = %s", (phone, name)
        )
        print(f"Updated phone number for {name}")
    else:
        curr.execute(
            "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (name, phone)
        )
        print(f"Dobavlen new user {name}")
    conn.commit()

def val(user_list):
    idata = []

    for name, phone in user_list:
        if not phone.isdigit():
            print(f"Некорректный номер: {phone} — пропущен")
            idata.append((name, phone))
            continue

        curr.execute("SELECT * FROM phonebook WHERE first_name = %s", (name,))
        existing = curr.fetchone()

        if existing:
            curr.execute("UPDATE phonebook SET phone = %s WHERE first_name = %s", (phone, name))
            print(f"Обновлён номер для {name}")
        else:
            curr.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (name, phone))
            print(f"Добавлен {name}")

    conn.commit()
    return idata

def page(lim, offs):
    curr.execute(
        "SELECT * FROM phonebook ORDER BY id LIMIT %s OFFSET %s", (lim, offs)
    )
    return curr.fetchall()

def delete(val):
    curr.execute(
        "DELETE FROM phonebook WHERE first_name = %s OR phone = %s", (val, val)
    )
    conn.commit()
    print(f"Удалены записи с именем или телефоном: {val}")

if __name__ == "__main__":
    menu = '''
        1. find
        2. insert(update)
        3. invalid data
        4. pagination
        5. delete
    '''
    print(menu)
    n = int(input("Выберите операцию: "))

    if n == 1:
        pr = input("Введите какую-то информацию: ")
        users = find(pr)
        for user in users:
            print(user)

    elif n == 2:
        name = input("Введите имя: ")
        phone = input("Введите телефон: ")
        ins_upd(name, phone)

    elif n == 3:
        lists = []
        n = int(input("Сколько пользователей добавить? "))
        for _ in range(n):
            name = input("Имя: ")
            phone = input("Телефон: ")
            lists.append((name, phone))

        nok = val(lists)
        if nok:
            print("Некорректные данные:")
            for i in nok:
                print(i)

    elif n == 4:
        lim = int(input("Сколько записей показать: "))
        page_num = int(input("Номер страницы: "))
        offs = (page_num - 1) * lim
        res = page(lim, offs)
        for r in res:
            print(r)

    elif n == 5:
        v = input("Введите имя или номер для удаления: ")
        delete(v)