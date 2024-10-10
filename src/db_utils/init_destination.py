from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.logger import logger
from db_utils.initial_data import initial_destinations, initial_strategy


async def init_database(db: AsyncIOMotorDatabase):
    existing_destinations = await db["destinations"].count_documents({})
    if existing_destinations != 0:
        await db["destinations"].delete_many({})
        logger.info("Deleted existing destinations.")

    await db["destinations"].insert_many(initial_destinations)
    logger.info(f"Initialized database with {len(initial_destinations)} destinations.")
    existing_strategy = await db["strategy"].count_documents({})
    if existing_strategy != 0:
        await db["strategy"].delete_many({})
        logger.info("Deleted existing strategy.")
    await db["strategy"].insert_one(initial_strategy)
    logger.info(f"Initialized database with strategy.")
