import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Providers from './providers';
import { Sidebar } from '@/components/sidebar';
import { Toaster } from '@/components/ui/toast'; // or toaster if it exists, wait, it's just toaster? I didn't add toaster component yet. Wait, shadcn toast adds toaster.tsx.

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Enterprise HR AI Agent',
  description: 'AI Agent Dashboard Demonstration',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} flex h-screen overflow-hidden bg-zinc-950 text-zinc-50`}>
        <Providers>
          <Sidebar />
          <main className="flex-1 overflow-y-auto">
            {children}
          </main>
          {/* <Toaster /> */}
        </Providers>
      </body>
    </html>
  );
}
