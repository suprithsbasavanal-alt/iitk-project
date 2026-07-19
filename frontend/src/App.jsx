import React, { useState, useEffect, useRef } from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, RadialLinearScale, ArcElement, Title as ChartTitle, Tooltip, Legend } from 'chart.js';
import { Line, Bar, Pie, Doughnut } from 'react-chartjs-2';

// Register Chart.js elements
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, RadialLinearScale, ArcElement, ChartTitle, Tooltip, Legend);

const API_BASE = "http://localhost:8000";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('hc_token') || '');
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('hc_user') || 'null'));
  const [activeTab, setActiveTab] = useState('dashboard');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Sync token and user to localStorage
  const handleLogin = (newToken, newUser) => {
    setToken(newToken);
    setUser(newUser);
    localStorage.setItem('hc_token', newToken);
    localStorage.setItem('hc_user', JSON.stringify(newUser));
    // If logged in as patient, default to the patient_history view
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
    <div className="min-h-screen bg-background text-slate-200 font-body antialiased flex">
      {/* Sidebar Navigation - Desktop */}
      <aside className="fixed left-0 top-0 h-full w-64 bg-surface flex flex-col py-6 border-r border-slate-800 shadow-xl z-50 hidden md:flex">
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
              onClick={() => setActiveTab('register_patient')}
              className={`w-full text-left px-4 py-3 flex items-center gap-3 transition-all rounded-lg active:scale-95 ${
                activeTab === 'register_patient'
                  ? 'bg-primary/20 text-primary border-l-4 border-primary font-bold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`}
            >
              <span className="material-symbols-outlined">person_add</span>
              <span>Register Patient</span>
            </button>
          )}

          {user.role !== 'patient' && (
            <button
              onClick={() => setActiveTab('new_prediction')}
              className={`w-full text-left px-4 py-3 flex items-center gap-3 transition-all rounded-lg active:scale-95 ${
                activeTab === 'new_prediction'
                  ? 'bg-primary/20 text-primary border-l-4 border-primary font-bold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`}
            >
              <span className="material-symbols-outlined">clinical_notes</span>
              <span>New Prediction</span>
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
            <span>{user.role === 'patient' ? 'My Diagnostics' : 'Patient History'}</span>
          </button>

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

          {user.role === 'admin' && (
            <button
              onClick={() => setActiveTab('admin_panel')}
              className={`w-full text-left px-4 py-3 flex items-center gap-3 transition-all rounded-lg active:scale-95 ${
                activeTab === 'admin_panel'
                  ? 'bg-primary/20 text-primary border-l-4 border-primary font-bold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`}
            >
              <span className="material-symbols-outlined">admin_panel_settings</span>
              <span>Admin Panel</span>
            </button>
          )}
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
      <div className="flex-1 md:ml-64 min-h-screen flex flex-col">
        {/* Top AppBar Header */}
        <header className="bg-surface/80 backdrop-blur-md border-b border-slate-800 sticky top-0 z-40 flex justify-between items-center px-6 md:px-8 h-20">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setMobileMenuOpen(true)}
              className="md:hidden p-2 hover:bg-slate-800/40 rounded-full text-primary"
            >
              <span className="material-symbols-outlined">menu</span>
            </button>
            <h1 className="font-headline font-black text-primary text-xl md:text-2xl tracking-tight">
              HeartCare Clinical AI
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <div className="hidden sm:flex flex-col items-end mr-2">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-tighter">Diagnostic Station</span>
              <span className="text-sm font-medium text-white">Central-04A</span>
            </div>
            <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-primary border border-primary/20">
              <span className="material-symbols-outlined">notifications</span>
            </div>
          </div>
        </header>

        {/* Dynamic Page Views */}
        <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto">
          {activeTab === 'dashboard' && user.role !== 'patient' && (
            <DashboardTab token={token} onNavigate={setActiveTab} />
          )}
          {activeTab === 'register_patient' && user.role !== 'patient' && (
            <RegisterPatientTab token={token} />
          )}
          {activeTab === 'new_prediction' && user.role !== 'patient' && (
            <NewPredictionTab token={token} onNavigate={setActiveTab} />
          )}
          {activeTab === 'patient_history' && (
            <PatientHistoryTab token={token} user={user} />
          )}
          {activeTab === 'analytics' && user.role !== 'patient' && (
            <AnalyticsTab token={token} />
          )}
          {activeTab === 'admin_panel' && user.role === 'admin' && (
            <AdminPanelTab token={token} />
          )}
        </main>
      </div>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-50 flex md:hidden">
          {/* Overlay backdrop */}
          <div 
            onClick={() => setMobileMenuOpen(false)}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm transition-opacity duration-300"
          ></div>
          
          {/* Menu Drawer */}
          <div className="relative w-64 max-w-xs bg-surface h-full flex flex-col py-6 px-4 shadow-2xl border-r border-slate-800">
            <div className="flex justify-between items-center mb-8 px-2">
              <span className="font-headline font-bold text-primary text-xl">HeartCare AI</span>
              <button 
                onClick={() => setMobileMenuOpen(false)}
                className="text-slate-400 hover:text-slate-200"
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
                  onClick={() => { setActiveTab('register_patient'); setMobileMenuOpen(false); }}
                  className={`w-full text-left px-4 py-3 flex items-center gap-3 rounded-lg ${
                    activeTab === 'register_patient' ? 'bg-primary/20 text-primary font-bold' : 'text-slate-400'
                  }`}
                >
                  <span className="material-symbols-outlined">person_add</span>
                  <span>Register Patient</span>
                </button>
              )}

              {user.role !== 'patient' && (
                <button
                  onClick={() => { setActiveTab('new_prediction'); setMobileMenuOpen(false); }}
                  className={`w-full text-left px-4 py-3 flex items-center gap-3 rounded-lg ${
                    activeTab === 'new_prediction' ? 'bg-primary/20 text-primary font-bold' : 'text-slate-400'
                  }`}
                >
                  <span className="material-symbols-outlined">clinical_notes</span>
                  <span>New Prediction</span>
                </button>
              )}

              <button
                onClick={() => { setActiveTab('patient_history'); setMobileMenuOpen(false); }}
                className={`w-full text-left px-4 py-3 flex items-center gap-3 rounded-lg ${
                  activeTab === 'patient_history' ? 'bg-primary/20 text-primary font-bold' : 'text-slate-400'
                }`}
              >
                <span className="material-symbols-outlined">history</span>
                <span>{user.role === 'patient' ? 'My Diagnostics' : 'Patient History'}</span>
              </button>

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

              {user.role === 'admin' && (
                <button
                  onClick={() => { setActiveTab('admin_panel'); setMobileMenuOpen(false); }}
                  className={`w-full text-left px-4 py-3 flex items-center gap-3 rounded-lg ${
                    activeTab === 'admin_panel' ? 'bg-primary/20 text-primary font-bold' : 'text-slate-400'
                  }`}
                >
                  <span className="material-symbols-outlined">admin_panel_settings</span>
                  <span>Admin Panel</span>
                </button>
              )}
            </nav>

            <div className="mt-auto px-2">
              <button
                onClick={handleLogout}
                className="w-full px-4 py-2 bg-red-950/40 text-red-400 hover:bg-red-900/30 border border-red-900/50 rounded-xl flex items-center justify-center gap-2"
              >
                <span className="material-symbols-outlined text-sm">logout</span>
                <span className="text-sm font-semibold">Sign Out</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// --------------------- LOGIN VIEW ---------------------
function LoginView({ onLogin }) {
  const [role, setRole] = useState('doctor'); // 'admin', 'doctor', 'patient'
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const details = new URLSearchParams();
      details.append('username', username);
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
      
      // Enforce selected role matches token role
      if (data.role !== role) {
        throw new Error(`Account role is '${data.role}', but you selected '${role}' login.`);
      }

      onLogin(data.access_token, {
        id: data.id,
        role: data.role,
        name: data.name,
        username: data.username
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
        {/* Glow effect */}
        <div className="absolute -top-12 -left-12 w-32 h-32 bg-primary/20 rounded-full blur-2xl"></div>
        <div className="absolute -bottom-12 -right-12 w-32 h-32 bg-secondary/15 rounded-full blur-2xl"></div>

        <div className="flex flex-col items-center mb-8 relative">
          <div className="w-12 h-12 rounded-full bg-primary/10 border border-primary/30 flex items-center justify-center mb-3">
            <span className="material-symbols-outlined text-primary text-3xl font-bold">medical_services</span>
          </div>
          <h2 className="text-2xl font-black text-white tracking-tight">HeartCare AI Portal</h2>
          <p className="text-xs text-slate-400 mt-1">Heart Disease Prediction and Clinical Management</p>
        </div>

        {/* Role Selector Tabs */}
        <div className="grid grid-cols-3 bg-slate-950 p-1.5 rounded-2xl mb-6 border border-slate-900">
          <button
            type="button"
            onClick={() => { setRole('doctor'); setUsername(''); setPassword(''); }}
            className={`py-2 rounded-xl text-xs font-bold transition-all ${
              role === 'doctor' ? 'bg-primary text-white shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Doctor
          </button>
          <button
            type="button"
            onClick={() => { setRole('admin'); setUsername(''); setPassword(''); }}
            className={`py-2 rounded-xl text-xs font-bold transition-all ${
              role === 'admin' ? 'bg-primary text-white shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Admin
          </button>
          <button
            type="button"
            onClick={() => { setRole('patient'); setUsername(''); setPassword(''); }}
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

        <form onSubmit={handleSubmit} className="space-y-4 relative">
          <div>
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">
              {role === 'patient' ? 'Patient ID' : 'Username'}
            </label>
            <input
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder={role === 'patient' ? 'e.g. PAT-001' : 'Enter username'}
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
            {!loading && <span className="material-symbols-outlined text-sm">login</span>}
          </button>
        </form>

        <div className="mt-8 text-center text-[10px] text-slate-500">
          {role === 'admin' && 'System Seed Accounts: admin / admin123'}
          {role === 'doctor' && 'System Seed Accounts: doctor / doctor123'}
          {role === 'patient' && 'Use registered Patient ID as both username & password'}
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
      if (!res.ok) throw new Error("Failed to download PDF report");
      
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `HeartCare_Report_${patientId}_${predId}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      alert("Error generating PDF: " + error.message);
    }
  };

  if (loading) return <div className="text-center py-12 text-slate-400 font-bold">Loading dashboard telemetry...</div>;

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Welcome Banner */}
      <div className="relative w-full h-48 rounded-3xl overflow-hidden group bg-gradient-to-r from-teal-950/40 via-surface to-background border border-slate-800 flex flex-col justify-center px-8">
        <div className="absolute inset-0 bg-gradient-to-r from-primary/10 via-transparent to-transparent pointer-events-none"></div>
        <h2 className="text-2xl md:text-3xl font-black text-white mb-2 leading-tight">
          Cardiovascular Diagnostics <br/><span className="text-primary">Overview</span>
        </h2>
        <p className="text-slate-400 max-w-md text-xs md:text-sm">
          Real-time diagnostics tracking powered by Random Forest heart disease prediction engine.
        </p>
      </div>

      {/* Metrics Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {/* Total Patients */}
        <div className="glass-panel p-5 rounded-2xl metric-card-glow border-l-4 border-l-secondary">
          <div className="flex justify-between items-start mb-4">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Total Patients</span>
            <span className="material-symbols-outlined text-secondary opacity-60">group</span>
          </div>
          <div className="text-3xl font-black text-white">{stats?.total_patients || 0}</div>
          <div className="mt-2 text-[10px] text-slate-500 font-medium">Registered profiles</div>
        </div>

        {/* Predictions Made */}
        <div className="glass-panel p-5 rounded-2xl metric-card-glow border-l-4 border-l-primary">
          <div className="flex justify-between items-start mb-4">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Predictions Made</span>
            <span className="material-symbols-outlined text-primary opacity-60">neurology</span>
          </div>
          <div className="text-3xl font-black text-white">{stats?.predictions_made || 0}</div>
          <div className="mt-2 text-[10px] text-slate-500 font-medium">Executed scans</div>
        </div>

        {/* High Risk Patients */}
        <div className="glass-panel p-5 rounded-2xl metric-card-glow border-l-4 border-l-error">
          <div className="flex justify-between items-start mb-4">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest font-bold">High Risk</span>
            <span className="material-symbols-outlined text-error opacity-60">emergency</span>
          </div>
          <div className="text-3xl font-black text-error">{stats?.high_risk_patients || 0}</div>
          <div className="mt-2 text-[10px] text-error/60 font-medium">Urgent consultation</div>
        </div>

        {/* Low Risk Patients */}
        <div className="glass-panel p-5 rounded-2xl metric-card-glow border-l-4 border-l-accent">
          <div className="flex justify-between items-start mb-4">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest font-bold">Low Risk</span>
            <span className="material-symbols-outlined text-accent opacity-60">verified_user</span>
          </div>
          <div className="text-3xl font-black text-accent">{stats?.low_risk_patients || 0}</div>
          <div className="mt-2 text-[10px] text-accent/60 font-medium">Routine monitoring</div>
        </div>

        {/* Accuracy */}
        <div className="glass-panel p-5 rounded-2xl metric-card-glow border-l-4 border-l-warning">
          <div className="flex justify-between items-start mb-4">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Model Accuracy</span>
            <span className="material-symbols-outlined text-warning opacity-60">target</span>
          </div>
          <div className="text-3xl font-black text-white">{stats?.prediction_accuracy || 0}%</div>
          <div className="mt-2 text-[10px] text-slate-500 font-medium">Baseline test score</div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Predictions Table */}
        <section className="lg:col-span-2">
          <div className="glass-panel rounded-3xl overflow-hidden">
            <div className="px-6 py-5 border-b border-slate-800 flex justify-between items-center bg-slate-900/40">
              <div>
                <h3 className="text-lg font-bold text-white">Recent Diagnostics</h3>
                <p className="text-xs text-slate-400">Cardiovascular Risk Scan Logs</p>
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
                    <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Risk Level</th>
                    <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Risk Index</th>
                    <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Date</th>
                    <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/50">
                  {stats?.recent_predictions && stats.recent_predictions.length > 0 ? (
                    stats.recent_predictions.map((pred) => (
                      <tr key={pred.id} className="hover:bg-slate-800/20 transition-colors">
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-xs font-bold text-slate-300">
                              {pred.patient_name.split(' ').map(n=>n[0]).join('')}
                            </div>
                            <div className="flex flex-col">
                              <span className="text-sm font-semibold text-white">{pred.patient_name}</span>
                              <span className="text-[10px] text-slate-500 font-medium">ID: {pred.patient_id}</span>
                            </div>
                          </div>
                        </td>
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
                        <td className="px-6 py-4 text-xs font-semibold text-slate-200">
                          {pred.risk_percentage}%
                        </td>
                        <td className="px-6 py-4 text-xs text-slate-400">
                          {new Date(pred.date).toLocaleDateString()}
                        </td>
                        <td className="px-6 py-4">
                          <button
                            onClick={() => handleDownloadPDF(pred.id, pred.patient_id)}
                            className="p-1.5 hover:bg-slate-800 rounded-lg text-primary hover:text-teal-400 transition-all cursor-pointer flex items-center"
                            title="Download PDF Report"
                          >
                            <span className="material-symbols-outlined text-lg">download</span>
                          </button>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="5" className="px-6 py-8 text-center text-slate-500 font-medium">
                        No prediction runs logged yet.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </section>

        {/* Quick Actions / Alerts */}
        <aside className="space-y-6">
          <div 
            onClick={() => onNavigate('new_prediction')}
            className="relative rounded-3xl overflow-hidden p-6 border border-teal-800 bg-gradient-to-br from-teal-950/80 to-slate-950 group cursor-pointer hover:border-teal-500 transition-all"
          >
            <div className="absolute inset-0 bg-primary/5 group-hover:bg-primary/10 transition-colors"></div>
            <span className="material-symbols-outlined text-primary text-3xl mb-2">add_circle</span>
            <h4 className="text-lg font-bold text-white">New Diagnosis</h4>
            <p className="text-slate-400 text-xs mt-1">Start a new AI-assisted heart disease prediction scan for a registered patient.</p>
          </div>

          <div className="glass-panel p-6 rounded-3xl space-y-4">
            <h4 className="font-bold text-white flex items-center gap-2 border-b border-slate-800 pb-3">
              <span className="material-symbols-outlined text-warning">clinical_notes</span>
              Clinical Guidelines
            </h4>
            <ul className="space-y-3 text-xs text-slate-400">
              <li className="flex gap-2">
                <span className="text-primary font-bold">1.</span>
                <span>Register the patient details first before running the AI assessment.</span>
              </li>
              <li className="flex gap-2">
                <span className="text-primary font-bold">2.</span>
                <span>Values such as Cholesterol and Blood Pressure must be from recent clinical lab results.</span>
              </li>
              <li className="flex gap-2">
                <span className="text-primary font-bold">3.</span>
                <span>PDF reports will include the logged physician's verified signature block.</span>
              </li>
            </ul>
          </div>
        </aside>
      </div>
    </div>
  );
}

// --------------------- REGISTER PATIENT VIEW ---------------------
function RegisterPatientTab({ token }) {
  const [patientId, setPatientId] = useState('');
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('Male');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [height, setHeight] = useState('');
  const [weight, setWeight] = useState('');
  
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/api/patients/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          patient_id: patientId.trim(),
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

      setSuccess(`Patient "${name}" registered successfully!`);
      // Reset form
      setPatientId('');
      setName('');
      setAge('');
      setPhone('');
      setEmail('');
      setHeight('');
      setWeight('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto glass-panel p-8 rounded-3xl animate-fadeIn">
      <div className="border-b border-slate-800 pb-4 mb-6">
        <h3 className="text-xl font-bold text-white">Patient Profile Registration</h3>
        <p className="text-xs text-slate-400 mt-1">Create a clinical health chart record for diagnostics tracking.</p>
      </div>

      {error && <div className="mb-4 p-3 bg-red-950/40 border border-red-900/50 text-red-400 text-xs rounded-xl">{error}</div>}
      {success && <div className="mb-4 p-3 bg-emerald-950/40 border border-emerald-900/50 text-emerald-400 text-xs rounded-xl">{success}</div>}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Patient ID *</label>
            <input
              type="text"
              required
              placeholder="e.g. PAT-983"
              value={patientId}
              onChange={(e) => setPatientId(e.target.value)}
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
            />
          </div>

          <div>
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Full Name *</label>
            <input
              type="text"
              required
              placeholder="e.g. Alice Mercer"
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
              placeholder="Age in years"
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
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Phone Number</label>
            <input
              type="text"
              placeholder="555-0100"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
            />
          </div>

          <div>
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Email Address</label>
            <input
              type="email"
              placeholder="alice@mail.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
            />
          </div>

          <div>
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Height (cm)</label>
            <input
              type="number"
              placeholder="Height in cm"
              value={height}
              onChange={(e) => setHeight(e.target.value)}
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
            />
          </div>

          <div>
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Weight (kg)</label>
            <input
              type="number"
              placeholder="Weight in kg"
              value={weight}
              onChange={(e) => setWeight(e.target.value)}
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3.5 bg-primary hover:bg-teal-700 text-white font-bold rounded-xl transition-all shadow-lg active:scale-95 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 mt-4"
        >
          {loading ? 'Creating Profile...' : 'Register Profile'}
          {!loading && <span className="material-symbols-outlined text-sm">person_add</span>}
        </button>
      </form>
    </div>
  );
}

// --------------------- HEALTH DATA FORM & PREDICTION tab ---------------------
function NewPredictionTab({ token, onNavigate }) {
  const [patients, setPatients] = useState([]);
  const [selectedPatientId, setSelectedPatientId] = useState('');
  
  // Health Form States
  const [age, setAge] = useState('');
  const [sex, setSex] = useState('1'); // 1 = Male, 0 = Female
  const [cp, setCp] = useState('4');   // Chest Pain Type (1, 2, 3, 4)
  const [trestbps, setTrestbps] = useState('120'); // Resting BP
  const [chol, setChol] = useState('200');         // Cholesterol
  const [fbs, setFbs] = useState('0');             // Fasting Blood Sugar
  const [restecg, setRestecg] = useState('0');     // Rest ECG
  const [thalach, setThalach] = useState('150');     // Max Heart Rate
  const [exang, setExang] = useState('0');         // Exercise Angina
  const [oldpeak, setOldpeak] = useState('0.0');     // ST Depression
  const [slope, setSlope] = useState('2');         // Slope
  const [ca, setCa] = useState('0');               // Vessels
  const [thal, setThal] = useState('3');           // Thalassemia
  const [recommendation, setRecommendation] = useState('');

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
        console.error("Failed to load patients list", err);
      }
    };
    fetchPatients();
  }, [token]);

  // Autofill age and gender when patient changes
  const handlePatientChange = (e) => {
    const pid = e.target.value;
    setSelectedPatientId(pid);
    const p = patients.find(pat => pat.patient_id === pid);
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
      setError("Please select a registered patient.");
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
          thal: parseInt(thal),
          doctor_recommendation: recommendation.trim() || null
        })
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "AI engine prediction fail");
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
      if (!res.ok) throw new Error("Failed to generate PDF");
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
          <h3 className="text-xl font-bold text-white">AI Heart Disease Prediction Scan</h3>
          <p className="text-xs text-slate-400 mt-1">Submit clinical diagnostics features to run neural classifier prediction.</p>
        </div>

        {error && <div className="mb-4 p-3 bg-red-950/40 border border-red-900/50 text-red-400 text-xs rounded-xl">{error}</div>}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Patient Selection */}
          <div className="max-w-md">
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Select Registered Patient *</label>
            <select
              value={selectedPatientId}
              onChange={handlePatientChange}
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
            >
              <option value="">-- Choose Patient Profile --</option>
              {patients.map(p => (
                <option key={p.patient_id} value={p.patient_id}>
                  {p.name} (ID: {p.patient_id}, Age: {p.age})
                </option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-4 gap-6 pt-4 border-t border-slate-800">
            {/* Age */}
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

            {/* Sex */}
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

            {/* Chest Pain Type */}
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

            {/* Resting BP */}
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

            {/* Cholesterol */}
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

            {/* Fasting Blood Sugar */}
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

            {/* Rest ECG */}
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

            {/* Max Heart Rate */}
            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Max Heart Rate achieved</label>
              <input
                type="number"
                required
                value={thalach}
                onChange={(e) => setThalach(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
              />
            </div>

            {/* Exercise Angina */}
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

            {/* Oldpeak ST Depression */}
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

            {/* Slope */}
            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">ST Slope Segment</label>
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

            {/* ca Vessels */}
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

            {/* Thalassemia */}
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

          <div className="pt-4 border-t border-slate-800">
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Physician Recommendation Override (Optional)</label>
            <textarea
              placeholder="Provide custom cardiologist recommendations here, or leave blank to auto-generate default instructions based on risk status."
              value={recommendation}
              onChange={(e) => setRecommendation(e.target.value)}
              rows="3"
              className="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-sm"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-4 bg-primary hover:bg-teal-700 text-white font-bold rounded-2xl shadow-xl active:scale-95 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
          >
            {loading ? 'Evaluating Health Data...' : 'Run AI Prediction'}
            {!loading && <span className="material-symbols-outlined text-sm">neurology</span>}
          </button>
        </form>
      </div>

      {/* Results Panel */}
      {result && (
        <div className="glass-panel p-8 rounded-3xl border-l-8 border-l-primary relative overflow-hidden animate-slideUp">
          <div className="absolute -top-12 -right-12 w-48 h-48 bg-primary/10 rounded-full blur-3xl"></div>
          
          <div className="border-b border-slate-800 pb-4 mb-6">
            <h4 className="text-lg font-bold text-white">AI Prediction Diagnostics Outcome</h4>
            <p className="text-xs text-slate-400 mt-1">Generated by neural network classifier on medical records.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 text-center">
            {/* Risk Status */}
            <div className="p-6 bg-slate-900/50 rounded-2xl border border-slate-800">
              <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">Heart Disease Risk</div>
              <div className={`text-2xl font-black ${
                result.prediction_status === 'HIGH RISK'
                  ? 'text-red-400 drop-shadow-[0_0_8px_rgba(239,68,68,0.3)]'
                  : result.prediction_status === 'MEDIUM RISK'
                  ? 'text-amber-400 drop-shadow-[0_0_8px_rgba(245,158,11,0.3)]'
                  : 'text-emerald-400 drop-shadow-[0_0_8px_rgba(16,185,129,0.3)]'
              }`}>
                {result.prediction_status}
              </div>
            </div>

            {/* Risk Index */}
            <div className="p-6 bg-slate-900/50 rounded-2xl border border-slate-800">
              <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">Risk Percentage</div>
              <div className="text-3xl font-black text-white">{result.risk_percentage}%</div>
            </div>

            {/* Confidence */}
            <div className="p-6 bg-slate-900/50 rounded-2xl border border-slate-800">
              <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">Prediction Confidence</div>
              <div className="text-3xl font-black text-primary">{result.prediction_confidence}%</div>
            </div>
          </div>

          {/* Recommendations */}
          <div className="p-6 bg-slate-900/40 border border-slate-800 rounded-2xl space-y-3 mb-6">
            <h5 className="font-bold text-white flex items-center gap-2 text-sm border-b border-slate-850 pb-2">
              <span className="material-symbols-outlined text-primary text-base">verified</span>
              Clinical Recommendations
            </h5>
            <div className="text-xs leading-relaxed text-slate-300 whitespace-pre-line">
              {result.doctor_recommendation}
            </div>
          </div>

          <div className="flex gap-4">
            <button
              onClick={handleDownloadPDF}
              className="py-3 px-6 bg-primary hover:bg-teal-700 text-white font-bold rounded-xl transition-all shadow-md flex items-center gap-2 cursor-pointer active:scale-95"
            >
              <span className="material-symbols-outlined">download</span>
              Download PDF Report
            </button>
            <button
              onClick={() => onNavigate('patient_history')}
              className="py-3 px-6 bg-slate-800 hover:bg-slate-700 text-white font-bold rounded-xl transition-all border border-slate-700 cursor-pointer active:scale-95"
            >
              View in Log History
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
      if (!res.ok) throw new Error("Failed to download PDF report");
      
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `HeartCare_Report_${patientId}_${predId}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      alert("Error generating PDF: " + error.message);
    }
  };

  if (loading) return <div className="text-center py-12 text-slate-400 font-bold">Loading diagnostic logs...</div>;

  return (
    <div className="glass-panel rounded-3xl overflow-hidden animate-fadeIn">
      <div className="px-6 py-5 border-b border-slate-800 bg-slate-900/40">
        <h3 className="text-lg font-bold text-white">
          {user.role === 'patient' ? 'My Cardiovascular Diagnostic Logs' : 'All Patient Diagnostics History'}
        </h3>
        <p className="text-xs text-slate-400 mt-0.5">Historical log records of predictions made on patients.</p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead className="bg-slate-800/30">
            <tr>
              <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">ID</th>
              <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Patient ID</th>
              <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Risk Level</th>
              <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Risk Index</th>
              <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Confidence</th>
              <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Date / Time</th>
              <th className="px-6 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Report</th>
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
                      pred.prediction_status === 'HIGH RISK'
                        ? 'bg-red-950/40 text-red-400 border-red-900/50'
                        : pred.prediction_status === 'MEDIUM RISK'
                        ? 'bg-amber-950/40 text-amber-400 border-amber-900/50'
                        : 'bg-emerald-950/40 text-emerald-400 border-emerald-900/50'
                    }`}>
                      {pred.prediction_status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-xs font-bold text-slate-200">{pred.risk_percentage}%</td>
                  <td className="px-6 py-4 text-xs text-primary font-medium">{pred.prediction_confidence}%</td>
                  <td className="px-6 py-4 text-xs text-slate-400">{new Date(pred.date).toLocaleString()}</td>
                  <td className="px-6 py-4">
                    <button
                      onClick={() => handleDownloadPDF(pred.id, pred.patient_id)}
                      className="py-1.5 px-3 bg-slate-800 hover:bg-slate-700 text-primary text-xs font-bold border border-slate-700 rounded-lg transition-all flex items-center gap-1.5 cursor-pointer active:scale-95"
                    >
                      <span className="material-symbols-outlined text-[14px]">download</span>
                      PDF
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="7" className="px-6 py-8 text-center text-slate-500 font-medium">
                  No prediction log history found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
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

  if (loading) return <div className="text-center py-12 text-slate-400 font-bold">Loading analytical charts...</div>;
  if (!chartData) return <div className="text-center py-12 text-red-400 font-bold">Failed to load analytics charts.</div>;

  // Chart configs
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
      legend: {
        labels: { color: '#94a3b8', font: { family: 'Inter', size: 11 } }
      }
    },
    scales: {
      y: {
        grid: { color: '#1e293b' },
        ticks: { color: '#94a3b8' }
      },
      x: {
        grid: { display: false },
        ticks: { color: '#94a3b8' }
      }
    }
  };

  const optionsPie = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: { color: '#94a3b8', font: { family: 'Inter', size: 11 } }
      }
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8 animate-fadeIn">
      {/* Risk Level Distribution */}
      <div className="glass-panel p-6 rounded-3xl h-80 flex flex-col">
        <h4 className="font-bold text-white mb-4 text-sm uppercase tracking-wider">Patient Risk Class Levels</h4>
        <div className="flex-1 relative">
          <Doughnut data={riskChart} options={optionsPie} />
        </div>
      </div>

      {/* Male vs Female */}
      <div className="glass-panel p-6 rounded-3xl h-80 flex flex-col">
        <h4 className="font-bold text-white mb-4 text-sm uppercase tracking-wider">Gender Demographics</h4>
        <div className="flex-1 relative">
          <Pie data={genderChart} options={optionsPie} />
        </div>
      </div>

      {/* Age Distribution */}
      <div className="glass-panel p-6 rounded-3xl h-80 flex flex-col">
        <h4 className="font-bold text-white mb-4 text-sm uppercase tracking-wider">Age Group Distribution</h4>
        <div className="flex-1 relative">
          <Bar data={ageChart} options={optionsDark} />
        </div>
      </div>

      {/* Predictions Monthly Timeline */}
      <div className="glass-panel p-6 rounded-3xl h-80 flex flex-col">
        <h4 className="font-bold text-white mb-4 text-sm uppercase tracking-wider">Monthly Predictions Run Activity</h4>
        <div className="flex-1 relative">
          <Line data={timelineChart} options={optionsDark} />
        </div>
      </div>
    </div>
  );
}

// --------------------- ADMIN PANEL VIEW ---------------------
function AdminPanelTab({ token }) {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);

  // New Doctor Form States
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const fetchDoctors = async () => {
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
  }, [token]);

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
          username: username.trim(),
          password,
          role: 'doctor',
          name: name.trim(),
          phone: phone.trim() || null,
          email: email.trim() || null
        })
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Failed to add doctor");
      }

      setSuccess(`Doctor "${name}" created successfully.`);
      setUsername('');
      setPassword('');
      setName('');
      setPhone('');
      setEmail('');
      fetchDoctors();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteDoctor = async (id) => {
    if (!window.confirm("Are you sure you want to delete this doctor?")) return;
    setError('');
    setSuccess('');

    try {
      const res = await fetch(`${API_BASE}/api/auth/doctors/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!res.ok) {
        throw new Error("Failed to delete doctor account");
      }

      setSuccess("Doctor deleted successfully.");
      fetchDoctors();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleExportData = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/predictions/history`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!res.ok) throw new Error("Failed to fetch history data for export");
      const data = await res.json();
      
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `HeartCare_Diagnostics_Export_${new Date().toISOString().slice(0,10)}.json`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      alert("Export fail: " + err.message);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 animate-fadeIn">
      {/* Create Doctor Form */}
      <div className="glass-panel p-6 rounded-3xl h-fit">
        <h4 className="font-bold text-white mb-4 text-sm uppercase tracking-wider border-b border-slate-800 pb-2">Add New Physician</h4>
        {error && <div className="mb-4 p-2 bg-red-950/40 border border-red-900/50 text-red-400 text-xs rounded-xl">{error}</div>}
        {success && <div className="mb-4 p-2 bg-emerald-950/40 border border-emerald-900/50 text-emerald-400 text-xs rounded-xl">{success}</div>}

        <form onSubmit={handleAddDoctor} className="space-y-4">
          <div>
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Username *</label>
            <input
              type="text"
              required
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
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Doctor Name *</label>
            <input
              type="text"
              required
              placeholder="e.g. Dr. Sarah Connor"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-xs"
            />
          </div>

          <div>
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Phone</label>
            <input
              type="text"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-xs"
            />
          </div>

          <div>
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl focus:border-primary focus:outline-none text-white text-xs"
            />
          </div>

          <button
            type="submit"
            className="w-full py-2.5 bg-primary hover:bg-teal-700 text-white font-bold rounded-xl transition-all shadow-md cursor-pointer"
          >
            Add Doctor
          </button>
        </form>
      </div>

      {/* List Doctors and Export */}
      <div className="lg:col-span-2 space-y-6">
        <div className="glass-panel rounded-3xl overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/40">
            <h4 className="font-bold text-white text-sm uppercase tracking-wider">Registered Doctors</h4>
            <span className="px-2 py-0.5 bg-slate-800 rounded-lg text-slate-400 text-xs font-bold">{doctors.length}</span>
          </div>

          <div className="overflow-y-auto max-h-96">
            <table className="w-full text-left border-collapse">
              <thead className="bg-slate-800/30">
                <tr>
                  <th className="px-6 py-3 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Name</th>
                  <th className="px-6 py-3 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Username</th>
                  <th className="px-6 py-3 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Contact</th>
                  <th className="px-6 py-3 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50 text-xs">
                {loading ? (
                  <tr>
                    <td colSpan="4" className="px-6 py-4 text-slate-400 font-bold">Loading...</td>
                  </tr>
                ) : doctors.length > 0 ? (
                  doctors.map((doc) => (
                    <tr key={doc.id} className="hover:bg-slate-800/10">
                      <td className="px-6 py-3 font-semibold text-white">{doc.name}</td>
                      <td className="px-6 py-3 text-slate-400">{doc.username}</td>
                      <td className="px-6 py-3">
                        <div className="flex flex-col">
                          <span>{doc.email || 'N/A'}</span>
                          <span className="text-[10px] text-slate-500">{doc.phone || ''}</span>
                        </div>
                      </td>
                      <td className="px-6 py-3">
                        <button
                          onClick={() => handleDeleteDoctor(doc.id)}
                          className="p-1 hover:bg-slate-800 text-red-400 hover:text-red-300 rounded cursor-pointer flex items-center"
                          title="Delete Doctor"
                        >
                          <span className="material-symbols-outlined text-base">delete</span>
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="4" className="px-6 py-4 text-center text-slate-500 font-semibold">No doctors registered.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Database Export Utility */}
        <div className="glass-panel p-6 rounded-3xl flex justify-between items-center bg-slate-900/20">
          <div>
            <h4 className="font-bold text-white text-sm uppercase tracking-wider">System Database Data Export</h4>
            <p className="text-slate-400 text-xs mt-1">Export full diagnostic history logs in JSON database format.</p>
          </div>
          <button
            onClick={handleExportData}
            className="py-2.5 px-4 bg-teal-950/60 border border-teal-900/60 text-primary hover:bg-teal-900/40 rounded-xl font-bold flex items-center gap-2 transition-all cursor-pointer"
          >
            <span className="material-symbols-outlined text-sm">database</span>
            Export Data
          </button>
        </div>
      </div>
    </div>
  );
}
