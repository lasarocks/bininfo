
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


class dbPersistente(object):
    def __init__(self, path_file_auth, path_file_token=None):
        print(f'instanciando dbPersistente --- {path_file_token}')
        self.path_file_auth = path_file_auth
        self.path_file_token = path_file_token
        self.inst_google_auth = GoogleAuth()
        self.inst_google_drive = None
        self.prepare()
    def do_login_code(self, url_auth):
        print(f'necessario liberar ---- \nAcesse o link\n\n{url_auth}\n\nE informe o codigo\n\n')
        code_google = input('Codigo -> ')
        self.do_login(code_google=code_google)
    def do_login(self, code_google=None):
        drive = None
        try:
            if code_google is not None:
                self.inst_google_auth.Auth(code_google)
            if self.inst_google_auth.credentials:
                drive = GoogleDrive(self.inst_google_auth)
        except Exception as err:
            print(f'dbPersistente.do_login exp --- {err}')
        else:
            self.inst_google_drive = drive
    def validate(self):
        if not self.inst_google_auth.credentials or not self.inst_google_drive:
            if not self.inst_google_drive:
                print(f'no googledrive instance')
            else:
                print(f'no credentials loaded')
            return False
        if self.inst_google_auth.credentials.access_token_expired:
            self.inst_google_auth.Refresh()
            return self.validate()
        else:
            return True
    def prepare(self):
        if self.path_file_token is None:
            try:
                self.inst_google_auth.LoadClientConfigFile(self.path_file_auth)
                url_auth = self.inst_google_auth.GetAuthUrl()
            except Exception as err:
                print(f'dbPersistente.prepare exp --- {err}')
            else:
                if url_auth:
                    self.do_login_code(url_auth=url_auth)
        else:
            try:
                self.inst_google_auth.LoadCredentialsFile(self.path_file_token)
            except Exception as err:
                print(f'dbPersistente.prepare exp --- {err}')
            else:
                self.do_login(code_google=None)
    def list(self, query={}):
        if not self.validate():
            return False
        if not query:
            query.update(
                {
                    'q': "'root' in parents"
                }
            )
        try:
            response = self.inst_google_drive.ListFile(query).GetList()
        except Exception as err:
            print(f'dbPersistente.list exp --- {query} --- {err}')
        else:
            return response
        return False
    def upload(self, path_file, name_file=None):
        if not self.validate():
            return False
        if not os.path.isfile(path_file):
            print(f'no file {path_file}')
            return False
        name_file_original = os.path.basename(path_file)
        if name_file is None:
            name_file = name_file_original
        try:
            temp_file = self.inst_google_drive.CreateFile(
                {
                    'title': name_file,
                    'originalFilename': name_file_original
                }
            )
            temp_file.SetContentFile(path_file)
            temp_file.Upload()
        except Exception as err:
            print(f'dbPersistente.upload exp -- {path_file} -- {err}')
        else:
            print(f'upload OK -- {name_file} -- {temp_file["title"]}')
            return temp_file
        return False
    def save_auth(self, path_file_save):
        if not self.inst_google_drive:
            print(f'sem GoogleDrive')
            return False
        try:
            self.inst_google_auth.SaveCredentialsFile(path_file_save)
        except Exception as err:
            print(f'dbPersistente.save_auth exp --- {err}')
        else:
            if os.path.isfile(path_file_save):
                return True
        return False
