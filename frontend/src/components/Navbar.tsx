import React, { useState, useEffect } from 'react';
import { ShieldCheck, ShieldAlert, User, ChevronDown, Globe, Activity, CheckCircle2 } from 'lucide-react';
import { UserProfile, DemoUser } from '../types';
import { api } from '../api';

interface NavbarProps {
  currentProfile: UserProfile | null;
  onProfileChange: (user: UserProfile) => void;
  language: string;
  onLanguageChange: (lang: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentProfile,
  onProfileChange,
  language,
  onLanguageChange
}) => {
  const [demoUsers, setDemoUsers] = useState<DemoUser[]>([]);
  const [showUserDropdown, setShowUserDropdown] = useState(false);

  useEffect(() => {
    api.getDemoUsers().then(setDemoUsers).catch(() => {});
  }, []);

  const handleSwitchUser = async (username: string) => {
    try {
      const res = await api.login(username);
      onProfileChange(res.user);
      setShowUserDropdown(false);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <header className="h-16 bg-[#070D1E] border-b border-[#1C2541] px-4 sm:px-6 flex items-center justify-between z-30 sticky top-0 shadow-lg">
      {/* Brand & Emblem */}
      <div className="flex items-center space-x-3">
        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-cyan-500 to-teal-600 flex items-center justify-center shadow-md shadow-cyan-500/20 border border-cyan-400/30">
          <ShieldCheck className="w-6 h-6 text-slate-950 font-bold" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <span className="font-extrabold text-base tracking-wider text-slate-100 flex items-center gap-1.5">
              NESFIC-D-36
              <span className="text-[10px] uppercase font-bold tracking-widest px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30">
                GOVT ASSAM
              </span>
            </span>
          </div>
          <p className="text-xs text-slate-400 hidden md:block">
            Trusted Knowledge, Rules & Document Assistant
          </p>
        </div>
      </div>

      {/* Persistent Demo Environment Badge */}
      <div className="hidden lg:flex items-center space-x-2 bg-gradient-to-r from-amber-500/10 to-orange-500/10 border border-amber-500/30 px-3 py-1 rounded-full text-xs font-semibold text-amber-300">
        <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
        <span>DEMONSTRATION & PILOT ENVIRONMENT — NESFIC 2026</span>
      </div>

      {/* Right Controls: Language, Health & Role Switcher */}
      <div className="flex items-center space-x-3">
        {/* Language Toggle */}
        <button
          onClick={() => onLanguageChange(language === 'English' ? 'Assamese' : 'English')}
          className="flex items-center space-x-1.5 bg-[#1C2541] hover:bg-[#29365C] border border-slate-700/60 px-2.5 py-1.5 rounded-lg text-xs font-medium text-slate-200 transition"
          title="Toggle Language"
        >
          <Globe className="w-3.5 h-3.5 text-cyan-400" />
          <span>{language === 'English' ? 'EN' : 'অসমীয়া'}</span>
        </button>

        {/* System Health Pulse */}
        <div className="hidden sm:flex items-center space-x-1.5 bg-[#1C2541]/70 border border-emerald-500/30 px-2.5 py-1.5 rounded-lg text-xs text-emerald-400 font-medium">
          <Activity className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
          <span>Trust Gate Active</span>
        </div>

        {/* User Role Quick Switch */}
        <div className="relative">
          <button
            onClick={() => setShowUserDropdown(!showUserDropdown)}
            className="flex items-center space-x-2.5 bg-[#1C2541] hover:bg-[#29365C] border border-cyan-500/30 px-3 py-1.5 rounded-lg text-xs transition"
          >
            <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-cyan-600 to-indigo-600 flex items-center justify-center text-white font-bold text-[11px]">
              {currentProfile?.full_name?.charAt(0) || 'U'}
            </div>
            <div className="text-left hidden sm:block">
              <div className="font-semibold text-slate-200 leading-tight">
                {currentProfile?.full_name || 'Loading...'}
              </div>
              <div className="text-[10px] text-cyan-400">
                {currentProfile?.role_name || 'Public User'}
              </div>
            </div>
            <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
          </button>

          {/* Dropdown Menu */}
          {showUserDropdown && (
            <div className="absolute right-0 mt-2 w-72 bg-[#0B132B] border border-[#29365C] rounded-xl shadow-2xl py-2 z-50">
              <div className="px-3 py-2 border-b border-slate-800 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                Switch Role / Identity (Demo RBAC)
              </div>
              <div className="max-h-64 overflow-y-auto divide-y divide-slate-800/60">
                {demoUsers.map((u) => {
                  const isActive = u.username === currentProfile?.username;
                  return (
                    <button
                      key={u.username}
                      onClick={() => handleSwitchUser(u.username)}
                      className={`w-full text-left px-3 py-2 text-xs flex items-center justify-between hover:bg-[#1C2541] transition ${
                        isActive ? 'bg-[#1C2541]/70 font-semibold text-cyan-300' : 'text-slate-300'
                      }`}
                    >
                      <div>
                        <div className="font-medium text-slate-200">{u.full_name}</div>
                        <div className="text-[10px] text-slate-400">{u.role_name} • {u.department}</div>
                      </div>
                      {isActive && <CheckCircle2 className="w-4 h-4 text-cyan-400" />}
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
