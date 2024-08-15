import os


arq_cred = os.getenv("Gcredentials", None)

from app.core.database import(
    DB_NAME,
    quickDbFreeze
)

quicker = quickDbFreeze(arq_cred)
quicker.update_local_db(DB_NAME)




import urllib.parse
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
    Base,
    SQLALCHEMY_DATABASE_URL,
)


from app.api.base import api_router



from app.exceptions import errorHandler



Base.metadata.create_all(bind=engine)


app = FastAPI()
app.path_database = os.path.abspath(urllib.parse.urlparse(SQLALCHEMY_DATABASE_URL).path[1:])
app.inst_gdrive = quicker.inst_db

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
    print(f'vamo tenta upar...')
    av = quicker.update_remote_db(DB_PATH=app.path_database, DB_NAME=DB_NAME)
    if av:
        print(f'upou av == True')
    else:
        print(f'av != true')



app.include_router(api_router)


errorHandler.setup_error_handlers(app)
