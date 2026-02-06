import { useState } from "react";
import { Building2, Code, Target, MessageCircle, BookOpen, ChevronDown, ChevronRight, Lightbulb } from "lucide-react";
import { AnalysisResult } from "@/types/analysis";
import { CitationBadge } from "@/components/CitationBadge";

export interface ResultsSectionsProps {
  result: AnalysisResult;
  /** When false, all sections start collapsed (e.g. when opening from history). */
  sectionsDefaultOpen?: boolean;
}

function Section({
  icon: Icon,
  title,
  defaultOpen = false,
  delay = 0,
  children,
}: {
  icon: React.ComponentType<{ className?: string }>;
  title: string;
  defaultOpen?: boolean;
  delay?: number;
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div
      className="rounded-xl border border-border/50 bg-card shadow-card overflow-hidden opacity-0 animate-fade-in-up"
      style={{ animationDelay: `${delay}ms`, animationFillMode: "forwards" }}
    >
      <button
        onClick={() => setOpen(!open)}
        className="flex w-full items-center gap-3 px-5 py-4 text-left hover:bg-secondary/30 transition-colors"
      >
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary/10">
          <Icon className="h-4 w-4 text-primary" />
        </div>
        <h3 className="flex-1 text-sm font-semibold text-foreground">{title}</h3>
        {open ? (
          <ChevronDown className="h-4 w-4 text-muted-foreground" />
        ) : (
          <ChevronRight className="h-4 w-4 text-muted-foreground" />
        )}
      </button>
      {open && (
        <div className="border-t border-border/30 px-5 py-4 animate-fade-in">
          {children}
        </div>
      )}
    </div>
  );
}

export function ResultsSections({ result, sectionsDefaultOpen = true }: ResultsSectionsProps) {
  return (
    <div className="space-y-4">
      <Section icon={Building2} title={`Company Intelligence — ${result.companyName}`} defaultOpen={sectionsDefaultOpen} delay={100}>
        <div className="space-y-3">
          {result.companyIntelligence.map((insight, i) => (
            <div key={i} className="flex flex-col gap-1.5">
              <p className="text-sm text-foreground/90 leading-relaxed">{insight.text}</p>
              {insight.citation && <CitationBadge citation={insight.citation} />}
            </div>
          ))}
        </div>
      </Section>

      <Section icon={Code} title="Technology Deep Dive" defaultOpen={false} delay={200}>
        <div className="space-y-6">
          {result.techAnalysis.map((tech) => (
            <div key={tech.name}>
              <h4 className="text-sm font-semibold text-accent mb-3 font-mono">{tech.name}</h4>
              <div className="space-y-2.5 pl-3 border-l-2 border-accent/20">
                {tech.points.map((point, j) => (
                  <div key={j} className="flex flex-col gap-1">
                    <p className="text-sm text-foreground/85 leading-relaxed">{point.text}</p>
                    {point.citation && <CitationBadge citation={point.citation} />}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </Section>

      <Section icon={Target} title="Interview Focus Areas" defaultOpen={false} delay={300}>
        <div className="space-y-3">
          {result.interviewFocus.map((focus, i) => (
            <div key={i} className="flex items-start gap-3 rounded-lg bg-secondary/30 px-4 py-3">
              <span className={`shrink-0 mt-0.5 ${
                focus.difficulty === "Hard" ? "difficulty-hard" :
                focus.difficulty === "Medium" ? "difficulty-medium" : "difficulty-easy"
              }`}>
                {focus.difficulty}
              </span>
              <div>
                <p className="text-sm font-medium text-foreground">{focus.topic}</p>
                <p className="text-xs text-muted-foreground mt-0.5">{focus.description}</p>
              </div>
            </div>
          ))}
        </div>
      </Section>

      <Section icon={MessageCircle} title="Practice Questions" defaultOpen={false} delay={400}>
        <div className="space-y-3">
          {result.practiceQuestions.map((q, i) => (
            <QuestionCard key={i} question={q} index={i + 1} />
          ))}
        </div>
      </Section>

      <Section icon={BookOpen} title="Key Resources" defaultOpen={false} delay={500}>
        <div className="grid gap-3 sm:grid-cols-2">
          {result.resources.map((resource, i) => (
            <a
              key={i}
              href={resource.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex flex-col gap-1 rounded-lg border border-border/50 bg-secondary/30 p-3 hover:border-primary/30 hover:bg-secondary/60 transition-all group"
            >
              <div className="flex items-center gap-2">
                <div className="h-4 w-4 rounded bg-accent/20 flex items-center justify-center">
                  <span className="text-[8px] text-accent font-bold">{resource.domain.charAt(0).toUpperCase()}</span>
                </div>
                <span className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">{resource.title}</span>
              </div>
              <p className="text-xs text-muted-foreground">{resource.description}</p>
              <span className="text-[10px] text-muted-foreground/60 font-mono">{resource.domain}</span>
            </a>
          ))}
        </div>
      </Section>
    </div>
  );
}

function QuestionCard({ question: q, index }: { question: AnalysisResult["practiceQuestions"][0]; index: number }) {
  const [showHint, setShowHint] = useState(false);

  return (
    <div className="rounded-lg border border-border/50 bg-secondary/20 p-4">
      <div className="flex items-start gap-3">
        <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-md bg-primary/10 text-xs font-mono text-primary">
          {index}
        </span>
        <div className="flex-1 space-y-2">
          <p className="text-sm text-foreground leading-relaxed">{q.question}</p>
          <div className="flex items-center gap-2 flex-wrap">
            <span className={
              q.difficulty === "Hard" ? "difficulty-hard" :
              q.difficulty === "Medium" ? "difficulty-medium" : "difficulty-easy"
            }>
              {q.difficulty}
            </span>
            <span className="category-tag">{q.category}</span>
          </div>
          <button
            onClick={() => setShowHint(!showHint)}
            className="flex items-center gap-1 text-xs text-accent hover:text-accent/80 transition-colors mt-1"
          >
            <Lightbulb className="h-3 w-3" />
            {showHint ? "Hide hint" : "Show hint"}
          </button>
          {showHint && (
            <p className="text-xs text-muted-foreground bg-accent/5 rounded-md px-3 py-2 border border-accent/10 animate-fade-in">
              {q.hint}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
