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
    
    def insert_servico(self, data):
        """
        Insere um novo serviço na tabela servicos_mei
        
        Args:
            data (dict): Dicionário com os dados do serviço
                - orgao_demandante (str)
                - titulo_servico (str)
                - tipo_atividade (str, opcional)
                - especificacao_atividade (str)
                - descricao_servico (str)
                - outras_informacoes (str, opcional)
                - endereco (str)
                - numero (str)
                - bairro (str)
                - forma_pagamento (str)
                - prazo_pagamento (str)
                - prazo_expiracao (str, formato YYYY-MM-DD)
                - data_limite_execucao (str, formato YYYY-MM-DD)
                - arquivo_csv (str, opcional)
                
        Returns:
            int: ID do serviço inserido ou None em caso de erro
        """
        try:
            connection = self.get_connection()
            
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO servicos_mei (
                        orgao_demandante, titulo_servico, tipo_atividade, 
                        especificacao_atividade, descricao_servico, outras_informacoes,
                        endereco, numero, bairro, forma_pagamento, prazo_pagamento,
                        prazo_expiracao, data_limite_execucao
                    ) VALUES (
                        %(orgao_demandante)s, %(titulo_servico)s, %(tipo_atividade)s,
                        %(especificacao_atividade)s, %(descricao_servico)s, %(outras_informacoes)s,
                        %(endereco)s, %(numero)s, %(bairro)s, %(forma_pagamento)s, %(prazo_pagamento)s,
                        %(prazo_expiracao)s, %(data_limite_execucao)s
                    )
                """
                
                cursor.execute(sql, data)
                connection.commit()
                
                return cursor.lastrowid
                
        except Exception as e:
            print(f"Erro ao inserir serviço no banco de dados: {e}")
            return None
        finally:
            if 'connection' in locals():
                connection.close()
    
    def list_servicos(self, limit=None, offset=0):
        """
        Lista todos os serviços cadastrados
        
        Args:
            limit (int, opcional): Número máximo de registros
            offset (int, opcional): Offset para paginação
            
        Returns:
            list: Lista de serviços
        """
        try:
            connection = self.get_connection()
            
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                    SELECT 
                        id, orgao_demandante, titulo_servico, tipo_atividade,
                        especificacao_atividade, descricao_servico, outras_informacoes,
                        endereco, numero, bairro, forma_pagamento, prazo_pagamento,
                        prazo_expiracao, data_limite_execucao, data_criacao
                    FROM servicos_mei WHERE ativo = 1
                    ORDER BY data_criacao DESC
                """
                
                if limit:
                    sql += f" LIMIT {int(limit)} OFFSET {int(offset)}"
                
                cursor.execute(sql)
                return cursor.fetchall()
                
        except Exception as e:
            print(f"Erro ao listar serviços: {e}")
            return []
        finally:
            if 'connection' in locals():
                connection.close()
    
    def get_servico_by_id(self, servico_id):
        """
        Busca um serviço específico por ID
        
        Args:
            servico_id (int): ID do serviço
            
        Returns:
            dict: Dados do serviço ou None se não encontrado
        """
        try:
            connection = self.get_connection()
            
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                sql = """
                    SELECT 
                        id, orgao_demandante, titulo_servico, tipo_atividade,
                        especificacao_atividade, descricao_servico, outras_informacoes,
                        endereco, numero, bairro, forma_pagamento, prazo_pagamento,
                        prazo_expiracao, data_limite_execucao, data_criacao
                    FROM servicos_mei
                    WHERE ativo = 1 AND id = %s
                """
                
                cursor.execute(sql, (servico_id,))
                return cursor.fetchone()
                
        except Exception as e:
            print(f"Erro ao buscar serviço: {e}")
            return None
        finally:
            if 'connection' in locals():
                connection.close()
    
    def delete_servico(self, servico_id):
        """
        Deleta um serviço do banco de dados
        
        Args:
            servico_id (int): ID do serviço
            
        Returns:
            bool: True se deletado com sucesso
        """
        try:
            connection = self.get_connection()
            
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM servicos_mei WHERE id = %s", (servico_id,))
                connection.commit()
                
                return cursor.rowcount > 0
                
        except Exception as e:
            print(f"Erro ao deletar serviço: {e}")
            return False
        finally:
            if 'connection' in locals():
                connection.close()
    
    def update_servico(self, servico_id, data):
        """
        Atualiza um serviço existente
        
        Args:
            servico_id (int): ID do serviço
            data (dict): Dicionário com os dados a atualizar
            
        Returns:
            bool: True se atualizado com sucesso
        """
        try:
            connection = self.get_connection()
            
            with connection.cursor() as cursor:
                sql = """
                    UPDATE servicos_mei SET
                        orgao_demandante = %(orgao_demandante)s,
                        titulo_servico = %(titulo_servico)s,
                        tipo_atividade = %(tipo_atividade)s,
                        especificacao_atividade = %(especificacao_atividade)s,
                        descricao_servico = %(descricao_servico)s,
                        outras_informacoes = %(outras_informacoes)s,
                        endereco = %(endereco)s,
                        numero = %(numero)s,
                        bairro = %(bairro)s,
                        forma_pagamento = %(forma_pagamento)s,
                        prazo_pagamento = %(prazo_pagamento)s,
                        prazo_expiracao = %(prazo_expiracao)s,
                        data_limite_execucao = %(data_limite_execucao)s
                    WHERE id = %(id)s
                """
                
                data['id'] = servico_id
                cursor.execute(sql, data)
                connection.commit()
                
                return cursor.rowcount > 0
                
        except Exception as e:
            print(f"Erro ao atualizar serviço: {e}")
            return False
        finally:
            if 'connection' in locals():
                connection.close()
    
    def count_servicos(self):
        """
        Conta o total de serviços cadastrados
        
        Returns:
            int: Número total de serviços
        """
        try:
            connection = self.get_connection()
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) as total FROM servicos_mei")
                result = cursor.fetchone()
                return result[0] if result else 0
                
        except Exception as e:
            print(f"Erro ao contar serviços: {e}")
            return 0
        finally:
            if 'connection' in locals():
                connection.close()