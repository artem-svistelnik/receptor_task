from fastapi import Request

from services.event_service import DestinationsService


async def get_destinations_service(request: Request):
    service = DestinationsService()
    service.db = request.app.mongodb
    return service
