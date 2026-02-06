import { Outlet } from "react-router-dom";
import { AnalysisProvider } from "@/contexts/AnalysisContext";
import { Navigation } from "@/components/Navigation";
import { Footer } from "@/components/Footer";

export function Layout() {
  return (
    <AnalysisProvider>
      <div className="min-h-screen max-h-screen bg-background flex flex-col overflow-y-auto">
        <Navigation />
        <main className="flex-1 min-h-0">
          <Outlet />
        </main>
        <Footer />
      </div>
    </AnalysisProvider>
  );
}
