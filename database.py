"""
Módulo para gerenciamento de conexão com banco de dados MySQL
"""

import os
import pymysql
import bcrypt as bcrypt_lib
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class DatabaseManager:
    """Gerenciador de conexão com MySQL"""
    
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'servicosmei'),
            'charset': os.getenv('DB_CHARSET', 'utf8mb4')
        }
    
    def get_connection(self):
        """Retorna uma conexão com o banco"""
        return pymysql.connect(**self.config)
    
    def authenticate_user(self, login, password):
        """
        Autentica usuário na tabela authuser
        
        Args:
            login (str): Login do usuário
            password (str): Senha em texto plano
            
        Returns:
            dict: Dados do usuário se autenticado, None caso contrário
        """
        try:
            connection = self.get_connection()
            
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                # Busca usuário pelo login
                cursor.execute("SELECT id, login, senha FROM authuser WHERE login = %s", (login,))
                user = cursor.fetchone()
                
                if not user:
                    return None
                
                stored_password = user['senha']
                
                # Verifica se a senha armazenada é um hash bcrypt
                if stored_password.startswith('$2b$') or stored_password.startswith('$2a$'):
                    # Senha com hash - verifica usando bcrypt
                    is_valid = bcrypt_lib.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))
                else:
                    # Senha em texto plano - comparação direta (inseguro, mas compatível)
                    is_valid = password == stored_password
                
                if is_valid:
                    return {
                        'id': user['id'],
                        'login': user['login']
                    }
                
                return None
                
        except Exception as e:
            print(f"Erro na autenticação: {e}")
            return None
        finally:
            if 'connection' in locals():
                connection.close()
    
    def update_user_password_hash(self, login, new_password):
        """
        Atualiza senha do usuário com hash bcrypt
        
        Args:
            login (str): Login do usuário
            new_password (str): Nova senha em texto plano
            
        Returns:
            bool: True se atualizado com sucesso
        """
        try:
            # Gera hash da nova senha
            salt = bcrypt_lib.gensalt()
            hashed = bcrypt_lib.hashpw(new_password.encode('utf-8'), salt)
            
            connection = self.get_connection()
            
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE authuser SET senha = %s WHERE login = %s",
                    (hashed.decode('utf-8'), login)
                )
                connection.commit()
                
                return cursor.rowcount > 0
                
        except Exception as e:
            print(f"Erro ao atualizar senha: {e}")
            return False
        finally:
            if 'connection' in locals():
                connection.close()
    
    def list_users(self):
        """
        Lista todos os usuários (sem senhas)
        
        Returns:
            list: Lista de usuários
        """
        try:
            connection = self.get_connection()
            
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT id, login FROM authuser ORDER BY login")
                return cursor.fetchall()
                
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            return []
        finally:
            if 'connection' in locals():
                connection.close()