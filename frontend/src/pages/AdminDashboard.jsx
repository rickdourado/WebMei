import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { apiService } from '../services/api';

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

  const handleDelete = async (filename) => {
    if (!confirm('Tem certeza que deseja excluir esta vaga?')) return;

    try {
      await apiService.deleteServico(filename);
      setVagas(vagas.filter(v => v.arquivo !== filename));
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
      <header>
        <h1>Painel Administrativo</h1>
        <nav>
          <span>Olá, {user?.username}</span>
          <Link to="/">Início</Link>
          <button onClick={handleLogout} className="btn-logout">Sair</button>
        </nav>
      </header>

      <main>
        <h2>Vagas Cadastradas ({vagas.length})</h2>

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
                  <tr key={vaga.arquivo}>
                    <td>{vaga.titulo_servico}</td>
                    <td>{vaga.tipo_atividade}</td>
                    <td>{vaga.bairro}</td>
                    <td>{vaga.prazo_expiracao}</td>
                    <td>
                      <Link to={`/vaga/${vaga.arquivo}`} className="btn-view">Ver</Link>
                      <button 
                        onClick={() => handleDelete(vaga.arquivo)} 
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
