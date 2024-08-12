
from fastapi.responses import JSONResponse



class baseException(Exception):
    def json(self):
        return JSONResponse(
            status_code=self.status_code,
            content={
                "error": True,
                "data": None,
                "error_code": self.name,
                "message": self.message
            }
        )






class ItemNotFound(baseException):
    def __init__(self, name: str = 'ItemNotFound', message: str = ''):
        self.name = name
        self.message = message
        self.status_code = 404





class InvalidParameters(baseException):
    def __init__(self, name: str = 'InvalidParameters', message: str = ''):
        self.name = name
        self.message = message
        self.status_code = 400






class InternalException(baseException):
    def __init__(self, name: str = 'InternalException', message: str = ''):
        self.name = name
        self.message = message
        self.status_code = 400





