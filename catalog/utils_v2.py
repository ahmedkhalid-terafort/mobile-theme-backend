from .utils import apply_query_params_validation


def apply_cached_items_filters(request, items):
    category_id = request.query_params.get("category_id")
    subcategory_id = request.query_params.get("subcategory_id")
    premium_only = request.query_params.get("premium_only", "false").lower()

    _, error_response = apply_query_params_validation(category_id, subcategory_id, premium_only)

    if error_response:
        return None, error_response

    filtered_items = []

    for item in items:
        if subcategory_id:
            if str(item.get("subcategory_id")) != subcategory_id:
                continue
        elif category_id:
            if str(item.get("category_id")) != category_id:
                continue
            if item.get("subcategory_id") is not None:
                continue

        if premium_only == "true":
            if item.get("premium") is not True:
                continue

        filtered_items.append(item)

    return filtered_items, None

