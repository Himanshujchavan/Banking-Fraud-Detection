import { useState, useEffect } from "react";

import Navbar from "../components/Navbar";
import { Pill, RiskScore } from "../components/StatCard";
import { C } from "../utils/constants";

import { getFraudAlerts } from "../services/fraudApi";

const TYPES = [
  "ALL",
  "RAPID_MOVEMENT",
  "DORMANT_ACCOUNT",
  "MULTIPLE_SENDERS",
  "ML_FRAUD",
];

export default function Alerts() {

  const [alerts, setAlerts] = useState([]);

  const [loading, setLoading] = useState(true);

  const [filter, setFilter] = useState("ALL");

  const [search, setSearch] = useState("");

  useEffect(() => {

    loadAlerts();

  }, []);

  const loadAlerts = async () => {

    try {

      const res =
        await getFraudAlerts();

      setAlerts(res.data);

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);

    }
  };

  const shown = alerts.filter(
    (a) =>
      (filter === "ALL" ||
        a.alert_type === filter) &&
      (!search ||
        a.account_number
          .toLowerCase()
          .includes(
            search.toLowerCase()
          ))
  );

  const openCount = alerts.filter(
    (a) => a.status === "OPEN"
  ).length;

  if (loading) {
    return <h2>Loading Alerts...</h2>;
  }

  return (
    <div>

      <Navbar
        title="Fraud Alerts"
        subtitle={`${openCount} open alerts requiring attention`}
      />

      {/* Filter Bar */}

      <div
        style={{
          display: "flex",
          gap: 8,
          marginBottom: 14,
          flexWrap: "wrap",
          alignItems: "center",
        }}
      >

        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            background: C.card,
            border: `1px solid ${C.border}`,
            borderRadius: 6,
            padding: "8px 12px",
            flex: "1 1 180px",
            maxWidth: 260,
          }}
        >
          <span
            style={{
              color: C.text2,
            }}
          >
            🔍
          </span>

          <input
            value={search}
            onChange={(e) =>
              setSearch(
                e.target.value
              )
            }
            placeholder="Search account..."
            style={{
              background:
                "transparent",
              border: "none",
              color: C.text,
              fontSize: 12,
              outline: "none",
              width: "100%",
            }}
          />
        </div>

        <div
          style={{
            display: "flex",
            gap: 6,
            flexWrap: "wrap",
          }}
        >
          {TYPES.map((t) => (
            <div
              key={t}
              onClick={() =>
                setFilter(t)
              }
              style={{
                padding: "6px 11px",
                borderRadius: 6,
                cursor: "pointer",
                fontSize: 10,
                fontWeight: 700,
                background:
                  filter === t
                    ? `${C.accent}12`
                    : C.card,
                border: `1px solid ${
                  filter === t
                    ? C.accent +
                      "40"
                    : C.border
                }`,
                color:
                  filter === t
                    ? C.accent
                    : C.text2,
              }}
            >
              {t.replace(
                /_/g,
                " "
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Table */}

      <div
        style={{
          background: C.card,
          border: `1px solid ${C.border}`,
          borderRadius: 8,
          overflow: "hidden",
        }}
      >

        <table
          style={{
            width: "100%",
            borderCollapse:
              "collapse",
          }}
        >

          <thead>

            <tr
              style={{
                background:
                  C.surf,
              }}
            >

              {[
                "#",
                "Account",
                "Alert Type",
                "Risk Score",
                "Status",
                "Created At",
              ].map((h) => (
                <th
                  key={h}
                  style={{
                    color:
                      C.text2,
                    fontSize: 9,
                    textAlign:
                      "left",
                    padding:
                      "12px 16px",
                    borderBottom: `1px solid ${C.border}`,
                  }}
                >
                  {h}
                </th>
              ))}

            </tr>

          </thead>

          <tbody>

            {shown.map(
              (
                alert,
                index
              ) => (

                <tr
                  key={
                    alert.id
                  }
                >

                  <td
                    style={{
                      padding:
                        "12px 16px",
                    }}
                  >
                    {index + 1}
                  </td>

                  <td
                    style={{
                      padding:
                        "12px 16px",
                      color:
                        C.accent,
                    }}
                  >
                    {
                      alert.account_number
                    }
                  </td>

                  <td
                    style={{
                      padding:
                        "12px 16px",
                    }}
                  >
                    {alert.alert_type.replace(
                      /_/g,
                      " "
                    )}
                  </td>

                  <td
                    style={{
                      padding:
                        "12px 16px",
                    }}
                  >
                    <RiskScore
                      value={
                        alert.risk_score
                      }
                    />
                  </td>

                  <td
                    style={{
                      padding:
                        "12px 16px",
                    }}
                  >
                    <Pill
                      label={
                        alert.status
                      }
                    />
                  </td>

                  <td
                    style={{
                      padding:
                        "12px 16px",
                    }}
                  >
                    {
                      alert.created_at
                    }
                  </td>

                </tr>
              )
            )}

          </tbody>

        </table>

        {shown.length === 0 && (
          <div
            style={{
              padding: 40,
              textAlign:
                "center",
            }}
          >
            No alerts found
          </div>
        )}

      </div>

    </div>
  );
}