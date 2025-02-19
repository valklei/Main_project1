#!/usr/bin/env python3
# При запуске программы выводится список категорий (номер и название категории)
# Пользователь может ввести номер категории
# Программа выводит все фильмы в данной категории, но не более 10 фильмов. О фильме выводится следующая информация: название, год выпуска, описание.
import pymysql
from query_manager import QueryHandler
from pymysql.cursors import DictCursor


dbconfig = { # для mysql порт по умолчанию 3306
'host': 'ich-edit.edu.itcareerhub.de',
'user': 'ich1',
'password': 'ich1_password_ilovedbs',
'database': 'Sakila',
'charset': 'utf8mb4',
'cursorclass': DictCursor
}

def task1(dbconfig, **params):
    query_handler = QueryHandler(dbconfig)
    try:
        print("All categories:")
        [print(row.get('category_id'), row.get('name'), sep=' : ') for row in query_handler.get_all_category()]
    except pymysql.Error as e:
        print( "SQLError", e )
    except Exception as e:
        print("Error", e)
        
if __name__ == "__main__":
    task1(dbconfig)