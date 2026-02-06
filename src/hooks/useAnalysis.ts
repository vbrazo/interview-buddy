import { useState, useCallback, useRef, useEffect } from "react";
import { StreamingStep, AnalysisResult } from "@/types/analysis";
import { MOCK_STEPS, MOCK_RESULT } from "@/data/mockData";

export type AnalysisState = "idle" | "streaming" | "complete";

export function useAnalysis() {
  const [state, setState] = useState<AnalysisState>("idle");
  const [steps, setSteps] = useState<StreamingStep[]>([]);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [progress, setProgress] = useState(0);
  const abortRef = useRef(false);

  const analyze = useCallback((jobDescription: string) => {
    abortRef.current = false;
    setState("streaming");
    setResult(null);
    setProgress(0);
    setSteps(MOCK_STEPS.map((s) => ({ ...s, status: "pending" as const })));

    const totalSteps = MOCK_STEPS.length;
    let currentStep = 0;

    const processStep = () => {
      if (abortRef.current) return;
      if (currentStep >= totalSteps) {
        setState("complete");
        setResult(MOCK_RESULT);
        setProgress(100);
        return;
      }

      setSteps((prev) =>
        prev.map((s, i) => ({
          ...s,
          status: i < currentStep ? "done" : i === currentStep ? "active" : "pending",
        }))
      );
      setProgress(Math.round(((currentStep + 1) / totalSteps) * 100));

      currentStep++;
      setTimeout(processStep, 800 + Math.random() * 600);
    };

    setTimeout(processStep, 400);
  }, []);

  const reset = useCallback(() => {
    abortRef.current = true;
    setState("idle");
    setSteps([]);
    setResult(null);
    setProgress(0);
  }, []);

  // Auto-save to localStorage
  const [savedInput, setSavedInput] = useState(() => {
    try { return localStorage.getItem("interview-prep-input") || ""; } catch { return ""; }
  });

  useEffect(() => {
    try { localStorage.setItem("interview-prep-input", savedInput); } catch {}
  }, [savedInput]);

  return { state, steps, result, progress, analyze, reset, savedInput, setSavedInput };
}
