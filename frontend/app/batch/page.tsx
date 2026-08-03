'use client';

import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { uploadBatch } from '@/services/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Upload, FileText, Loader2, Download, CheckCircle, AlertCircle } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

export default function BatchPage() {
  const [file, setFile] = useState<File | null>(null);
  
  const mutation = useMutation({
    mutationFn: (f: File) => uploadBatch(f),
  });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = () => {
    if (file) {
      mutation.mutate(file);
    }
  };

  const results = mutation.data?.results || [];

  const handleDownload = () => {
    if (!results || results.length === 0) return;
    const headers = ['trace_id', 'query_id', 'employee_id', 'user_query', 'intent', 'security_flag', 'auth_approved', 'draft_response'];
    const csvContent = [
      headers.join(','),
      ...results.map((res: any) => 
        headers.map(header => {
          let val = res[header] ?? '';
          if (typeof val === 'string') {
            val = `"${val.replace(/"/g, '""')}"`;
          }
          return val;
        }).join(',')
      )
    ].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'batch_results.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Batch Processing</h1>
          <p className="text-zinc-400 mt-1">Upload a CSV to process multiple HR queries asynchronously.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="bg-zinc-900 border-zinc-800 lg:col-span-1">
          <CardHeader>
            <CardTitle className="text-zinc-200">Upload Queries</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="border-2 border-dashed border-zinc-700 rounded-lg p-6 text-center hover:bg-zinc-800/50 transition-colors">
              <input
                type="file"
                accept=".csv"
                id="file-upload"
                className="hidden"
                onChange={handleFileChange}
              />
              <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center">
                <FileText className="h-8 w-8 text-zinc-400 mb-2" />
                <span className="text-sm text-zinc-300 font-medium">
                  {file ? file.name : "Select a CSV file"}
                </span>
                <span className="text-xs text-zinc-500 mt-1">
                  Expected columns: employee_id, user_query
                </span>
              </label>
            </div>
            <Button 
              onClick={handleUpload} 
              disabled={!file || mutation.isPending}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white"
            >
              {mutation.isPending ? (
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <Upload className="h-4 w-4 mr-2" />
              )}
              {mutation.isPending ? 'Processing Batch...' : 'Process Batch'}
            </Button>
          </CardContent>
        </Card>

        <Card className="bg-zinc-900 border-zinc-800 lg:col-span-2">
          <CardHeader className="flex flex-row justify-between items-center">
            <CardTitle className="text-zinc-200">Batch Results</CardTitle>
            {results.length > 0 && (
              <Button variant="outline" size="sm" className="border-zinc-700 text-zinc-300" onClick={handleDownload}>
                <Download className="h-4 w-4 mr-2" />
                Download CSV
              </Button>
            )}
          </CardHeader>
          <CardContent>
            {mutation.isPending ? (
              <div className="flex flex-col items-center justify-center h-48 space-y-4 text-zinc-400">
                <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
                <p>Executing LangGraph Nodes for each query...</p>
              </div>
            ) : results.length > 0 ? (
              <div className="overflow-auto max-h-[400px]">
                <Table>
                  <TableHeader>
                    <TableRow className="border-zinc-800 hover:bg-transparent">
                      <TableHead className="text-zinc-400">Emp ID</TableHead>
                      <TableHead className="text-zinc-400">Query</TableHead>
                      <TableHead className="text-zinc-400">Intent</TableHead>
                      <TableHead className="text-zinc-400">Status</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {results.map((res: any, idx: number) => {
                      const success = res.security_flag === false && res.auth_approved === true;
                      return (
                        <TableRow key={idx} className="border-zinc-800 hover:bg-zinc-800/50">
                          <TableCell className="font-mono text-xs text-zinc-300">{res.employee_id}</TableCell>
                          <TableCell className="text-zinc-300 max-w-[200px] truncate" title={res.user_query}>
                            {res.user_query}
                          </TableCell>
                          <TableCell>
                            <Badge variant="outline" className="bg-zinc-800 text-zinc-300 border-zinc-700">
                              {res.intent || 'N/A'}
                            </Badge>
                          </TableCell>
                          <TableCell>
                            {success ? (
                              <div className="flex items-center text-emerald-500 text-xs font-medium">
                                <CheckCircle className="h-3 w-3 mr-1" /> OK
                              </div>
                            ) : (
                              <div className="flex items-center text-rose-500 text-xs font-medium">
                                <AlertCircle className="h-3 w-3 mr-1" /> BLOCKED
                              </div>
                            )}
                          </TableCell>
                        </TableRow>
                      );
                    })}
                  </TableBody>
                </Table>
              </div>
            ) : (
              <div className="flex h-48 items-center justify-center text-zinc-500">
                Upload a CSV to see results.
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
