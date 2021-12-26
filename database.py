import json
import sqlite3

import requests


class Database:
    def __init__(self, check_same_thread=True):
        self.connection = sqlite3.connect("api_database.db", check_same_thread=check_same_thread)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def insert_many(self, table, objects_list):
        if table == 'users':
            query = f'INSERT INTO {table} VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        else:
            query = f'INSERT INTO {table} VALUES (?, ?, ?, ?)'
        self.cursor.executemany(query, objects_list)
        self.connection.commit()

    def create_schema(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                user_id integer PRIMARY KEY,
                name text NOT NULL,
                username text NOT NULL,
                email text NOT NULL,
                address JSON NOT NULL,
                phone text NOT NULL,
                website text NOT NULL,
                company JSON NOT NULL)
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS todos(
            user_id integer NOT NULL,
            task_id integer PRIMARY_KEY,
            title text NOT NULL,
            completed integer NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id))
            """
        )
        self.connection.commit()

    def download_and_save_users_data(self):
        users_json = requests.get('https://jsonplaceholder.typicode.com/users').json()
        users = []
        for user in users_json:
            user["address"] = json.dumps(user["address"])
            user["company"] = json.dumps(user["company"])
            users.append(tuple(user.values()))
        return self.insert_many('users', users)

    def download_and_save_todo_data(self):
        todos_json = requests.get('https://jsonplaceholder.typicode.com/todos').json()
        todos = []
        for todo in todos_json:
            if todo["completed"] is True:
                todo["completed"] = 1
            else:
                todo["completed"] = 0
            todos.append(tuple(todo.values()))
        return self.insert_many('todos', todos)

    def get_users(self):
        self.cursor.execute("select * from users")
        raw_users = self.cursor.fetchall()
        return [User(u[0], u[1], u[2], u[3], json.loads(u[4]), u[5], u[6], json.loads(u[7])) for u in raw_users]

    def get_todos(self):
        self.cursor.execute("select * from todos")
        raw_todos = self.cursor.fetchall()
        return [Todo(td[0], td[1], td[2], td[3]) for td in raw_todos]


class User:

    def __init__(self, user_id, name, username, email, address, phone, website, company):
        """
        :param user_id: int
        :param name: str
        :param username: str
        :param email: str
        :param address: dict
        :param phone: str
        :param website: str
        :param company: dict
        """
        self.user_id = user_id
        self.name = name
        self.username = username
        self.email = email
        self.address = address
        self.phone = phone
        self.website = website
        self.company = company


class Todo:

    def __init__(self, user_id, task_id, title, completed):
        """
        :param user_id: int
        :param task_id: int
        :param title: str
        :param completed: int
        """
        self.user_id = user_id
        self.task_id = task_id
        self.title = title
        self.completed = completed
