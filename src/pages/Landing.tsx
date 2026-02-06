import { Link } from "react-router-dom";
import { Building2, Code, Target, BookOpen, ArrowRight, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";

const FEATURES = [
  { icon: Building2, title: "Live Company Intelligence", description: "Real-time research on company news, culture, and products" },
  { icon: Code, title: "Tech Stack Analysis", description: "Deep dive into technologies with trends and interview topics" },
  { icon: Target, title: "Tailored Practice Questions", description: "Difficulty-rated questions specific to your target role" },
  { icon: BookOpen, title: "Citation-Backed Research", description: "Every insight backed by verifiable sources" },
];

const STEPS = [
  { step: "01", title: "Paste Job Description", description: "Drop in any job posting or role description" },
  { step: "02", title: "AI Analyzes in Real-Time", description: "Watch as the agent researches and generates insights" },
  { step: "03", title: "Get Your Prep Guide", description: "Comprehensive prep with questions, resources, and citations" },
];

export default function Landing() {
  return (
    <div>
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 gradient-primary opacity-[0.07]" />
        <div className="container mx-auto px-6 py-24 sm:py-32 relative">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            <div className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-4 py-1.5 text-xs text-primary font-medium">
              <Sparkles className="h-3.5 w-3.5" />
              AI-Powered Interview Preparation
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-foreground leading-[1.1]">
              Ace Your Next{" "}
              <span className="bg-gradient-to-r from-primary to-[hsl(258,90%,66%)] bg-clip-text text-transparent">
                Interview
              </span>
            </h1>
            <p className="text-lg text-muted-foreground max-w-xl mx-auto leading-relaxed">
              AI-powered prep with real-time company research, tech stack analysis, and tailored practice questions — all backed by citations.
            </p>
            <div className="flex items-center justify-center gap-4 pt-2">
              <Button asChild size="lg" className="gradient-primary text-primary-foreground rounded-xl h-12 px-8 text-sm font-medium hover:opacity-90">
                <Link to="/prepare">
                  Start Preparing
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg" className="rounded-xl h-12 px-8 text-sm">
                <Link to="/history">View History</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="container mx-auto px-6 py-20">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {FEATURES.map((f) => (
            <div
              key={f.title}
              className="rounded-xl border border-border/50 bg-card p-6 shadow-card hover:border-primary/20 hover:shadow-card-hover transition-all group"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 mb-4 group-hover:bg-primary/20 transition-colors">
                <f.icon className="h-5 w-5 text-primary" />
              </div>
              <h3 className="text-sm font-semibold text-foreground mb-1.5">{f.title}</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">{f.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="container mx-auto px-6 py-20">
        <h2 className="text-2xl font-bold text-foreground text-center mb-12">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-3xl mx-auto">
          {STEPS.map((s) => (
            <div key={s.step} className="text-center space-y-3">
              <div className="inline-flex h-12 w-12 items-center justify-center rounded-xl gradient-primary text-primary-foreground text-sm font-bold">
                {s.step}
              </div>
              <h3 className="text-sm font-semibold text-foreground">{s.title}</h3>
              <p className="text-xs text-muted-foreground leading-relaxed">{s.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="container mx-auto px-6 py-16">
        <div className="rounded-2xl border border-border/50 bg-card p-10 text-center shadow-card">
          <h2 className="text-xl font-bold text-foreground mb-3">Ready to prepare?</h2>
          <p className="text-sm text-muted-foreground mb-6">Paste a job description and get a comprehensive prep guide in seconds.</p>
          <Button asChild size="lg" className="gradient-primary text-primary-foreground rounded-xl h-12 px-8 text-sm font-medium hover:opacity-90">
            <Link to="/prepare">
              Get Started
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
}
