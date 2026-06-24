import { useEffect, useState } from "react";

import Navbar from "../components/Navbar";
import { Pill } from "../components/StatCard";
import { C } from "../utils/constants";

import { getTransactions } from "../services/fraudApi";

const FILTERS = [
  "ALL",
  "SUCCESS",
  "FAILED",
  "HIGH_RISK",
  "FRAUD"
];

export default function Transaction() {

  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  const [filter, setFilter] = useState("ALL");
  const [search, setSearch] = useState("");

  useEffect(() => {
    loadTransactions();
  }, []);

  const loadTransactions = async () => {

    try {

      const res = await getTransactions();

      setTransactions(res.data);

    } catch (err) {

      console.error(err);

    } finally {

      setLoading(false);
    }
  };

  const shown = transactions.filter((t) => {

    const matchesSearch =
      !search ||
      String(t.id).includes(search) ||
      t.sender_account?.toLowerCase().includes(search.toLowerCase()) ||
      t.receiver_account?.toLowerCase().includes(search.toLowerCase());

    if (!matchesSearch) return false;

    switch (filter) {

      case "FRAUD":
        return t.is_fraud === true;

      case "HIGH_RISK":
        return t.risk_score >= 80;

      case "SUCCESS":
        return t.status === "SUCCESS";

      case "FAILED":
        return t.status === "FAILED";

      default:
        return true;
    }
  });

  if (loading) {

    return (
      <div
        style={{
          height: "70vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#3b82f6",
          fontSize: 20,
          fontWeight: 700
        }}
      >
        Loading Transactions...
      </div>
    );
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#081120"
      }}
    >
      <Navbar
        title="Transaction Monitor"
        subtitle="Real-time banking transaction stream"
        actions={
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 8,
              color: "#22c55e",
              fontWeight: 700
            }}
          >
            <span
              style={{
                width: 8,
                height: 8,
                borderRadius: "50%",
                background: "#22c55e",
                boxShadow: "0 0 10px #22c55e"
              }}
            />
            LIVE
          </div>
        }
      />

      {/* Search + Filters */}

      <div
        style={{
          display: "flex",
          gap: 12,
          marginBottom: 20,
          flexWrap: "wrap"
        }}
      >
        <input
          value={search}
          onChange={(e) =>
            setSearch(e.target.value)
          }
          placeholder="Search Transaction / Account"
          style={{
            padding: 12,
            minWidth: 350,
            background: "#111827",
            border: "1px solid #1e293b",
            color: "white",
            borderRadius: 10
          }}
        />

        {FILTERS.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            style={{
              padding: "10px 16px",
              borderRadius: 10,
              border:
                filter === f
                  ? "1px solid #3b82f6"
                  : "1px solid #1e293b",
              background:
                filter === f
                  ? "#1d4ed8"
                  : "#111827",
              color: "white",
              cursor: "pointer",
              fontWeight: 600
            }}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Stats */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(180px,1fr))",
          gap: 15,
          marginBottom: 20
        }}
      >
        <SummaryCard
          title="Total Transactions"
          value={transactions.length}
          color="#3b82f6"
        />

        <SummaryCard
          title="Fraud Cases"
          value={
            transactions.filter(
              (t) => t.is_fraud
            ).length
          }
          color="#ef4444"
        />

        <SummaryCard
          title="High Risk"
          value={
            transactions.filter(
              (t) => t.risk_score >= 80
            ).length
          }
          color="#f59e0b"
        />

        <SummaryCard
          title="Success"
          value={
            transactions.filter(
              (t) => t.status === "SUCCESS"
            ).length
          }
          color="#22c55e"
        />
      </div>

      {/* Table */}

      <div
        style={{
          background: "#111827",
          border: "1px solid #1e293b",
          borderRadius: 14,
          overflow: "hidden",
          boxShadow:
            "0 10px 30px rgba(0,0,0,.25)"
        }}
      >
        <div
          style={{
            maxHeight: "75vh",
            overflowY: "auto"
          }}
        >
          <table
            style={{
              width: "100%",
              borderCollapse: "collapse"
            }}
          >
            <thead
              style={{
                position: "sticky",
                top: 0,
                zIndex: 10
              }}
            >
              <tr
                style={{
                  background: "#0f172a"
                }}
              >
                {[
                  "ID",
                  "Timestamp",
                  "Sender",
                  "Receiver",
                  "Amount",
                  "Risk",
                  "Fraud",
                  "Status"
                ].map((h) => (
                  <th
                    key={h}
                    style={{
                      padding: 15,
                      textAlign: "left",
                      color: "#94a3b8",
                      fontSize: 12
                    }}
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {shown.map((txn) => (
                <tr
                  key={txn.id}
                  style={{
                    borderBottom:
                      "1px solid rgba(255,255,255,.05)"
                  }}
                >
                  <td style={{ padding: 15 }}>
                    {txn.id}
                  </td>

                  <td style={{ padding: 15 }}>
                    {new Date(
                      txn.timestamp
                    ).toLocaleString()}
                  </td>

                  <td
                    style={{
                      padding: 15,
                      color: "#60a5fa"
                    }}
                  >
                    {txn.sender_account}
                  </td>

                  <td
                    style={{
                      padding: 15,
                      color: "#60a5fa"
                    }}
                  >
                    {txn.receiver_account}
                  </td>

                  <td
                    style={{
                      padding: 15,
                      fontWeight: 700
                    }}
                  >
                    ₹
                    {txn.amount.toLocaleString(
                      "en-IN"
                    )}
                  </td>

                  <td
                    style={{
                      padding: 15,
                      fontWeight: 700,
                      color:
                        txn.risk_score >= 85
                          ? "#ef4444"
                          : txn.risk_score >= 60
                          ? "#f59e0b"
                          : "#22c55e"
                    }}
                  >
                    {txn.risk_score}
                  </td>

                  <td style={{ padding: 15 }}>
                    {txn.is_fraud ? (
                      <span
                        style={{
                          color: "#ef4444",
                          fontSize: 18
                        }}
                      >
                        🚨
                      </span>
                    ) : (
                      "—"
                    )}
                  </td>

                  <td style={{ padding: 15 }}>
                    <Pill
                      label={txn.status}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function SummaryCard({
  title,
  value,
  color
}) {

  return (
    <div
      style={{
        background: "#111827",
        border: "1px solid #1e293b",
        borderRadius: 14,
        padding: 20
      }}
    >
      <div
        style={{
          color: "#94a3b8",
          fontSize: 12,
          marginBottom: 8
        }}
      >
        {title}
      </div>

      <div
        style={{
          color,
          fontSize: 28,
          fontWeight: 700
        }}
      >
        {value}
      </div>
    </div>
  );
}