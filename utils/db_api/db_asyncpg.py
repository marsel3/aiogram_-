from loader import dp


async def user_exists(user_id: int):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            result = await connection.fetchrow('SELECT "user_id" FROM "users" WHERE "user_id"=$1', user_id)
            return result is not None


async def add_user(user_id: int, fio: str, referral=None):
    async with dp['db_pool'].acquire() as connection:
        async with connection.transaction():
            await connection.execute('INSERT INTO "users" ("user_id", "fio", "referral") '
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