import { Navigate } from "react-router-dom";

// Redirect legacy / route — now handled by Landing
export default function Index() {
  return <Navigate to="/" replace />;
}
