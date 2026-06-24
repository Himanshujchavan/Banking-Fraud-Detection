import { C, scoreColor, STATUS_STYLES } from "../utils/constants";

// ══════════════════════════════════════════════
// StatCard  — used on Dashboard & Mule Center
// ══════════════════════════════════════════════
export default function StatCard({ label, value, sub, color, icon }) {
  return (
    <div style={{
      background: C.card,
      border:     `1px solid ${C.border}`,
      borderLeft: `3px solid ${color || C.accent}`,
      borderRadius: 8,
      padding: "14px 16px",
    }}>
      <div style={{ display:"flex", justifyContent:"space-between", marginBottom:6 }}>
        <span style={{
          color: C.text2, fontSize: 9, fontWeight: 700,
          letterSpacing: "0.1em", textTransform: "uppercase",
        }}>
          {label}
        </span>
        {icon && <span style={{ fontSize: 14 }}>{icon}</span>}
      </div>

      <div style={{
        color: C.text, fontSize: 26, fontWeight: 900,
        fontFamily: "monospace", lineHeight: 1,
      }}>
        {typeof value === "number" ? value.toLocaleString("en-IN") : value}
      </div>

      {sub && (
        <div style={{ color: C.text2, fontSize: 10, marginTop: 3 }}>{sub}</div>
      )}
    </div>
  );
}

// ══════════════════════════════════════════════
// Pill  — coloured status badge
// ══════════════════════════════════════════════
export function Pill({ label }) {
  const s = STATUS_STYLES[label] || STATUS_STYLES.OPEN;
  return (
    <span style={{
      background: s.bg, color: s.col, border: `1px solid ${s.bd}`,
      borderRadius: 4, padding: "2px 9px",
      fontSize: 10, fontWeight: 800, letterSpacing: "0.06em",
    }}>
      {label}
    </span>
  );
}

// ══════════════════════════════════════════════
// RiskScore  — monospace numeric risk badge
// ══════════════════════════════════════════════
export function RiskScore({ value }) {
  const col = scoreColor(value);
  return (
    <span style={{
      background: `${col}18`, color: col, border: `1px solid ${col}40`,
      borderRadius: 4, padding: "2px 8px",
      fontSize: 11, fontWeight: 700, fontFamily: "monospace",
    }}>
      {value}
    </span>
  );
}

// ══════════════════════════════════════════════
// ChartTooltip  — shared recharts tooltip
// ══════════════════════════════════════════════
export function ChartTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: C.card, border: `1px solid ${C.border}`,
      borderRadius: 6, padding: "8px 12px",
    }}>
      <div style={{ color: C.text2, fontSize: 10, marginBottom: 4 }}>{label}</div>
      {payload.map((p, i) => (
        <div key={i} style={{ color: p.color, fontSize: 11, fontFamily: "monospace" }}>
          {p.name}: {p.value}
        </div>
      ))}
    </div>
  );
}