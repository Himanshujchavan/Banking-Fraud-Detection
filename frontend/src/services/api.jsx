// ══════════════════════════════════════════════
// MOCK DATA  (replace each function body with
// a real axios/fetch call to your backend)
// ══════════════════════════════════════════════

import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export default api;

// ── GET /admin/dashboard/stats ──────────────────
export const dashboardStats = {
  totalUsers:        12847,
  totalAccounts:     18392,
  totalTransactions: 284710,
  fraudTransactions: 1247,
  openAlerts:        89,
  blockedAccounts:   34,
  highRiskAccounts:  156,
  avgRiskScore:      42,
};

// ── GET /admin/fraud-trends ─────────────────────
export const fraudTrend = [
  { day: "Mon", detected: 50,  blocked: 32  },
  { day: "Tue", detected: 70,  blocked: 48  },
  { day: "Wed", detected: 120, blocked: 85  },
  { day: "Thu", detected: 90,  blocked: 61  },
  { day: "Fri", detected: 145, blocked: 102 },
  { day: "Sat", detected: 60,  blocked: 39  },
  { day: "Sun", detected: 88,  blocked: 58  },
];

// ── GET /admin/alert-distribution ──────────────
export const alertDistribution = [
  { name: "Rapid Movement",  value: 35, color: "#FF3D3D" },
  { name: "Dormant Account", value: 25, color: "#FFA920" },
  { name: "Multiple Sender", value: 20, color: "#9B6FFF" },
  { name: "ML Detection",    value: 20, color: "#00C8FF" },
];

// ── GET /admin/fraud-alerts ─────────────────────
export const fraudAlerts = [
  { id:1, account:"ACC1001", type:"RAPID_MOVEMENT",   risk:90, status:"OPEN",          ts:"2025-06-01 09:23" },
  { id:2, account:"ACC1002", type:"DORMANT_ACCOUNT",  risk:85, status:"OPEN",          ts:"2025-06-01 10:11" },
  { id:3, account:"ACC1003", type:"MULTIPLE_SENDER",  risk:78, status:"INVESTIGATING",  ts:"2025-06-01 11:05" },
  { id:4, account:"ACC1004", type:"ML_FRAUD",         risk:95, status:"OPEN",          ts:"2025-06-01 12:30" },
  { id:5, account:"ACC1005", type:"RAPID_MOVEMENT",   risk:72, status:"CLOSED",        ts:"2025-06-01 13:45" },
  { id:6, account:"ACC1006", type:"DORMANT_ACCOUNT",  risk:68, status:"OPEN",          ts:"2025-06-01 14:20" },
  { id:7, account:"ACC1007", type:"ML_FRAUD",         risk:91, status:"OPEN",          ts:"2025-06-01 15:10" },
  { id:8, account:"ACC1008", type:"MULTIPLE_SENDER",  risk:83, status:"INVESTIGATING",  ts:"2025-06-01 16:00" },
];

// ── GET /admin/transactions/high-risk ───────────
export const highRiskTransactions = [
  { from:"ACC1001", to:"ACC2002", amount:45000,  risk:92, prob:98, decision:"BLOCK"       },
  { from:"ACC1004", to:"ACC5001", amount:120000, risk:88, prob:94, decision:"BLOCK"       },
  { from:"ACC3002", to:"ACC1002", amount:78000,  risk:85, prob:89, decision:"FACE_VERIFY" },
  { from:"ACC2001", to:"ACC7003", amount:200000, risk:91, prob:96, decision:"BLOCK"       },
  { from:"ACC6001", to:"ACC1004", amount:55000,  risk:76, prob:82, decision:"FACE_VERIFY" },
  { from:"ACC9002", to:"ACC3005", amount:98000,  risk:80, prob:85, decision:"BLOCK"       },
];

// ── GET /transactions ───────────────────────────
export const allTransactions = [
  { id:"TXN001", from:"ACC1001", to:"ACC2002", amount:45000,  status:"FLAGGED",    time:"09:23:14" },
  { id:"TXN002", from:"ACC3001", to:"ACC1001", amount:120000, status:"BLOCKED",    time:"09:45:02" },
  { id:"TXN003", from:"ACC2003", to:"ACC5001", amount:18000,  status:"COMPLETED",  time:"10:01:33" },
  { id:"TXN004", from:"ACC4002", to:"ACC7003", amount:200000, status:"SUSPICIOUS", time:"10:22:18" },
  { id:"TXN005", from:"ACC1005", to:"ACC6001", amount:35000,  status:"COMPLETED",  time:"10:45:50" },
  { id:"TXN006", from:"ACC8001", to:"ACC1003", amount:67000,  status:"FLAGGED",    time:"11:02:07" },
  { id:"TXN007", from:"ACC2001", to:"ACC9001", amount:9000,   status:"COMPLETED",  time:"11:15:43" },
  { id:"TXN008", from:"ACC5002", to:"ACC1001", amount:200000, status:"BLOCKED",    time:"11:30:11" },
  { id:"TXN009", from:"ACC3003", to:"ACC2004", amount:54000,  status:"COMPLETED",  time:"11:48:29" },
  { id:"TXN010", from:"ACC9001", to:"ACC1002", amount:250000, status:"SUSPICIOUS", time:"12:05:00" },
];

// ── GET /account/{id} ───────────────────────────
export const accountsDB = {
  "ACC1001": {
    number:    "ACC1001",
    balance:   "₹2,34,500",
    userName:  "Rahul Sharma",
    riskScore: 95,
    decision:  "BLOCK",
    devices:   ["Samsung Galaxy S23", "Windows 11 Laptop", "iPhone 15 Pro"],
    locations: ["Mumbai, MH", "Nagpur, MH", "Delhi, DL"],
    alerts:    ["RAPID_MOVEMENT", "DORMANT_ACCOUNT"],
    transactions: [
      { id:"TXN001", from:"ACC1001", to:"ACC2002", amount:"₹45,000",   status:"FLAGGED",    time:"09:23" },
      { id:"TXN002", from:"ACC3001", to:"ACC1001", amount:"₹1,20,000", status:"BLOCKED",    time:"10:45" },
      { id:"TXN003", from:"ACC1001", to:"ACC4005", amount:"₹78,000",   status:"FLAGGED",    time:"11:20" },
      { id:"TXN004", from:"ACC5002", to:"ACC1001", amount:"₹2,00,000", status:"SUSPICIOUS", time:"12:15" },
      { id:"TXN005", from:"ACC1001", to:"ACC6001", amount:"₹35,000",   status:"COMPLETED",  time:"13:30" },
    ],
  },
  "ACC1002": {
    number:    "ACC1002",
    balance:   "₹89,200",
    userName:  "Priya Patel",
    riskScore: 85,
    decision:  "FACE_VERIFY",
    devices:   ["OnePlus Nord CE", "MacBook Air"],
    locations: ["Ahmedabad, GJ", "Surat, GJ"],
    alerts:    ["DORMANT_ACCOUNT"],
    transactions: [
      { id:"TXN010", from:"ACC9001", to:"ACC1002", amount:"₹2,50,000", status:"SUSPICIOUS", time:"08:10" },
      { id:"TXN011", from:"ACC1002", to:"ACC7003", amount:"₹2,45,000", status:"BLOCKED",    time:"08:45" },
    ],
  },
  "ACC1003": {
    number:    "ACC1003",
    balance:   "₹4,12,800",
    userName:  "Amit Verma",
    riskScore: 78,
    decision:  "FACE_VERIFY",
    devices:   ["Redmi Note 12", "Windows 10 Desktop"],
    locations: ["Pune, MH", "Bengaluru, KA"],
    alerts:    ["MULTIPLE_SENDER"],
    transactions: [
      { id:"TXN020", from:"ACC2001", to:"ACC1003", amount:"₹80,000",   status:"SUSPICIOUS", time:"07:30" },
      { id:"TXN021", from:"ACC3002", to:"ACC1003", amount:"₹90,000",   status:"SUSPICIOUS", time:"07:35" },
      { id:"TXN022", from:"ACC1003", to:"ACC6002", amount:"₹1,65,000", status:"BLOCKED",    time:"08:00" },
    ],
  },
};

// ── GET /admin/network-analysis ─────────────────
export const networkNodes = [
  { id:"ACC1001", x:370, y:160, risk:95, level:"high"   },
  { id:"ACC1002", x:170, y:300, risk:85, level:"high"   },
  { id:"ACC2003", x:570, y:300, risk:72, level:"medium" },
  { id:"ACC3004", x: 70, y:445, risk:45, level:"low"    },
  { id:"ACC4005", x:270, y:445, risk:88, level:"high"   },
  { id:"ACC5006", x:470, y:445, risk:65, level:"medium" },
  { id:"ACC6007", x:670, y:445, risk:30, level:"low"    },
  { id:"ACC7008", x:155, y:570, risk:58, level:"medium" },
  { id:"ACC8009", x:370, y:570, risk:92, level:"high"   },
];

export const networkEdges = [
  { from:"ACC1001", to:"ACC1002", amt:"₹2,34,000" },
  { from:"ACC1001", to:"ACC2003", amt:"₹1,12,000" },
  { from:"ACC1002", to:"ACC3004", amt:"₹45,000"   },
  { from:"ACC1002", to:"ACC4005", amt:"₹1,80,000" },
  { from:"ACC2003", to:"ACC5006", amt:"₹67,000"   },
  { from:"ACC2003", to:"ACC6007", amt:"₹23,000"   },
  { from:"ACC4005", to:"ACC7008", amt:"₹90,000"   },
  { from:"ACC4005", to:"ACC8009", amt:"₹1,56,000" },
  { from:"ACC8009", to:"ACC1001", amt:"₹78,000"   }, // closes the fraud ring
];

// IDs that form the circular fraud ring
export const FRAUD_RING_IDS = ["ACC1001", "ACC1002", "ACC4005", "ACC8009"];