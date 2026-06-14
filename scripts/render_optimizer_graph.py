"""Render the optimizer knowledge graph to Mermaid and interactive HTML."""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCAL_PACKAGES = ROOT / ".tools" / "python-packages"
DEFAULT_DATA_DIR = ROOT / "data" / "optimizer-graph"
DEFAULT_OUT_DIR = ROOT / "outputs"

if LOCAL_PACKAGES.exists():
    sys.path.insert(0, str(LOCAL_PACKAGES))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing graph file: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_graph(data_dir: Path):
    nodes = read_csv(data_dir / "nodes.csv")
    edges = read_csv(data_dir / "edges.csv")
    return SimpleGraph(nodes, edges)


class SimpleGraph:
    def __init__(self, nodes: list[dict[str, str]], edges: list[dict[str, str]]):
        self._nodes = [(node["id"].strip(), node) for node in nodes if node.get("id", "").strip()]
        self._edges = [
            (edge["source"].strip(), edge["target"].strip(), edge)
            for edge in edges
            if edge.get("source", "").strip() and edge.get("target", "").strip()
        ]

    def nodes(self, data: bool = False):
        return self._nodes if data else [node_id for node_id, _ in self._nodes]

    def edges(self, data: bool = False):
        return self._edges if data else [(source, target) for source, target, _ in self._edges]

    def number_of_nodes(self) -> int:
        return len(self._nodes)

    def number_of_edges(self) -> int:
        return len(self._edges)


def mermaid_id(node_id: str) -> str:
    return "n_" + "".join(ch if ch.isalnum() else "_" for ch in node_id)


def write_mermaid(graph, output_path: Path) -> None:
    lines = ["flowchart LR"]
    for node_id, data in graph.nodes(data=True):
        label = data.get("label") or node_id
        node_type = data.get("type") or "node"
        safe_label = html.escape(f"{label}\\n({node_type})")
        lines.append(f'  {mermaid_id(node_id)}["{safe_label}"]')
    for source, target, data in graph.edges(data=True):
        relation = data.get("type") or "related_to"
        lines.append(f"  {mermaid_id(source)} -- {html.escape(relation)} --> {mermaid_id(target)}")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_pyvis(graph, output_path: Path) -> None:
    try:
        from pyvis.network import Network

        net = Network(height="760px", width="100%", directed=True, bgcolor="#ffffff", font_color="#1f2937")
        net.barnes_hut()
        for node_id, data in graph.nodes(data=True):
            label = data.get("label") or node_id
            node_type = data.get("type") or "node"
            title = "<br>".join(
                html.escape(part)
                for part in [
                    f"id: {node_id}",
                    f"type: {node_type}",
                    f"year: {data.get('year', '')}",
                    data.get("summary", ""),
                ]
                if part
            )
            net.add_node(node_id, label=label, title=title, group=node_type)
        for source, target, data in graph.edges(data=True):
            relation = data.get("type") or "related_to"
            title = html.escape(data.get("summary") or relation)
            net.add_edge(source, target, label=relation, title=title)
        net.write_html(str(output_path), notebook=False, open_browser=False)
    except Exception as exc:
        write_standalone_html(graph, output_path, exc)


def write_standalone_html(graph, output_path: Path, error: Exception | None = None) -> None:
    nodes = graph.nodes(data=True)
    edges = graph.edges(data=True)
    radius = 300
    center = 380
    positions = {}
    for index, (node_id, _) in enumerate(nodes):
        angle = 2 * math.pi * index / max(len(nodes), 1)
        positions[node_id] = (center + radius * math.cos(angle), center + radius * math.sin(angle))

    node_json = json.dumps([data for _, data in nodes], ensure_ascii=False)
    edge_json = json.dumps([data for _, _, data in edges], ensure_ascii=False)
    svg_edges = []
    for source, target, data in edges:
        if source not in positions or target not in positions:
            continue
        x1, y1 = positions[source]
        x2, y2 = positions[target]
        label = html.escape(data.get("type") or "related_to")
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        svg_edges.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#9ca3af" stroke-width="1.3" marker-end="url(#arrow)" />'
            f'<text x="{mx:.1f}" y="{my:.1f}" font-size="10" fill="#374151">{label}</text>'
        )
    svg_nodes = []
    for node_id, data in nodes:
        x, y = positions[node_id]
        label = html.escape(data.get("label") or node_id)
        node_type = html.escape(data.get("type") or "node")
        summary = html.escape(data.get("summary") or "")
        svg_nodes.append(
            f'<g><circle cx="{x:.1f}" cy="{y:.1f}" r="24" fill="#dbeafe" stroke="#1d4ed8" />'
            f'<title>{label} ({node_type}) - {summary}</title>'
            f'<text x="{x:.1f}" y="{y + 42:.1f}" text-anchor="middle" font-size="11" fill="#111827">{label}</text></g>'
        )
    warning = f"<p><strong>PyVis fallback:</strong> {html.escape(str(error))}</p>" if error else ""
    output_path.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Optimizer Knowledge Graph</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 24px; color: #111827; }}
    svg {{ border: 1px solid #e5e7eb; max-width: 100%; height: auto; }}
    details {{ margin-top: 16px; }}
    pre {{ white-space: pre-wrap; background: #f9fafb; padding: 12px; border: 1px solid #e5e7eb; }}
  </style>
</head>
<body>
  <h1>Optimizer Knowledge Graph</h1>
  {warning}
  <svg viewBox="0 0 760 760" role="img" aria-label="Optimizer graph">
    <defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#9ca3af" /></marker></defs>
    {''.join(svg_edges)}
    {''.join(svg_nodes)}
  </svg>
  <details><summary>Nodes JSON</summary><pre>{html.escape(node_json)}</pre></details>
  <details><summary>Edges JSON</summary><pre>{html.escape(edge_json)}</pre></details>
</body>
</html>
""",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    graph = load_graph(args.data_dir)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_mermaid(graph, args.out_dir / "optimizer-graph.mmd")
    write_pyvis(graph, args.out_dir / "optimizer-graph.html")
    print(f"nodes={graph.number_of_nodes()} edges={graph.number_of_edges()} out={args.out_dir}")


if __name__ == "__main__":
    main()
