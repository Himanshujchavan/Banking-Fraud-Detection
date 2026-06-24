import { useState, useEffect } from "react";
import { C } from "../utils/constants";

/**
 * Navbar / Page Section Header
 * Props: title, subtitle, actions (optional JSX)
 */
export default function Navbar({ title, subtitle, actions }) {
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  return (
    <div style={{
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      paddingBottom: 18,
      marginBottom: 22,
      borderBottom: `1px solid ${C.border}`,
    }}>
      {/* Left — title + subtitle */}
      <div>
        <h2 style={{ margin: 0, color: C.text, fontSize: 19, fontWeight: 900 }}>
          {title}
        </h2>
        {subtitle && (
          <p style={{ margin: "4px 0 0", color: C.text2, fontSize: 11 }}>
            {subtitle}
          </p>
        )}
      </div>

      {/* Right — optional actions + live clock */}
      <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
        {actions}

        <div style={{ textAlign: "right" }}>
          <div style={{ color: C.accent, fontFamily: "monospace", fontSize: 12, fontWeight: 700 }}>
            {now.toLocaleTimeString()}
          </div>
          <div style={{ color: C.text2, fontSize: 10 }}>
            {now.toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" })}
          </div>
        </div>
      </div>
    </div>
  );
}