import os
from app.core.g1 import dbPersistente
from app.utils.utils import timestamp

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_NAME = 'wpbraintree.db'



class quickDbFreeze(object):
    def __init__(self, raw_credentials=None):
        self.raw_credentials = raw_credentials or os.getenv("Gcredentials", None)
        self.inst_db = None
        self.prepare()
    def prepare(self):
        if not self.raw_credentials:
            print(f'no raw_credentials')
            return False
        name_credentials = f'credtemp-{timestamp()}.json'
        with open(name_credentials, 'w') as f_cred:
            f_cred.write(self.raw_credentials)
        inst_db = None
        try:
            inst_db = dbPersistente(path_file_auth=None, path_file_token=name_credentials)
            if inst_db.validate():
                self.inst_db = inst_db
        except Exception as err:
            print(f'quickDbFreeze.prepare exp --- {err}')
        else:
            if self.inst_db:
                print(f'instanciou ok')
        finally:
            os.remove(name_credentials)
    def update_local_db(self, DB_NAME):
        if not self.inst_db:
            print(f'no inst_db')
            return False
        query = {
            'q': "title != 'wpbraintree.db' and title starts with 'wpbraintree'",
            'orderBy': 'createdDate desc,title'
        }
        response = self.inst_db.list(query=query)
        if response:
            db_use = response[0]
            print(f'vamo usar esse arq --- {db_use["originalFilename"]} -- {db_use["title"]}')
            if os.path.isfile(db_use['originalFilename']):
                av = os.remove(db_use['originalFilename'])
            db_use.GetContentFile(DB_NAME)
            if os.path.isfile(DB_NAME):
                return True
        return False
    def update_remote_db(self, DB_PATH, DB_NAME):
        if not self.inst_db:
            print(f'no inst_db')
            return False
        name_db_edit = os.path.splitext(os.path.basename(DB_PATH))
        if name_db_edit:
            name_db_items = '.'.join(x for x in name_db_edit[:-1])
            name_db_new = f'{name_db_items}-{timestamp()}{name_db_edit[-1]}'
            print(f'updando remote {name_db_new} --- {DB_PATH}')
            response = self.inst_db.upload(path_file=DB_PATH, name_file=name_db_new)
            if response:
                return True
        return False








# if arq_cred:
#     print(arq_cred)
#     with open('teste.json', 'w') as f_cred:
#         f_cred.write(arq_cred)
#     dd = dbPersistente(path_file_auth=None, path_file_token='teste.json')
#     arqs_rmt = dd.list()
#     if arqs_rmt:
#         arq_db = arqs_rmt[0]
#         if os.path.isfile(arq_db['title']):
#             print(f'deletando antigo')
#             av = os.remove(arq_db['title'])
#         arq_db.GetContentFile(arq_db['title'])
#         print(f'baixando novo')
#         if os.path.isfile(arq_db['title']):
#             print(f'novo OK')
#     print(f'chego refresh status == {dd.inst_google_auth.credentials.access_token_expired}')
# else:
#     print(f'sem arq_cred')


#SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://teste:123456@localhost/teste'


SQLALCHEMY_DATABASE_URL = f'sqlite:///{DB_NAME}?check_same_thread=False'




engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
