import { Sparkles } from "lucide-react";

export function Header() {
  return (
    <header className="border-b border-border/50 bg-card/50 backdrop-blur-sm sticky top-0 z-50">
      <div className="container mx-auto flex items-center justify-between px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg gradient-primary">
            <Sparkles className="h-5 w-5 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-lg font-semibold tracking-tight text-foreground">
              Interview Prep Agent
            </h1>
            <p className="text-xs text-muted-foreground">
              AI-powered interview preparation with real-time research
            </p>
          </div>
        </div>
        <div className="hidden sm:flex items-center gap-1 rounded-full border border-border/50 bg-secondary px-3 py-1 text-xs text-muted-foreground">
          <span className="h-1.5 w-1.5 rounded-full bg-accent animate-pulse-glow" />
          Ready
        </div>
      </div>
    </header>
  );
}
