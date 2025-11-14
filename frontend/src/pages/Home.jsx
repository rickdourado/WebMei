import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';

function Home() {
  const navigate = useNavigate();
  const [config, setConfig] = useState(null);
  const [formData, setFormData] = useState({
    orgao_demandante: '',
    titulo_servico: '',
    tipo_atividade: '',
    especificacao_atividade: '',
    descricao_servico: '',
    outras_informacoes: '',
    endereco: '',
    numero: '',
    bairro: '',
    forma_pagamento: '',
    prazo_pagamento: '',
    prazo_expiracao: '',
    data_limite_execucao: '',
  });
  const [especificacoes, setEspecificacoes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const response = await apiService.getConfig();
      setConfig(response.data);
      setFormData(prev => ({ ...prev, prazo_expiracao: response.data.today }));
    } catch (error) {
      console.error('Erro ao carregar configurações:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));

    if (name === 'tipo_atividade' && config) {
      setEspecificacoes(config.especificacaoAtividade[value] || []);
      setFormData(prev => ({ ...prev, especificacao_atividade: '' }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      const response = await apiService.createServico(formData);
      setMessage({ type: 'success', text: 'Serviço cadastrado com sucesso!' });
      
      setTimeout(() => {
        navigate('/vagas');
      }, 2000);
    } catch (error) {
      const errorMsg = error.response?.data?.errors?.join(', ') || 'Erro ao cadastrar serviço';
      setMessage({ type: 'error', text: errorMsg });
    } finally {
      setLoading(false);
    }
  };

  if (!config) return <div className="loading">Carregando...</div>;

  return (
    <div className="container">
      <header>
        <h1>Portal Empreendedor Unificado</h1>
        <nav>
          <a href="/vagas">Ver Vagas</a>
          <a href="/admin/login">Admin</a>
        </nav>
      </header>

      <main>
        <h2>Cadastrar Nova Oportunidade</h2>

        {message && (
          <div className={`message ${message.type}`}>
            {message.text}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Órgão Demandante *</label>
            <select name="orgao_demandante" value={formData.orgao_demandante} onChange={handleChange} required>
              <option value="">Selecione...</option>
              {config.orgaos.map(orgao => (
                <option key={orgao} value={orgao}>{orgao}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Título do Serviço *</label>
            <input type="text" name="titulo_servico" value={formData.titulo_servico} onChange={handleChange} required />
          </div>

          <div className="form-group">
            <label>Tipo de Atividade</label>
            <select name="tipo_atividade" value={formData.tipo_atividade} onChange={handleChange}>
              <option value="">Selecione...</option>
              {config.tipoAtividade.map(tipo => (
                <option key={tipo} value={tipo}>{tipo}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Especificação da Atividade *</label>
            <select name="especificacao_atividade" value={formData.especificacao_atividade} onChange={handleChange} required>
              <option value="">Selecione...</option>
              {especificacoes.map(esp => (
                <option key={esp} value={esp}>{esp}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Descrição do Serviço *</label>
            <textarea name="descricao_servico" value={formData.descricao_servico} onChange={handleChange} required rows="4" />
          </div>

          <div className="form-group">
            <label>Outras Informações</label>
            <textarea name="outras_informacoes" value={formData.outras_informacoes} onChange={handleChange} rows="3" />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Endereço *</label>
              <input type="text" name="endereco" value={formData.endereco} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Número *</label>
              <input type="text" name="numero" value={formData.numero} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Bairro *</label>
              <input type="text" name="bairro" value={formData.bairro} onChange={handleChange} required />
            </div>
          </div>

          <div className="form-group">
            <label>Forma de Pagamento *</label>
            <select name="forma_pagamento" value={formData.forma_pagamento} onChange={handleChange} required>
              <option value="">Selecione...</option>
              {config.formaPagamento.map(forma => (
                <option key={forma} value={forma}>{forma}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Prazo de Pagamento *</label>
            <input type="text" name="prazo_pagamento" value={formData.prazo_pagamento} onChange={handleChange} required />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Prazo de Expiração *</label>
              <input type="date" name="prazo_expiracao" value={formData.prazo_expiracao} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label>Data Limite de Execução *</label>
              <input type="date" name="data_limite_execucao" value={formData.data_limite_execucao} onChange={handleChange} required />
            </div>
          </div>

          <button type="submit" disabled={loading}>
            {loading ? 'Cadastrando...' : 'Cadastrar Serviço'}
          </button>
        </form>
      </main>
    </div>
  );
}

export default Home;
