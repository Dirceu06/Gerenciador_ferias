from app.core.database.opDB import Banco
from hashlib import pbkdf2_hmac
import os
import sqlite3
import base64

def get_db_path():
    base = os.getenv("APPDATA")  # C:\Users\Você\AppData\Roaming
    pasta = os.path.join(base, "GerenciadorSenhas")
    os.makedirs(pasta, exist_ok=True)
    return os.path.join(pasta, "cad.db")

def get_user_db_path(login: str):
    base = os.getenv("APPDATA")  # Windows
    pasta = os.path.join(base, "GerenciadorSenhas", "users")
    os.makedirs(pasta, exist_ok=True)
    return os.path.join(pasta, f"reg_{login}.db")

class Verifica:
    def __init__(self,login,senha_tenta):
        self.login=login
        self.senha=senha_tenta
        self.cad = sqlite3.connect(get_db_path(),check_same_thread=False)
        self.cursorCad = self.cad.cursor()
        self.cursorCad.executescript("""
            CREATE TABLE IF NOT EXISTS cadastros (
                login text PRIMARY KEY,
                salt_veri blob not null,
                hash_veri blob not null,
                salt_crypt blob not null
            )
        """)
    
    def verificaLogin(self):
        cad = self.receberLoginCad(self.login)
        
        if cad is None: return False
            
        return self.verificarSenha(cad[1],cad[2],cad[3])
    
    def criarLogin(self,senha_criada,login):
        if self.receberLoginCad(login) is None:    
            salt_login = os.urandom(16)
            salt_crypto = os.urandom(16)
            hash_login = pbkdf2_hmac("sha256",senha_criada.encode(),salt_login,300000)
            arq = open(get_user_db_path(login),'w')
            arq.close()
            self.inserirCad(login,salt_login,hash_login,salt_crypto)
            hashMestre = pbkdf2_hmac("sha256",senha_criada.encode(),salt_crypto,300000)
            chavefernet = base64.urlsafe_b64encode(hashMestre)
            self.banco= Banco(self.login,chavefernet)
            return True
        else:
            return False
        
    def verificarSenha(self,saltVeri,hashVeri,salt_cryp):
        hash = pbkdf2_hmac("sha256",self.senha.encode(),saltVeri,300000)
        if hashVeri==hash:
            
            hash_veri = pbkdf2_hmac("sha256",self.senha.encode(),salt_cryp,300000)
            chavefernet = base64.urlsafe_b64encode(hash_veri)
            self.banco= Banco(self.login,chavefernet)
            return True
        else: 
            return False
        
    def inserirCad(self,login,salt_veri,hash_veri,salt_crypto):
        self.cursorCad.execute("""INSERT INTO cadastros(login, salt_veri, hash_veri, salt_crypt) values (?,?,?,?)""",(login,salt_veri,hash_veri,salt_crypto))
        self.cad.commit()
        return True
    
    def receberLoginCad(self,login):
        self.cursorCad.execute("""select * from cadastros where login=?""",(login,))
        return self.cursorCad.fetchone()