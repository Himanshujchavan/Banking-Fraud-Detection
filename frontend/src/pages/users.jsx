import { useState } from "react";

import Navbar from "../components/Navbar";
import { Pill, RiskScore } from "../components/StatCard";
import { C } from "../utils/constants";

import {
  getAccountDetails,
  getAccountRisk,
} from "../services/fraudApi";

export default function AccountInvestigation() {

  const [input, setInput] = useState("");

  const [account, setAccount] = useState(null);

  const [risk, setRisk] = useState(null);

  const [loading, setLoading] = useState(false);

  const lookup = async () => {

    if (!input) return;

    try {

      setLoading(true);

      const accountRes =
        await getAccountDetails(input);

      setAccount(accountRes.data);

      const accountNumber =
        accountRes.data.account.account_number;

      const riskRes =
        await getAccountRisk(
          accountNumber
        );

      setRisk(riskRes.data);

    } catch (err) {

      console.error(err);

      alert("Account not found");

    } finally {

      setLoading(false);

    }
  };

  return (
    <div>

      <Navbar
        title="Account Investigation"
        subtitle="Investigate suspicious accounts"
      />

      <div
        style={{
          display: "flex",
          gap: 10,
          marginBottom: 20,
        }}
      >
        <input
          value={input}
          onChange={(e) =>
            setInput(e.target.value)
          }
          placeholder="Enter Account ID"
          style={{
            flex: 1,
            padding: 12,
          }}
        />

        <button
          onClick={lookup}
        >
          Investigate
        </button>
      </div>

      {loading && (
        <h3>
          Loading...
        </h3>
      )}

      {account && risk && (

        <>

          {/* Account Card */}

          <div
            style={{
              background: C.card,
              padding: 20,
              marginBottom: 20,
              borderRadius: 8,
            }}
          >

            <h2>
              Account Details
            </h2>

            <p>
              Account Number:
              {" "}
              {
                account.account.account_number
              }
            </p>

            <p>
              User ID:
              {" "}
              {
                account.account.user_id
              }
            </p>

            <p>
              Balance:
              ₹
              {
                account.account.balance
              }
            </p>

          </div>

          {/* Risk Card */}

          <div
            style={{
              background: C.card,
              padding: 20,
              marginBottom: 20,
              borderRadius: 8,
            }}
          >

            <h2>
              Risk Analysis
            </h2>

            <RiskScore
              value={
                risk.risk_score
              }
            />

            <br />
            <br />

            <Pill
              label={
                risk.decision
              }
            />

          </div>

          {/* Transactions */}

          <div
            style={{
              background: C.card,
              padding: 20,
              borderRadius: 8,
            }}
          >

            <h2>
              Transactions
            </h2>

            <table
              style={{
                width: "100%",
              }}
            >

              <thead>

                <tr>

                  <th>ID</th>

                  <th>Sender</th>

                  <th>Receiver</th>

                  <th>Amount</th>

                  <th>Risk</th>

                  <th>Status</th>

                </tr>

              </thead>

              <tbody>

                {account.transactions.map(
                  (txn) => (

                    <tr
                      key={txn.id}
                    >

                      <td>
                        {txn.id}
                      </td>

                      <td>
                        {
                          txn.sender_account
                        }
                      </td>

                      <td>
                        {
                          txn.receiver_account
                        }
                      </td>

                      <td>
                        ₹
                        {txn.amount}
                      </td>

                      <td>

                        <RiskScore
                          value={
                            txn.risk_score
                          }
                        />

                      </td>

                      <td>

                        <Pill
                          label={
                            txn.status
                          }
                        />

                      </td>

                    </tr>
                  )
                )}

              </tbody>

            </table>

          </div>

        </>
      )}

    </div>
  );
}