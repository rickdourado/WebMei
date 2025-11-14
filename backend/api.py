from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from datetime import datetime
import os
import csv
import bcrypt as bcrypt_lib
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')

# Configuração CORS para permitir requisições do React
CORS(app, supports_credentials=True, origins=['http://localhost:3000', 'http://localhost:5173'])

# Inicializa gerenciador de banco de dados (opcional)
db_manager = None
try:
    from database import DatabaseManager
    db_manager = DatabaseManager()
    print("✓ Banco de dados MySQL conectado")
except Exception as e:
    print(f"⚠ Banco de dados não disponível: {e}")
    print("⚠ Aplicação funcionará apenas com CSV")

# Configurações de admin
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')
ADMIN_PASSWORD_HASH = os.getenv('ADMIN_PASSWORD_HASH', None)

# Diretórios
BASE_DIR = os.path.dirname(__file__)
CSV_DIR = os.path.join(BASE_DIR, 'CSV')
os.makedirs(CSV_DIR, exist_ok=True)

# Funções auxiliares
def load_unique_ocupacoes(csv_path):
    ocupacoes = []
    vistos = set()
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                valor = (row.get('OCUPACAO') or '').strip()
                if valor and valor not in vistos:
                    vistos.add(valor)
                    ocupacoes.append(valor)
    except Exception:
        pass
    return ocupacoes or []

def load_ocupacao_to_servicos(csv_path):
    mapping = {}
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ocupacao = (row.get('OCUPACAO') or '').strip()
                servico = (row.get('SERVICO') or '').strip()
                if not ocupacao or not servico:
                    continue
                if ocupacao not in mapping:
                    mapping[ocupacao] = []
                if servico not in mapping[ocupacao]:
                    mapping[ocupacao].append(servico)
    except Exception:
        pass
    return mapping

def load_orgaos():
    orgaos = []
    try:
        orgaos_csv = os.path.join(os.path.dirname(__file__), 'refs', 'lista_orgaos.csv')
        with open(orgaos_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                orgao = (row.get('orgao') or '').strip()
                if orgao:
                    orgaos.append(orgao)
        orgaos.sort()
    except Exception as e:
        print(f"⚠ Erro ao carregar órgãos: {e}")
    return orgaos

def safe_slug(texto: str) -> str:
    permitidos = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    texto = texto.replace(' ', '_')
    return ''.join(ch for ch in texto if ch in permitidos)[:80] or 'vaga'

def verify_admin_password(username, password):
    # Tenta autenticar via banco de dados primeiro
    if db_manager:
        try:
            user = db_manager.authenticate_user(username, password)
            if user:
                return user
        except Exception as e:
            print(f"⚠ Erro ao autenticar via banco: {e}")
    
    # Fallback: autenticação via .env
    if username == ADMIN_USERNAME:
        if ADMIN_PASSWORD_HASH:
            try:
                if bcrypt_lib.checkpw(password.encode('utf-8'), ADMIN_PASSWORD_HASH.encode('utf-8')):
                    return {'id': 0, 'login': username}
            except Exception:
                pass
        elif password == ADMIN_PASSWORD:
            return {'id': 0, 'login': username}
    
    return None

# Carrega dados de referência
OCUPACAO_CSV = os.path.join(os.path.dirname(__file__), 'refs', 'ServicosConsolidados.csv')
TIPO_ATIVIDADE_OPCOES = load_unique_ocupacoes(OCUPACAO_CSV)
OCUPACAO_TO_SERVICOS = load_ocupacao_to_servicos(OCUPACAO_CSV)
ORGAOS_OPCOES = load_orgaos()

# ==================== ROTAS API ====================

@app.route('/')
def index():
    """Rota raiz - informações da API"""
    return jsonify({
        'name': 'Portal Empreendedor API',
        'version': '2.0.0',
        'status': 'online',
        'database': 'MySQL' if db_manager else 'Indisponível',
        'endpoints': {
            'config': '/api/config',
            'list_servicos': 'GET /api/servicos',
            'get_servico': 'GET /api/servicos/<id>',
            'create_servico': 'POST /api/servicos',
            'export_csv': 'GET /api/servicos/<id>/export',
            'login': 'POST /api/auth/login',
            'logout': 'POST /api/auth/logout',
            'check_auth': 'GET /api/auth/check',
            'delete_servico': 'DELETE /api/admin/servicos/<id>'
        }
    })

@app.route('/api/config', methods=['GET'])
def get_config():
    """Retorna configurações iniciais para o frontend"""
    return jsonify({
        'orgaos': ORGAOS_OPCOES,
        'tipoAtividade': TIPO_ATIVIDADE_OPCOES,
        'especificacaoAtividade': OCUPACAO_TO_SERVICOS,
        'formaPagamento': ['Cheque', 'Dinheiro', 'Cartão', 'Transferência'],
        'today': datetime.now().strftime('%Y-%m-%d')
    })

@app.route('/api/servicos', methods=['GET'])
def list_servicos():
    """Lista todos os serviços cadastrados"""
    if not db_manager:
        return jsonify({'error': 'Banco de dados não disponível'}), 500
    
    try:
        servicos = db_manager.list_servicos()
        
        # Formata datas para string
        for servico in servicos:
            if servico.get('prazo_expiracao'):
                servico['prazo_expiracao'] = str(servico['prazo_expiracao'])
            if servico.get('data_limite_execucao'):
                servico['data_limite_execucao'] = str(servico['data_limite_execucao'])
            if servico.get('data_cadastro'):
                servico['data_cadastro'] = str(servico['data_cadastro'])
        
        return jsonify(servicos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/servicos/<int:servico_id>', methods=['GET'])
def get_servico(servico_id):
    """Retorna detalhes de um serviço específico"""
    if not db_manager:
        return jsonify({'error': 'Banco de dados não disponível'}), 500
    
    try:
        servico = db_manager.get_servico_by_id(servico_id)
        
        if not servico:
            return jsonify({'error': 'Serviço não encontrado'}), 404
        
        # Formata datas para string
        if servico.get('prazo_expiracao'):
            servico['prazo_expiracao'] = str(servico['prazo_expiracao'])
        if servico.get('data_limite_execucao'):
            servico['data_limite_execucao'] = str(servico['data_limite_execucao'])
        if servico.get('data_cadastro'):
            servico['data_cadastro'] = str(servico['data_cadastro'])
        
        return jsonify(servico)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/servicos', methods=['POST'])
def create_servico():
    """Cria um novo serviço"""
    if not db_manager:
        return jsonify({'error': 'Banco de dados não disponível'}), 500
    
    data = request.json
    
    # Validação
    obrigatorios = [
        'orgao_demandante', 'titulo_servico', 'especificacao_atividade',
        'descricao_servico', 'endereco', 'numero', 'bairro',
        'forma_pagamento', 'prazo_pagamento', 'prazo_expiracao',
        'data_limite_execucao'
    ]
    
    erros = []
    for campo in obrigatorios:
        if not data.get(campo):
            erros.append(f'{campo} é obrigatório')
    
    # Validação de número
    if data.get('numero'):
        numero_limpo = data['numero'].strip().upper()
        if not (numero_limpo.isdigit() or numero_limpo in ['S/N', 'SN', 'S.N.', 'SEM NUMERO', 'SEM NÚMERO']):
            erros.append('Número inválido')
    
    if erros:
        return jsonify({'errors': erros}), 400
    
    # Salva no banco de dados
    try:
        service_id = db_manager.insert_servico(data)
        
        if not service_id:
            return jsonify({'error': 'Erro ao salvar serviço'}), 500
        
        print(f"✓ Serviço inserido no banco com ID: {service_id}")
        
        return jsonify({
            'message': 'Serviço cadastrado com sucesso',
            'id': service_id,
            'data': data
        }), 201
        
    except Exception as e:
        print(f"✗ Erro ao salvar no banco: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/servicos/<int:servico_id>/export', methods=['GET'])
def export_servico_csv(servico_id):
    """Exporta um serviço específico como CSV"""
    if not db_manager:
        return jsonify({'error': 'Banco de dados não disponível'}), 500
    
    try:
        servico = db_manager.get_servico_by_id(servico_id)
        
        if not servico:
            return jsonify({'error': 'Serviço não encontrado'}), 404
        
        # Cria CSV temporário
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        slug = safe_slug(servico['titulo_servico'])
        filename = f"{slug}_{timestamp}.csv"
        filepath = os.path.join(CSV_DIR, filename)
        
        # Garante que o diretório existe
        os.makedirs(CSV_DIR, exist_ok=True)
        
        headers = [
            'orgao_demandante', 'titulo_servico', 'tipo_atividade', 'especificacao_atividade',
            'descricao_servico', 'outras_informacoes', 'endereco', 'numero', 'bairro',
            'forma_pagamento', 'prazo_pagamento', 'prazo_expiracao', 'data_limite_execucao'
        ]
        
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerow({k: servico.get(k, '') for k in headers})
        
        return send_from_directory(CSV_DIR, filename, as_attachment=True)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Autenticação de admin"""
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': 'Usuário e senha obrigatórios'}), 400
    
    user = verify_admin_password(username, password)
    if user:
        session['logged_in'] = True
        session['user_id'] = user['id']
        session['username'] = user['login']
        session.permanent = True
        return jsonify({
            'message': 'Login realizado com sucesso',
            'user': {'id': user['id'], 'username': user['login']}
        })
    
    return jsonify({'error': 'Credenciais inválidas'}), 401

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout de admin"""
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('username', None)
    return jsonify({'message': 'Logout realizado com sucesso'})

@app.route('/api/auth/check', methods=['GET'])
def check_auth():
    """Verifica se usuário está autenticado"""
    if session.get('logged_in'):
        return jsonify({
            'authenticated': True,
            'user': {
                'id': session.get('user_id'),
                'username': session.get('username')
            }
        })
    return jsonify({'authenticated': False})

@app.route('/api/admin/servicos/<int:servico_id>', methods=['DELETE'])
def delete_servico(servico_id):
    """Deleta um serviço (apenas admin)"""
    if not session.get('logged_in'):
        return jsonify({'error': 'Não autorizado'}), 401
    
    if not db_manager:
        return jsonify({'error': 'Banco de dados não disponível'}), 500
    
    try:
        success = db_manager.delete_servico(servico_id)
        
        if success:
            print(f"✓ Serviço {servico_id} deletado com sucesso")
            return jsonify({'message': 'Serviço excluído com sucesso'})
        else:
            return jsonify({'error': 'Serviço não encontrado'}), 404
            
    except Exception as e:
        print(f"✗ Erro ao deletar serviço: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)
