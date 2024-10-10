import requests
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.logger import logger
from event_strategy.base import CustomStrategy
from event_strategy.base import RoutingStrategy
from exceptions.event_exceptions import UnknownDestinationError


class DestinationsService:
    db: AsyncIOMotorDatabase

    async def get_collections_list(self, collection_name):
        return await self.db.get_collection(collection_name).find().to_list()

    async def get_collection_one(self, collection_name):
        return await self.db.get_collection(collection_name).find_one({})

    async def get_filtered_destinations(self, strategy, available_destinations):
        if strategy in RoutingStrategy.strategies:
            strategy_cls = RoutingStrategy.strategies[strategy]
            strategy_instance = strategy_cls()
            filtered_destinations = strategy_instance.filter_intents(
                available_destinations
            )
        elif strategy.startswith("lambda"):
            strategy_instance = CustomStrategy(strategy)
            filtered_destinations = strategy_instance.filter_intents(
                available_destinations
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid strategy")
        return filtered_destinations

    async def get_response(
        self, event, filtered_destinations_dict, available_destinations_dict
    ):
        response = {}
        for intent in event.routingIntents:
            if intent.destinationName in filtered_destinations_dict:
                destination = filtered_destinations_dict[intent.destinationName]
                await self.send_payload(destination, event.payload)
                response[intent.destinationName] = True
                logger.info(
                    f"payload sent to [{intent.destinationName}] via [{destination.get('transport', None)}] transport"
                )
            elif (
                intent.destinationName not in filtered_destinations_dict
                and intent.destinationName in available_destinations_dict
            ):
                response[intent.destinationName] = False
                logger.info(f"{intent.destinationName}: skipped")
            else:
                response[intent.destinationName] = False
                logger.info(f"{UnknownDestinationError()} ({intent.destinationName})")
        return response

    async def send_payload(self, destination, payload):
        match destination["transport"]:
            case "http.post":
                response = requests.post(destination["url"], json=payload)
                """TODO something with response"""
                logger.info(f"send POST {destination['url']}")
            case "http.get":
                response = requests.post(destination["url"], json=payload)
                """TODO something with response"""
                logger.info(f"send GET {destination['url']}")
            case "log.info":
                logger.info(f"Payload to {destination['destinationName']}: {payload}")
            case "log.warn":
                logger.info(f"Payload to {destination['destinationName']}: {payload}")

    async def send_post(self, destination, payload):
        r = requests.post(destination.url, json=payload)
        print(r.status_code)

    async def send_get(self, destination, payload):
        r = requests.get(destination.url, params=payload)
        print(r.status_code)

    async def save_request_and_response(self, event, response):
        await self.db["request_response"].insert_one(
            {
                "request": event,
                "response": response,
            }
        )
