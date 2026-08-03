'use client';

import { useQuery } from '@tanstack/react-query';
import { getSettings } from '@/services/api';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Loader2, Server, Key, Database, Globe } from 'lucide-react';

export default function SettingsPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['settings'],
    queryFn: getSettings,
  });

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Settings & Environment</h1>
          <p className="text-zinc-400 mt-1">View the current configuration of the HR AI Agent.</p>
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center p-12">
          <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card className="bg-zinc-900 border-zinc-800">
            <CardHeader>
              <CardTitle className="text-zinc-200 flex items-center gap-2">
                <Server className="h-5 w-5 text-blue-500" />
                Backend Configuration
              </CardTitle>
              <CardDescription className="text-zinc-500">Core server settings.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center py-2 border-b border-zinc-800">
                <span className="text-sm text-zinc-400">Environment</span>
                <span className="text-sm font-medium text-white">{data?.environment}</span>
              </div>
              <div className="flex justify-between items-center py-2 border-b border-zinc-800">
                <span className="text-sm text-zinc-400">Backend Health</span>
                <Badge className="bg-emerald-500/20 text-emerald-500 hover:bg-emerald-500/20">
                  {data?.backend_health}
                </Badge>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-zinc-900 border-zinc-800">
            <CardHeader>
              <CardTitle className="text-zinc-200 flex items-center gap-2">
                <Key className="h-5 w-5 text-blue-500" />
                AI Models
              </CardTitle>
              <CardDescription className="text-zinc-500">LLM and Embedding providers.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center py-2 border-b border-zinc-800">
                <span className="text-sm text-zinc-400">LLM Provider</span>
                <span className="text-sm font-medium text-white uppercase">{data?.llm_provider}</span>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-zinc-900 border-zinc-800">
            <CardHeader>
              <CardTitle className="text-zinc-200 flex items-center gap-2">
                <Database className="h-5 w-5 text-blue-500" />
                Vector Database
              </CardTitle>
              <CardDescription className="text-zinc-500">Pinecone RAG setup.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center py-2 border-b border-zinc-800">
                <span className="text-sm text-zinc-400">Pinecone Status</span>
                <Badge variant="outline" className={data?.pinecone_status === 'Enabled' ? 'text-emerald-500 border-emerald-500/50' : 'text-zinc-500 border-zinc-700'}>
                  {data?.pinecone_status}
                </Badge>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-zinc-900 border-zinc-800">
            <CardHeader>
              <CardTitle className="text-zinc-200 flex items-center gap-2">
                <Globe className="h-5 w-5 text-blue-500" />
                Observability
              </CardTitle>
              <CardDescription className="text-zinc-500">LangSmith Tracing.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center py-2 border-b border-zinc-800">
                <span className="text-sm text-zinc-400">LangSmith Status</span>
                <Badge variant="outline" className={data?.langsmith_status === 'Enabled' ? 'text-blue-500 border-blue-500/50' : 'text-zinc-500 border-zinc-700'}>
                  {data?.langsmith_status}
                </Badge>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
