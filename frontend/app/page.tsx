'use client';

import { useQuery } from '@tanstack/react-query';
import { getMetrics } from '@/services/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { ShieldAlert, Activity, CheckCircle, Brain, Target, Lock } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

export default function DashboardPage() {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['metrics'],
    queryFn: getMetrics,
    refetchInterval: 5000,
  });

  if (isLoading || !metrics) {
    return (
      <div className="p-8 space-y-6">
        <h1 className="text-3xl font-bold tracking-tight text-white">Dashboard Overview</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map(i => (
            <Card key={i} className="bg-zinc-900 border-zinc-800">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <Skeleton className="h-4 w-[100px] bg-zinc-800" />
                <Skeleton className="h-4 w-4 bg-zinc-800" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-8 w-[60px] bg-zinc-800" />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  const intentData = Object.entries(metrics.intents).map(([name, value]) => ({
    name,
    value
  }));

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight text-white">Dashboard Overview</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard 
          title="Total Queries" 
          value={metrics.total_queries} 
          icon={Activity} 
          description="Total processed by LangGraph"
        />
        <MetricCard 
          title="Successful Responses" 
          value={metrics.successful_requests} 
          icon={CheckCircle} 
          className="text-emerald-500"
          description="Queries with valid intent and auth"
        />
        <MetricCard 
          title="Security Blocks" 
          value={metrics.security_blocks} 
          icon={ShieldAlert}
          className="text-rose-500"
          description="Prompt injections caught"
        />
        <MetricCard 
          title="Auth Denials" 
          value={metrics.authorization_blocks} 
          icon={Lock}
          className="text-amber-500"
          description="Cross-employee access blocked"
        />
        <MetricCard 
          title="Avg Confidence" 
          value={`${(metrics.average_confidence * 100).toFixed(1)}%`} 
          icon={Target}
          description="Based on LLM self-evaluation"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <Card className="bg-zinc-900 border-zinc-800">
          <CardHeader>
            <CardTitle className="text-zinc-200">Intent Distribution</CardTitle>
          </CardHeader>
          <CardContent className="h-[300px]">
            {intentData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={intentData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                  <XAxis dataKey="name" stroke="#888" tickLine={false} axisLine={false} />
                  <YAxis stroke="#888" tickLine={false} axisLine={false} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a' }}
                    itemStyle={{ color: '#fff' }}
                  />
                  <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex h-full items-center justify-center text-zinc-500">
                No intent data available yet.
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function MetricCard({ title, value, icon: Icon, description, className = "text-blue-500" }: any) {
  return (
    <Card className="bg-zinc-900 border-zinc-800">
      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
        <CardTitle className="text-sm font-medium text-zinc-400">{title}</CardTitle>
        <Icon className={`h-4 w-4 ${className}`} />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold text-white">{value}</div>
        {description && (
          <p className="text-xs text-zinc-500 mt-1">{description}</p>
        )}
      </CardContent>
    </Card>
  );
}
