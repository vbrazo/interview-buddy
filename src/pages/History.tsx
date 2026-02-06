import { Link, useNavigate } from "react-router-dom";
import { ClipboardList, Trash2, Eye, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useSavedAnalyses } from "@/hooks/useSavedAnalyses";
import { useToast } from "@/hooks/use-toast";

export default function History() {
  const { items, remove } = useSavedAnalyses();
  const { toast } = useToast();
  const navigate = useNavigate();

  const handleDelete = (id: string) => {
    remove(id);
    toast({ title: "Deleted", description: "Analysis removed from history." });
  };

  if (items.length === 0) {
    return (
      <div className="container mx-auto px-6 py-20">
        <div className="flex flex-col items-center justify-center text-center">
          <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-2xl border-2 border-dashed border-border">
            <ClipboardList className="h-8 w-8 text-muted-foreground/50" />
          </div>
          <h2 className="text-lg font-semibold text-foreground mb-2">No saved analyses yet</h2>
          <p className="text-sm text-muted-foreground mb-6 max-w-sm">
            Analyze a job description and save it to build your interview prep history.
          </p>
          <Button asChild className="gradient-primary text-primary-foreground rounded-xl">
            <Link to="/prepare">
              Start your first analysis
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-6 py-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-foreground">Analysis History</h1>
        <p className="text-sm text-muted-foreground mt-1">{items.length} saved {items.length === 1 ? "analysis" : "analyses"}</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {items.map((item) => (
          <div
            key={item.id}
            className="rounded-xl border border-border/50 bg-card p-5 shadow-card hover:border-primary/20 hover:shadow-card-hover transition-all group"
          >
            <div className="flex items-start justify-between mb-3">
              <div>
                <h3 className="text-sm font-semibold text-foreground">{item.companyName}</h3>
                <p className="text-xs text-muted-foreground mt-0.5">
                  {new Date(item.savedAt).toLocaleDateString(undefined, {
                    month: "short",
                    day: "numeric",
                    year: "numeric",
                  })}
                </p>
              </div>
              <button
                onClick={() => handleDelete(item.id)}
                className="text-muted-foreground/50 hover:text-destructive transition-colors p-1"
                aria-label="Delete analysis"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
            <p className="text-xs text-muted-foreground leading-relaxed line-clamp-2 mb-4">
              {item.jobDescription.slice(0, 120)}...
            </p>
            <Button
              variant="secondary"
              size="sm"
              className="w-full gap-2 text-xs"
              onClick={() => navigate("/prepare", { state: { loaded: item } })}
            >
              <Eye className="h-3.5 w-3.5" />
              View Analysis
            </Button>
          </div>
        ))}
      </div>
    </div>
  );
}
