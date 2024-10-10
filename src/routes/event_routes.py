from fastapi import APIRouter
from fastapi import Depends
from jwt_auth.auth_bearer import JWTBearer
from routes.depends import get_destinations_service
from schemas.event_schemas import EventSchema
from services.event_service import DestinationsService

event_router = APIRouter(prefix="/event", tags=["Event"])


@event_router.post(
    "/",
    dependencies=(Depends(JWTBearer()),),
)
async def event(
    event: EventSchema, service: DestinationsService = Depends(get_destinations_service)
):
    available_destinations = await service.get_collections_list("destinations")
    if event.strategy:
        strategy = event.strategy
    else:
        strategy_obj = await service.get_collection_one("strategy")
        strategy = strategy_obj.get("strategy", None)

    filtered_intents = await service.get_filtered_destinations(
        strategy, event.routingIntents
    )

    available_destinations_dict = [
        destination["destinationName"] for destination in available_destinations
    ]
    filtered_intents_names = [intent.destinationName for intent in filtered_intents]
    filtered_destinations_dict = {
        destination["destinationName"]: destination
        for destination in available_destinations
        if destination["destinationName"] in filtered_intents_names
    }

    response = await service.get_response(
        event, filtered_destinations_dict, available_destinations_dict
    )
    await service.save_request_and_response(event.dict(), response)

    return response
