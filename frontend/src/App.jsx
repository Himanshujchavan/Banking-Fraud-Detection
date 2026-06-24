import { useState }     from "react";
import Sidebar           from "./components/Sidebar";
import Login             from "./pages/Login";
import Dashboard         from "./pages/Dashboard";
import Alerts            from "./pages/fraud-alert";
import HigherRisk        from "./pages/HigherRisk";
import Users             from "./pages/users";
import NetworkAnalysis   from "./pages/NetworkAnalysis";
import Transaction       from "./pages/Transaction";
import { C }             from "./utils/constants";

// ── Page registry ────────────────────────────────
const PAGES = {
  dashboard:   <Dashboard />,
  alerts:      <Alerts />,
  higherRisk:  <HigherRisk />,
  users:       <Users />,
  network:     <NetworkAnalysis />,
  transaction: <Transaction />,
};

export default function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [page,     setPage]     = useState("dashboard");

  if (!loggedIn) {
    return <Login onLogin={() => setLoggedIn(true)} />;
  }

  return (
    <div style={{
      fontFamily: "system-ui, -apple-system, sans-serif",
      background:  C.bg,
      minHeight:   "100vh",
    }}>
      {/* Fixed sidebar */}
      <Sidebar
        page={page}
        setPage={setPage}
        onLogout={() => setLoggedIn(false)}
      />

      {/* Main content — offset by sidebar width */}
      <main style={{
        marginLeft: 242,
        padding:    "26px 30px",
        minHeight:  "100vh",
      }}>
        {PAGES[page] ?? <Dashboard />}
      </main>
    </div>
  );
}