import uuid
from rest_framework.response import Response



def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
    except (ValueError, TypeError, AttributeError):
        return False

    return True




'''Gets and validates the pagination parameters'''
def get_pagination_params(request, default_limit):
    try:
        skip = int(request.query_params.get("skip", 0))
        limit = int(request.query_params.get("limit", default_limit))
    except (ValueError, TypeError):
        return None, None, Response(
            {
                "status": 422,
                "data": None,
                "message": "skip and limit must be integers"
            },
            status=422
        )

    if skip < 0 or limit < 1 or limit > 100:
        return None, None, Response(
            {
                "status": 422,
                "data": None,
                "message": ("skip must be 0 or greater and "
                           "limit must be between 1 and 100")
            },
            status=422
        )

    return skip, limit, None




'''Applies query parameter filters to the requested data'''
def apply_query_params_filters(request, query_set):
    category_id = request.query_params.get("category_id")
    subcategory_id = request.query_params.get("subcategory_id")
    premium_only = request.query_params.get("premium_only", "false").lower()

    _, error_response = apply_query_params_validation(category_id=category_id, subcategory_id=subcategory_id, premium_only=premium_only)

    if error_response is not None:
        return None, error_response

    if subcategory_id:
        query_set = query_set.filter(subcategory_id=subcategory_id)
    elif category_id:
        query_set = query_set.filter(
            category_id=category_id,
            subcategory__isnull=True
        )

    if premium_only == "true":
        query_set = query_set.filter(premium=True)

    return query_set, None



'''Validates the query parameters for type safety'''
def apply_query_params_validation(category_id, subcategory_id, premium_only):

    if category_id is not None and not is_valid_uuid(category_id):
        return None, Response(
            {
                "status": 422,
                "data": None,
                "message": "category_id must be a valid UUID"
            },
            status=422
        )

    if subcategory_id is not None and not is_valid_uuid(subcategory_id):
        return None, Response(
            {
                "status": 422,
                "data": None,
                "message": "subcategory_id must be a valid UUID"
            },
            status=422
        )

    if premium_only not in ("true", "false"):
        return None, Response(
            {
                "status": 422,
                "data": None,
                "message": "premium_only must be either true or false"
            },
            status=422
        )

    return True, None
