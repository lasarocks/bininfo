import os
import time
import random
import string
import re
import base64
import json
import datetime


def timestamp():
    return datetime.datetime.utcnow().timestamp()


def load_json_file(path):
    if os.path.isfile(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as err:
            print(f'load_json_file exp --- {err}')
    return {}


def b64decfixpad(s):
    s = s if type(s) == bytes else s.encode()
    try:
        return base64.b64decode(s + b'=' * (-len(s) % 4)).decode()
    except Exception as err:
        print(f'b64decfixpad exp --- {err}')
    return False





def add_arquivo(nome, msg, breakline=True):
    try:
        with open(nome, 'a') as f:
            f.write('{}{}'.format(msg, ('\n' if breakline == True else '')))
    except Exception as err:
        print('ERRO CRIAR ARQUIVO {} - {} U00'.format(nome, err))




def write_arquivo(nome, msg, breakline=False):
    try:
        with open(nome, 'w') as f:
            f.write('{}{}'.format(msg, ('\n' if breakline == True else '')))
    except Exception as err:
        print('ERRO CRIAR ARQUIVO {} - {} U00'.format(nome, err))




def gibe_proxy():
    if check_arquivo('proxies.txt'):
        dados = read_arquivo('proxies.txt')
        if len(dados)>5:
            try:
                dados_s = dados.split('\n')
                addr = random.choice(dados_s).strip()
                if addr.startswith('http://') == False:
                    addr = 'http://{}'.format(addr)
                return {'http': addr, 'https': addr}
            except Exception as err:
                pass
    return {}


def gibe_random_ua():
    if check_arquivo('useragents.txt'):
        uas = read_arquivo('useragents.txt')
        if len(uas)>3:
            try:
                dados_s = uas.split('\n')
                ua = random.choice(dados_s).strip()
                return ua
            except Exception as err:
                pass
    return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'




def check_arquivo(nome):
    retorno = False
    if os.path.isfile(nome):
        retorno = True
    return retorno



def read_arquivo(nome):
    retorno = False
    try:
        with open(nome, 'r', errors='ignore') as fa:
            dados = fa.read()
        dados = dados.strip().encode('utf-8').decode('utf-8', 'ignore')
        dados_limpo = ''.join(x for x in dados if x in string.printable)
        retorno = dados_limpo
    except Exception as err:
        print('ERRO LER ARQUIVO {} - {} U01'.format(nome, err))
    return retorno



def str2int(v):
    try:
        return int(v)
    except Exception as err:
        pass
    return False
