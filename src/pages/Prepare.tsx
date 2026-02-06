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
import { Save } from "lucide-react";
import { SavedAnalysis } from "@/types/analysis";

export default function Prepare() {
  const { state, steps, result, progress, analyze, reset, loadResult, savedInput, setSavedInput } = useAnalysis();
  const { save } = useSavedAnalyses();
  const { toast } = useToast();
  const resultsRef = useRef<HTMLDivElement>(null);
  const location = useLocation();

  // Load from history navigation
  useEffect(() => {
    const loaded = (location.state as { loaded?: SavedAnalysis })?.loaded;
    if (loaded) {
      setSavedInput(loaded.jobDescription);
      loadResult(loaded.results);
      // Clear navigation state
      window.history.replaceState({}, document.title);
    }
  }, [location.state, setSavedInput, loadResult]);

  useEffect(() => {
    if (state === "complete" && resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [state]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        reset();
        setSavedInput("");
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [reset, setSavedInput]);

  const handleSave = () => {
    if (!result) return;
    save(savedInput, result);
    toast({ title: "Analysis saved!", description: "View it anytime from your History." });
  };

  return (
    <div className="container mx-auto px-4 sm:px-6 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
        <div className={`lg:col-span-2 ${state === "complete" ? "lg:sticky lg:top-20 lg:self-start" : ""}`}>
          <div className="rounded-xl border border-border/50 bg-card p-5 shadow-card">
            <JobInput
              value={savedInput}
              onChange={setSavedInput}
              onAnalyze={analyze}
              isLoading={state === "streaming"}
            />
          </div>
        </div>

        <div className="lg:col-span-3" ref={resultsRef}>
          {state === "idle" && <EmptyState />}
          {state === "streaming" && <StreamingDisplay steps={steps} progress={progress} />}
          {state === "complete" && result && (
            <div className="space-y-4">
              <ResultsSections result={result} />
              <div className="flex flex-wrap items-center gap-3">
                <Button variant="secondary" size="sm" onClick={handleSave} className="gap-2 text-xs">
                  <Save className="h-3.5 w-3.5" />
                  Save This Analysis
                </Button>
              </div>
              <ActionBar result={result} onReset={() => { reset(); setSavedInput(""); }} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
