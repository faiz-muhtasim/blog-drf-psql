# core/utils/response.py

def success_response(data=None, message="Success", code=200, include_data=False):
    response = {}

    if include_data and data is not None:
        response["data"] = data

    response["response_status"] = {
        "success": True,
        "code": code,
        "message": message,
    }

    return response


def error_response(message="Error", code=400):
    return {
        "response_status": {
            "success": False,
            "code": code,
            "message": message,
        }
    }