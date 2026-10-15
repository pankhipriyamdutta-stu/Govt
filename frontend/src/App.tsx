import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Sidebar, PageId } from './components/Sidebar';
import { CommandCentre } from './pages/CommandCentre';
import { AiCopilot } from './pages/AiCopilot';
import { DocumentRepository } from './pages/DocumentRepository';
import { SourceDetective } from './pages/SourceDetective';
import { TrustSecurityCenter } from './pages/TrustSecurityCenter';
import { ReportsWorkspace } from './pages/ReportsWorkspace';
import { AdminControl } from './pages/AdminControl';
import { UserProfile } from './types';
import { api } from './api';

export const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<PageId>('dashboard');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [language, setLanguage] = useState<string>('English');
  const [navigationPayload, setNavigationPayload] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initial login as default officer for seamless demo experience
    api.login('officer_sharma', 'GovtSecure@2026')
      .then((res) => {
        setUserProfile(res.user);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Initial login error:', err);
        setLoading(false);
      });
  }, []);

  const handleNavigate = (page: PageId, extraData?: any) => {
    setCurrentPage(page);
    if (extraData) {
      setNavigationPayload(extraData);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#070D1E] flex flex-col items-center justify-center text-slate-300">
        <div className="w-12 h-12 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin mb-4"></div>
        <div className="font-extrabold text-lg text-white tracking-wider">NESFIC-D-36</div>
        <div className="text-xs text-slate-400">Loading Trusted Government Assistant Operating Environment...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0B132B] flex flex-col text-slate-100">
      {/* Top Navigation Bar */}
      <Navbar
        currentProfile={userProfile}
        onProfileChange={setUserProfile}
        language={language}
        onLanguageChange={setLanguage}
      />

      {/* Main Body Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Collapsible Sidebar */}
        <Sidebar
          currentPage={currentPage}
          onPageChange={handleNavigate}
          collapsed={sidebarCollapsed}
          onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
          pendingReviewCount={5}
        />

        {/* Dynamic Page Workspace */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 bg-gradient-to-b from-[#0B132B] via-[#0D1630] to-[#070D1E]">
          {currentPage === 'dashboard' && (
            <CommandCentre userProfile={userProfile} onNavigate={handleNavigate} />
          )}

          {currentPage === 'copilot' && (
            <AiCopilot
              userProfile={userProfile}
              onNavigate={handleNavigate}
              initialQuery={navigationPayload?.initialQuery || ''}
              language={language}
            />
          )}

          {currentPage === 'repository' && (
            <DocumentRepository userProfile={userProfile} onNavigate={handleNavigate} />
          )}

          {currentPage === 'detective' && (
            <SourceDetective
              initialClaimId={navigationPayload?.claimId || 'CLM-SCST-001'}
            />
          )}

          {currentPage === 'security' && (
            <TrustSecurityCenter />
          )}

          {currentPage === 'reports' && (
            <ReportsWorkspace userProfile={userProfile} />
          )}

          {currentPage === 'admin' && (
            <AdminControl userProfile={userProfile} />
          )}
        </main>
      </div>
    </div>
  );
};

export default App;
