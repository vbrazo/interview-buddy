import { useState, useEffect, useRef, KeyboardEvent } from "react";
import { Loader2, Send, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { EXAMPLE_JOB_DESCRIPTIONS } from "@/data/mockData";

interface JobInputProps {
  value: string;
  onChange: (value: string) => void;
  onAnalyze: (value: string) => void;
  isLoading: boolean;
}

const MAX_CHARS = 10000;

export function JobInput({ value, onChange, onAnalyze, isLoading }: JobInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter" && value.trim()) {
      e.preventDefault();
      onAnalyze(value);
    }
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-semibold text-foreground">Job Description</h2>
        <span className="text-xs text-muted-foreground font-mono">
          {value.length.toLocaleString()} / {MAX_CHARS.toLocaleString()} characters
        </span>
      </div>

      <div className="relative">
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => onChange(e.target.value.slice(0, MAX_CHARS))}
          onKeyDown={handleKeyDown}
          placeholder={`Paste your job description here...\n\nExample:\nSenior Software Engineer at Stripe\nWe're looking for engineers with 5+ years experience in Python, React, and distributed systems...`}
          className="w-full min-h-[260px] resize-none rounded-xl border border-border bg-secondary/50 px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary/50 transition-all"
        />
      </div>

      <Button
        onClick={() => onAnalyze(value)}
        disabled={!value.trim() || isLoading}
        className="w-full gradient-primary text-primary-foreground font-medium rounded-xl h-11 text-sm transition-all hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed"
      >
        {isLoading ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Analyzing...
          </>
        ) : (
          <>
            <Send className="mr-2 h-4 w-4" />
            Analyze & Prepare
          </>
        )}
      </Button>

      <p className="text-xs text-muted-foreground text-center">
        <kbd className="px-1.5 py-0.5 rounded bg-secondary text-muted-foreground text-[10px] font-mono">⌘</kbd>
        {" + "}
        <kbd className="px-1.5 py-0.5 rounded bg-secondary text-muted-foreground text-[10px] font-mono">Enter</kbd>
        {" to analyze"}
      </p>

      <div className="border-t border-border/50 pt-4">
        <p className="text-xs text-muted-foreground mb-2">Quick start:</p>
        <div className="flex flex-col gap-2">
          {EXAMPLE_JOB_DESCRIPTIONS.map((ex) => (
            <button
              key={ex.label}
              onClick={() => onChange(ex.text)}
              disabled={isLoading}
              className="flex items-center gap-2 rounded-lg border border-border/50 bg-secondary/30 px-3 py-2 text-xs text-muted-foreground hover:text-foreground hover:border-primary/30 hover:bg-secondary/60 transition-all text-left disabled:opacity-40"
            >
              <Zap className="h-3 w-3 text-accent shrink-0" />
              {ex.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
