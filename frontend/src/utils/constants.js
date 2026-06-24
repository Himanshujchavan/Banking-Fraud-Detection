// ══════════════════════════════════════════════
// DESIGN TOKENS — ops-center dark navy palette
// ══════════════════════════════════════════════
export const C = {
  bg:      "#060D1B",
  surf:    "#0A1528",
  card:    "#0E1D35",
  border:  "#152540",
  accent:  "#00C8FF",
  danger:  "#FF3D3D",
  warn:    "#FFA920",
  success: "#00C48C",
  purple:  "#9B6FFF",
  text:    "#C5DEFF",
  text2:   "#4A6A8A",
  text3:   "#243550",
};

// ── Colour helpers ──────────────────────────────
export function scoreColor(score) {
  if (score >= 80) return C.danger;
  if (score >= 60) return C.warn;
  return C.success;
}

export function levelColor(level) {
  if (level === "high")   return C.danger;
  if (level === "medium") return C.warn;
  return C.success;
}

// ── Status → badge style map ────────────────────
export const STATUS_STYLES = {
  OPEN:          { bg: `${C.danger}18`,  col: C.danger,  bd: `${C.danger}40`  },
  INVESTIGATING: { bg: `${C.warn}18`,   col: C.warn,   bd: `${C.warn}40`   },
  CLOSED:        { bg: `${C.success}18`,col: C.success, bd: `${C.success}40` },
  BLOCK:         { bg: `${C.danger}18`,  col: C.danger,  bd: `${C.danger}40`  },
  FACE_VERIFY:   { bg: `${C.warn}18`,   col: C.warn,   bd: `${C.warn}40`   },
  FLAGGED:       { bg: `${C.warn}18`,   col: C.warn,   bd: `${C.warn}40`   },
  BLOCKED:       { bg: `${C.danger}18`,  col: C.danger,  bd: `${C.danger}40`  },
  SUSPICIOUS:    { bg: `${C.purple}18`, col: C.purple,  bd: `${C.purple}40` },
  COMPLETED:     { bg: `${C.success}18`,col: C.success, bd: `${C.success}40` },
};