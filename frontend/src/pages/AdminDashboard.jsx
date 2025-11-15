import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { apiService } from '../services/api';
import Header from '../components/Header';

function AdminDashboard() {
  const navigate = useNavigate();
  const [vagas, setVagas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await apiService.checkAuth();
      if (!response.data.authenticated) {
        navigate('/admin/login');
        return;
      }
      setUser(response.data.user);
      loadVagas();
    } catch (error) {
      navigate('/admin/login');
    }
  };

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

  const handleDelete = async (servicoId) => {
    if (!confirm('Tem certeza que deseja excluir esta vaga?')) return;

    try {
      await apiService.deleteServico(servicoId);
      setVagas(vagas.filter(v => v.id !== servicoId));
    } catch (error) {
      alert('Erro ao excluir vaga');
    }
  };

  const handleLogout = async () => {
    try {
      await apiService.logout();
      navigate('/admin/login');
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
    }
  };

  if (loading) return <div className="loading">Carregando...</div>;

  return (
    <div className="container">
      <Header 
        title={`Admin — Olá, ${user?.username || 'Admin'}`} 
        showAdmin={false}
        showLogout={true}
        onLogout={handleLogout}
      />

      <main>
        <h2 style={{ marginTop: 0, marginBottom: '16px' }}>Vagas Cadastradas ({vagas.length})</h2>

        <div className="admin-table">
          {vagas.length === 0 ? (
            <p>Nenhuma vaga cadastrada.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Título</th>
                  <th>Tipo</th>
                  <th>Bairro</th>
                  <th>Expira em</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {vagas.map(vaga => (
                  <tr key={vaga.id}>
                    <td>{vaga.titulo_servico}</td>
                    <td>{vaga.tipo_atividade}</td>
                    <td>{vaga.bairro}</td>
                    <td>{vaga.prazo_expiracao}</td>
                    <td>
                      <Link to={`/vaga/${vaga.id}`} className="btn-view">Ver</Link>
                      <button 
                        onClick={() => handleDelete(vaga.id)} 
                        className="btn-delete"
                      >
                        Excluir
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </main>
    </div>
  );
}

export default AdminDashboard;
