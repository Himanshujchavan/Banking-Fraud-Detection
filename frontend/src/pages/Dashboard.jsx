import { useEffect, useState } from "react";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

import Navbar from "../components/Navbar";
import StatCard, {
  Pill,
  RiskScore,
  ChartTooltip,
} from "../components/StatCard";

import { C } from "../utils/constants";

import {
  getDashboardStats,
  getFraudAlerts,
} from "../services/fraudApi";

export default function Dashboard() {

  const [stats, setStats] = useState(null);

  const [alerts, setAlerts] = useState([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {

    loadDashboard();

  }, []);

  const loadDashboard = async () => {

    try {

      const statsRes =
        await getDashboardStats();

      const alertsRes =
        await getFraudAlerts();

      setStats(statsRes.data);

      setAlerts(alertsRes.data);

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);

    }
  };

  if (loading) {
    return <h2>Loading Dashboard...</h2>;
  }

  const CARDS = [
    {
      label: "Total Users",
      value: stats.total_users,
      color: C.accent,
      icon: "👤",
    },
    {
      label: "Total Accounts",
      value: stats.total_accounts,
      color: C.accent,
      icon: "🏦",
    },
    {
      label: "Total Transactions",
      value: stats.total_transactions,
      color: C.text2,
      icon: "⇄",
    },
    {
      label: "Fraud Transactions",
      value: stats.fraud_transactions,
      color: C.danger,
      icon: "⚡",
    },
    {
      label: "Open Alerts",
      value: stats.open_alerts,
      color: C.danger,
      icon: "🔔",
    },
    {
      label: "Total Alerts",
      value: stats.total_alerts,
      color: C.warn,
      icon: "🚨",
    },
    {
      label: "Blocked Transactions",
      value: stats.blocked_transactions,
      color: C.warn,
      icon: "🔒",
    },
    {
      label: "High Risk Accounts",
      value: stats.high_risk_accounts || 0,
      color: C.success,
      icon: "📊",
    },
  ];

  // Temporary chart data
  const fraudTrend = [
    { day: "Mon", detected: 45, blocked: 30 },
    { day: "Tue", detected: 80, blocked: 50 },
    { day: "Wed", detected: 65, blocked: 55 },
    { day: "Thu", detected: 120, blocked: 90 },
    { day: "Fri", detected: 95, blocked: 80 },
    { day: "Sat", detected: 70, blocked: 60 },
    { day: "Sun", detected: 50, blocked: 40 },
  ];

  const alertDistribution = [
    {
      name: "Rapid Movement",
      value: 40,
      color: "#ff4d4f",
    },
    {
      name: "Dormant",
      value: 35,
      color: "#faad14",
    },
    {
      name: "Multiple Sender",
      value: 25,
      color: "#52c41a",
    },
  ];

  return (
    <div>

      <Navbar
        title="Dashboard"
        subtitle="Real-time fraud monitoring overview"
      />

      {/* Cards */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(4,1fr)",
          gap: 10,
          marginBottom: 20,
        }}
      >
        {CARDS.map((card, index) => (
          <StatCard
            key={index}
            {...card}
          />
        ))}
      </div>

      {/* Charts */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "2fr 1fr",
          gap: 14,
          marginBottom: 22,
        }}
      >

        <div
          style={{
            background: C.card,
            border: `1px solid ${C.border}`,
            borderRadius: 8,
            padding: 20,
          }}
        >
          <h3>Fraud Trend</h3>

          <ResponsiveContainer
            width="100%"
            height={220}
          >
            <AreaChart data={fraudTrend}>
              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis dataKey="day" />

              <YAxis />

              <Tooltip
                content={<ChartTooltip />}
              />

              <Area
                dataKey="detected"
                stroke={C.danger}
                fill={C.danger}
              />

              <Area
                dataKey="blocked"
                stroke={C.success}
                fill={C.success}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div
          style={{
            background: C.card,
            border: `1px solid ${C.border}`,
            borderRadius: 8,
            padding: 20,
          }}
        >
          <h3>Alert Distribution</h3>

          <ResponsiveContainer
            width="100%"
            height={220}
          >
            <PieChart>

              <Pie
                data={alertDistribution}
                dataKey="value"
                innerRadius={50}
                outerRadius={80}
              >
                {alertDistribution.map(
                  (entry, index) => (
                    <Cell
                      key={index}
                      fill={entry.color}
                    />
                  )
                )}
              </Pie>

              <Tooltip />

            </PieChart>
          </ResponsiveContainer>

        </div>
      </div>

      {/* Recent Alerts */}

      <div
        style={{
          background: C.card,
          border: `1px solid ${C.border}`,
          borderRadius: 8,
          padding: 20,
        }}
      >

        <h3>
          Recent Fraud Alerts
        </h3>

        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
          }}
        >

          <thead>

            <tr>

              <th>Account</th>

              <th>Alert Type</th>

              <th>Risk</th>

              <th>Status</th>

            </tr>

          </thead>

          <tbody>

            {alerts.slice(0, 10).map(
              (alert) => (

                <tr key={alert.id}>

                  <td>
                    {alert.account_number}
                  </td>

                  <td>
                    {alert.alert_type}
                  </td>

                  <td>
                    <RiskScore
                      value={alert.risk_score}
                    />
                  </td>

                  <td>
                    <Pill
                      label={alert.status}
                    />
                  </td>

                </tr>
              )
            )}

          </tbody>

        </table>

      </div>

    </div>
  );
}