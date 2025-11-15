import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { apiService } from '../services/api';
import Header from '../components/Header';

function Vagas() {
  const [vagas, setVagas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadVagas();
  }, []);

  const loadVagas = async () => {
    try {
      const response = await apiService.getServicos();
      setVagas(response.data);
    } catch (error) {
      console.error('Erro ao carregar vagas:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Carregando vagas...</div>;

  return (
    <div className="container">
      <Header title="Vagas MEI" />

      <main>
        <h2 style={{ marginTop: 0, marginBottom: '16px' }}>Vagas cadastradas</h2>
        <div className="vagas-grid">
          {vagas.length === 0 ? (
            <p>Nenhuma vaga cadastrada ainda.</p>
          ) : (
            vagas.map(vaga => (
              <div key={vaga.id} className="vaga-card">
                <h3>{vaga.titulo_servico}</h3>
                <p><strong>Tipo:</strong> {vaga.tipo_atividade}</p>
                <p><strong>Bairro:</strong> {vaga.bairro}</p>
                <p><strong>Expira em:</strong> {vaga.prazo_expiracao}</p>
                <Link to={`/vaga/${vaga.id}`} className="btn-detalhes">
                  Ver Detalhes
                </Link>
              </div>
            ))
          )}
        </div>
      </main>
    </div>
  );
}

export default Vagas;
