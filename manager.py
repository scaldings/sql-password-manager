import string
import random
import stdiomask
import os
import creds
import mysql.connector
import time


def connect():
    connection = mysql.connector.connect(
        host=creds.HOST,
        user=creds.USER,
        password=creds.PASSWORD,
        database=creds.DATABASE
    )
    return connection


def start():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS manager_passwords (
                            name text,
                            platform text,
                            password text
                            )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS manager_accounts (
                            name text,
                            password text
                            )""")
    connection.commit()
    connection.close()
    cls()
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
        cls()
        print('Unknown function.\n')
        prompt_login()


def add_account():
    connection = connect()
    cursor = connection.cursor()

    name = input('Enter your account name: ')
    cursor.execute(f"SELECT name FROM manager_accounts")
    names = str(cursor.fetchall())

    if name in names:
        cls()
        print(f'Name already in use.\n')
        prompt_login()

    password_input = stdiomask.getpass('Enter your account master password: ')

    cursor.execute(f"INSERT INTO manager_accounts VALUES ('{name}', '{password_input}')")
    connection.commit()
    connection.close()
    cls()
    print(f'Your account has been created.\n')
    prompt_login()


def login():
    cls()
    connection = connect()
    cursor = connection.cursor()

    name = input('Enter your account name: ')
    cursor.execute(f"SELECT name FROM manager_accounts")
    names = format_result(cursor.fetchall())
    if name not in names:
        print(f'Invalid name.\n')
        login()

    password_input = stdiomask.getpass(prompt='Enter your master password: ')

    cursor.execute(f"SELECT password FROM manager_accounts WHERE name='{name}'")
    password = format_result(cursor.fetchone())

    connection.close()

    if password_input == password:
        print('Logged in successfully.\n')
        prompt(name)
    else:
        print('Invalid password.\n')
        login()


def prompt(name: str):
    cls()
    print('*'*15)
    print('quit = quit')
    print('store = store password')
    print('get = get password')
    print('remove = remove password')
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
    elif selected == 'remove':
        print('\n')
        remove_password(name)
    elif selected == 'logout':
        cls()
        print('Logged out.\n')
        prompt_login()
    else:
        print('Unknown function.\n')
        prompt(name)


def store_password(name: str):
    cls()
    platform = input('Enter the name of the platform: ')
    print('*'*15)
    print('gen = generate random password')
    print('in = input your own password')
    print('*'*15)
    selected = input(': ')

    if selected == 'gen':
        password = generate_password()
        print(f'Your new password is: {password}')
    elif selected == 'in':
        password = input('Enter your password: ')
        print(f'Your password is: {password}')
    else:
        print('Unknown function.\n')
        store_password(name)

    connection = connect()
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO manager_passwords VALUES ('{name}', '{platform}', '{password}')")
    connection.commit()
    connection.close()
    print('Password saved.\n')
    prompt(name)


def get_password(name: str):
    cls()
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT platform FROM manager_passwords WHERE name='{name}'")
    platforms = format_result(cursor.fetchall())

    print('*'*15)
    if type(platforms) == list:
        for platform in platforms:
            print(platform)
    else:
        if platforms is not None:
        	print(platforms[0])
        else:
        	print(platforms)
    print('*'*15 + '\n')

    if platforms is not None:
        platform_input = input('Enter the name of the platform: ')
        cursor.execute(f"SELECT password FROM manager_passwords WHERE platform='{platform_input}' AND name='{name}'")
        password = format_result(cursor.fetchone())
        if password != '':
            print(f'Your password for {platform_input} is {password}\n')
            time.sleep(7)
        else:
            print('There is no password available.\n')
    else:
        time.sleep(3)
    connection.commit()
    connection.close()
    prompt(name)


def remove_password(name: str):
    cls()
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(f"SELECT platform FROM manager_passwords WHERE name='{name}'")
    platforms = format_result(cursor.fetchall())

    print('*'*15)
    if type(platforms) == list:
        for platform in platforms:
            print(platform)
    else:
        if platforms is not None:
        	print(platforms[0])
        else:
        	print(platforms)
    print('*'*15 + '\n')

    if platforms is not None:
        platform_input = input('Enter the name of the platform: ')
        cursor.execute(f"DELETE platform FROM manager_passwords WHERE platform='{platform_input}'")
        print('Password removed.')
    else:
        time.sleep(3)
    connection.commit()
    connection.close()
    prompt(name)
    

def generate_password():
    characters, password = list(string.ascii_letters + '0123456789'), ''
    for x in range(10):
        index = random.randint(0, len(characters) - 1)
        password += characters[index]
    return password


def format_result(result):
    formatted = []
    if len(result) > 0:
        if len(result) > 1:
            for x in range(0, len(result)):
                formatted.append(result[x][0])
        else:
            return result[0]
    else:
        return None
    if len(formatted) == 1:
        return formatted[0]
    else:
        return formatted


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    start()
