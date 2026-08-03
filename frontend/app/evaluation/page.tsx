'use client';

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer,
  LineChart, Line, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';

// Simulated evaluation metrics for demonstration
const trendData = [
  { name: 'Mon', intentAcc: 94, groundedness: 88, refusalAcc: 98 },
  { name: 'Tue', intentAcc: 95, groundedness: 89, refusalAcc: 99 },
  { name: 'Wed', intentAcc: 93, groundedness: 92, refusalAcc: 97 },
  { name: 'Thu', intentAcc: 97, groundedness: 94, refusalAcc: 99 },
  { name: 'Fri', intentAcc: 96, groundedness: 95, refusalAcc: 98 },
];

const radarData = [
  { subject: 'Intent Accuracy', A: 96, fullMark: 100 },
  { subject: 'Refusal Accuracy', A: 98, fullMark: 100 },
  { subject: 'Groundedness', A: 92, fullMark: 100 },
  { subject: 'Format Adherence', A: 99, fullMark: 100 },
  { subject: 'Tone', A: 95, fullMark: 100 },
  { subject: 'Hallucination (Inv)', A: 94, fullMark: 100 }, // Inverted so higher is better
];

const errorData = [
  { name: 'Missing Context', count: 12 },
  { name: 'Wrong Intent', count: 5 },
  { name: 'Hallucination', count: 3 },
  { name: 'Formatting', count: 8 },
];

export default function EvaluationPage() {
  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Agent Evaluation</h1>
          <p className="text-zinc-400 mt-1">Continuous performance monitoring and quality metrics.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="bg-zinc-900 border-zinc-800">
          <CardHeader>
            <CardTitle className="text-zinc-200">Quality Trends over Time</CardTitle>
            <CardDescription className="text-zinc-500">7-day rolling average of key metrics</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                <XAxis dataKey="name" stroke="#888" tickLine={false} axisLine={false} />
                <YAxis stroke="#888" tickLine={false} axisLine={false} domain={[80, 100]} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Line type="monotone" dataKey="intentAcc" name="Intent Accuracy" stroke="#3b82f6" strokeWidth={2} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="groundedness" name="Groundedness" stroke="#10b981" strokeWidth={2} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="refusalAcc" name="Refusal Accuracy" stroke="#f59e0b" strokeWidth={2} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="bg-zinc-900 border-zinc-800">
          <CardHeader>
            <CardTitle className="text-zinc-200">Capabilities Radar</CardTitle>
            <CardDescription className="text-zinc-500">Holistic view of agent performance dimensions</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                <PolarGrid stroke="#333" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#888', fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: '#555' }} />
                <Radar name="Agent v1.2" dataKey="A" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.4} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a' }}
                  itemStyle={{ color: '#fff' }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="bg-zinc-900 border-zinc-800 md:col-span-2">
          <CardHeader>
            <CardTitle className="text-zinc-200">Error Distribution</CardTitle>
            <CardDescription className="text-zinc-500">Categorization of imperfect responses from the evaluator node.</CardDescription>
          </CardHeader>
          <CardContent className="h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={errorData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" horizontal={true} vertical={false} />
                <XAxis type="number" stroke="#888" tickLine={false} axisLine={false} />
                <YAxis dataKey="name" type="category" stroke="#888" tickLine={false} axisLine={false} width={120} />
                <RechartsTooltip 
                  cursor={{ fill: '#27272a' }}
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Bar dataKey="count" name="Issues" fill="#ef4444" radius={[0, 4, 4, 0]} barSize={20} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
