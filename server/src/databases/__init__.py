import motor
import motor.motor_asyncio

from settings import MONGODB_URL, MONGODB_NAME

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client[MONGODB_NAME]