import { useEffect, useState, useMemo } from "react";

import ReactFlow, {
  Controls,
  MiniMap,
  Background,
  MarkerType,
} from "reactflow";

import "reactflow/dist/style.css";

import Navbar from "../components/Navbar";
import { getNetworkAnalysis } from "../services/fraudApi";

export default function NetworkAnalysis() {

  const [allNodes, setAllNodes] = useState([]);
  const [allEdges, setAllEdges] = useState([]);

  const [search, setSearch] = useState("");

  const [riskFilter, setRiskFilter] =
    useState(80);

  const loadNetwork = async () => {

    try {

      const res =
        await getNetworkAnalysis();

      const backendNodes =
        res.data.nodes.map(
          (node, index) => ({

            id: String(node.id),

            data: {
              label: (
                <div
                  style={{
                    textAlign: "center",
                    fontSize: 11,
                  }}
                >
                  <div
                    style={{
                      fontWeight: 700,
                    }}
                  >
                    {node.id}
                  </div>

                  <div>
                    Risk: {node.risk}
                  </div>
                </div>
              )
            },

            position: {
              x:
                (index % 5) * 350,
              y:
                Math.floor(index / 5) *
                220
            },

            style: {

              background:
                node.risk >= 90
                  ? "#7f1d1d"
                  : node.risk >= 80
                  ? "#78350f"
                  : "#14532d",

              color: "white",

              border:
                node.risk >= 90
                  ? "2px solid #ef4444"
                  : node.risk >= 80
                  ? "2px solid #f59e0b"
                  : "2px solid #22c55e",

              borderRadius: "12px",

              width: 180,

              padding: 12,
            }
          })
        );

      const backendEdges =
        res.data.edges.map(
          (edge, index) => ({

            id: `e${index}`,

            source:
              String(edge.from),

            target:
              String(edge.to),

            label:
              edge.amount > 50000
                ? `₹${edge.amount}`
                : "",

            animated:
              edge.amount > 50000,

            markerEnd: {
              type:
                MarkerType.ArrowClosed
            }
          })
        );

      setAllNodes(
        backendNodes
      );

      setAllEdges(
        backendEdges
      );

    } catch (err) {

      console.error(err);

    }
  };

  useEffect(() => {

    loadNetwork();

  }, []);

  const filteredNodes =
    useMemo(() => {

      return allNodes.filter(
        (node) => {

          const risk =
            parseInt(
              node.data.label.props.children[1]
                .props.children[1]
            );

          return (
            risk >= riskFilter &&
            (
              search === "" ||
              node.id
                .toLowerCase()
                .includes(
                  search.toLowerCase()
                )
            )
          );
        }
      );

    }, [
      allNodes,
      search,
      riskFilter
    ]);

  const allowedIds =
    new Set(
      filteredNodes.map(
        (n) => n.id
      )
    );

  const filteredEdges =
    allEdges.filter(
      (e) =>
        allowedIds.has(
          e.source
        ) &&
        allowedIds.has(
          e.target
        )
    );

  return (
    <div>

      <Navbar
        title="Network Analysis"
        subtitle="Money Flow & Fraud Ring Detection"
      />

      {/* Filters */}

      <div
        style={{
          display: "flex",
          gap: 12,
          marginBottom: 15,
          flexWrap: "wrap",
        }}
      >

        <input
          placeholder="Search Account Number"
          value={search}
          onChange={(e) =>
            setSearch(
              e.target.value
            )
          }
          style={{
            padding: 10,
            borderRadius: 8,
            border:
              "1px solid #334155",
            minWidth: 250
          }}
        />

        <select
          value={riskFilter}
          onChange={(e) =>
            setRiskFilter(
              Number(
                e.target.value
              )
            )
          }
          style={{
            padding: 10,
            borderRadius: 8
          }}
        >

          <option value={0}>
            All Accounts
          </option>

          <option value={50}>
            Risk ≥ 50
          </option>

          <option value={80}>
            Risk ≥ 80
          </option>

          <option value={90}>
            Risk ≥ 90
          </option>

        </select>

      </div>

      {/* Stats */}

      <div
        style={{
          display: "flex",
          gap: 20,
          marginBottom: 15,
          color: "white",
        }}
      >

        <div>
          Accounts:
          {" "}
          {filteredNodes.length}
        </div>

        <div>
          Connections:
          {" "}
          {filteredEdges.length}
        </div>

      </div>

      {/* Network */}

      <div
        style={{
          height: "75vh",
          width: "100%",
          background: "#0f172a",
          borderRadius: 12,
          overflow: "hidden",
          border:
            "1px solid #1e293b"
        }}
      >

        <ReactFlow

          nodes={filteredNodes}

          edges={filteredEdges}

          fitView

          minZoom={0.2}

          maxZoom={2}

          panOnScroll

          zoomOnScroll

          zoomOnPinch

          zoomOnDoubleClick

          attributionPosition="bottom-left"

          onNodeClick={(
            event,
            node
          ) => {

            console.log(
              "Selected:",
              node.id
            );

          }}

        >

          <MiniMap
            zoomable
            pannable
            style={{
              height: 120,
              width: 180,
            }}
          />

          <Controls
            showInteractive={
              false
            }
          />

          <Background
            gap={20}
          />

        </ReactFlow>

      </div>

    </div>
  );
}