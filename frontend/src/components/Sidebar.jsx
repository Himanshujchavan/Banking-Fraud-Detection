import { useState, useEffect } from "react";
import { C } from "../utils/constants";

const NAV_ITEMS = [
  { id: "dashboard",     icon: "⊞", label: "Dashboard"             },
  { id: "alerts",        icon: "◉", label: "Fraud Alerts", badge: 89 },
  { id: "higherRisk",    icon: "⇄", label: "High Risk Txns"         },
  { id: "users",         icon: "◎", label: "Account Investigation"  },
  { id: "network",       icon: "⬡", label: "Network Analysis"       },
  { id: "transaction",   icon: "≋", label: "Transaction Monitor"    },
];

export default function Sidebar({ page, setPage, onLogout }) {
  const [pulse, setPulse] = useState(true);

  useEffect(() => {
    const t = setInterval(() => setPulse(p => !p), 900);
    return () => clearInterval(t);
  }, []);

  return (
    <div style={{
      width: 242,
      minHeight: "100vh",
      background: C.surf,
      borderRight: `1px solid ${C.border}`,
      position: "fixed",
      left: 0,
      top: 0,
      zIndex: 100,
      display: "flex",
      flexDirection: "column",
    }}>

      {/* ── Logo ── */}
      <div style={{ padding: "18px 18px 14px", borderBottom: `1px solid ${C.border}` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{
            width: 34, height: 34, borderRadius: 8,
            background: `${C.accent}14`, border: `1px solid ${C.accent}35`,
            display: "flex", alignItems: "center", justifyContent: "center", fontSize: 17,
          }}>🛡</div>
          <div>
            <div style={{ color: C.text, fontWeight: 900, fontSize: 14, letterSpacing: "0.01em" }}>
              FraudShield
            </div>
            <div style={{ color: C.text2, fontSize: 9, letterSpacing: "0.12em" }}>
              AI · ANALYST PORTAL
            </div>
          </div>
        </div>
      </div>

      {/* ── Threat Level Ticker ── */}
      <div style={{
        margin: "12px 12px 0",
        background: `${C.danger}0E`,
        border: `1px solid ${C.danger}28`,
        borderRadius: 7,
        padding: "10px 12px",
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ color: C.text2, fontSize: 9, letterSpacing: "0.12em" }}>THREAT LEVEL</span>
          <span style={{ display: "flex", alignItems: "center", gap: 5, color: C.danger, fontSize: 11, fontWeight: 800 }}>
            <span style={{
              width: 6, height: 6, borderRadius: "50%",
              background: C.danger, display: "inline-block",
              boxShadow: `0 0 7px ${C.danger}`,
              opacity: pulse ? 1 : 0.25,
              transition: "opacity 0.4s",
            }} />
            HIGH
          </span>
        </div>
        <div style={{ marginTop: 7, height: 3, background: `${C.danger}18`, borderRadius: 2, overflow: "hidden" }}>
          <div style={{ height: "100%", width: "84%", background: C.danger, borderRadius: 2 }} />
        </div>
        <div style={{ color: C.text2, fontSize: 9, marginTop: 5 }}>89 open alerts · 34 blocked accounts</div>
      </div>

      {/* ── Navigation ── */}
      <nav style={{ flex: 1, padding: "10px 10px" }}>
        {NAV_ITEMS.map(n => {
          const active = page === n.id;
          return (
            <div
              key={n.id}
              onClick={() => setPage(n.id)}
              style={{
                display: "flex", alignItems: "center", gap: 10,
                padding: "10px 12px", borderRadius: 6, marginBottom: 2,
                cursor: "pointer",
                background: active ? `${C.accent}12` : "transparent",
                border: `1px solid ${active ? C.accent + "30" : "transparent"}`,
                transition: "all 0.15s",
              }}
            >
              <span style={{ fontSize: 13, opacity: active ? 1 : 0.42 }}>{n.icon}</span>
              <span style={{
                color: active ? C.accent : C.text2,
                fontSize: 12, fontWeight: active ? 700 : 400, flex: 1,
              }}>
                {n.label}
              </span>
              {n.badge && (
                <span style={{
                  background: C.danger, color: "#fff",
                  borderRadius: 10, padding: "1px 6px",
                  fontSize: 9, fontWeight: 800,
                }}>
                  {n.badge}
                </span>
              )}
            </div>
          );
        })}
      </nav>

      {/* ── Analyst Info + Logout ── */}
      <div style={{ padding: "12px 14px", borderTop: `1px solid ${C.border}` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
          <div style={{
            width: 30, height: 30, borderRadius: "50%",
            background: `${C.accent}18`,
            display: "flex", alignItems: "center", justifyContent: "center",
          }}>
            <span style={{ color: C.accent, fontSize: 11, fontWeight: 800 }}>AM</span>
          </div>
          <div>
            <div style={{ color: C.text, fontSize: 12, fontWeight: 700 }}>Analyst Mehta</div>
            <div style={{ color: C.text2, fontSize: 9 }}>Senior Fraud Analyst</div>
          </div>
        </div>

        <div
          onClick={onLogout}
          style={{
            display: "flex", alignItems: "center", gap: 5,
            color: C.text2, fontSize: 11, cursor: "pointer",
            padding: "5px 8px", borderRadius: 4,
          }}
        >
          ⇠ Logout
        </div>
      </div>
    </div>
  );
}