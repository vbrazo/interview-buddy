import { Outlet } from "react-router-dom";
import { AnalysisProvider } from "@/contexts/AnalysisContext";
import { Navigation } from "@/components/Navigation";
import { Footer } from "@/components/Footer";

export function Layout() {
  return (
    <AnalysisProvider>
      <div className="min-h-screen bg-background flex flex-col">
        <Navigation />
        <main className="flex-1">
          <Outlet />
        </main>
        <Footer />
      </div>
    </AnalysisProvider>
  );
}
