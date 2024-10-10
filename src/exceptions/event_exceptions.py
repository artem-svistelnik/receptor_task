from starlette import status

from exceptions.base import ApiError


class UnknownDestinationError(ApiError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Unknown Destination"
