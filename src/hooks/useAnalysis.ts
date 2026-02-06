import { useState, useCallback, useRef, useEffect } from "react";
import { StreamingStep, AnalysisResult } from "@/types/analysis";

export type AnalysisState = "idle" | "streaming" | "complete" | "error";

const BACKEND_URL =
  import.meta.env.VITE_BACKEND_URL ?? "";

export function useAnalysis() {
  const [state, setState] = useState<AnalysisState>("idle");
  const [steps, setSteps] = useState<StreamingStep[]>([]);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const analyze = useCallback(async (jobDescription: string) => {
    // Abort any running request
    abortControllerRef.current?.abort();
    const controller = new AbortController();
    abortControllerRef.current = controller;

    setState("streaming");
    setResult(null);
    setProgress(0);
    setError(null);
    setSteps([]);

    try {
      const resp = await fetch(`${BACKEND_URL}/api/prepare`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ jobDescription }),
        signal: controller.signal,
      });

      if (!resp.ok) {
        throw new Error(`Server error: ${resp.status}`);
      }

      const reader = resp.body?.getReader();
      if (!reader) throw new Error("No response stream");

      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        // Process complete SSE lines
        const lines = buffer.split("\n");
        buffer = lines.pop() ?? ""; // keep incomplete line in buffer

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed.startsWith("data: ")) continue;

          try {
            const payload = JSON.parse(trimmed.slice(6));
            handleSSEEvent(payload);
          } catch {
            // skip malformed lines
          }
        }
      }

      // Process any remaining data in buffer
      if (buffer.trim().startsWith("data: ")) {
        try {
          const payload = JSON.parse(buffer.trim().slice(6));
          handleSSEEvent(payload);
        } catch {
          // ignore
        }
      }
    } catch (err: unknown) {
      if (err instanceof DOMException && err.name === "AbortError") return;
      const message =
        err instanceof Error ? err.message : "An unexpected error occurred";
      setError(message);
      setState("error");
    }

    function handleSSEEvent(payload: Record<string, unknown>) {
      switch (payload.type) {
        case "steps": {
          const stepsData = payload.steps as { emoji: string; text: string }[];
          setSteps(
            stepsData.map((s) => ({ ...s, status: "pending" as const }))
          );
          break;
        }
        case "progress": {
          const idx = payload.stepIndex as number;
          const status = payload.status as "active" | "done";
          const prog = payload.progress as number;
          setProgress(prog);
          setSteps((prev) =>
            prev.map((s, i) => ({
              ...s,
              status:
                i < idx ? "done" : i === idx ? status : s.status,
            }))
          );
          break;
        }
        case "result": {
          setResult(payload.data as AnalysisResult);
          setProgress(100);
          setState("complete");
          break;
        }
        case "error": {
          setError(payload.message as string);
          setState("error");
          break;
        }
      }
    }
  }, []);

  const loadResult = useCallback((r: AnalysisResult) => {
    abortControllerRef.current?.abort();
    setState("complete");
    setSteps([]);
    setResult(r);
    setProgress(100);
    setError(null);
  }, []);

  const reset = useCallback(() => {
    abortControllerRef.current?.abort();
    setState("idle");
    setSteps([]);
    setResult(null);
    setProgress(0);
    setError(null);
  }, []);

  // Auto-save to localStorage
  const [savedInput, setSavedInput] = useState(() => {
    try {
      return localStorage.getItem("interview-prep-input") || "";
    } catch {
      return "";
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem("interview-prep-input", savedInput);
    } catch {
      // ignore
    }
  }, [savedInput]);

  return {
    state,
    steps,
    result,
    progress,
    error,
    analyze,
    reset,
    loadResult,
    savedInput,
    setSavedInput,
  };
}
