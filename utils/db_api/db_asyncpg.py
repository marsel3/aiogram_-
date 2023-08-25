from loader import dp


async def user_exists(user_id: int):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            result = await connection.fetchrow('SELECT "user_id" FROM "users" WHERE "user_id"=$1', user_id)
            return result is not None


async def add_user(user_id: int, fio: str, referral=None):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('INSERT INTO "users" ("user_id", "fio", "referralz") '
                                     'VALUES ($1, $2, $3)', user_id, fio, referral)


async def category_list():
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            return await connection.fetch('SELECT * FROM "category"')


async def category_by_tovar(tovar_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            result = await connection.fetchrow('SELECT "category_id" FROM "tovar" WHERE "id"=$1', tovar_id)
            return result["category_id"] if result else None


async def tovar_by_category(category):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            result = await connection.fetch('SELECT * FROM "tovar" WHERE "category_id"=$1', category)
            return result


async def tovar_by_id(id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            result = await connection.fetchrow('SELECT * FROM "tovar" WHERE "id"=$1', id)
            return result


async def search_tovar_by_name(keyword):
    async with dp['db_pool'].acquire() as connection:
        return await connection.fetch('SELECT * FROM "tovar" WHERE LOWER("name") LIKE $1', f'%{keyword.lower()}%')


async def tovar_favourite_list(user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            return await connection.fetch(
                'SELECT f.*, t."name" FROM "favourite" f JOIN "tovar" t ON f."tovar_id" = t."id" '
                'WHERE f."user_id" = $1', user_id)


async def tovar_is_favourite(tovar_id, user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            result = await connection.fetchrow('SELECT * FROM "favourite" WHERE "tovar_id"=$1 and "user_id"=$2',
                                               tovar_id, user_id)
            return True if result else False


async def tovar_set_favourite(tovar_id, user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            if await tovar_is_favourite(tovar_id=tovar_id, user_id=user_id):
                await tovar_favourite_del(tovar_id, user_id)
            else:
                await connection.execute('INSERT INTO "favourite" ("tovar_id", "user_id") VALUES ($1, $2)',
                                         tovar_id, user_id)


async def tovar_favourite_del(tovar_id, user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('DELETE FROM "favourite" WHERE "tovar_id" = $1 AND "user_id" = $2',
                                     tovar_id, user_id)


async def tovar_favourite_clear(user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('DELETE FROM "favourite" WHERE "user_id" = $1', user_id)


async def tovar_add_to_basket(user_id, tovar_id, count):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('INSERT INTO "basket" ("user_id", "tovar_id", "count") '
                                     'VALUES ($1, $2, $3) ON CONFLICT ("user_id", "tovar_id") DO UPDATE '
                                     'SET "count" = "basket"."count" + EXCLUDED."count"', user_id, tovar_id, count)


async def basket_list(user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            return await connection.fetch('SELECT t.*, b."count" FROM "basket" b '
                                          'JOIN "tovar" t ON b."tovar_id" = t."id" '
                                          'WHERE b."user_id" = $1', user_id)


async def basket_tovar_set_count(tovar_id, count):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            return await connection.fetch('UPDATE "basket" SET "count"=$1 WHERE "tovar_id"=$2', count, tovar_id)


async def basket_clear(user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('DELETE FROM "basket" WHERE "user_id" = $1', user_id)


async def basket_tovar_del(tovar_id, user_id):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('DELETE FROM "basket" WHERE "tovar_id" = $1 AND "user_id" = $2',
                                     tovar_id, user_id)


