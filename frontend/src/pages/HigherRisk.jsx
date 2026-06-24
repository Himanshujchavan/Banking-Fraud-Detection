import { useEffect, useState } from "react";

import Navbar from "../components/Navbar";
import { Pill, RiskScore } from "../components/StatCard";
import { C } from "../utils/constants";

import { getHighRiskTransactions } from "../services/fraudApi";

export default function HigherRisk() {

  const [transactions, setTransactions] = useState([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {

    loadTransactions();

  }, []);

  const loadTransactions = async () => {

    try {

      const res =
        await getHighRiskTransactions();

      setTransactions(res.data);

    } catch (err) {

      console.error(err);

    } finally {

      setLoading(false);

    }
  };

  if (loading) {
    return <h2>Loading Transactions...</h2>;
  }

  return (
    <div>

      <Navbar
        title="High Risk Transactions"
        subtitle="Transactions flagged by ML model"
      />

      <div
        style={{
          background: C.card,
          border: `1px solid ${C.border}`,
          borderRadius: 8,
          overflow: "hidden",
        }}
      >

        <div
          style={{
            padding: "14px 20px",
            borderBottom: `1px solid ${C.border}`,
            display: "flex",
            justifyContent: "space-between",
          }}
        >
          <span
            style={{
              color: C.text,
              fontWeight: 700,
            }}
          >
            ML Flagged Transactions
          </span>

          <span
            style={{
              color: C.text2,
            }}
          >
            {transactions.length} transactions
          </span>

        </div>

        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
          }}
        >

          <thead>

            <tr>

              {[
                "#",
                "Sender",
                "Receiver",
                "Amount",
                "Risk Score",
                "Fraud",
                "Decision",
              ].map((h) => (
                <th
                  key={h}
                  style={{
                    padding: "12px",
                    textAlign: "left",
                    borderBottom: `1px solid ${C.border}`,
                  }}
                >
                  {h}
                </th>
              ))}

            </tr>

          </thead>

          <tbody>

            {transactions.map(
              (txn, index) => {

                let decision = "APPROVE";

                if (txn.risk_score >= 85) {
                  decision = "BLOCK";
                } else if (
                  txn.risk_score >= 60
                ) {
                  decision =
                    "FACE_VERIFY";
                } else if (
                  txn.risk_score >= 30
                ) {
                  decision =
                    "OTP_VERIFY";
                }

                return (

                  <tr
                    key={txn.id}
                  >

                    <td
                      style={{
                        padding: "12px",
                      }}
                    >
                      {index + 1}
                    </td>

                    <td
                      style={{
                        padding: "12px",
                        color: C.accent,
                      }}
                    >
                      {txn.sender_account}
                    </td>

                    <td
                      style={{
                        padding: "12px",
                        color: C.accent,
                      }}
                    >
                      {txn.receiver_account}
                    </td>

                    <td
                      style={{
                        padding: "12px",
                      }}
                    >
                      ₹
                      {txn.amount.toLocaleString(
                        "en-IN"
                      )}
                    </td>

                    <td
                      style={{
                        padding: "12px",
                      }}
                    >
                      <RiskScore
                        value={
                          txn.risk_score
                        }
                      />
                    </td>

                    <td
                      style={{
                        padding: "12px",
                      }}
                    >
                      {txn.is_fraud
                        ? "🚨 YES"
                        : "NO"}
                    </td>

                    <td
                      style={{
                        padding: "12px",
                      }}
                    >
                      <Pill
                        label={
                          decision
                        }
                      />
                    </td>

                  </tr>
                );
              }
            )}

          </tbody>

        </table>

      </div>

    </div>
  );
}