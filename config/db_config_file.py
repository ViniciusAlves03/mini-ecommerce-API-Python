import os
from dotenv import load_dotenv
load_dotenv()

db_config = {
    "DB_CONNECTION": os.getenv("DB_CONNECTION"),
}
