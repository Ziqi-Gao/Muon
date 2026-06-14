"""Render the optimizer knowledge graph to Mermaid and interactive HTML."""

from __future__ import annotations

import argparse
import csv
import html
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
    import networkx as nx

    nodes = read_csv(data_dir / "nodes.csv")
    edges = read_csv(data_dir / "edges.csv")
    graph = nx.DiGraph()

    for node in nodes:
        node_id = node["id"].strip()
        if not node_id:
            continue
        graph.add_node(node_id, **node)

    for edge in edges:
        source = edge["source"].strip()
        target = edge["target"].strip()
        if not source or not target:
            continue
        graph.add_edge(source, target, **edge)

    return graph


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
    net.show(str(output_path), notebook=False)


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
