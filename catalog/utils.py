import uuid
from rest_framework.response import Response


def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
    except (ValueError, TypeError, AttributeError):
        return False

    return True


def get_pagination_params(request, default_limit):
    try:
        skip = int(request.query_params.get("skip", 0))
        limit = int(request.query_params.get("limit", default_limit))
    except (ValueError, TypeError):
        return Response(
            {
                "status": 422,
                "data": None,
                "message": "skip and limit must be integers"
            },
            status=422
        )

    if skip < 0 or limit < 1 or limit > 100:
        return Response(
            {
                "status": 422,
                "data": None,
                "message": ("skip must be 0 or greater and "
                           "limit must be between 1 and 100")
            },
            status=422
        )

    return skip, limit
