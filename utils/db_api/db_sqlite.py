import sqlite3
import datetime



class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def category(self):
        with self.connection:
            result = self.cursor.execute(f'SELECT * FROM "category"').fetchall()
            return result

    def category_list(self):
        with self.connection:
            result = self.cursor.execute(f'SELECT "category_id" FROM "category"').fetchall()
            return [i[0] for i in result]

    def tovar(self, category):
        with self.connection:
            result = self.cursor.execute(f'SELECT "tovar_id", "tovar_name" FROM "tovar" WHERE "category_id"="{category}"').fetchall()
            return result

    def tovar_card(self, tovar):
        with self.connection:
            result = self.cursor.execute(f'SELECT "tovar_name", "tovar_price", "tovar_disc", "tovar_photo"'
                                         f'FROM "tovar" WHERE "tovar_id"="{tovar}"').fetchall()[0]
            return result


class User:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute(f'SELECT * FROM "users" WHERE user_id="{user_id}"').fetchall()
            return bool(len(result))

    def add_user(self, user_id, user_username, user_fullname):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' ('user_id', 'user_username', 'user_fullname') "
                                       "VALUES (?, ?, ?)", (user_id, user_username, user_fullname,))

    def add_basket(self, user, tovar_id, count):
        with self.connection:
       #     return self.cursor.execute("INSERT INTO 'users' ('user_id', 'user_username', 'user_fullname') "
                                       "VALUES (?, ?, ?)", (user_id, user_username, user_fullname,))

    def user_info(self, user_id):
        with self.connection:
            return self.cursor.execute(f'SELECT * FROM "users" WHERE user_id={user_id}').fetchall()[0]

    def set_status(self, user_id):
        with self.connection:
            status = 1 if self.user_status(user_id) == 0 else 0
            return self.cursor.execute('UPDATE "users" SET "status" = ? WHERE "user_id" = ?', (status, user_id,))

    def user_status(self, user_id):
        with self.connection:
            result = self.cursor.execute(f'SELECT "status" FROM "users" WHERE user_id="{user_id}"').fetchmany(1)
            return int(result[0][0])

    def user_demo(self, user_id):
        with self.connection:
            result = self.cursor.execute(f'SELECT "demo" FROM "users" WHERE user_id="{user_id}"').fetchmany(1)
            return int(result[0][0])

    def set_demo(self, user_id, demo):
        with self.connection:
            return self.cursor.execute('UPDATE "users" SET "demo" = ? WHERE "user_id" = ?', (demo, user_id,))

    def edit_demo(self, user_id):
        with self.connection:
            demo = 10 if self.user_demo(user_id) == 0 else 0
            return self.cursor.execute('UPDATE "users" SET "demo" = ? WHERE "user_id" = ?', (demo, user_id,))

