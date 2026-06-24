import { useState } from "react";
import { C } from "../utils/constants";

export default function Login({ onLogin }) {
  const [email,  setEmail]  = useState("");
  const [pass,   setPass]   = useState("");
  const [error,  setError]  = useState("");
  const [loading, setLoading] = useState(false);

  function handleLogin() {
    if (!email || !pass) {
      setError("Enter your credentials to continue.");
      return;
    }
    setError("");
    setLoading(true);
    // Replace setTimeout with real POST /login call
    setTimeout(() => {
      setLoading(false);
      onLogin();
    }, 1100);
  }

  const inputStyle = {
    width: "100%",
    background: C.surf,
    border: `1px solid ${C.border}`,
    borderRadius: 6,
    padding: "10px 12px",
    color: C.text,
    fontSize: 13,
    outline: "none",
    boxSizing: "border-box",
    fontFamily: "monospace",
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: C.bg,
      fontFamily: "system-ui, sans-serif",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      position: "relative",
    }}>

      {/* Background grid */}
      <div style={{
        position: "absolute", inset: 0, opacity: 0.25,
        backgroundImage: `linear-gradient(${C.border} 1px, transparent 1px),
                          linear-gradient(90deg, ${C.border} 1px, transparent 1px)`,
        backgroundSize: "44px 44px",
      }} />

      <div style={{
        position: "relative", zIndex: 1, width: 370,
        background: C.card,
        border: `1px solid ${C.border}`,
        borderTop: `3px solid ${C.accent}`,
        borderRadius: 12,
        padding: 36,
        boxShadow: `0 0 70px ${C.accent}0A`,
      }}>

        {/* Logo */}
        <div style={{ textAlign: "center", marginBottom: 30 }}>
          <div style={{
            width: 54, height: 54, borderRadius: 13,
            background: `${C.accent}12`,
            border: `1px solid ${C.accent}28`,
            margin: "0 auto 14px",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 24,
          }}>🛡</div>
          <div style={{ color: C.text, fontSize: 21, fontWeight: 900 }}>FraudShield AI</div>
          <div style={{ color: C.text2, fontSize: 10, letterSpacing: "0.14em", marginTop: 4 }}>
            BANK FRAUD MONITORING SYSTEM
          </div>
        </div>

        {/* Email */}
        <label style={{ color: C.text2, fontSize: 10, letterSpacing: "0.1em", display: "block", marginBottom: 6 }}>
          ANALYST EMAIL
        </label>
        <input
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          placeholder="analyst@bank.gov.in"
          style={{ ...inputStyle, marginBottom: 14 }}
          onFocus={e  => (e.target.style.borderColor = C.accent)}
          onBlur={e   => (e.target.style.borderColor = C.border)}
        />

        {/* Password */}
        <label style={{ color: C.text2, fontSize: 10, letterSpacing: "0.1em", display: "block", marginBottom: 6 }}>
          PASSWORD
        </label>
        <input
          type="password"
          value={pass}
          onChange={e => setPass(e.target.value)}
          placeholder="••••••••••"
          onKeyDown={e => e.key === "Enter" && handleLogin()}
          style={{ ...inputStyle, marginBottom: 18 }}
          onFocus={e  => (e.target.style.borderColor = C.accent)}
          onBlur={e   => (e.target.style.borderColor = C.border)}
        />

        {/* Error */}
        {error && (
          <div style={{
            color: C.danger, fontSize: 11, marginBottom: 12,
            padding: "8px 10px",
            background: `${C.danger}10`,
            border: `1px solid ${C.danger}28`,
            borderRadius: 4,
          }}>
            {error}
          </div>
        )}

        {/* Submit */}
        <div
          onClick={handleLogin}
          style={{
            width: "100%",
            background: loading ? `${C.accent}50` : C.accent,
            color: "#000",
            padding: "12px",
            borderRadius: 6,
            fontWeight: 900,
            fontSize: 12,
            letterSpacing: "0.1em",
            textAlign: "center",
            cursor: "pointer",
            transition: "all 0.2s",
          }}
        >
          {loading ? "AUTHENTICATING…" : "ACCESS PORTAL"}
        </div>

        {/* Warning banner */}
        <div style={{
          marginTop: 18, padding: "10px 12px",
          background: `${C.warn}08`,
          border: `1px solid ${C.warn}20`,
          borderRadius: 6,
        }}>
          <div style={{ color: C.warn, fontSize: 10, letterSpacing: "0.04em" }}>
            ⚠ RESTRICTED ACCESS · Authorized Personnel Only ·
            All sessions are logged and audited.
          </div>
        </div>
      </div>
    </div>
  );
}