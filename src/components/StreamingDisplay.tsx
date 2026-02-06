import { Search } from "lucide-react";
import { StreamingStep } from "@/types/analysis";
import { Progress } from "@/components/ui/progress";

interface StreamingDisplayProps {
  steps: StreamingStep[];
  progress: number;
}

export function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center h-full min-h-[400px] text-center px-6">
      <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-2xl border-2 border-dashed border-border">
        <Search className="h-8 w-8 text-muted-foreground/50" />
      </div>
      <h3 className="text-lg font-semibold text-foreground mb-2">
        Paste a job description to get started
      </h3>
      <p className="text-sm text-muted-foreground max-w-sm">
        Get company insights, tech analysis, and practice questions tailored to your target role
      </p>
    </div>
  );
}

export function StreamingDisplay({ steps, progress }: StreamingDisplayProps) {
  return (
    <div className="flex flex-col items-center justify-center h-full min-h-[400px] px-6">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center mb-8">
          <div className="inline-flex h-12 w-12 items-center justify-center rounded-xl gradient-primary mb-4">
            <div className="h-5 w-5 rounded-full border-2 border-primary-foreground border-t-transparent animate-spin" />
          </div>
          <h3 className="text-lg font-semibold text-foreground">Analyzing...</h3>
        </div>

        <Progress value={progress} className="h-1.5 bg-secondary" />
        <p className="text-xs text-muted-foreground text-center font-mono">{progress}%</p>

        <div className="space-y-3">
          {steps.map((step, i) => (
            <div
              key={i}
              className={`flex items-center gap-3 rounded-lg px-4 py-2.5 text-sm transition-all duration-300 ${
                step.status === "active"
                  ? "bg-primary/10 text-foreground border border-primary/20"
                  : step.status === "done"
                  ? "bg-secondary/50 text-muted-foreground"
                  : "text-muted-foreground/40"
              }`}
              style={{
                opacity: step.status === "pending" ? 0.4 : 1,
                animation: step.status === "active" ? "slide-up 0.3s ease-out" : undefined,
              }}
            >
              <span className="text-base">{step.emoji}</span>
              <span>{step.text}</span>
              {step.status === "active" && (
                <div className="ml-auto h-1.5 w-1.5 rounded-full bg-accent animate-pulse-glow" />
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
