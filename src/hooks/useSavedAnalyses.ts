import { useState, useCallback, useEffect } from "react";
import { SavedAnalysis, AnalysisResult } from "@/types/analysis";

const STORAGE_KEY = "interview-prep-saved";
const API_BASE = import.meta.env.VITE_BACKEND_URL ?? "";

function loadFromStorage(): SavedAnalysis[] {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
  } catch {
    return [];
  }
}

function persistToStorage(items: SavedAnalysis[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
}

export function useSavedAnalyses() {
  const [items, setItems] = useState<SavedAnalysis[]>([]);
  const [loading, setLoading] = useState(true);
  const [useApi, setUseApi] = useState<boolean | null>(null);

  const fetchFromApi = useCallback(async () => {
    try {
      const resp = await fetch(`${API_BASE}/api/history`);
      if (resp.ok) {
        const data = await resp.json();
        setItems(Array.isArray(data) ? data : []);
        setUseApi(true);
        return true;
      }
    } catch {
      // API not available
    }
    setUseApi(false);
    setItems(loadFromStorage());
    return false;
  }, []);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetchFromApi().finally(() => {
      if (!cancelled) setLoading(false);
    });
    return () => {
      cancelled = true;
    };
  }, [fetchFromApi]);

  const refresh = useCallback(async () => {
    const fromApi = await fetchFromApi();
    if (!fromApi) setItems(loadFromStorage());
  }, [fetchFromApi]);

  const save = useCallback(
    async (jobDescription: string, results: AnalysisResult) => {
      const entry: SavedAnalysis = {
        id: crypto.randomUUID(),
        jobDescription,
        companyName: results.companyName,
        roleTitle: `${results.companyName} Analysis`,
        results,
        savedAt: Date.now(),
      };

      if (useApi !== false) {
        try {
          const resp = await fetch(`${API_BASE}/api/history`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              jobDescription,
              results,
            }),
          });
          if (resp.ok) {
            const created = await resp.json();
            setItems((prev) => [created, ...prev]);
            setUseApi(true);
            return created.id;
          }
        } catch {
          setUseApi(false);
        }
      }

      // Fallback: localStorage
      setItems((prev) => {
        const next = [entry, ...prev];
        persistToStorage(next);
        return next;
      });
      return entry.id;
    },
    [useApi]
  );

  const remove = useCallback(
    async (id: string) => {
      if (useApi !== false) {
        try {
          const resp = await fetch(`${API_BASE}/api/history/${id}`, {
            method: "DELETE",
          });
          if (resp.ok) {
            setItems((prev) => prev.filter((i) => i.id !== id));
            setUseApi(true);
            return;
          }
        } catch {
          setUseApi(false);
        }
      }

      setItems((prev) => {
        const next = prev.filter((i) => i.id !== id);
        persistToStorage(next);
        return next;
      });
    },
    [useApi]
  );

  return { items, save, remove, refresh, loading };
}
