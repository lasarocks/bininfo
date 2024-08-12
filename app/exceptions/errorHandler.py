from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI


from app.exceptions.general import(
    ItemNotFound,
    InvalidParameters,
    InternalException
)

def setup_error_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(ItemNotFound)
    async def notfound_exception_handler(request: Request, exc: ItemNotFound):
        print(f'entro em gay')
        return exc.json()

    @app.exception_handler(InvalidParameters)
    async def invalid_params_exception_handler(request: Request, exc: InvalidParameters):
        return exc.json()

    @app.exception_handler(InternalException)
    async def internal_exception_handler(request: Request, exc: InternalException):
        return exc.json()
        