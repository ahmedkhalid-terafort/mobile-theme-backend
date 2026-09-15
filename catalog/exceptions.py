from rest_framework.views import exception_handler

def mobile_theme_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return None

    if isinstance(response.data, dict):
        detail = response.data.get("detail")
    else:
        detail = None

    message = str(detail) if detail else "Request could not be completed."

    response.data = {
        "status": response.status_code,
        "data": None,
        "message": message,
    }

    return response