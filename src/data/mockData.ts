import { AnalysisResult, StreamingStep } from "@/types/analysis";

export const MOCK_STEPS: Omit<StreamingStep, "status">[] = [
  { emoji: "⏳", text: "Extracting job details..." },
  { emoji: "🔍", text: "Researching Stripe..." },
  { emoji: "📊", text: "Analyzing tech stack..." },
  { emoji: "💡", text: "Generating interview questions..." },
  { emoji: "✅", text: "Complete!" },
];

export const MOCK_RESULT: AnalysisResult = {
  companyName: "Stripe",
  companyIntelligence: [
    {
      text: "Stripe is a global financial technology company that builds economic infrastructure for the internet, processing hundreds of billions of dollars annually for millions of businesses worldwide.",
      citation: { title: "About Stripe", domain: "stripe.com", url: "https://stripe.com/about" },
    },
    {
      text: "Stripe launched Stripe Billing v3 with usage-based pricing support and improved subscription management capabilities in late 2024.",
      citation: { title: "Stripe Billing v3", domain: "stripe.com/blog", url: "https://stripe.com/blog" },
    },
    {
      text: "Q4 2024 valuation reached $65B after a secondary share sale, making it one of the most valuable private tech companies globally.",
      citation: { title: "Stripe Valuation", domain: "techcrunch.com", url: "https://techcrunch.com" },
    },
    {
      text: "Stripe expanded its AI-powered fraud detection suite, Radar, with new machine learning models trained on data from across the Stripe network.",
      citation: { title: "Stripe Radar ML", domain: "stripe.com/radar", url: "https://stripe.com/radar" },
    },
    {
      text: "Engineering culture emphasizes writing quality, code review rigor, and incremental delivery. Known for high hiring bar and strong internal documentation practices.",
    },
  ],
  techAnalysis: [
    {
      name: "Python",
      points: [
        { text: "Stripe uses Python extensively for backend API services, with a strong emphasis on type annotations and mypy for static analysis.", citation: { title: "Stripe Engineering Blog", domain: "stripe.com/blog", url: "https://stripe.com/blog/python" } },
        { text: "Focus areas: async/await patterns with asyncio, advanced decorator patterns, context managers, and comprehensive testing with pytest.", citation: { title: "Python Best Practices", domain: "realpython.com", url: "https://realpython.com" } },
        { text: "Common gotcha: Understanding the GIL and when to use multiprocessing vs threading vs asyncio for concurrent workloads." },
      ],
    },
    {
      name: "React",
      points: [
        { text: "Powers the Stripe Dashboard — one of the most complex React applications in production. Heavy use of hooks, context, and performance optimization.", citation: { title: "Stripe Dashboard Stack", domain: "stackshare.io", url: "https://stackshare.io/stripe" } },
        { text: "Key topics: React.memo, useMemo, useCallback for render optimization, Suspense for data fetching, and component composition patterns." },
        { text: "Accessibility is a first-class concern — expect questions about ARIA attributes, keyboard navigation, and screen reader compatibility.", citation: { title: "Stripe Accessibility", domain: "stripe.com/blog", url: "https://stripe.com/blog/accessibility" } },
      ],
    },
    {
      name: "Distributed Systems",
      points: [
        { text: "Stripe processes payments at massive scale requiring eventual consistency, idempotency, and robust failure handling across distributed services.", citation: { title: "Stripe Idempotency", domain: "stripe.com/blog", url: "https://stripe.com/blog/idempotency-keys" } },
        { text: "Key concepts: CAP theorem trade-offs, distributed consensus (Raft/Paxos), event sourcing, and saga patterns for distributed transactions." },
        { text: "Understanding rate limiting, circuit breakers, and backpressure mechanisms is critical for Stripe's scale." },
      ],
    },
  ],
  interviewFocus: [
    { topic: "System Design at Scale", difficulty: "Hard", description: "Design payment processing systems, rate limiters, or distributed caches" },
    { topic: "API Design & REST Principles", difficulty: "Medium", description: "Stripe is known for world-class API design — expect questions on versioning, error handling, and idempotency" },
    { topic: "Data Modeling & Storage", difficulty: "Medium", description: "Schema design for financial data, ACID compliance, and choosing appropriate storage solutions" },
    { topic: "Concurrency & Async Programming", difficulty: "Hard", description: "Deep knowledge of async patterns in Python and concurrent state management in React" },
    { topic: "Testing & Reliability", difficulty: "Medium", description: "Testing strategies for financial systems: unit, integration, contract, and chaos testing" },
    { topic: "Behavioral & Leadership", difficulty: "Easy", description: "Stripe values clear communication, ownership, and user empathy — prepare STAR-format stories" },
  ],
  practiceQuestions: [
    { question: "Design a rate limiting system for API requests that supports multiple tiers and burst allowances.", difficulty: "Hard", category: "System Design", hint: "Consider token bucket vs sliding window algorithms. Think about distributed rate limiting across multiple servers." },
    { question: "Explain async/await vs threading in Python. When would you choose one over the other?", difficulty: "Medium", category: "Python", hint: "Discuss the GIL, I/O-bound vs CPU-bound tasks, and the event loop architecture." },
    { question: "Tell me about a time you improved system reliability or reduced incidents.", difficulty: "Medium", category: "Behavioral", hint: "Use STAR format. Focus on measurable impact — reduced p99 latency, fewer incidents, improved uptime percentage." },
    { question: "How would you design an idempotent payment processing API?", difficulty: "Hard", category: "System Design", hint: "Think about idempotency keys, exactly-once semantics, and handling network partitions during payment flows." },
    { question: "Optimize a React dashboard that renders 10,000+ rows of transaction data.", difficulty: "Medium", category: "React", hint: "Consider virtualization (react-window), pagination, memo strategies, and Web Workers for data processing." },
    { question: "Describe the CAP theorem and how it applies to a payment system.", difficulty: "Hard", category: "Distributed Systems", hint: "Payments typically need CP (consistency + partition tolerance). Discuss trade-offs and how eventual consistency fits." },
    { question: "How do you ensure a REST API is backward compatible when adding new features?", difficulty: "Medium", category: "API Design", hint: "Discuss versioning strategies, additive changes, deprecation policies, and Stripe's approach to API evolution." },
    { question: "Write a Python decorator that retries a function with exponential backoff.", difficulty: "Easy", category: "Python", hint: "Use functools.wraps, accept max_retries and base_delay params, add jitter to prevent thundering herd." },
    { question: "How would you implement a feature flag system for gradual rollouts?", difficulty: "Medium", category: "System Design", hint: "Consider user segmentation, percentage-based rollouts, kill switches, and consistent hashing for sticky assignments." },
    { question: "What accessibility considerations are critical for a payment form?", difficulty: "Easy", category: "React", hint: "Focus on ARIA labels, keyboard navigation, error announcements, color contrast, and screen reader testing." },
  ],
  resources: [
    { title: "Stripe Engineering Blog", domain: "stripe.com", url: "https://stripe.com/blog/engineering", description: "Technical deep dives from Stripe's engineering team" },
    { title: "Designing Data-Intensive Applications", domain: "dataintensive.net", url: "https://dataintensive.net", description: "Essential reading for distributed systems interviews" },
    { title: "System Design Interview by Alex Xu", domain: "bytebytego.com", url: "https://bytebytego.com", description: "Comprehensive system design preparation guide" },
    { title: "Python Type Checking Guide", domain: "mypy.readthedocs.io", url: "https://mypy.readthedocs.io", description: "Master Python type hints and mypy for Stripe's codebase" },
    { title: "React Performance Patterns", domain: "react.dev", url: "https://react.dev/reference/react", description: "Official React docs on performance optimization" },
  ],
};

export const EXAMPLE_JOB_DESCRIPTIONS = [
  {
    label: "Software Engineer at Stripe",
    text: `Senior Software Engineer at Stripe

We're looking for engineers with 5+ years of experience in Python, React, and distributed systems to join our Payments Infrastructure team.

Responsibilities:
- Design and build scalable payment processing systems
- Develop APIs used by millions of businesses worldwide
- Collaborate with cross-functional teams on product features
- Improve system reliability and performance

Requirements:
- 5+ years of software engineering experience
- Strong proficiency in Python and/or Ruby
- Experience with React or similar frontend frameworks
- Understanding of distributed systems concepts
- Experience with databases (PostgreSQL, Redis)
- Excellent communication skills`,
  },
  {
    label: "Frontend at Vercel",
    text: `Frontend Engineer at Vercel

Join the team building the future of web development. We're looking for a frontend engineer passionate about developer experience and web performance.

Requirements:
- Expert-level React and TypeScript
- Deep understanding of Next.js
- Experience with design systems
- Performance optimization skills
- 3+ years of professional experience`,
  },
];
