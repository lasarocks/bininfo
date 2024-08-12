from fastapi import(
    Depends,
    FastAPI,
    HTTPException,
    Response,
    status
)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse


from app.core.database import(
    SessionLocal,
    engine,
    Base
)

from app.api.base import api_router



from app.exceptions import errorHandler


#Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.on_event("startup")
async def startup_event():
    print('startandooo bicha')


@app.on_event("shutdown")
def shutdown_event():
    print(f'tamoooo indo de offf')



app.include_router(api_router)


errorHandler.setup_error_handlers(app)
