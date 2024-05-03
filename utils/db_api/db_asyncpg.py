import datetime

from loader import dp


async def get_all_users_data():
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            query = '''
                        SELECT
                            ROW_NUMBER() OVER (ORDER BY u.user_id) AS row_number,
                            u.user_id,
                            u.fio,
                            CASE
                                WHEN u.isadmin THEN 'Администратор'
                                ELSE 'Пользователь'
                            END AS status
                        FROM
                            users u
            '''
            return await connection.fetch(query)


async def active_users_list():
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            return await connection.fetch('SELECT * FROM "users"')



async def user_exists(user_id: int):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            result = await connection.fetchrow('SELECT "user_id" FROM "users" WHERE "user_id"=$1', user_id)
            return result is not None


async def user_info_by_id(user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            return await connection.fetchrow('SELECT u.*, '
                                             '(SELECT COUNT(*) FROM "users" WHERE "referral" = $1) AS referral_count '
                                             'FROM "users" AS u WHERE "user_id" = $1', user_id)


async def user_is_admin(user_id: int):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            result = await connection.fetchrow('SELECT * FROM "users" WHERE "user_id"=$1 AND "isadmin"=True', user_id)
            return result is not None


async def admin_list():
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            return await connection.fetch('SELECT "user_id" FROM "users" WHERE "isadmin"=True')


async def add_user(user_id: int, fio: str, referral=None):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('INSERT INTO "users" ("user_id", "fio", "bonus", "referral", "isadmin") '
                                     'VALUES ($1, $2, $3, $4, $5)', user_id, fio, 10, referral, False)


async def user_list():
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            return await connection.fetch('SELECT * FROM "users"')


async def category_list():
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            return await connection.fetch('SELECT * FROM "categories" ORDER BY "id"')


async def tovars_by_category(category_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            return await connection.fetch('SELECT * FROM "products" WHERE "category"=$1', category_id)


async def search_tovar_by_name(keyword):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            return await connection.fetch('SELECT * FROM "products" WHERE LOWER("tovar") LIKE $1 '
                                          'or LOWER("description") LIKE $1', f'%{keyword.lower()}%')


async def tovar_info_by_id(id: int):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            return await connection.fetchrow('SELECT * FROM "products" WHERE "id"=$1', id)


async def tovar_favourite_list(user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            return await connection.fetch(
                'SELECT f.user_id, p.* FROM "favourite" f JOIN "products" p ON f."product_id" = p."id" '
                'WHERE f."user_id" = $1', user_id)


async def tovar_is_favourite(product_id, user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            result = await connection.fetchrow('SELECT * FROM "favourite" WHERE "product_id"=$1 and "user_id"=$2',
                                               product_id, user_id)

            return result is not None


async def tovar_set_favourite(product_id, user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            if await tovar_is_favourite(product_id=product_id, user_id=user_id):
                await tovar_favourite_del(product_id, user_id)
            else:
                await connection.execute('INSERT INTO "favourite" ("product_id", "user_id") VALUES ($1, $2)',
                                         product_id, user_id)


async def tovar_favourite_del(product_id, user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('DELETE FROM "favourite" WHERE "product_id" = $1 AND "user_id" = $2',
                                     product_id, user_id)


async def tovar_favourite_clear(user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('DELETE FROM "favourite" WHERE "user_id" = $1', user_id)


async def basket_list(user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            return await connection.fetch('SELECT p.*, b."count" FROM "basket" b '
                                          'JOIN "products" p ON b."product_id" = p."id" '
                                          'WHERE b."user_id" = $1', user_id)


async def tovar_add_to_basket(user_id, product_id, count):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            dt = datetime.datetime.now()
            await connection.execute(
                'INSERT INTO "basket" ("user_id", "product_id", "count", "dt") '
                'VALUES ($1, $2, $3, $4) '
                'ON CONFLICT ("user_id", "product_id") DO UPDATE '
                'SET "count" = "basket"."count" + EXCLUDED."count", "dt" = $4',
                user_id, product_id, count, dt
            )


async def add_history(user_id, total):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            dt = datetime.datetime.now()
            result = await connection.fetchrow('INSERT INTO "history" ("user_id", "dt", "total", "received") '
                                               'VALUES ($1, $2, $3, $4) RETURNING "id"', user_id, dt, total, False)
            return result["id"]


async def del_history(id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('DELETE FROM "history" WHERE "id"=$1', id)


async def set_history_received(id, received=True):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('UPDATE "history" SET "received"=$1 WHERE "id"=$2', received, id)


async def basket_clear(user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('DELETE FROM "basket" WHERE "user_id" = $1', user_id)


async def basket_tovar_del(product_id, user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('DELETE FROM "basket" WHERE "product_id" = $1 AND "user_id" = $2',
                                     product_id, user_id)


async def basket_tovar_set_count(product_id, count):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            return await connection.fetch('UPDATE "basket" SET "count"=$1 WHERE "product_id"=$2', count, product_id)


async def add_category(category):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('INSERT INTO "categories" ("category") VALUES ($1)', category)


async def delete_category_by_id(id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('DELETE FROM "categories" WHERE "id"=$1', id)


async def category_name_by_id(id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            result = await connection.fetchrow('SELECT "category" FROM "categories" WHERE "id"=$1', id)
            return result["category"] if result else None


async def add_tovar(category, price, description, photo, tovar):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            result = await connection.fetchrow(
                """
                INSERT INTO "products" 
                    ("category", "tovar", "photo", "price", "description")
                VALUES 
                    ($1, $2, $3, $4, $5)
                RETURNING "id"
                """,
                category, tovar, photo, price, description
            )
            return result["id"]


async def product_title_by_id(id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            result = await connection.fetchrow('SELECT "tovar" FROM "products" WHERE "id"=$1', id)
            return result["tovar"] if result else None


async def delete_tovar_by_id(id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('DELETE FROM "products" WHERE "id"=$1', id)


async def edit_tovar_photo(id, photo):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('UPDATE "products" SET "photo"=$1 WHERE "id"=$2', photo, id)


async def edit_tovar_title(id, title):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('UPDATE "products" SET "tovar"=$1 WHERE "id"=$2', title, id)


async def edit_tovar_price(id, price):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('UPDATE "products" SET "price"=$1 WHERE "id"=$2', price, id)


async def edit_tovar_description(id, description):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('UPDATE "products" SET "description"=$1 WHERE "id"=$2', description, id)


async def edit_tovar_rating(id, rating):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('UPDATE "products" SET "rating"=$1 WHERE "id"=$2', rating, id)
