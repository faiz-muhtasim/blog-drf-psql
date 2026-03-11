# core/utils/response.py

def success_response(data=None, message="Success", code=200):
    return {
        "data": data,
        "response_status": {
            "success": True,
            "code": code,
            "message": message,
        },
    }

def error_response(data=None, message="Error", code=400):
    return {
        "data": data,
        "response_status": {
            "success": False,
            "code": code,
            "message": message,
        },
    }