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
  const { state, steps, result, resultSource, progress, error, analyze, reset, loadResult, savedInput, setSavedInput } = useAnalysis();
  const { save } = useSavedAnalyses();
  const { toast } = useToast();
  const resultsRef = useRef<HTMLDivElement>(null);
  const pageTopRef = useRef<HTMLDivElement>(null);
  const location = useLocation();
  const didAutoSaveRef = useRef(false);

  const scrollContainer = () => document.querySelector<HTMLElement>("[data-scroll-container]") ?? document.documentElement;

  // When navigating to Prepare, scroll to absolute top (instant; repeat after 100ms for late layout)
  useEffect(() => {
    const scrollToTop = () => {
      const el = scrollContainer();
      if (el === document.documentElement) {
        window.scrollTo(0, 0);
        document.documentElement.scrollTop = 0;
        document.body.scrollTop = 0;
      } else {
        el.scrollTop = 0;
      }
      pageTopRef.current?.scrollIntoView({ block: "start", behavior: "auto" });
    };
    let timeoutId: ReturnType<typeof setTimeout> | undefined;
    const rafId = requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        scrollToTop();
        timeoutId = setTimeout(scrollToTop, 100);
      });
    });
    return () => {
      cancelAnimationFrame(rafId);
      if (timeoutId != null) clearTimeout(timeoutId);
    };
  }, [location.pathname]);

  // On full page refresh, clear both left (input) and right (results) so the page is fully reset
  useEffect(() => {
    const nav = window.performance.getEntriesByType?.("navigation")[0] as PerformanceNavigationTiming | undefined;
    if (nav?.type === "reload") {
      setSavedInput("");
      reset();
    }
  }, [setSavedInput, reset]);

  // Load from history navigation
  useEffect(() => {
    const loaded = (location.state as { loaded?: SavedAnalysis })?.loaded;
    if (loaded) {
      setSavedInput(loaded.jobDescription);
      loadResult(loaded.results);
      window.history.replaceState({}, document.title);
    }
  }, [location.state, setSavedInput, loadResult]);

  // When opening a result from history, scroll to top of results panel after paint
  useEffect(() => {
    if (resultSource !== "history" || !resultsRef.current) return;
    const el = resultsRef.current;
    const container = scrollContainer();
    const id = requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        const rect = el.getBoundingClientRect();
        const top = rect.top + (container === document.documentElement ? window.scrollY : container.scrollTop);
        const target = Math.max(0, top - 24);
        if (container === document.documentElement) {
          window.scrollTo({ top: target, behavior: "smooth" });
        } else {
          container.scrollTo({ top: target, behavior: "smooth" });
        }
      });
    });
    return () => cancelAnimationFrame(id);
  }, [resultSource]);

  // Auto-save to history only when a fresh analysis completes (never when result came from history)
  useEffect(() => {
    if (state !== "complete" || resultSource !== "streaming" || !result || !savedInput.trim()) return;
    if (didAutoSaveRef.current) return;
    save(savedInput, result);
    didAutoSaveRef.current = true;
    toast({ title: "Analysis saved", description: "View it anytime from History." });
  }, [state, resultSource, result, savedInput, save, toast]);

  // When a fresh analysis completes, scroll so the top of the results panel is visible
  useEffect(() => {
    if (state !== "complete" || resultSource !== "streaming" || !resultsRef.current) return;
    const el = resultsRef.current;
    const container = scrollContainer();
    const id = requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        const rect = el.getBoundingClientRect();
        const top = rect.top + (container === document.documentElement ? window.scrollY : container.scrollTop);
        const target = Math.max(0, top - 24);
        if (container === document.documentElement) {
          window.scrollTo({ top: target, behavior: "smooth" });
        } else {
          container.scrollTo({ top: target, behavior: "smooth" });
        }
      });
    });
    return () => cancelAnimationFrame(id);
  }, [state, resultSource, result]);

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
        reset();
        setSavedInput("");
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [reset, setSavedInput]);

  const handleAnalyze = (jobDescription: string) => {
    didAutoSaveRef.current = false;
    analyze(jobDescription);
  };

  const handleReset = () => {
    didAutoSaveRef.current = false;
    reset();
    setSavedInput("");
  };

  return (
    <div ref={pageTopRef} className="container mx-auto px-4 sm:px-6 py-8">
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
              <ResultsSections result={result} sectionsDefaultOpen={false} />
              <ActionBar result={result} onReset={handleReset} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
