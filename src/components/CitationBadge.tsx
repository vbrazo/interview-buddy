import { Link2 } from "lucide-react";
import { Citation } from "@/types/analysis";

interface CitationBadgeProps {
  citation: Citation;
}

export function CitationBadge({ citation }: CitationBadgeProps) {
  return (
    <a
      href={citation.url}
      target="_blank"
      rel="noopener noreferrer"
      className="citation-badge hover:bg-primary/10 transition-colors cursor-pointer"
    >
      <Link2 className="h-3 w-3" />
      <span>{citation.domain}</span>
    </a>
  );
}
