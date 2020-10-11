#!/usr/bin/python3
from db_config import config
import psycopg2
import re
import sys


def sanitize_data(data):
    return re.sub(r'[^a-zA-Z0-9-%]', '', data)


def check_or_create_table():
    table = '''CREATE TABLE IF NOT EXISTS outgoings(
                        Bill_id SERIAL PRIMARY KEY,
                        Category VARCHAR(50),
                        Description VARCHAR(50),
                        Amount INT, 
                        Created_at TIME DEFAULT CURRENT_TIME,
                        Created_on DATE DEFAULT CURRENT_DATE);'''
    return table


def add_bill():
    c = sanitize_data(input('\nChoose category of your bill: (Food,Others,Tax) '))
    d = sanitize_data(input('Write a short description: '))
    a = sanitize_data(input('Amount: '))
    if a.isdigit():
        statement = f'INSERT INTO outgoings(category,description,amount) VALUES(\'{c}\',\'{d}\',{a});'
        return statement
    else:
        print('Amount must be a digit.')


def sort_by_date():
    y = sanitize_data(input('\nYear: ') or '%')
    m = sanitize_data(input('Month: ') or '%')
    d = sanitize_data(input('Day: ') or '%')
    sort_dates = f'SELECT * from outgoings where CAST(created_on as TEXT) LIKE \'{y}-{m}-{d}\';'
    return sort_dates


def sort_by_category():
    c = sanitize_data(input('Category:') or '%')
    sort_categories = f'SELECT * FROM outgoings WHERE category LIKE \'{c}\';'
    return sort_categories


def sum_amount():
    y = sanitize_data(input('\nYear: ') or '%')
    m = sanitize_data(input('Month: ') or '%')
    d = sanitize_data(input('Day: ') or '%')
    whole_amount = f'SELECT SUM(amount) AS Total FROM outgoings WHERE CAST(created_on as TEXT) LIKE \'{y}-{m}-{d}\';'
    return whole_amount


def list_categories():
    list_cat = 'SELECT DISTINCT category FROM outgoings;'
    return list_cat


def execute_statement(statement):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(statement)
        cur.close()
    except(Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if conn is not None:
            conn.commit()
            conn.close()


def get_response(statement, flag):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        print('\nStatement result:\n')
        cur.execute(statement)
        answ_list = []
        answer = cur.fetchone()
        while answer is not None:
            if flag == 1:
                print(f'Category: {answer[1]}\nDescription: {answer[2]}\nAmount: {answer[3]}\nDate created: {answer[5]}\n')
            elif flag == 2:
                for i in answer:
                    print(i)
            elif flag == 3:
                print(f'Total amount: {answer[0]}\n')
            else:
                pass
            answ_list.append(answer)
            answer = cur.fetchone()
        cur.close()

    except(Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()
            print('\nDatabase connection closed.')


def show_menu():
    while 1:
        print('''
        Menu:
        add - add new data.
        sortbd - sort data by date.
        sortbc - sort data by category.
        list - list categories.
        sum - sum your outgoings by date.
        quit - quit program.\n''')
        option = input('What would you like to do?')
        menu(option)


def menu(option):
    menu_dict = {'add': add_bill, 'sortbd': sort_by_date, 'sortbc': sort_by_category, 'list': list_categories,
                 'sum': sum_amount, 'quit': sys.exit}
    if option not in menu_dict:
        print('Wrong option.')
        sys.exit()
    else:
        if option == 'add':
            execute_statement(menu_dict[option]())
        elif option == 'sortbd':
            get_response(menu_dict[option](), 1)
        elif option == 'sortbc':
            get_response(menu_dict[option](), 1)
        elif option == 'list':
            get_response(menu_dict[option](), 2)
        elif option == 'sum':
            get_response(menu_dict[option](), 3)
        elif option == 'quit':
            menu_dict[option]()


def main():
    execute_statement(check_or_create_table())
    show_menu()


if __name__ == '__main__':
    main()