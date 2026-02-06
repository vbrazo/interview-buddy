import { useEffect, useRef } from "react";
import { Header } from "@/components/Header";
import { JobInput } from "@/components/JobInput";
import { EmptyState, StreamingDisplay } from "@/components/StreamingDisplay";
import { ResultsSections } from "@/components/ResultsSections";
import { ActionBar } from "@/components/ActionBar";
import { useAnalysis } from "@/hooks/useAnalysis";

const Index = () => {
  const { state, steps, result, progress, analyze, reset, savedInput, setSavedInput } = useAnalysis();
  const resultsRef = useRef<HTMLDivElement>(null);

  // Scroll to results on complete
  useEffect(() => {
    if (state === "complete" && resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [state]);

  // Keyboard shortcut: Cmd+K to clear
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

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container mx-auto px-4 sm:px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
          {/* Left Column — Input */}
          <div className={`lg:col-span-2 ${state === "complete" ? "lg:sticky lg:top-24 lg:self-start" : ""}`}>
            <div className="rounded-xl border border-border/50 bg-card p-5 shadow-card">
              <JobInput
                value={savedInput}
                onChange={setSavedInput}
                onAnalyze={analyze}
                isLoading={state === "streaming"}
              />
            </div>
          </div>

          {/* Right Column — Results */}
          <div className="lg:col-span-3" ref={resultsRef}>
            {state === "idle" && <EmptyState />}
            {state === "streaming" && <StreamingDisplay steps={steps} progress={progress} />}
            {state === "complete" && result && (
              <div className="space-y-4">
                <ResultsSections result={result} />
                <ActionBar result={result} onReset={() => { reset(); setSavedInput(""); }} />
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
