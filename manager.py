import sqlite3
import string
import random


def start():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS passwords (
                            name text,
                            platform text,
                            password text
                            )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (
                            name text,
                            password text
                            )""")
    connection.commit()
    connection.close()
    prompt_login()


def prompt_login():
    print('*'*15)
    print('quit = quit')
    print('add = add account')
    print('login = login')
    print('*' * 15)
    selected = input(': ')

    if selected == 'quit':
        exit()
    elif selected == 'add':
        print('\n')
        add_account()
    elif selected == 'login':
        print('\n')
        login()
    else:
        print('Unknown function.\n')
        prompt_login()


def add_account():
    name = input('Enter your account name: ')
    password = input('Enter your account master password: ')

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO accounts VALUES ('{name}', '{password}')")
    connection.commit()
    connection.close()
    print(f'Your account has been created.\n')
    prompt_login()


def login():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    name = input('Enter your account name: ')

    cursor.execute(f"SELECT name FROM accounts")
    names = str(cursor.fetchall())

    if name not in names:
        print(f'Invalid name.\n')
        login()

    password_input = input('Enter your master password: ')

    cursor.execute(f"SELECT password FROM accounts WHERE name='{name}'")
    password = str(cursor.fetchone())[2:][:-3]

    connection.commit()
    connection.close()

    if password_input == password:
        print('Logged in successfully.\n')
        prompt(name)
    else:
        print('Invalid password.\n')
        login()


def prompt(name: str):
    print('*'*15)
    print('quit = quit')
    print('store = store password')
    print('get = get password')
    print('logout = logout')
    print('*'*15)
    selected = input(': ')

    if selected == 'quit':
        exit()
    elif selected == 'store':
        print('\n')
        store_password(name)
    elif selected == 'get':
        print('\n')
        get_password(name)
    elif selected == 'logout':
        print('Logged out.\n')
        prompt_login()
    else:
        print('Unknown function.\n')
        prompt(name)


def store_password(name: str):
    platform = input('Enter the name of the platform: ')
    password = generate_password()
    print(f'Your new password is: {password}')

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO passwords VALUES ('{name}', '{platform}', '{password}')")
    connection.commit()
    connection.close()
    print('Password saved.\n')
    prompt(name)


def get_password(name: str):
    platform = input('Enter the name of the platform: ')

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f"SELECT password FROM passwords WHERE platform='{platform}' AND name='{name}'")
    password = str(cursor.fetchone())[2:][:-3]
    connection.commit()
    connection.close()
    if password != '':
        print(f'Your password is {password}\n')
    else:
        print('There is no password available.\n')
    prompt(name)


def generate_password():
    characters, password = list(string.ascii_letters + '0123456789'), ''
    for x in range(10):
        index = random.randint(0, len(characters) - 1)
        password += characters[index]
    return password


if __name__ == '__main__':
    start()
