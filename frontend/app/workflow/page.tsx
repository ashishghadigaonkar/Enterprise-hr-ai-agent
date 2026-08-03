'use client';

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { ArrowDown, Check, GitCommit, GitBranch, GitMerge, FileText } from 'lucide-react';

export default function WorkflowPage() {
  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-white">LangGraph Architecture</h1>
        <p className="text-zinc-400 mt-1">Visual representation of the HR Agent's stateful execution graph.</p>
      </div>

      <Card className="bg-zinc-900 border-zinc-800">
        <CardHeader>
          <CardTitle className="text-zinc-200">Execution Flow</CardTitle>
          <CardDescription className="text-zinc-500">Every query traverses this directed acyclic graph (DAG).</CardDescription>
        </CardHeader>
        <CardContent className="flex justify-center py-10">
          <div className="flex flex-col items-center space-y-4">
            
            <Node label="START" variant="default" />
            <Arrow />
            
            <Node label="Input Validation" icon={Check} />
            <Arrow />
            
            <Node label="Prompt Injection Detection" icon={Check} />
            <Arrow />
            
            <Node label="Intent Classification" icon={GitCommit} variant="primary" />
            <Arrow />
            
            <Node label="Authorization Check" icon={Check} />
            <Arrow />
            
            <div className="flex flex-col items-center">
              <Node label="Conditional Router" icon={GitBranch} variant="warning" />
              <div className="h-8 w-px bg-zinc-700"></div>
              <div className="w-[600px] h-px bg-zinc-700"></div>
              <div className="flex justify-between w-[600px] pt-4">
                <div className="flex flex-col items-center">
                  <div className="h-4 w-px bg-zinc-700"></div>
                  <ArrowDown className="text-zinc-700 w-4 h-4" />
                  <Node label="PTO Tool" variant="secondary" />
                </div>
                <div className="flex flex-col items-center">
                  <div className="h-4 w-px bg-zinc-700"></div>
                  <ArrowDown className="text-zinc-700 w-4 h-4" />
                  <Node label="Expense Tool" variant="secondary" />
                </div>
                <div className="flex flex-col items-center">
                  <div className="h-4 w-px bg-zinc-700"></div>
                  <ArrowDown className="text-zinc-700 w-4 h-4" />
                  <Node label="IT Tool" variant="secondary" />
                </div>
                <div className="flex flex-col items-center">
                  <div className="h-4 w-px bg-zinc-700"></div>
                  <ArrowDown className="text-zinc-700 w-4 h-4" />
                  <Node label="HR Policy (RAG)" icon={FileText} variant="secondary" />
                </div>
              </div>
              <div className="flex justify-between w-[600px] pb-4">
                <div className="flex flex-col items-center w-full">
                  <div className="h-8 w-px bg-zinc-700"></div>
                </div>
                <div className="flex flex-col items-center w-full">
                  <div className="h-8 w-px bg-zinc-700"></div>
                </div>
                <div className="flex flex-col items-center w-full">
                  <div className="h-8 w-px bg-zinc-700"></div>
                </div>
                <div className="flex flex-col items-center w-full">
                  <div className="h-8 w-px bg-zinc-700"></div>
                </div>
              </div>
              <div className="w-[600px] h-px bg-zinc-700 relative">
                <div className="absolute left-1/2 -top-4 -translate-x-1/2">
                   <ArrowDown className="text-zinc-700 w-4 h-4" />
                </div>
              </div>
              <div className="h-8 w-px bg-zinc-700"></div>
            </div>
            
            <Node label="Draft Response" icon={GitMerge} variant="primary" />
            <Arrow />
            
            <Node label="Self Evaluation" icon={Check} />
            <Arrow />
            
            <Node label="Audit Logger" icon={FileText} />
            <Arrow />

            <Node label="END" variant="default" />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function Arrow() {
  return (
    <div className="h-6 w-px bg-zinc-700 relative">
      <ArrowDown className="absolute -bottom-3 -left-[7px] text-zinc-700 w-4 h-4" />
    </div>
  );
}

function Node({ label, icon: Icon, variant = 'default' }: { label: string, icon?: any, variant?: 'default' | 'primary' | 'secondary' | 'warning' }) {
  const baseClasses = "flex items-center gap-2 px-4 py-2 rounded-lg border text-sm font-medium shadow-sm w-48 justify-center";
  
  const variants = {
    default: "bg-zinc-950 border-zinc-800 text-zinc-300",
    primary: "bg-blue-950/30 border-blue-900/50 text-blue-400",
    secondary: "bg-emerald-950/30 border-emerald-900/50 text-emerald-400",
    warning: "bg-amber-950/30 border-amber-900/50 text-amber-400",
  };

  return (
    <div className={`${baseClasses} ${variants[variant]}`}>
      {Icon && <Icon className="w-4 h-4" />}
      <span className="text-center">{label}</span>
    </div>
  );
}
