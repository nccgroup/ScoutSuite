import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import NewScan from './pages/NewScan';
import ScanDetails from './pages/ScanDetails';
import Credentials from './pages/Credentials';
import Reports from './pages/Reports';

const ProtectedLayout = ({ children }) => {
  const token = localStorage.getItem('scout_token');
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen bg-dark-bg text-dark-text flex flex-col">
      <Navbar />
      <div className="flex-1 flex overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto bg-dark-bg/50">
          {children}
        </main>
      </div>
    </div>
  );
};

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        
        <Route
          path="/"
          element={
            <ProtectedLayout>
              <Dashboard />
            </ProtectedLayout>
          }
        />
        <Route
          path="/new-scan"
          element={
            <ProtectedLayout>
              <NewScan />
            </ProtectedLayout>
          }
        />
        <Route
          path="/scans/:scanId"
          element={
            <ProtectedLayout>
              <ScanDetails />
            </ProtectedLayout>
          }
        />
        <Route
          path="/credentials"
          element={
            <ProtectedLayout>
              <Credentials />
            </ProtectedLayout>
          }
        />
        <Route
          path="/reports"
          element={
            <ProtectedLayout>
              <Reports />
            </ProtectedLayout>
          }
        />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
