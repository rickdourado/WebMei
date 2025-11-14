import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { apiService } from '../services/api';

function VagaDetalhes() {
  const { filename } = useParams();
  const [vaga, setVaga] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadVaga();
  }, [filename]);

  const loadVaga = async () => {
    try {
      const response = await apiService.getServico(filename);
      setVaga(response.data);
    } catch (error) {
      console.error('Erro ao carregar vaga:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Carregando...</div>;
  if (!vaga) return <div className="error">Vaga não encontrada</div>;

  return (
    <div className="container">
      <header>
        <h1>Detalhes da Oportunidade</h1>
        <nav>
          <Link to="/vagas">Voltar</Link>
        </nav>
      </header>

      <main>
        <div className="vaga-detalhes">
          <h2>{vaga.titulo_servico}</h2>
          
          <div className="info-group">
            <label>Órgão Demandante:</label>
            <p>{vaga.orgao_demandante}</p>
          </div>

          <div className="info-group">
            <label>Tipo de Atividade:</label>
            <p>{vaga.tipo_atividade}</p>
          </div>

          <div className="info-group">
            <label>Especificação:</label>
            <p>{vaga.especificacao_atividade}</p>
          </div>

          <div className="info-group">
            <label>Descrição:</label>
            <p>{vaga.descricao_servico}</p>
          </div>

          {vaga.outras_informacoes && (
            <div className="info-group">
              <label>Outras Informações:</label>
              <p>{vaga.outras_informacoes}</p>
            </div>
          )}

          <div className="info-group">
            <label>Endereço:</label>
            <p>{vaga.endereco}, {vaga.numero} - {vaga.bairro}</p>
          </div>

          <div className="info-group">
            <label>Forma de Pagamento:</label>
            <p>{vaga.forma_pagamento}</p>
          </div>

          <div className="info-group">
            <label>Prazo de Pagamento:</label>
            <p>{vaga.prazo_pagamento}</p>
          </div>

          <div className="info-group">
            <label>Prazo de Expiração:</label>
            <p>{vaga.prazo_expiracao}</p>
          </div>

          <div className="info-group">
            <label>Data Limite de Execução:</label>
            <p>{vaga.data_limite_execucao}</p>
          </div>

          <a 
            href={apiService.downloadServico(filename)} 
            className="btn-download"
            download
          >
            Baixar CSV
          </a>
        </div>
      </main>
    </div>
  );
}

export default VagaDetalhes;
