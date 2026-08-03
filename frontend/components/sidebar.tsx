'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, 
  Bot, 
  GitMerge, 
  Files, 
  BarChart, 
  ShieldAlert, 
  Settings 
} from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'AI Playground', href: '/playground', icon: Bot },
  { name: 'Workflow', href: '/workflow', icon: GitMerge },
  { name: 'Batch Processing', href: '/batch', icon: Files },
  { name: 'Evaluation', href: '/evaluation', icon: BarChart },
  { name: 'Audit Logs', href: '/audit', icon: ShieldAlert },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex h-screen w-64 flex-col border-r bg-zinc-950 text-zinc-50">
      <div className="flex h-14 items-center border-b px-6">
        <div className="flex items-center gap-2 font-semibold">
          <Bot className="h-5 w-5 text-blue-500" />
          <span>HR AI Agent</span>
        </div>
      </div>
      <div className="flex-1 overflow-auto py-4">
        <nav className="grid gap-1 px-4">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                  isActive 
                    ? "bg-zinc-800 text-zinc-50" 
                    : "text-zinc-400 hover:bg-zinc-900 hover:text-zinc-50"
                )}
              >
                <item.icon className="h-4 w-4" />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>
      <div className="border-t p-4">
        <div className="rounded-md bg-zinc-900 p-3 text-xs text-zinc-400">
          <p className="font-semibold text-zinc-300">Agent Status</p>
          <div className="mt-2 flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-500"></span>
            </span>
            <span className="text-emerald-500 font-medium">Online</span>
          </div>
        </div>
      </div>
    </div>
  );
}
