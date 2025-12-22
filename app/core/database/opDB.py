import sqlite3
from cryptography.fernet import Fernet
import os

def get_user_db_path(login: str):
    base = os.getenv("APPDATA")  # Windows
    pasta = os.path.join(base, "GerenciadorSenhas", "users")
    os.makedirs(pasta, exist_ok=True)
    return os.path.join(pasta, f"reg_{login}.db")

class Banco:
    _instance = None  # SINGLETON
    _initialized = False
    TABELAS_VALIDAS = {"reg","reg_deletados"}
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self,login='',Chave=''):
        if Banco._initialized: return
        
        self.login=login
        self.banco = sqlite3.connect(get_user_db_path(login),check_same_thread=False)
        
        self.cursorReg = self.banco.cursor()
        self.key = Chave
        self.fer = Fernet(self.key)
        self.cursorReg.executescript("""
        CREATE TABLE IF NOT EXISTS reg (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            dominio TEXT NOT NULL,
            usuario TEXT,
            senha_criptografada BLOB NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS reg_deletados (
            id INTEGER PRIMARY KEY,
            titulo TEXT NOT NULL,
            dominio TEXT NOT NULL,
            usuario TEXT,
            senha_criptografada BLOB NOT NULL,
            data_deletado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TRIGGER IF NOT EXISTS backup_delecao
            AFTER DELETE ON reg
            FOR EACH ROW
            BEGIN
                INSERT INTO reg_deletados (id, titulo, dominio, usuario, senha_criptografada,data_deletado)
                VALUES (OLD.id, OLD.titulo, OLD.dominio, OLD.usuario, OLD.senha_criptografada, CURRENT_TIMESTAMP);
            END;
            
        
        """)
        
        self.banco.commit()
        
        Banco._initialized = True
    
    def __del__(self):
        """Fecha automaticamente quando o objeto é destruído"""
        self.banco.close()

    def inserirReg(self,titulo,dominio,usuario,senha):
        self.cursorReg.execute("""INSERT INTO reg(titulo,dominio,usuario,senha_criptografada) values (?,?,?,?)""",(titulo,dominio,usuario,self.criptografar(senha)))
        self.banco.commit()
        return True
     
    def lerReg(self,condicao=False,pesquisa='',banco='reg'):
        if banco not in self.TABELAS_VALIDAS:
            return ValueError("Tabela inválida")

        order= 'data_criacao' if banco=='reg' else 'data_deletado'    
        
        if not condicao:
            self.cursorReg.execute(f"""
                SELECT id, titulo, dominio, usuario, 
                    senha_criptografada, 
                    datetime({order}) as {order}
                FROM {banco} 
                ORDER BY {order} DESC
            """)
        else:
            self.cursorReg.execute(f"""
                SELECT id, titulo, dominio, usuario, 
                    senha_criptografada, 
                    datetime({order}) as {order}
                FROM {banco} where dominio like ?
                ORDER BY {order} DESC
            """,(f'%{pesquisa}%',))
        
        registro = self.cursorReg.fetchall()
        resultado = []
        for reg in registro:
            tu = (reg[0],reg[1],reg[2],reg[3],self.descriptografar(reg[4]),reg[5])
            resultado.append(tu)
        
        return resultado
                
    def descriptografar(self,senhaCrip):
        return self.fer.decrypt(senhaCrip).decode()
    
    def criptografar(self,senha:str):
        return self.fer.encrypt(senha.encode())

    def deletarReg(self,id,banco='reg'):
        self.cursorReg.execute(f"""Delete from {banco} where id == ?""",(id,))
        self.banco.commit()
    
    def update(self,id,titulo,dominio,usuario,senha):
        self.cursorReg.execute("""update reg set titulo=?, dominio=?, usuario=?, senha_criptografada=? where id=?;""", (titulo,dominio,usuario,self.criptografar(senha),id))
        self.banco.commit()
        
    def logout(self):
        # fecha o banco com segurança
        try:
            if self.banco:
                self.banco.commit()
                self.banco.close()
        except Exception:
            pass

        self.cursorReg = None
        self.banco = None
        self.fer = None
        self.key = None
        Banco._initialized = False
        Banco._instance = None

    def restaurar(self, id):
        try:
            self.banco.execute("BEGIN")

            self.cursorReg.execute("""
                INSERT INTO reg (titulo, dominio, usuario, senha_criptografada)
                SELECT titulo, dominio, usuario, senha_criptografada
                FROM reg_deletados
                WHERE id = ?
            """, (id,))

            self.cursorReg.execute("""
                DELETE FROM reg_deletados WHERE id = ?
            """, (id,))

            self.banco.commit()

        except Exception:
            self.banco.rollback()
            raise