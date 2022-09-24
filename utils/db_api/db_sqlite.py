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

    def tovar_card(self, tovar_id):
        with self.connection:
            result = self.cursor.execute(f'SELECT "tovar_name", "tovar_price", "tovar_disc", "tovar_photo"'
                                         f'FROM "tovar" WHERE "tovar_id"="{tovar_id}"').fetchall()[0]
            return result

    def tovar_name(self, tovar_id):
        with self.connection:
            result = self.cursor.execute(f'SELECT "tovar_name" FROM "tovar" WHERE "tovar_id" = "{tovar_id}" ').fetchall()[0]
            return result[0] if len(result) > 0 else []

    def category_id(self, tovar_id):
        with self.connection:
            result = self.cursor.execute(f'SELECT "category_id" FROM "tovar" WHERE "tovar_id" = "{tovar_id}" ').fetchall()[0]
            return result[0] if len(result) > 0 else []

    def tovar_price(self, tovar_id):
        with self.connection:
            result = self.cursor.execute(f'SELECT "tovar_price" FROM "tovar" WHERE "tovar_id" = "{tovar_id}" ').fetchall()[0]
            return result[0] if len(result) > 0 else []


class User:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute(f'SELECT * FROM "users" WHERE user_id="{user_id}"').fetchall()
            return bool(len(result))

    def create_basket(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                f'CREATE TABLE IF NOT EXISTS "{user_id}" '
                f'(tovar_id integer not null, '
                f'tovar_name string, '
                f'tovar_price real, '
                f'tovar_count integer, '
                f'favourite integer not null default 0)')

    def add_user(self, user_id, user_username, user_fullname):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' ('user_id', 'user_username', 'user_fullname', 'total_amount') "
                                       "VALUES (?, ?, ?, ?)", (user_id, user_username, user_fullname, 0))

    def total_amount(self, user_id):
        with self.connection:
            return self.cursor.execute(f'SELECT "total_amount" FROM "users" WHERE "user_id"="{user_id}"').fetchall()[0][0]

    def basket_add(self, tovar_id, user_id, tovar_name, tovar_price=0, count=0, favourite=0):
        with self.connection:
            result = self.cursor.execute(f'SELECT "tovar_count" FROM "{user_id}"'
                                         f' WHERE "tovar_id"="{tovar_id}" '
                                         f'AND "favourite"=0').fetchall()
            if len(result) != 0:
                 count += result[0][0]
                 self.cursor.execute(f'UPDATE "{user_id}" '
                                     f'SET "tovar_count"= "{count}" '
                                     f'WHERE "tovar_id" = "{tovar_id}" AND "tovar_count" != "{0}" ')

            else:
                self.cursor.execute(f'INSERT INTO "{user_id}" '
                                    f'VALUES ("{tovar_id}", "{tovar_name}", "{tovar_price}", "{count}", 0'
                                    f''
                                    f')')

    def set_favourite(self, tovar_id, user_id, tovar_name):
        with self.connection:
            fav = self.favourite_info(tovar_id, user_id)
            if fav == 1:
                return self.cursor.execute(f'DELETE FROM "{user_id}" '
                                           f'WHERE "tovar_id" = "{tovar_id}" '
                                           f'AND "tovar_count" = "0"')
            elif fav == None:
                return self.cursor.execute(f'INSERT INTO "{user_id}" '
                                           f'VALUES ("{tovar_id}", "{tovar_name}", 0, 0, 1)')

    def favourite_info(self, tovar_id, user_id):
        with self.connection:
            result = self.cursor.execute(
                f'SELECT "favourite" FROM "{user_id}" '
                f'WHERE "tovar_id"="{tovar_id}" AND "tovar_count"="0"').fetchall()
            return result[0][0] if len(result) > 0 else None


    def favourite_list(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                f'SELECT "tovar_id", "tovar_name" FROM "{user_id}" '
                f'WHERE favourite="1"').fetchall()
            return result if len(result) > 0 else []

    def basket_list(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                f'SELECT "tovar_id", "tovar_name", "tovar_price", "tovar_count" FROM "{user_id}" '
                f'WHERE favourite="0" and "tovar_count"!=0').fetchall()
            return result if len(result) > 0 else []

    def clean_favourite(self, user_id):
        with self.connection:
            return self.cursor.execute(f'DELETE FROM "{user_id}" WHERE "favourite" = 1')

    def clean_basket(self, user_id):
        with self.connection:
            return self.cursor.execute(f'DELETE FROM "{user_id}" WHERE "favourite" = 0')

