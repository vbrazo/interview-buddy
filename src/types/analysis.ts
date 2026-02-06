export interface StreamingStep {
  emoji: string;
  text: string;
  status: "pending" | "active" | "done";
}

export interface Citation {
  title: string;
  domain: string;
  url: string;
}

export interface CompanyInsight {
  text: string;
  citation?: Citation;
}

export interface TechAnalysis {
  name: string;
  points: { text: string; citation?: Citation }[];
}

export interface InterviewFocus {
  topic: string;
  difficulty: "Easy" | "Medium" | "Hard";
  description: string;
}

export interface PracticeQuestion {
  question: string;
  difficulty: "Easy" | "Medium" | "Hard";
  category: string;
  hint: string;
}

export interface Resource {
  title: string;
  domain: string;
  url: string;
  description: string;
}

export interface AnalysisResult {
  companyName: string;
  companyIntelligence: CompanyInsight[];
  techAnalysis: TechAnalysis[];
  interviewFocus: InterviewFocus[];
  practiceQuestions: PracticeQuestion[];
  resources: Resource[];
}

export interface SavedAnalysis {
  id: string;
  jobDescription: string;
  companyName: string;
  roleTitle: string;
  results: AnalysisResult;
  savedAt: number;
}
