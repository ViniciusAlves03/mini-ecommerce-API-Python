import os
from dotenv import load_dotenv
load_dotenv()

swagger_config = {
    "SWAGGER_URL": os.getenv("SWAGGER_URL"),
    "API_URL": os.getenv("API_URL")
}
