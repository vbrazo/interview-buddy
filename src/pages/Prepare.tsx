import { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import { JobInput } from "@/components/JobInput";
import { EmptyState, StreamingDisplay } from "@/components/StreamingDisplay";
import { ResultsSections } from "@/components/ResultsSections";
import { ActionBar } from "@/components/ActionBar";
import { useAnalysis } from "@/hooks/useAnalysis";
import { useSavedAnalyses } from "@/hooks/useSavedAnalyses";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { AlertTriangle } from "lucide-react";
import { SavedAnalysis } from "@/types/analysis";

export default function Prepare() {
  const { state, steps, result, progress, error, analyze, reset, loadResult, savedInput, setSavedInput } = useAnalysis();
  const { save } = useSavedAnalyses();
  const { toast } = useToast();
  const resultsRef = useRef<HTMLDivElement>(null);
  const location = useLocation();
  const loadedFromHistoryRef = useRef(false);
  const didAutoSaveRef = useRef(false);

  // Load from history navigation
  useEffect(() => {
    const loaded = (location.state as { loaded?: SavedAnalysis })?.loaded;
    if (loaded) {
      loadedFromHistoryRef.current = true;
      setSavedInput(loaded.jobDescription);
      loadResult(loaded.results);
      window.history.replaceState({}, document.title);
    }
  }, [location.state, setSavedInput, loadResult]);

  // Auto-save to history when a new analysis completes (not when loaded from history)
  useEffect(() => {
    if (state !== "complete" || !result || !savedInput.trim()) return;
    if (loadedFromHistoryRef.current || didAutoSaveRef.current) return;
    save(savedInput, result);
    didAutoSaveRef.current = true;
    toast({ title: "Analysis saved", description: "View it anytime from History." });
  }, [state, result, savedInput, save, toast]);

  useEffect(() => {
    if (state === "complete" && resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [state]);

  // Show toast on error
  useEffect(() => {
    if (state === "error" && error) {
      toast({ title: "Analysis failed", description: error, variant: "destructive" });
    }
  }, [state, error, toast]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        didAutoSaveRef.current = false;
        loadedFromHistoryRef.current = false;
        reset();
        setSavedInput("");
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [reset, setSavedInput]);

  const handleAnalyze = (jobDescription: string) => {
    loadedFromHistoryRef.current = false;
    didAutoSaveRef.current = false;
    analyze(jobDescription);
  };

  const handleReset = () => {
    didAutoSaveRef.current = false;
    loadedFromHistoryRef.current = false;
    reset();
    setSavedInput("");
  };

  return (
    <div className="container mx-auto px-4 sm:px-6 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
        <div className={`lg:col-span-2 ${state === "complete" ? "lg:sticky lg:top-20 lg:self-start" : ""}`}>
          <div className="rounded-xl border border-border/50 bg-card p-5 shadow-card">
            <JobInput
              value={savedInput}
              onChange={setSavedInput}
              onAnalyze={handleAnalyze}
              isLoading={state === "streaming"}
            />
          </div>
        </div>

        <div className="lg:col-span-3" ref={resultsRef}>
          {state === "idle" && <EmptyState />}
          {state === "streaming" && <StreamingDisplay steps={steps} progress={progress} />}
          {state === "error" && (
            <div className="flex flex-col items-center justify-center h-full min-h-[400px] text-center px-6">
              <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-2xl border-2 border-destructive/30 bg-destructive/10">
                <AlertTriangle className="h-8 w-8 text-destructive" />
              </div>
              <h3 className="text-lg font-semibold text-foreground mb-2">Something went wrong</h3>
              <p className="text-sm text-muted-foreground max-w-sm mb-6">{error || "An unexpected error occurred. Please try again."}</p>
              <Button variant="secondary" size="sm" onClick={() => { reset(); }}>
                Try Again
              </Button>
            </div>
          )}
          {state === "complete" && result && (
            <div className="space-y-4">
              <ResultsSections result={result} />
              <ActionBar result={result} onReset={handleReset} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
