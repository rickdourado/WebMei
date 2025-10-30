from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session
from datetime import datetime
import os
import csv


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')

# Diretório para CSVs
BASE_DIR = os.path.dirname(__file__)
CSV_DIR = os.path.join(BASE_DIR, 'CSV')
os.makedirs(CSV_DIR, exist_ok=True)

# Carregar opções únicas de OCUPACAO do CSV
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
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return ocupacoes or ['Teste 1', 'Teste 2']

OCUPACAO_CSV = os.path.join(os.path.dirname(__file__), 'refs', 'ServicosConsolidados.csv')
TIPO_ATIVIDADE_OPCOES = load_unique_ocupacoes(OCUPACAO_CSV)

# Mapeamento OCUPACAO -> lista de SERVICO (sem duplicados, ordem preservada)
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

OCUPACAO_TO_SERVICOS = load_ocupacao_to_servicos(OCUPACAO_CSV)


@app.route('/')
def index():
    today_iso = datetime.now().strftime('%Y-%m-%d')
    return render_template(
        'index.html',
        today_iso=today_iso,
        tipo_atividade_opcoes=TIPO_ATIVIDADE_OPCOES,
        especificacao_atividade_opcoes=['Teste 1', 'Teste 2'],
        forma_pagamento_opcoes=['Cheque', 'Dinheiro', 'Cartão', 'Transferência'],
        ocupacao_to_servicos=OCUPACAO_TO_SERVICOS,
    )


@app.route('/create_service', methods=['POST'])
def create_service():
    # Coleta básica dos dados do formulário
    data = {
        'orgao_demandante': request.form.get('orgao_demandante', '').strip(),
        'titulo_servico': request.form.get('titulo_servico', '').strip(),
        'tipo_atividade': request.form.get('tipo_atividade', '').strip(),
        'especificacao_atividade': request.form.get('especificacao_atividade', '').strip(),
        'descricao_servico': request.form.get('descricao_servico', '').strip(),
        'outras_informacoes': request.form.get('outras_informacoes', '').strip(),
        'endereco': request.form.get('endereco', '').strip(),
        'numero': request.form.get('numero', '').strip(),
        'bairro': request.form.get('bairro', '').strip(),
        'forma_pagamento': request.form.get('forma_pagamento', '').strip(),
        'prazo_pagamento': request.form.get('prazo_pagamento', '').strip(),
        'prazo_expiracao': request.form.get('prazo_expiracao', '').strip(),  # DD/MM/AAAA
        'data_limite_execucao': request.form.get('data_limite_execucao', '').strip(),  # YYYY-MM-DD
    }

    # Validação mínima de obrigatórios
    erros = []
    obrigatorios = [
        ('orgao_demandante', 'Órgão Demandante'),
        ('titulo_servico', 'Título do serviço'),
        ('especificacao_atividade', 'Especificação da Atividade'),
        ('descricao_servico', 'Descrição do Serviço'),
        ('endereco', 'Endereço'),
        ('numero', 'Número'),
        ('bairro', 'Bairro'),
        ('forma_pagamento', 'Forma de pagamento'),
        ('prazo_pagamento', 'Prazo de pagamento'),
        ('prazo_expiracao', 'Prazo para expiração da oportunidade'),
        ('data_limite_execucao', 'Data limite para execução do serviço'),
    ]

    for key, label in obrigatorios:
        if not data.get(key):
            erros.append(f'{label} é obrigatório.')

    # Número precisa ser numérico
    if data.get('numero') and not data['numero'].isdigit():
        erros.append('Número deve conter apenas dígitos.')

    if erros:
        for e in erros:
            flash(e, 'error')
        return redirect(url_for('index'))

    # Persistência em CSV
    def safe_slug(texto: str) -> str:
        permitidos = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
        texto = texto.replace(' ', '_')
        return ''.join(ch for ch in texto if ch in permitidos)[:80] or 'vaga'

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    slug = safe_slug(data['titulo_servico'])
    filename = f"{slug}_{timestamp}.csv"
    filepath = os.path.join(CSV_DIR, filename)

    headers = [
        'orgao_demandante','titulo_servico','tipo_atividade','especificacao_atividade',
        'descricao_servico','outras_informacoes','endereco','numero','bairro',
        'forma_pagamento','prazo_pagamento','prazo_expiracao','data_limite_execucao'
    ]
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerow(data)

    flash('Serviço cadastrado com sucesso!', 'success')
    return render_template('service_success.html', data=data, csv_file=filename)


# Download de CSV gerado
@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(CSV_DIR, filename, as_attachment=True)

# Listagem pública de vagas
@app.route('/vagas')
def vagas_public():
    vagas = []
    for name in sorted(os.listdir(CSV_DIR)):
        if not name.lower().endswith('.csv'):
            continue
        try:
            with open(os.path.join(CSV_DIR, name), 'r', encoding='utf-8') as f:
                r = csv.DictReader(f)
                row = next(r, None)
                if row:
                    vagas.append({
                        'arquivo': name,
                        'titulo_servico': row.get('titulo_servico',''),
                        'tipo_atividade': row.get('tipo_atividade',''),
                        'bairro': row.get('bairro',''),
                        'prazo_expiracao': row.get('prazo_expiracao',''),
                    })
        except Exception:
            continue
    return render_template('vagas_public.html', vagas=vagas)

# Visualização de vaga individual
@app.route('/vaga/<path:filename>')
def vaga_view(filename):
    path = os.path.join(CSV_DIR, filename)
    if not os.path.isfile(path):
        flash('Vaga não encontrada.', 'error')
        return redirect(url_for('vagas_public'))
    with open(path, 'r', encoding='utf-8') as f:
        r = csv.DictReader(f)
        data = next(r, None) or {}
    return render_template('vaga_view.html', data=data, csv_file=filename)

# -----------------------------
# Admin: login/logout/dashboard
# -----------------------------
def login_required(view_func):
    from functools import wraps
    @wraps(view_func)
    def _wrapped(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Faça login para acessar esta página.', 'warning')
            return redirect(url_for('admin_login'))
        return view_func(*args, **kwargs)
    return _wrapped

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username','')
        password = request.form.get('password','')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Credenciais inválidas.', 'error')
        return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    flash('Logout realizado com sucesso.', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    vagas = []
    for name in sorted(os.listdir(CSV_DIR)):
        if not name.lower().endswith('.csv'):
            continue
        try:
            with open(os.path.join(CSV_DIR, name), 'r', encoding='utf-8') as f:
                r = csv.DictReader(f)
                row = next(r, None)
                if row:
                    vagas.append({
                        'arquivo': name,
                        'titulo_servico': row.get('titulo_servico',''),
                        'tipo_atividade': row.get('tipo_atividade',''),
                        'bairro': row.get('bairro',''),
                        'prazo_expiracao': row.get('prazo_expiracao',''),
                    })
        except Exception:
            continue
    return render_template('admin_dashboard.html', vagas=vagas)

@app.route('/admin/delete/<path:filename>', methods=['POST'])
@login_required
def admin_delete(filename):
    path = os.path.join(CSV_DIR, filename)
    if os.path.isfile(path):
        try:
            os.remove(path)
            flash('Vaga excluída com sucesso.', 'success')
        except Exception as e:
            flash(f'Erro ao excluir vaga: {e}', 'error')
    else:
        flash('Arquivo não encontrado.', 'error')
    return redirect(url_for('admin_dashboard'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)

