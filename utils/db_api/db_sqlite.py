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

    def tovar_name_price(self, tovar_id):
        with self.connection:
            result = self.cursor.execute(f'SELECT "tovar_name", "tovar_price" FROM "tovar" WHERE "tovar_id" = "{tovar_id}" ').fetchall()
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
                f'(tovar_id integer not null,'
                f' tovar_count integer default 1,'
                f' favourite integer not null default 0)')

    def add_user(self, user_id, user_username, user_fullname):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' ('user_id', 'user_username', 'user_fullname') "
                                       "VALUES (?, ?, ?)", (user_id, user_username, user_fullname,))

    def add_tovar_(self, tovar_id, user_id, count=0, favourite=0):
        with self.connection:
            result = self.cursor.execute(f'SELECT "favourite", "tovar_count" FROM "{user_id}" WHERE "tovar_id"="{tovar_id}"').fetchall()
            if len(result) != 0:
                if result[0][0] == 0:
                    count += result[0][1]
                    self.cursor.execute(f'UPDATE "{user_id}" '
                                        f'SET "tovar_count"= "{count}" '
                                        f'WHERE "tovar_id" = "{tovar_id}" AND "tovar_count" != "{0}" ')

                else:
                    self.cursor.execute(f'INSERT INTO "{user_id}" '
                                        f'VALUES ("{tovar_id}", "{count}", "{favourite}")')


    def favourite_info(self, tovar_id, user_id):
        with self.connection:
            result = self.cursor.execute(
                f'SELECT "favourite" FROM "{user_id}" '
                f'WHERE "tovar_id"="{tovar_id}" AND "tovar_count"="0"').fetchall()
            return result[0][0] if len(result) > 0 else None


    def set_favourite(self, tovar_id, user_id):
        with self.connection:
            fav = self.favourite_info(tovar_id, user_id)
            if fav == 1:
                return self.cursor.execute(f'DELETE FROM "{user_id}" '
                                           f'WHERE "tovar_id" = "{tovar_id}" '
                                           f'AND "tovar_count" = "0"')
            elif fav == None:
                return self.cursor.execute(f'INSERT INTO "{user_id}" '
                                           f'VALUES ("{tovar_id}", 0, 1)')

    def favourite_list(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                f'SELECT "tovar_id" FROM "{user_id}" '
                f'WHERE favourite="1"').fetchall()
            return result if len(result) > 0 else []

    def basket_list(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                f'SELECT "tovar_id", "tovar_count" FROM "{user_id}" '
                f'WHERE favourite="0" and "tovar_count"!=0').fetchall()
            return result if len(result) > 0 else []




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

