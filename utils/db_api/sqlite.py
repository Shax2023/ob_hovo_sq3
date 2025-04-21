import sqlite3


class Database:
    def __init__(self, db_path="data/main.db"):
        self.db_path = db_path

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.set_trace_callback(self.logger)
        return conn

    def execute(self, sql, parameters=(), fetchone=False, fetchall=False, commit=False):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(sql, parameters)
            data = None

            if commit:
                connection.commit()
            if fetchone:
                data = cursor.fetchone()
            if fetchall:
                data = cursor.fetchall()

        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            language TEXT DEFAULT 'uz'
        );
        """
        self.execute(sql, commit=True)

    def add_user(self, user_id, name, email=None, language='uz'):
        sql = """
    INSERT INTO Users (id, name, email, language)
    VALUES (?, ?, ?, ?)
    """
        self.execute(sql, (user_id, name, email, language), commit=True)


    def select_all_users(self):
        return self.execute("SELECT * FROM Users", fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users", fetchone=True)

    def update_user_email(self, email, user_id):
        sql = "UPDATE Users SET email=? WHERE id=?"
        self.execute(sql, (email, user_id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users", commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(f"{key}=?" for key in parameters)
        return sql, tuple(parameters.values())

    @staticmethod
    def logger(statement):
        print(f"""
=========================
Executing SQL:
{statement}
=========================
""")
