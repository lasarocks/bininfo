import os
from app.core.g1 import dbPersistente

arq_cred = os.getenv("Gcredentials", None)
dd = None

if arq_cred:
    print(arq_cred)
    with open('teste.json', 'w') as f_cred:
        f_cred.write(arq_cred)
    dd = dbPersistente(path_file_auth=None, path_file_token='teste.json')
    arqs_rmt = dd.list()
    if arqs_rmt:
        arq_db = arqs_rmt[0]
        if os.path.isfile(arq_db['title']):
            print(f'deletando antigo')
            av = os.remove(arq_db['title'])
        arq_db.GetContentFile(arq_db['title'])
        print(f'baixando novo')
        if os.path.isfile(arq_db['title']):
            print(f'novo OK')
    print(f'chego refresh status == {dd.inst_google_auth.credentials.access_token_expired}')
else:
    print(f'sem arq_cred')


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
    SQLALCHEMY_DATABASE_URL
)


from app.api.base import api_router



from app.exceptions import errorHandler


#Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)


app = FastAPI()
app.path_database = os.path.abspath(urllib.parse.urlparse(SQLALCHEMY_DATABASE_URL).path[1:])
app.inst_gdrive = dd

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
    dd.upload(arq_db['title'])
    print(f'acho que upou....')



app.include_router(api_router)


errorHandler.setup_error_handlers(app)
