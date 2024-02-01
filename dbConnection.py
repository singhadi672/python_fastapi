from motor import motor_asyncio
from dotenv import load_dotenv

import os

load_dotenv()

CONNECTION_STR = os.getenv("MONGO_DB_CONNECTION_STR")
DB_NAME = os.getenv("MONGO_DB_NAME")

client = motor_asyncio.AsyncIOMotorClient(CONNECTION_STR)

database = client[DB_NAME]
