"use client";

import { useState } from "react";

interface LandAnalysisFormProps {
  onSubmit: (file: File) => Promise<void>;
  loading: boolean;
}

export default function LandAnalysisForm({
  onSubmit,
  loading,
}: LandAnalysisFormProps) {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!file) return;

    setError(null);

    try {
      await onSubmit(file);
    } catch (submissionError) {
      setError(
        submissionError instanceof Error
          ? submissionError.message
          : "Failed to analyze the land document."
      );
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-[3px] border border-[#D9CFB8] bg-[#F3EEE3] p-6"
    >
      <p className="mb-1 font-mono text-[11px] uppercase tracking-[0.16em] text-[#79705C]">
        Land Intelligence
      </p>
      <h2 className="font-serif text-lg font-semibold text-[#1B1F27]">
        Upload a land survey or plan
      </h2>
      <p className="mt-2 text-sm leading-relaxed text-[#79705C]">
        Upload a PDF, JPG, or PNG to extract document evidence and prepare a
        source-separated business report.
      </p>

      <label className="mt-5 flex cursor-pointer items-center justify-between gap-4 rounded-[3px] border border-dashed border-[#A9791F] bg-white/70 p-4 text-sm text-[#1B1F27]">
        <span className="min-w-0 truncate">
          {file ? file.name : "Choose a PDF, JPG, or PNG"}
        </span>
        <span className="shrink-0 font-mono text-[11px] uppercase tracking-[0.1em] text-[#79705C]">
          Browse
        </span>
        <input
          className="sr-only"
          type="file"
          accept=".pdf,.jpg,.jpeg,.png,application/pdf,image/jpeg,image/png"
          onChange={(event) => setFile(event.target.files?.[0] ?? null)}
        />
      </label>

      <div className="mt-4 flex justify-end">
        <button
          type="submit"
          disabled={!file || loading}
          className="rounded-[3px] bg-[#1B1F27] px-6 py-3 font-mono text-sm uppercase tracking-[0.08em] text-[#F3EEE3] transition-colors hover:bg-[#2B6660] disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? "Analyzing…" : "Analyze Land"}
        </button>
      </div>

      {error && (
        <p role="alert" className="mt-4 text-sm text-[#9B3B2E]">
          {error}
        </p>
      )}
    </form>
  );
}
