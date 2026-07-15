"use client";

import React, { useState, useEffect } from "react";

interface Lead {
  id: number;
  company_name: string;
  website_url: string;
  opportunity_score: number;
  conversion_status: string;
  generated_outreach: string | null;
}

export default function DashboardPage() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchLeads() {
      try {
        // Points directly to the FastAPI Backend implementation route layer
        const response = await fetch("http://localhost:8000/api/v1/leads");
        if (!response.ok) {
          throw new Error("Failed to pull live platform context matrices.");
        }
        const data = await response.json();
        setLeads(data);
      } catch (err: any) {
        setError(err.message || "An unexpected system error occurred.");
      } finally {
        setLoading(false);
      }
    }
    fetchLeads();
  }, []);

  // Structural aggregates calculated directly inline
  const totalLeads = leads.length;
  const criticalLeads = leads.filter((l) => l.opportunity_score >= 75).length;
  const convertedLeads = leads.filter((l) => l.conversion_status === "CONVERTED").length;

  if (loading) {
    return (
      <div className="flex h-screen w-full items-center justify-center bg-slate-950 text-slate-200">
        <div className="text-center space-y-4">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent mx-auto"></div>
          <p className="text-sm font-medium tracking-wide text-slate-400">Loading Pipeline Infrastructure...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-screen w-full items-center justify-center bg-slate-950 p-6">
        <div className="max-w-md rounded-xl border border-red-500/20 bg-red-950/10 p-6 text-center text-red-400">
          <h3 className="text-lg font-bold">System Connection Failure</h3>
          <p className="mt-2 text-sm text-red-300/80">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 p-8 text-slate-100 selection:bg-indigo-500 selection:text-white">
      <div className="mx-auto max-w-7xl space-y-8">
        
        {/* Header Block */}
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between border-b border-slate-800 pb-6">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
              Lead Acquisition Engine
            </h1>
            <p className="mt-1 text-sm text-slate-400">
              Enterprise analysis matrix and programmatic intelligence routing framework.
            </p>
          </div>
          <button className="inline-flex h-10 items-center justify-center rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-indigo-600/20 transition-all hover:bg-indigo-500 hover:shadow-indigo-600/30 active:scale-95">
            Initialize Domain Ingestion
          </button>
        </div>

        {/* Aggregates Dashboard Analytics row */}
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6 shadow-sm backdrop-blur-md">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">Total Targets Indexed</p>
            <p className="mt-2 text-4xl font-black tracking-tight text-white">{totalLeads}</p>
          </div>
          <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6 shadow-sm backdrop-blur-md">
            <p className="text-xs font-semibold uppercase tracking-wider text-amber-500">Critical Priority Gaps (Score ≥ 75)</p>
            <p className="mt-2 text-4xl font-black tracking-tight text-amber-400">{criticalLeads}</p>
          </div>
          <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-6 shadow-sm backdrop-blur-md">
            <p className="text-xs font-semibold uppercase tracking-wider text-emerald-500">Converted Pipelines</p>
            <p className="mt-2 text-4xl font-black tracking-tight text-emerald-400">{convertedLeads}</p>
          </div>
        </div>

        {/* Main Leads Data Structure Presentation */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/40 shadow-xl backdrop-blur-md overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-800 bg-slate-900/80">
            <h2 className="text-lg font-bold text-slate-200">Optimization Acquisition Queue</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-800 bg-slate-950/50 text-xs font-semibold uppercase tracking-wider text-slate-400">
                  <th className="px-6 py-4">Company Profile</th>
                  <th className="px-6 py-4">Target Domain</th>
                  <th className="px-6 py-4 text-center">Opportunity Index</th>
                  <th className="px-6 py-4">Lifecycle State</th>
                  <th className="px-6 py-4">Generated Outreach Payload Hook</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 bg-transparent text-sm">
                {leads.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-12 text-center text-slate-500 font-medium">
                      No active acquisition records found within platform data nodes.
                    </td>
                  </tr>
                ) : (
                  leads.map((lead) => (
                    <tr key={lead.id} className="transition-colors hover:bg-slate-900/40">
                      <td className="whitespace-nowrap px-6 py-4 font-semibold text-slate-200">
                        {lead.company_name}
                      </td>
                      <td className="whitespace-nowrap px-6 py-4 text-slate-400">
                        <a href={lead.website_url} target="_blank" rel="noopener noreferrer" className="hover:text-indigo-400 transition-colors underline decoration-slate-700 underline-offset-4">
                          {lead.website_url}
                        </a>
                      </td>
                      <td className="whitespace-nowrap px-6 py-4 text-center">
                        <span className={`inline-flex items-center justify-center px-2.5 py-1 rounded-md text-xs font-bold tracking-tight ${
                          lead.opportunity_score >= 75 
                            ? "bg-red-500/10 text-red-400 border border-red-500/20" 
                            : lead.opportunity_score >= 40 
                            ? "bg-amber-500/10 text-amber-400 border border-amber-500/20" 
                            : "bg-slate-800 text-slate-400"
                        }`}>
                          {lead.opportunity_score} / 100
                        </span>
                      </td>
                      <td className="whitespace-nowrap px-6 py-4">
                        <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-300">
                          <span className={`h-2 w-2 rounded-full ${
                            lead.conversion_status === "CONVERTED" ? "bg-emerald-500" : "bg-indigo-400 animate-pulse"
                          }`} />
                          {lead.conversion_status}
                        </span>
                      </td>
                      <td className="px-6 py-4 max-w-md text-slate-300 font-normal leading-relaxed text-xs">
                        {lead.generated_outreach ? (
                          <div className="rounded-lg bg-slate-950 p-3 border border-slate-800/80 text-slate-300 italic">
                            "{lead.generated_outreach}"
                          </div>
                        ) : (
                          <span className="text-slate-500 tracking-wide text-xs">Generation bypass triggered.</span>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  );
}