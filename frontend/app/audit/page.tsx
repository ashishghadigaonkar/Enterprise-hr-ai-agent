'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getLogs } from '@/services/api';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Search, Loader2 } from 'lucide-react';

export default function AuditPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['logs'],
    queryFn: getLogs,
    refetchInterval: 5000,
  });

  const [search, setSearch] = useState('');

  const logs = data?.logs || [];
  
  const filteredLogs = logs.filter((log: any) => 
    log.employee_id?.toLowerCase().includes(search.toLowerCase()) ||
    log.user_query?.toLowerCase().includes(search.toLowerCase()) ||
    log.intent?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Audit Logs</h1>
          <p className="text-zinc-400 mt-1">Immutable execution records of all HR Agent interactions.</p>
        </div>
      </div>

      <Card className="bg-zinc-900 border-zinc-800">
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle className="text-zinc-200">Execution History</CardTitle>
            <div className="relative w-64">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-zinc-500" />
              <Input
                placeholder="Search logs..."
                className="pl-8 bg-zinc-950 border-zinc-800 text-white h-9"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex justify-center p-8">
              <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
            </div>
          ) : (
            <div className="rounded-md border border-zinc-800 overflow-hidden">
              <Table>
                <TableHeader className="bg-zinc-950">
                  <TableRow className="border-zinc-800 hover:bg-transparent">
                    <TableHead className="text-zinc-400">Timestamp</TableHead>
                    <TableHead className="text-zinc-400">Trace ID</TableHead>
                    <TableHead className="text-zinc-400">Emp ID</TableHead>
                    <TableHead className="text-zinc-400 w-[200px]">Intent</TableHead>
                    <TableHead className="text-zinc-400">Sec Block</TableHead>
                    <TableHead className="text-zinc-400">Auth Block</TableHead>
                    <TableHead className="text-zinc-400 text-right">Confidence</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredLogs.map((log: any, i: number) => (
                    <TableRow key={i} className="border-zinc-800 hover:bg-zinc-800/50">
                      <TableCell className="text-xs text-zinc-400">{log.timestamp}</TableCell>
                      <TableCell className="font-mono text-xs text-zinc-500">{log.trace_id?.substring(0,8)}</TableCell>
                      <TableCell className="text-zinc-300">{log.employee_id}</TableCell>
                      <TableCell>
                        <Badge variant="outline" className="bg-zinc-800 border-zinc-700 text-zinc-300 font-normal">
                          {log.intent || 'N/A'}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        {log.security_flag ? (
                          <Badge variant="destructive" className="bg-rose-500/20 text-rose-400 border-rose-500/20 hover:bg-rose-500/20">Blocked</Badge>
                        ) : (
                          <span className="text-zinc-500 text-xs">Pass</span>
                        )}
                      </TableCell>
                      <TableCell>
                        {log.auth_approved === false || log.auth_approved === 0 || log.auth_approved === 'False' ? (
                          <Badge variant="destructive" className="bg-amber-500/20 text-amber-500 border-amber-500/20 hover:bg-amber-500/20">Denied</Badge>
                        ) : (
                          <span className="text-zinc-500 text-xs">Pass</span>
                        )}
                      </TableCell>
                      <TableCell className="text-right text-blue-400">
                        {log.confidence_score ? `${(parseFloat(log.confidence_score) * 100).toFixed(0)}%` : '-'}
                      </TableCell>
                    </TableRow>
                  ))}
                  {filteredLogs.length === 0 && (
                    <TableRow>
                      <TableCell colSpan={7} className="text-center text-zinc-500 py-8">
                        No audit logs found.
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
