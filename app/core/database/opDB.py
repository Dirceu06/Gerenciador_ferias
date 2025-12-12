import sqlite3
from cryptography.fernet import Fernet

class Banco:
    _instance = None  # SINGLETON
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self,login='',Chave=''):
        if Banco._initialized: return
        
        self.banco = sqlite3.connect(f"app/core/database/dadosUser/reg_{login}.db",check_same_thread=False)
        
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
     
    def lerReg(self,condicao=False,pesquisa=''):
        if not condicao:
            self.cursorReg.execute("""
                SELECT id, titulo, dominio, usuario, 
                    senha_criptografada, 
                    datetime(data_criacao) as data_criacao
                FROM reg 
                ORDER BY data_criacao DESC
            """)
        else:
            self.cursorReg.execute("""
                SELECT id, titulo, dominio, usuario, 
                    senha_criptografada, 
                    datetime(data_criacao) as data_criacao
                FROM reg where dominio like ?
                ORDER BY data_criacao DESC
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

    def deletarReg(self,reg):
        self.cursorReg.execute(f"""Delete from reg where id == ?""",(reg,))
        self.banco.commit()
    
    def update(self,id,titulo,dominio,usuario,senha):
        self.cursorReg.execute("""update reg set titulo=?, dominio=?, usuario=?, senha_criptografada=? where id=?;""", (titulo,dominio,usuario,self.criptografar(senha),id))
        self.banco.commit()
        
