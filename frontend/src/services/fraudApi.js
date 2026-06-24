import api from "./api";

// Dashboard
export const getDashboardStats = () =>
  api.get("/admin/dashboard/stats");

// Alerts
export const getFraudAlerts = () =>
  api.get("/admin/fraud-alerts");

// High Risk Transactions
export const getHighRiskTransactions = () =>
  api.get("/admin/transactions/high-risk");

//All Transactions
export const getTransactions = () =>
  api.get("/admin/transactions");

// Top Risk Accounts
export const getTopRiskAccounts = () =>
  api.get("/mule/top-risk");


// Network Analysis
export const getNetworkAnalysis = () =>
  api.get("/admin/network-analysis");

// Fraud Network
export const getFraudNetwork = () =>
  api.get("/admin/network-analysis/fraud");

// Account Investigation
export const getAccountDetails = (accountNumber) =>
  api.get(`/admin/account/${accountNumber}`);

export const getAccountRisk = (accountNumber) =>
  api.get(`/mule/risk/${accountNumber}`);