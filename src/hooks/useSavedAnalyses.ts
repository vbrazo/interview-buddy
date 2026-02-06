import { useState, useCallback } from "react";
import { SavedAnalysis, AnalysisResult } from "@/types/analysis";

const STORAGE_KEY = "interview-prep-saved";

function loadAll(): SavedAnalysis[] {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
  } catch {
    return [];
  }
}

function persistAll(items: SavedAnalysis[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
}

export function useSavedAnalyses() {
  const [items, setItems] = useState<SavedAnalysis[]>(loadAll);

  const save = useCallback((jobDescription: string, results: AnalysisResult) => {
    const entry: SavedAnalysis = {
      id: crypto.randomUUID(),
      jobDescription,
      companyName: results.companyName,
      roleTitle: `${results.companyName} Analysis`,
      results,
      savedAt: Date.now(),
    };
    setItems((prev) => {
      const next = [entry, ...prev];
      persistAll(next);
      return next;
    });
    return entry.id;
  }, []);

  const remove = useCallback((id: string) => {
    setItems((prev) => {
      const next = prev.filter((i) => i.id !== id);
      persistAll(next);
      return next;
    });
  }, []);

  const refresh = useCallback(() => {
    setItems(loadAll());
  }, []);

  return { items, save, remove, refresh };
}
