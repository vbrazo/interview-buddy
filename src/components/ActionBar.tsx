import { Download, Copy, RotateCcw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { AnalysisResult } from "@/types/analysis";

interface ActionBarProps {
  result: AnalysisResult;
  onReset: () => void;
}

function resultToMarkdown(r: AnalysisResult): string {
  let md = `# Interview Prep: ${r.companyName}\n\n`;
  md += `## Company Intelligence\n`;
  r.companyIntelligence.forEach((i) => {
    md += `- ${i.text}${i.citation ? ` [${i.citation.domain}](${i.citation.url})` : ""}\n`;
  });
  md += `\n## Technology Deep Dive\n`;
  r.techAnalysis.forEach((t) => {
    md += `### ${t.name}\n`;
    t.points.forEach((p) => {
      md += `- ${p.text}${p.citation ? ` [${p.citation.domain}](${p.citation.url})` : ""}\n`;
    });
  });
  md += `\n## Interview Focus Areas\n`;
  r.interviewFocus.forEach((f) => {
    md += `- **[${f.difficulty}]** ${f.topic}: ${f.description}\n`;
  });
  md += `\n## Practice Questions\n`;
  r.practiceQuestions.forEach((q, i) => {
    md += `${i + 1}. **[${q.difficulty}] [${q.category}]** ${q.question}\n   - *Hint:* ${q.hint}\n`;
  });
  md += `\n## Resources\n`;
  r.resources.forEach((re) => {
    md += `- [${re.title}](${re.url}) — ${re.description}\n`;
  });
  return md;
}

export function ActionBar({ result, onReset }: ActionBarProps) {
  const { toast } = useToast();

  const handleCopy = async () => {
    const md = resultToMarkdown(result);
    await navigator.clipboard.writeText(md);
    toast({ title: "Copied to clipboard!", description: "Results copied as Markdown." });
  };

  const handleExport = () => {
    const md = resultToMarkdown(result);
    const blob = new Blob([md], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `interview-prep-${result.companyName.toLowerCase().replace(/\s+/g, "-")}.md`;
    a.click();
    URL.revokeObjectURL(url);
    toast({ title: "Exported!", description: "Markdown file downloaded." });
  };

  return (
    <div className="flex flex-wrap items-center gap-3 rounded-xl border border-border/50 bg-card p-4 shadow-card opacity-0 animate-fade-in-up" style={{ animationDelay: "600ms", animationFillMode: "forwards" }}>
      <Button variant="secondary" size="sm" onClick={handleExport} className="gap-2 text-xs">
        <Download className="h-3.5 w-3.5" />
        Export as Markdown
      </Button>
      <Button variant="secondary" size="sm" onClick={handleCopy} className="gap-2 text-xs">
        <Copy className="h-3.5 w-3.5" />
        Copy to Clipboard
      </Button>
      <Button variant="outline" size="sm" onClick={onReset} className="gap-2 text-xs ml-auto">
        <RotateCcw className="h-3.5 w-3.5" />
        Start New Analysis
      </Button>
    </div>
  );
}
