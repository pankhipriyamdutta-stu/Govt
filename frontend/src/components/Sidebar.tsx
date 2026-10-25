import React from 'react';
import {
  LayoutDashboard,
  Bot,
  FolderLock,
  SearchCode,
  ShieldAlert,
  FileSpreadsheet,
  Settings,
  ChevronLeft,
  ChevronRight,
  Fingerprint
} from 'lucide-react';

export type PageId = 'dashboard' | 'veritrace' | 'copilot' | 'repository' | 'detective' | 'security' | 'reports' | 'admin';

interface SidebarProps {
  currentPage: PageId;
  onPageChange: (page: PageId) => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
  pendingReviewCount?: number;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentPage,
  onPageChange,
  collapsed,
  onToggleCollapse,
  pendingReviewCount = 5
}) => {
  const navItems = [
    {
      id: 'dashboard' as PageId,
      label: 'Command Centre',
      description: 'Home & Operational Status',
      icon: LayoutDashboard,
    },
    {
      id: 'veritrace' as PageId,
      label: 'VERITRACE AI',
      description: 'Fraud, Forensics & Provenance',
      icon: Fingerprint,
      badge: 'CYBER',
      highlight: true
    },
    {
      id: 'copilot' as PageId,
      label: 'AI Co-Pilot',
      description: 'Tripartite Grounded Assistant',
      icon: Bot,
      highlight: false
    },
    {
      id: 'repository' as PageId,
      label: 'Document Repository',
      description: 'Gazettes, Acts & Rules',
      icon: FolderLock,
    },
    {
      id: 'detective' as PageId,
      label: 'Source Detective',
      description: '360° Forensic Lineage',
      icon: SearchCode,
      badge: 'PROVENANCE'
    },
    {
      id: 'security' as PageId,
      label: 'Trust & Security',
      description: 'Signatures & Audit Trail',
      icon: ShieldAlert,
    },
    {
      id: 'reports' as PageId,
      label: 'Reports & Workspace',
      description: 'Drafts, Diffs & Exports',
      icon: FileSpreadsheet,
    },
    {
      id: 'admin' as PageId,
      label: 'Admin & Control',
      description: 'RBAC, Queue & AI Config',
      icon: Settings,
      badgeCount: pendingReviewCount
    },
  ];

  return (
    <aside
      className={`bg-[#070D1E] border-r border-[#1C2541] transition-all duration-300 flex flex-col justify-between shrink-0 ${
        collapsed ? 'w-18' : 'w-64'
      }`}
    >
      {/* Navigation items */}
      <div className="py-4 space-y-1 px-3">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentPage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onPageChange(item.id)}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl text-left transition relative group ${
                isActive
                  ? 'bg-gradient-to-r from-cyan-500/20 to-teal-500/10 text-cyan-300 border border-cyan-500/30 font-semibold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-[#1C2541]/50 font-medium'
              }`}
            >
              <Icon
                className={`w-5 h-5 shrink-0 transition ${
                  isActive ? 'text-cyan-400' : 'text-slate-400 group-hover:text-slate-200'
                }`}
              />

              {!collapsed && (
                <div className="flex-1 min-w-0">
                  <div className="text-xs flex items-center justify-between">
                    <span className="truncate">{item.label}</span>
                    {item.badge && (
                      <span className="text-[9px] font-bold tracking-wider px-1.5 py-0.2 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">
                        {item.badge}
                      </span>
                    )}
                    {item.badgeCount !== undefined && item.badgeCount > 0 && (
                      <span className="text-[10px] font-bold px-1.5 py-0.2 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30">
                        {item.badgeCount}
                      </span>
                    )}
                  </div>
                  <div className="text-[10px] text-slate-500 truncate font-normal">
                    {item.description}
                  </div>
                </div>
              )}
            </button>
          );
        })}
      </div>

      {/* Collapse Toggle Footer */}
      <div className="p-3 border-t border-[#1C2541]/80">
        <button
          onClick={onToggleCollapse}
          className="w-full flex items-center justify-center p-2 rounded-lg bg-[#1C2541]/40 hover:bg-[#1C2541] text-slate-400 hover:text-slate-200 transition text-xs"
          title={collapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <div className="flex items-center space-x-2"><ChevronLeft className="w-4 h-4" /><span>Collapse Sidebar</span></div>}
        </button>
      </div>
    </aside>
  );
};
