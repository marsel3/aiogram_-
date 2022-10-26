import os

from dotenv import load_dotenv
load_dotenv()


#BOT_TOKEN = str(os.getenv(("BOT_TOKEN")))
#PAYMENT_TOKEN = str(os.getenv(("PAYMENT_TOKEN")))
BOT_TOKEN = '1672438859:AAFjoueNYWY2ZwUM1UqNIBC_USPJ2N4hE48'
PAYMENT_TOKEN = '401643678:TEST:f9a3cffc-fb31-4e1d-b4dd-328da00693c8'

PGUSER = str(os.getenv(("PGUSER")))
PGPASSWORD = str(os.getenv(("PGPASSWORD")))


admins_id = [
    789420601
]