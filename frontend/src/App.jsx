import React, { useState, useEffect } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, RadialLinearScale, ArcElement, Title as ChartTitle, Tooltip, Legend } from 'chart.js';
import { Line, Bar, Pie, Doughnut } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, RadialLinearScale, ArcElement, ChartTitle, Tooltip, Legend);

const API_BASE = "http://localhost:8000";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('hc_token') || '');
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('hc_user') || 'null'));
  const [activeTab, setActiveTab] = useState('dashboard');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogin = (newToken, newUser) => {
    setToken(newToken);
    setUser(newUser);
    localStorage.setItem('hc_token', newToken);
    localStorage.setItem('hc_user', JSON.stringify(newUser));
    if (newUser.role === 'patient') {
      setActiveTab('patient_history');
    } else {
      setActiveTab('dashboard');
    }
  };

  const handleLogout = () => {
    setToken('');
    setUser(null);
    localStorage.removeItem('hc_token');
    localStorage.removeItem('hc_user');
  };

  if (!token || !user) {
    return <LoginView onLogin={handleLogin} />;
  }

  return (
    <div className="min-h-screen bg-background text-slate-200 font-body antialiased flex flex-col md:flex-row">
      {/* Sidebar Navigation - Desktop */}
      <aside className="h-auto md:h-screen w-full md:w-64 bg-surface flex flex-col py-6 border-r border-slate-800 shadow-xl z-50 md:fixed md:left-0 md:top-0">
        {/* Branding Profile Header */}
        <div className="px-6 mb-8 flex flex-col items-start">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center border border-primary/30">
              <span className="material-symbols-outlined text-primary font-bold">medical_services</span>
            </div>
            <span className="font-headline font-bold text-primary text-xl tracking-tight">HeartCare AI</span>
          </div>
          
          <div className="flex items-center gap-3 p-3 rounded-xl bg-slate-800/40 w-full">
            <div className="w-10 h-10 rounded-full bg-primary/30 flex items-center justify-center text-primary font-bold">
              {user.name.split(' ').map(n=>n[0]).join('')}
            </div>
            <div className="flex flex-col overflow-hidden">
              <span className="text-sm font-bold text-white leading-tight truncate">{user.name}</span>
              <span className="text-[10px] text-slate-400 uppercase tracking-wider font-bold truncate">
                {user.role === 'admin' ? 'Administrator' : user.role === 'doctor' ? 'Cardiologist' : 'Patient'}
              </span>
            </div>
          </div>
        </div>

        {/* Sidebar Nav Items */}
        <nav className="flex-1 px-4 space-y-1">
          {user.role !== 'patient' && (
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`w-full text-left px-4 py-3 flex items-center gap-3 transition-all rounded-lg active:scale-95 ${
                activeTab === 'dashboard'
                  ? 'bg-primary/20 text-primary border-l-4 border-primary font-bold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`}
            >
              <span className="material-symbols-outlined">dashboard</span>
              <span>Dashboard</span>
            </button>
          )}

          {user.role !== 'patient' && (
            <button
              onClick={() => setActiveTab('patients')}
              className={`w-full text-left px-4 py-3 flex items-center gap-3 transition-all rounded-lg active:scale-95 ${
                activeTab === 'patients'
                  ? 'bg-primary/20 text-primary border-l-4 border-primary font-bold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`}
            >
              <span className="material-symbols-outlined">group</span>
              <span>Patients</span>
            </button>
          )}

          {user.role !== 'patient' && (
            <button
              onClick={() => setActiveTab('prediction')}
              className={`w-full text-left px-4 py-3 flex items-center gap-3 transition-all rounded-lg active:scale-95 ${
                activeTab === 'prediction'
                  ? 'bg-primary/20 text-primary border-l-4 border-primary font-bold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`}
            >
              <span className="material-symbols-outlined">clinical_notes</span>
              <span>Prediction</span>
            </button>
          )}

          <button
            onClick={() => setActiveTab('patient_history')}
            className={`w-full text-left px-4 py-3 flex items-center gap-3 transition-all rounded-lg active:scale-95 ${
              activeTab === 'patient_history'
                ? 'bg-primary/20 text-primary border-l-4 border-primary font-bold'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
            }`}
          >
            <span className="material-symbols-outlined">history</span>
            <span>History</span>
          </button>

          {user.role !== 'patient' && (
            <button
              onClick={() => setActiveTab('reports')}
              className={`w-full text-left px-4 py-3 flex items-center gap-3 transition-all rounded-lg active:scale-95 ${
                activeTab === 'reports'
                  ? 'bg-primary/20 text-primary border-l-4 border-primary font-bold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`}
            >
              <span className="material-symbols-outlined">description</span>
              <span>Reports</span>
            </button>
          )}

          {user.role !== 'patient' && (
            <button
              onClick={() => setActiveTab('analytics')}
              className={`w-full text-left px-4 py-3 flex items-center gap-3 transition-all rounded-lg active:scale-95 ${
                activeTab === 'analytics'
                  ? 'bg-primary/20 text-primary border-l-4 border-primary font-bold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`}
            >
              <span className="material-symbols-outlined">analytics</span>
              <span>Analytics</span>
            </button>
          )}

          <button
            onClick={() => setActiveTab('settings')}
            className={`w-full text-left px-4 py-3 flex items-center gap-3 transition-all rounded-lg active:scale-95 ${
              activeTab === 'settings'
                ? 'bg-primary/20 text-primary border-l-4 border-primary font-bold'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
            }`}
          >
            <span className="material-symbols-outlined">settings</span>
            <span>Settings</span>
          </button>
        </nav>

        {/* Logout Section */}
        <div className="px-4 mt-auto">
          <button
            onClick={handleLogout}
            className="w-full px-4 py-2 bg-red-950/40 text-red-400 hover:bg-red-900/30 border border-red-900/50 hover:text-red-300 rounded-xl flex items-center justify-center gap-2 transition-all cursor-pointer"
          >
            <span className="material-symbols-outlined text-sm">logout</span>
            <span className="text-sm font-semibold">Sign Out</span>
          </button>
          <div className="text-[9px] text-slate-500 font-bold uppercase tracking-widest mt-4 text-center">
            HeartCare AI • v2.4.0
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 md:pl-64 min-h-screen flex flex-col">
        {/* Top Bar Navigation */}
        <header className="bg-surface/80 backdrop-blur-md border-b border-slate-800 sticky top-0 z-40 flex justify-between items-center px-6 md:px-8 h-20">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setMobileMenuOpen(true)}
              className="md:hidden p-2 hover:bg-slate-800/40 rounded-full text-primary"
            >
              <span className="material-symbols-outlined">menu</span>
            </button>
            <h1 className="font-headline font-black text-primary text-xl md:text-2xl tracking-tight">
              HeartCare AI
            </h1>
          </div>
          
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center text-xs text-slate-400 font-bold border border-slate-700">
                DR
              </div>
              <div className="hidden sm:flex flex-col items-start">
                <span className="text-xs font-bold text-white">{user.name}</span>
                <span className="text-[9px] text-slate-400 uppercase tracking-wider">{user.role}</span>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="px-3 py-1.5 bg-slate-850 hover:bg-slate-800 border border-slate-700 hover:text-red-400 rounded-lg text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer"
            >
              <span className="material-symbols-outlined text-[14px]">logout</span>
              Logout
            </button>
          </div>
        </header>

        {/* Dynamic Views */}
        <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto">
          {activeTab === 'dashboard' && user.role !== 'patient' && (
            <DashboardTab token={token} onNavigate={setActiveTab} />
          )}
          {activeTab === 'patients' && user.role !== 'patient' && (
            <PatientsTab token={token} />
          )}
          {activeTab === 'prediction' && user.role !== 'patient' && (
            <PredictionTab token={token} onNavigate={setActiveTab} />
          )}
          {activeTab === 'patient_history' && (
            <PatientHistoryTab token={token} user={user} />
          )}
          {activeTab === 'reports' && user.role !== 'patient' && (
            <ReportsTab token={token} />
          )}
          {activeTab === 'analytics' && user.role !== 'patient' && (
            <AnalyticsTab token={token} />
          )}
          {activeTab === 'settings' && (
            <SettingsTab token={token} user={user} />
          )}
        </main>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-50 flex md:hidden">
          <div 
            onClick={() => setMobileMenuOpen(false)}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm transition-opacity duration-300"
          ></div>
          
          <div className="relative w-64 max-w-xs bg-surface h-full flex flex-col py-6 px-4 shadow-2xl border-r border-slate-800">
            <div className="flex justify-between items-center mb-8 px-2">
              <span className="font-headline font-bold text-primary text-xl">HeartCare AI</span>
              <button 
                onClick={() => setMobileMenuOpen(false)}
                className="text-slate-400"
              >
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>

            <nav className="space-y-1">
              {user.role !== 'patient' && (
                <button
                  onClick={() => { setActiveTab('dashboard'); setMobileMenuOpen(false); }}
                  className={`w-full text-left px-4 py-3 flex items-center gap-3 rounded-lg ${
                    activeTab === 'dashboard' ? 'bg-primary/20 text-primary font-bold' : 'text-slate-400'
                  }`}
                >
                  <span className="material-symbols-outlined">dashboard</span>
                  <span>Dashboard</span>
                </button>
              )}

              {user.role !== 'patient' && (
                <button
                  onClick={() => { setActiveTab('patients'); setMobileMenuOpen(false); }}
                  className={`w-full text-left px-4 py-3 flex items-center gap-3 rounded-lg ${
                    activeTab === 'patients' ? 'bg-primary/20 text-primary font-bold' : 'text-slate-400'
                  }`}
                >
                  <span className="material-symbols-outlined">group</span>
                  <span>Patients</span>
                </button>
              )}

              {user.role !== 'patient' && (
                <button
                  onClick={() => { setActiveTab('prediction'); setMobileMenuOpen(false); }}
                  className={`w-full text-left px-4 py-3 flex items-center gap-3 rounded-lg ${
                    activeTab === 'prediction' ? 'bg-primary/20 text-primary font-bold' : 'text-slate-400'
                  }`}
                >
                  <span className="material-symbols-outlined">clinical_notes</span>
                  <span>Prediction</span>
                </button>
              )}

              <button
                onClick={() => { setActiveTab('patient_history'); setMobileMenuOpen(false); }}
                className={`w-full text-left px-4 py-3 flex items-center gap-3 rounded-lg ${
                  activeTab === 'patient_history' ? 'bg-primary/20 text-primary font-bold' : 'text-slate-400'
                }`}
              >
                <span className="material-symbols-outlined">history</span>
                <span>History</span>
              </button>

              {user.role !== 'patient' && (
                <button
                  onClick={() => { setActiveTab('reports'); setMobileMenuOpen(false); }}
                  className={`w-full text-left px-4 py-3 flex items-center gap-3 rounded-lg ${
                    activeTab === 'reports' ? 'bg-primary/20 text-primary font-bold' : 'text-slate-400'
                  }`}
                >
                  <span className="material-symbols-outlined">description</span>
                  <span>Reports</span>
                </button>
              )}

              {user.role !== 'patient' && (
                <button
                  onClick={() => { setActiveTab('analytics'); setMobileMenuOpen(false); }}
                  className={`w-full text-left px-4 py-3 flex items-center gap-3 rounded-lg ${
                    activeTab === 'analytics' ? 'bg-primary/20 text-primary font-bold' : 'text-slate-400'
                  }`}
                >
                  <span className="material-symbols-outlined">analytics</span>
                  <span>Analytics</span>
                </button>
              )}

              <button
                onClick={() => { setActiveTab('settings'); setMobileMenuOpen(false); }}
                className={`w-full text-left px-4 py-3 flex items-center gap-3 rounded-lg ${
                  activeTab === 'settings' ? 'bg-primary/20 text-primary font-bold' : 'text-slate-400'
                }`}
              >
                <span className="material-symbols-outlined">settings</span>
                <span>Settings</span>
              </button>
            </nav>
          </div>
        </div>
      )}
    </div>
  );
}

// --------------------- LOGIN VIEW ---------------------
function LoginView({ onLogin }) {
  const [role, setRole] = useState('doctor'); // 'admin', 'doctor', 'patient'
  const [emailInput, setEmailInput] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const details = new URLSearchParams();
      details.append('username', emailInput); // OAuth2 expects 'username' parameter
      details.append('password', password);

      const res = await fetch(`${API_BASE}/api/auth/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: details
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Authentication Failed");
      }

      const data = await res.json();
      
      if (data.role !== role) {
        throw new Error(`Account role is '${data.role}', but you selected '${role}' login.`);
      }

      onLogin(data.access_token, {
        id: data.id,
        role: data.role,
        name: data.name,
        email: data.email
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-slate-100 flex items-center justify-center p-6 antialiased font-body">
      <div className="w-full max-w-md bg-surface border border-slate-800 rounded-3xl p-8 shadow-2xl relative overflow-hidden">
        <div className="absolute -top-12 -left-12 w-32 h-32 bg-primary/20 rounded-full blur-2xl"></div>
        <div className="absolute -bottom-12 -right-12 w-32 h-32 bg-secondary/15 rounded-full blur-2xl"></div>

        <div className="flex flex-col items-center mb-8 relative">
          <div className="w-12 h-12 rounded-full bg-primary/10 border border-primary/30 flex items-center justify-center mb-3">
            <span className="material-symbols-outlined text-primary text-3xl font-bold">medical_services</span>
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">HeartCare AI Portal</h2>
          <p className="text-xs text-slate-400 mt-1">Heart Disease Prediction System</p>
        </div>

        {/* Role Selectors */}
        <div className="grid grid-cols-3 bg-slate-950 p-1.5 rounded-2xl mb-6 border border-slate-900">
          <button
            type="button"
            onClick={() => { setRole('doctor'); setEmailInput(''); setPassword(''); }}
            className={`py-2 rounded-xl text-xs font-bold transition-all ${
              role === 'doctor' ? 'bg-primary text-white shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Doctor
          </button>
          <button
            type="button"
            onClick={() => { setRole('admin'); setEmailInput(''); setPassword(''); }}
            className={`py-2 rounded-xl text-xs font-bold transition-all ${
              role === 'admin' ? 'bg-primary text-white shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Admin
          </button>
          <button
            type="button"
            onClick={() => { setRole('patient'); setEmailInput(''); setPassword(''); }}
            className={`py-2 rounded-xl text-xs font-bold transition-all ${
              role === 'patient' ? 'bg-primary text-white shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Patient
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-950/40 border border-red-900/50 text-red-400 text-xs rounded-xl font-medium">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">
              {role === 'patient' ? 'Patient ID' : 'Doctor Email'}
            </label>
            <input
              type="text"
              required
              value={emailInput}
              onChange={(e) => setEmailInput(e.target.value)}
              placeholder={role === 'patient' ? 'e.g. PAT-001' : 'doctor@heartcare.ai'}
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
            />
          </div>

          <div>
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">
              Password
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder={role === 'patient' ? 'Patient ID or patient123' : 'Enter password'}
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-2 py-3 bg-primary hover:bg-teal-700 text-white font-bold rounded-xl transition-all shadow-lg active:scale-95 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
          >
            {loading ? 'Authenticating...' : 'Sign In'}
          </button>
        </form>

        <div className="mt-6 text-center text-[10px] text-slate-500">
          {role === 'admin' && 'Seed Account: admin@heartcare.ai / admin123'}
          {role === 'doctor' && 'Seed Account: doctor@heartcare.ai / doctor123'}
          {role === 'patient' && 'Seed Account: Register a patient ID, then login with Patient ID / patient123'}
        </div>
      </div>
    </div>
  );
}

// --------------------- DASHBOARD VIEW ---------------------
function DashboardTab({ token, onNavigate }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchStats = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/analytics/summary`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setStats(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, [token]);

  const handleDownloadPDF = async (predId, patientId) => {
    try {
      const res = await fetch(`${API_BASE}/api/reports/${predId}/pdf`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!res.ok) throw new Error("Failed to download PDF");
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `HeartCare_Report_${patientId}_${predId}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      alert("Error: " + error.message);
    }
  };

  if (loading) return <div className="text-center py-12 text-slate-400">Loading diagnostic telemetry...</div>;

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Top Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="glass-panel p-6 rounded-2xl border-l-4 border-l-secondary">
          <div className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">Total Patients</div>
          <div className="text-3xl font-black text-white">{stats?.total_patients || 0}</div>
        </div>
        <div className="glass-panel p-6 rounded-2xl border-l-4 border-l-primary">
          <div className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">Predictions</div>
          <div className="text-3xl font-black text-white">{stats?.predictions_made || 0}</div>
        </div>
        <div className="glass-panel p-6 rounded-2xl border-l-4 border-l-error">
          <div className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">High Risk Patients</div>
          <div className="text-3xl font-black text-error">{stats?.high_risk_patients || 0}</div>
        </div>
        <div className="glass-panel p-6 rounded-2xl border-l-4 border-l-accent">
          <div className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">Low Risk Patients</div>
          <div className="text-3xl font-black text-accent">{stats?.low_risk_patients || 0}</div>
        </div>
      </div>

      {/* Recent Predictions Table */}
      <div className="glass-panel rounded-3xl overflow-hidden">
        <div className="px-6 py-5 border-b border-slate-800 flex justify-between items-center bg-slate-900/40">
          <div>
            <h3 className="text-lg font-bold text-white">Recent predictions</h3>
            <p className="text-xs text-slate-400">Chronological history logs</p>
          </div>
          <button 
            onClick={() => onNavigate('patient_history')}
            className="text-primary text-sm font-bold flex items-center gap-1 hover:underline cursor-pointer"
          >
            View History <span className="material-symbols-outlined text-sm">arrow_forward</span>
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead className="bg-slate-800/30">
              <tr>
                <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Patient</th>
                <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Prediction</th>
                <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Risk %</th>
                <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Confidence</th>
                <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Date</th>
                <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Report</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {stats?.recent_predictions && stats.recent_predictions.length > 0 ? (
                stats.recent_predictions.map((pred) => (
                  <tr key={pred.id} className="hover:bg-slate-800/20 transition-colors">
                    <td className="px-6 py-4 text-sm font-semibold text-white">{pred.patient_name}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2.5 py-0.5 rounded-full text-[9px] font-bold border ${
                        pred.prediction_status === 'HIGH RISK'
                          ? 'bg-red-950/40 text-red-400 border-red-900/50'
                          : pred.prediction_status === 'MEDIUM RISK'
                          ? 'bg-amber-950/40 text-amber-400 border-amber-900/50'
                          : 'bg-emerald-950/40 text-emerald-400 border-emerald-900/50'
                      }`}>
                        {pred.prediction_status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-xs font-semibold text-slate-200">{pred.risk_percentage}%</td>
                    <td className="px-6 py-4 text-xs font-semibold text-primary">{pred.prediction_confidence}%</td>
                    <td className="px-6 py-4 text-xs text-slate-400">{new Date(pred.date).toLocaleDateString()}</td>
                    <td className="px-6 py-4">
                      <button
                        onClick={() => handleDownloadPDF(pred.id, pred.patient_id)}
                        className="text-primary hover:underline font-bold text-xs cursor-pointer flex items-center gap-1"
                      >
                        <span className="material-symbols-outlined text-sm">download</span> PDF
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="6" className="px-6 py-8 text-center text-slate-500 font-medium">
                    No diagnostics logged.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// --------------------- PATIENTS VIEW (LIST & REGISTRATION) ---------------------
function PatientsTab({ token }) {
  const [view, setView] = useState('list'); // 'list' or 'add'
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);

  // Form states
  const [id, setId] = useState('');
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('Male');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [height, setHeight] = useState('');
  const [weight, setWeight] = useState('');

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const fetchPatients = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/patients/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setPatients(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (view === 'list') {
      fetchPatients();
    }
  }, [view, token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const res = await fetch(`${API_BASE}/api/patients/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          id: id.trim(),
          name: name.trim(),
          age: parseInt(age),
          gender,
          phone: phone.trim() || null,
          email: email.trim() || null,
          height: height ? parseFloat(height) : null,
          weight: weight ? parseFloat(weight) : null
        })
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Registration failed");
      }

      setSuccess("Patient profile created successfully!");
      setId('');
      setName('');
      setAge('');
      setPhone('');
      setEmail('');
      setHeight('');
      setWeight('');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Toggle Header */}
      <div className="flex justify-between items-center bg-surface p-4 rounded-2xl border border-slate-800">
        <h3 className="font-bold text-white text-lg">Patient Management</h3>
        <div className="flex gap-2">
          <button
            onClick={() => setView('list')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
              view === 'list' ? 'bg-primary text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Patient List
          </button>
          <button
            onClick={() => setView('add')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
              view === 'add' ? 'bg-primary text-white' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Add Patient
          </button>
        </div>
      </div>

      {view === 'list' ? (
        <div className="glass-panel rounded-3xl overflow-hidden">
          {loading ? (
            <div className="text-center py-12 text-slate-400">Loading patients...</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead className="bg-slate-800/30">
                  <tr>
                    <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">ID</th>
                    <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Name</th>
                    <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Age/Gender</th>
                    <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Contact</th>
                    <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">H/W Index</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/50">
                  {patients.length > 0 ? (
                    patients.map((p) => (
                      <tr key={p.id} className="hover:bg-slate-800/10">
                        <td className="px-6 py-4 text-xs font-bold text-slate-300">{p.id}</td>
                        <td className="px-6 py-4 text-sm font-semibold text-white">{p.name}</td>
                        <td className="px-6 py-4 text-xs text-slate-300">{p.age} yrs / {p.gender}</td>
                        <td className="px-6 py-4 text-xs text-slate-400">
                          <div>{p.phone || 'No phone'}</div>
                          <div>{p.email || 'No email'}</div>
                        </td>
                        <td className="px-6 py-4 text-xs text-slate-450">
                          {p.height ? `${p.height} cm` : 'N/A'} / {p.weight ? `${p.weight} kg` : 'N/A'}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="5" className="px-6 py-8 text-center text-slate-500 font-medium">No patient profiles registered.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
      ) : (
        <div className="max-w-2xl mx-auto glass-panel p-8 rounded-3xl">
          <div className="border-b border-slate-800 pb-4 mb-6">
            <h4 className="font-bold text-white text-md">Register New Patient Profile</h4>
            <p className="text-xs text-slate-400 mt-1">Fields marked * are mandatory.</p>
          </div>

          {error && <div className="mb-4 p-3 bg-red-950/40 border border-red-900/50 text-red-400 text-xs rounded-xl">{error}</div>}
          {success && <div className="mb-4 p-3 bg-emerald-950/40 border border-emerald-900/50 text-emerald-400 text-xs rounded-xl">{success}</div>}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Patient ID *</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. PAT-001"
                  value={id}
                  onChange={(e) => setId(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
                />
              </div>

              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Full Name *</label>
                <input
                  type="text"
                  required
                  placeholder="Patient name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
                />
              </div>

              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Age *</label>
                <input
                  type="number"
                  required
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
                />
              </div>

              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Gender *</label>
                <select
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
                >
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                </select>
              </div>

              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Phone</label>
                <input
                  type="text"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
                />
              </div>

              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Email</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
                />
              </div>

              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Height (cm)</label>
                <input
                  type="number"
                  value={height}
                  onChange={(e) => setHeight(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
                />
              </div>

              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Weight (kg)</label>
                <input
                  type="number"
                  value={weight}
                  onChange={(e) => setWeight(e.target.value)}
                  className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full py-3.5 bg-primary hover:bg-teal-700 text-white font-bold rounded-xl transition-all cursor-pointer mt-4"
            >
              Register Profile
            </button>
          </form>
        </div>
      )}
    </div>
  );
}

// --------------------- PREDICTION VIEW ---------------------
function PredictionTab({ token, onNavigate }) {
  const [patients, setPatients] = useState([]);
  const [selectedPatientId, setSelectedPatientId] = useState('');
  
  // Clinical Metric States
  const [age, setAge] = useState('');
  const [sex, setSex] = useState('1');
  const [cp, setCp] = useState('4');
  const [trestbps, setTrestbps] = useState('120');
  const [chol, setChol] = useState('200');
  const [fbs, setFbs] = useState('0');
  const [restecg, setRestecg] = useState('0');
  const [thalach, setThalach] = useState('150');
  const [exang, setExang] = useState('0');
  const [oldpeak, setOldpeak] = useState('0.0');
  const [slope, setSlope] = useState('2');
  const [ca, setCa] = useState('0');
  const [thal, setThal] = useState('3');

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/patients/`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setPatients(data);
        }
      } catch (err) {
        console.error(err);
      }
    };
    fetchPatients();
  }, [token]);

  const handlePatientChange = (e) => {
    const pid = e.target.value;
    setSelectedPatientId(pid);
    const p = patients.find(pat => pat.id === pid);
    if (p) {
      setAge(p.age.toString());
      setSex(p.gender === 'Male' ? '1' : '0');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setLoading(true);

    if (!selectedPatientId) {
      setError("Please select a registered patient profile.");
      setLoading(false);
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/api/predictions/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          patient_id: selectedPatientId,
          age: parseInt(age),
          sex: parseInt(sex),
          cp: parseInt(cp),
          trestbps: parseInt(trestbps),
          chol: parseInt(chol),
          fbs: parseInt(fbs),
          restecg: parseInt(restecg),
          thalach: parseInt(thalach),
          exang: parseInt(exang),
          oldpeak: parseFloat(oldpeak),
          slope: parseInt(slope),
          ca: parseInt(ca),
          thal: parseInt(thal)
        })
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Prediction request failed");
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!result) return;
    try {
      const res = await fetch(`${API_BASE}/api/reports/${result.id}/pdf`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!res.ok) throw new Error("Failed to download PDF");
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `HeartCare_Report_${selectedPatientId}_${result.id}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      alert("Error: " + error.message);
    }
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      <div className="glass-panel p-8 rounded-3xl">
        <div className="border-b border-slate-800 pb-4 mb-6">
          <h3 className="text-xl font-bold text-white">Clinical Risk Predictor (Mock)</h3>
          <p className="text-xs text-slate-400 mt-1">Submit clinical values. Mock responses operate in Step 1.</p>
        </div>

        {error && <div className="mb-4 p-3 bg-red-950/40 border border-red-900/50 text-red-400 text-xs rounded-xl">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="max-w-md">
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Select Patient Profile *</label>
            <select
              value={selectedPatientId}
              onChange={handlePatientChange}
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
            >
              <option value="">-- Select Registered Patient --</option>
              {patients.map(p => (
                <option key={p.id} value={p.id}>{p.name} (ID: {p.id})</option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-4 gap-6 pt-4 border-t border-slate-800">
            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Age</label>
              <input
                type="number"
                required
                value={age}
                onChange={(e) => setAge(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
              />
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Sex</label>
              <select
                value={sex}
                onChange={(e) => setSex(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
              >
                <option value="1">Male</option>
                <option value="0">Female</option>
              </select>
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Chest Pain Type</label>
              <select
                value={cp}
                onChange={(e) => setCp(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
              >
                <option value="1">Typical Angina</option>
                <option value="2">Atypical Angina</option>
                <option value="3">Non-anginal Pain</option>
                <option value="4">Asymptomatic</option>
              </select>
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Resting BP (mmHg)</label>
              <input
                type="number"
                required
                value={trestbps}
                onChange={(e) => setTrestbps(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
              />
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Cholesterol (mg/dL)</label>
              <input
                type="number"
                required
                value={chol}
                onChange={(e) => setChol(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
              />
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Fasting Sugar &gt; 120</label>
              <select
                value={fbs}
                onChange={(e) => setFbs(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
              >
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Rest ECG Result</label>
              <select
                value={restecg}
                onChange={(e) => setRestecg(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
              >
                <option value="0">Normal</option>
                <option value="1">ST-T Wave Abnormality</option>
                <option value="2">LV Hypertrophy</option>
              </select>
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Max Heart Rate (bpm)</label>
              <input
                type="number"
                required
                value={thalach}
                onChange={(e) => setThalach(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
              />
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Ex. Induced Angina</label>
              <select
                value={exang}
                onChange={(e) => setExang(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
              >
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">ST Depression (Oldpeak)</label>
              <input
                type="number"
                step="0.1"
                required
                value={oldpeak}
                onChange={(e) => setOldpeak(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
              />
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Slope of ST Segment</label>
              <select
                value={slope}
                onChange={(e) => setSlope(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
              >
                <option value="1">Upsloping</option>
                <option value="2">Flat</option>
                <option value="3">Downsloping</option>
              </select>
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Major Vessels (0-3)</label>
              <select
                value={ca}
                onChange={(e) => setCa(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
              >
                <option value="0">0</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
              </select>
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Thalassemia</label>
              <select
                value={thal}
                onChange={(e) => setThal(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
              >
                <option value="3">Normal</option>
                <option value="6">Fixed Defect</option>
                <option value="7">Reversible Defect</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 bg-primary hover:bg-teal-700 text-white font-bold rounded-2xl shadow-xl active:scale-95 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
          >
            {loading ? 'Processing scan...' : 'Run AI Prediction'}
          </button>
        </form>
      </div>

      {result && (
        <div className="glass-panel p-8 rounded-3xl border-l-8 border-l-primary relative overflow-hidden animate-slideUp">
          <div className="border-b border-slate-800 pb-4 mb-6">
            <h4 className="text-lg font-bold text-white">AI Diagnostics Result</h4>
            <p className="text-xs text-slate-400 mt-0.5">Powered by Random Forest Classifier trained on UCI Cleveland Heart Disease dataset</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 text-center">
            <div className={`p-6 rounded-2xl border-2 ${
              result.prediction === 'HIGH RISK'
                ? 'bg-red-950/30 border-red-800/60'
                : result.prediction === 'MEDIUM RISK'
                ? 'bg-amber-950/30 border-amber-800/60'
                : 'bg-emerald-950/30 border-emerald-800/60'
            }`}>
              <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">AI Assessment Risk</div>
              <div className={`text-2xl font-black ${
                result.prediction === 'HIGH RISK' ? 'text-red-400' : result.prediction === 'MEDIUM RISK' ? 'text-amber-400' : 'text-emerald-400'
              }`}>
                {result.prediction}
              </div>
            </div>

            <div className="p-6 bg-slate-900/50 rounded-2xl border border-slate-800">
              <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">Risk Probability Index</div>
              <div className="text-3xl font-black text-white">{result.risk_percentage}%</div>
            </div>

            <div className="p-6 bg-slate-900/50 rounded-2xl border border-slate-800">
              <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">Model Confidence</div>
              <div className="text-3xl font-black text-primary">{result.confidence}%</div>
            </div>
          </div>

          <div className="flex gap-4">
            <button
              onClick={handleDownloadPDF}
              className="py-3 px-6 bg-primary hover:bg-teal-700 text-white font-bold rounded-xl transition-all shadow-md flex items-center gap-2 cursor-pointer"
            >
              <span className="material-symbols-outlined">download</span>
              Download PDF Report
            </button>
            <button
              onClick={() => onNavigate('patient_history')}
              className="py-3 px-6 bg-slate-800 hover:bg-slate-700 text-white font-bold rounded-xl transition-all border border-slate-700 cursor-pointer"
            >
              View History Log
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

// --------------------- PATIENT HISTORY VIEW ---------------------
function PatientHistoryTab({ token, user }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchHistory = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/predictions/history`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setHistory(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [token]);

  const handleDownloadPDF = async (predId, patientId) => {
    try {
      const res = await fetch(`${API_BASE}/api/reports/${predId}/pdf`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!res.ok) throw new Error("Failed to download PDF");
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `HeartCare_Report_${patientId}_${predId}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      alert("Error: " + error.message);
    }
  };

  if (loading) return <div className="text-center py-12 text-slate-400 font-bold">Loading logs...</div>;

  return (
    <div className="glass-panel rounded-3xl overflow-hidden animate-fadeIn">
      <div className="px-6 py-5 border-b border-slate-800 bg-slate-900/40">
        <h3 className="text-lg font-bold text-white">Diagnostics History Log</h3>
        <p className="text-xs text-slate-400 mt-0.5">Historical records of heart disease predictions.</p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead className="bg-slate-800/30">
            <tr>
              <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">ID</th>
              <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Patient ID</th>
              <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Prediction</th>
              <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Risk Index</th>
              <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Confidence</th>
              <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Date / Time</th>
              <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/50">
            {history.length > 0 ? (
              history.map((pred) => (
                <tr key={pred.id} className="hover:bg-slate-800/20 transition-colors">
                  <td className="px-6 py-4 text-xs font-semibold text-slate-300">#{pred.id}</td>
                  <td className="px-6 py-4 text-sm font-semibold text-white">{pred.patient_id}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2.5 py-0.5 rounded-full text-[9px] font-bold border ${
                      pred.prediction === 'HIGH RISK' ? 'bg-red-950/40 text-red-400 border-red-900/50' : pred.prediction === 'MEDIUM RISK' ? 'bg-amber-950/40 text-amber-400 border-amber-900/50' : 'bg-emerald-950/40 text-emerald-400 border-emerald-900/50'
                    }`}>
                      {pred.prediction}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-xs font-bold text-slate-200">{pred.risk_percentage}%</td>
                  <td className="px-6 py-4 text-xs text-primary font-medium">{pred.confidence}%</td>
                  <td className="px-6 py-4 text-xs text-slate-400">{new Date(pred.date).toLocaleString()}</td>
                  <td className="px-6 py-4">
                    <button
                      onClick={() => handleDownloadPDF(pred.id, pred.patient_id)}
                      className="py-1 px-2.5 bg-slate-800 hover:bg-slate-700 text-primary text-xs font-bold border border-slate-700 rounded-lg cursor-pointer"
                    >
                      Report
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="7" className="px-6 py-8 text-center text-slate-500 font-medium">No history logged.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// --------------------- REPORTS tab VIEW ---------------------
function ReportsTab({ token }) {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/predictions/history`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setPredictions(data);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, [token]);

  const handleDownloadPDF = async (predId, patientId) => {
    try {
      const res = await fetch(`${API_BASE}/api/reports/${predId}/pdf`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!res.ok) throw new Error("Failed to download PDF");
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `HeartCare_Report_${patientId}_${predId}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      alert("Error: " + error.message);
    }
  };

  return (
    <div className="glass-panel p-8 rounded-3xl space-y-6 animate-fadeIn">
      <div className="border-b border-slate-800 pb-4">
        <h3 className="text-xl font-bold text-white">Diagnostic Reports Directory</h3>
        <p className="text-xs text-slate-400 mt-1">Download official PDF medical report records of predictions.</p>
      </div>

      {loading ? (
        <div className="text-center py-12 text-slate-400">Loading reports directory...</div>
      ) : predictions.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {predictions.map(pred => (
            <div key={pred.id} className="p-5 bg-slate-900/50 rounded-2xl border border-slate-800 flex justify-between items-center">
              <div>
                <h5 className="font-bold text-white text-sm">Patient ID: {pred.patient_id}</h5>
                <p className="text-xs text-slate-450 mt-1">Date: {new Date(pred.date).toLocaleDateString()}</p>
                <div className="mt-2 text-xs flex gap-2">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${
                    pred.prediction === 'HIGH RISK' ? 'bg-red-950/40 text-red-400 border-red-900/50' : pred.prediction === 'MEDIUM RISK' ? 'bg-amber-950/40 text-amber-400 border-amber-900/50' : 'bg-emerald-950/40 text-emerald-400 border-emerald-900/50'
                  }`}>{pred.prediction}</span>
                  <span className="text-slate-400">Risk: {pred.risk_percentage}%</span>
                </div>
              </div>
              <button
                onClick={() => handleDownloadPDF(pred.id, pred.patient_id)}
                className="px-4 py-2 bg-primary hover:bg-teal-700 text-white font-bold text-xs rounded-xl flex items-center gap-1.5 cursor-pointer"
              >
                <span className="material-symbols-outlined text-[14px]">download</span> PDF Report
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 text-slate-500 font-medium">No diagnostic reports logged yet.</div>
      )}
    </div>
  );
}

// --------------------- ANALYTICS VIEW ---------------------
function AnalyticsTab({ token }) {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/analytics/charts-data`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setChartData(data);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchChartData();
  }, [token]);

  if (loading) return <div className="text-center py-12 text-slate-400">Loading charts...</div>;
  if (!chartData) return <div className="text-center py-12 text-red-405">Failed to fetch analytics charts.</div>;

  const genderChart = {
    labels: chartData.gender_distribution.labels,
    datasets: [{
      data: chartData.gender_distribution.datasets,
      backgroundColor: ['#3b82f6', '#ec4899'],
      borderColor: '#0f172a',
      borderWidth: 2,
    }]
  };

  const riskChart = {
    labels: chartData.risk_distribution.labels,
    datasets: [{
      data: chartData.risk_distribution.datasets,
      backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
      borderColor: '#0f172a',
      borderWidth: 2,
    }]
  };

  const ageChart = {
    labels: chartData.age_distribution.labels,
    datasets: [{
      label: 'Patient Count',
      data: chartData.age_distribution.datasets,
      backgroundColor: '#0d9488',
      borderRadius: 6,
    }]
  };

  const timelineChart = {
    labels: chartData.monthly_predictions.labels,
    datasets: [{
      label: 'Predictions Run',
      data: chartData.monthly_predictions.datasets,
      borderColor: '#0d9488',
      backgroundColor: 'rgba(13, 148, 136, 0.1)',
      fill: true,
      tension: 0.3,
    }]
  };

  const optionsDark = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { labels: { color: '#94a3b8', font: { family: 'Inter', size: 11 } } }
    },
    scales: {
      y: { grid: { color: '#1e293b' }, ticks: { color: '#94a3b8' } },
      x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
    }
  };

  const optionsPie = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'bottom', labels: { color: '#94a3b8', font: { family: 'Inter', size: 11 } } }
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 animate-fadeIn">
      <div className="glass-panel p-6 rounded-3xl h-80 flex flex-col">
        <h4 className="font-bold text-white mb-4 text-sm uppercase tracking-wider">Patient Risk Class Levels</h4>
        <div className="flex-1 relative">
          <Doughnut data={riskChart} options={optionsPie} />
        </div>
      </div>

      <div className="glass-panel p-6 rounded-3xl h-80 flex flex-col">
        <h4 className="font-bold text-white mb-4 text-sm uppercase tracking-wider">Gender Demographics</h4>
        <div className="flex-1 relative">
          <Pie data={genderChart} options={optionsPie} />
        </div>
      </div>

      <div className="glass-panel p-6 rounded-3xl h-80 flex flex-col">
        <h4 className="font-bold text-white mb-4 text-sm uppercase tracking-wider">Age Group Distribution</h4>
        <div className="flex-1 relative">
          <Bar data={ageChart} options={optionsDark} />
        </div>
      </div>

      <div className="glass-panel p-6 rounded-3xl h-80 flex flex-col">
        <h4 className="font-bold text-white mb-4 text-sm uppercase tracking-wider">Monthly Predictions timeline</h4>
        <div className="flex-1 relative">
          <Line data={timelineChart} options={optionsDark} />
        </div>
      </div>
    </div>
  );
}

// --------------------- SETTINGS tab VIEW ---------------------
function SettingsTab({ token, user }) {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);

  // New Doctor Account Form
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const fetchDoctors = async () => {
    if (user.role !== 'admin') {
      setLoading(false);
      return;
    }
    try {
      const res = await fetch(`${API_BASE}/api/auth/doctors`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setDoctors(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDoctors();
  }, [token, user]);

  const handleAddDoctor = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const res = await fetch(`${API_BASE}/api/auth/doctors`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          username: username.trim(), // API parameter maps email to username internally
          email: username.trim(),
          password,
          role: 'doctor',
          name: name.trim()
        })
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Failed to create doctor account");
      }

      setSuccess(`Doctor account "${name}" created successfully.`);
      setUsername('');
      setPassword('');
      setName('');
      fetchDoctors();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteDoctor = async (id) => {
    if (!window.confirm("Are you sure?")) return;
    setError('');
    setSuccess('');

    try {
      const res = await fetch(`${API_BASE}/api/auth/doctors/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!res.ok) throw new Error("Delete failed");
      setSuccess("Physician profile removed.");
      fetchDoctors();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Profile Overview */}
      <div className="glass-panel p-6 rounded-3xl">
        <h4 className="font-bold text-white mb-4 text-sm uppercase tracking-wider border-b border-slate-800 pb-2">Profile Information</h4>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-slate-400 font-bold">User Name:</span> <span className="text-white font-semibold">{user.name}</span>
          </div>
          <div>
            <span className="text-slate-400 font-bold">Role:</span> <span className="text-primary font-bold uppercase">{user.role}</span>
          </div>
          <div>
            <span className="text-slate-400 font-bold">Email / ID:</span> <span className="text-white">{user.email}</span>
          </div>
        </div>
      </div>

      {user.role === 'admin' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Add Doctor Form */}
          <div className="glass-panel p-6 rounded-3xl h-fit">
            <h4 className="font-bold text-white mb-4 text-sm uppercase tracking-wider border-b border-slate-800 pb-2">Add Physician</h4>
            {error && <div className="mb-4 p-2 bg-red-950/40 border border-red-900/50 text-red-400 text-xs rounded-xl">{error}</div>}
            {success && <div className="mb-4 p-2 bg-emerald-950/40 border border-emerald-900/50 text-emerald-400 text-xs rounded-xl">{success}</div>}

            <form onSubmit={handleAddDoctor} className="space-y-4">
              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Doctor Email *</label>
                <input
                  type="email"
                  required
                  placeholder="e.g. sarah@heartcare.ai"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-xs"
                />
              </div>

              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Password *</label>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-xs"
                />
              </div>

              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Name *</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Dr. Sarah Connor"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-xs"
                />
              </div>

              <button
                type="submit"
                className="w-full py-2 bg-primary hover:bg-teal-700 text-white font-bold rounded-xl transition-all cursor-pointer"
              >
                Create Account
              </button>
            </form>
          </div>

          {/* List Doctors */}
          <div className="lg:col-span-2 glass-panel rounded-3xl overflow-hidden h-fit">
            <div className="px-6 py-4 border-b border-slate-800 bg-slate-900/40">
              <h4 className="font-bold text-white text-sm uppercase tracking-wider">Registered Physicians</h4>
            </div>

            <div className="overflow-y-auto max-h-96">
              <table className="w-full text-left border-collapse">
                <thead className="bg-slate-800/30">
                  <tr>
                    <th className="px-6 py-3 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Name</th>
                    <th className="px-6 py-3 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Email</th>
                    <th className="px-6 py-3 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/50 text-xs">
                  {loading ? (
                    <tr>
                      <td colSpan="3" className="px-6 py-4 text-slate-400 font-bold">Loading...</td>
                    </tr>
                  ) : doctors.length > 0 ? (
                    doctors.map((doc) => (
                      <tr key={doc.id} className="hover:bg-slate-800/10">
                        <td className="px-6 py-3 font-semibold text-white">{doc.name}</td>
                        <td className="px-6 py-3 text-slate-400">{doc.email}</td>
                        <td className="px-6 py-3">
                          <button
                            onClick={() => handleDeleteDoctor(doc.id)}
                            className="text-red-400 hover:text-red-300 font-bold cursor-pointer"
                          >
                            Remove
                          </button>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="3" className="px-6 py-4 text-center text-slate-500">No physicians registered.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
