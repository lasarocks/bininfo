
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


class dbPersistente(object):
    def __init__(self, path_file_auth, path_file_token=None):
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
    def list(self):
        if not self.inst_google_drive:
            print(f'sem GoogleDrive')
            return False
        file_list = self.inst_google_drive.ListFile({'q': "'root' in parents"}).GetList()
        for file1 in file_list:
            print('title: %s, id: %s' % (file1['title'], file1['id']))
    def upload(self, path_file):
        if not self.inst_google_drive:
            print(f'sem GoogleDrive')
            return False
        if not os.path.isfile(path_file):
            print(f'no file {path_file}')
            return False
        name_file = os.path.basename(path_file)
        try:
            temp_file = self.inst_google_drive.CreateFile(
                {
                    'title': name_file
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
