import os

from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = str(os.getenv(("BOT_TOKEN")))
PAYMENT_TOKEN = str(os.getenv(("PAYMENT_TOKEN")))

PGUSER = str(os.getenv(("PGUSER")))
PGPASSWORD = str(os.getenv(("PGPASSWORD")))


admins_id = [
    789420601
]