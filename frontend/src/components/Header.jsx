import { Link, useNavigate } from 'react-router-dom';

function Header({ title = "Portal Empreendedor", showAdmin = true, showLogout = false, onLogout }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    if (onLogout) {
      onLogout();
    } else {
      navigate('/admin/login');
    }
  };

  return (
    <header>
      <div className="header-content">
        <div className="logo-section">
          <img 
            src="/logo_ciclocarioca.png" 
            alt="Ciclo Carioca" 
            onError={(e) => e.target.style.display = 'none'}
          />
          <h1 className="logo-title">Oportunidades Cariocas — {title}</h1>
        </div>
        <nav>
          <Link to="/" className="nav-link home-link" title="Página Inicial">
            <i className="fas fa-home"></i>
          </Link>
          <Link to="/vagas" className="nav-link">Vagas</Link>
          {showAdmin && !showLogout && (
            <Link to="/admin/login" className="nav-link">Admin</Link>
          )}
          {showLogout && (
            <button onClick={handleLogout} className="nav-link">
              <i className="fas fa-sign-out-alt"></i> Sair
            </button>
          )}
        </nav>
      </div>
    </header>
  );
}

export default Header;
