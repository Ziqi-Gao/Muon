"""Render the optimizer knowledge graph to readable local artifacts."""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = ROOT / "data" / "optimizer-graph"
DEFAULT_OUT_DIR = ROOT / "outputs"

LINEAGE_IDS = [
    "sgd",
    "momentum-sgd",
    "adagrad",
    "rmsprop",
    "adam",
    "adamw",
    "shampoo",
    "soap",
    "muon",
]

CLUSTER_ORDER = [
    "lineage",
    "muon_core",
    "variants",
    "theory",
    "systems",
    "applications",
    "components",
    "results",
    "other",
]

CLUSTER_META = {
    "lineage": {
        "label": "Optimizer Lineage",
        "tone": "#2563eb",
        "summary": "SGD-to-Muon historical backbone and baseline optimizers.",
    },
    "muon_core": {
        "label": "Muon Core",
        "tone": "#7c3aed",
        "summary": "Muon definition, Newton-Schulz orthogonalization, and core implementation records.",
    },
    "variants": {
        "label": "Muon Variants",
        "tone": "#0891b2",
        "summary": "Named Muon-family optimizers and method extensions.",
    },
    "theory": {
        "label": "Theory And Geometry",
        "tone": "#16a34a",
        "summary": "Convergence, spectral geometry, implicit bias, curvature, and negative results.",
    },
    "systems": {
        "label": "Systems And Scaling",
        "tone": "#d97706",
        "summary": "LLM training, distributed optimization, quantization, memory, and throughput.",
    },
    "applications": {
        "label": "Applications",
        "tone": "#db2777",
        "summary": "Fine-tuning, LoRA, MoE, ViT, scientific ML, privacy, and model editing uses.",
    },
    "components": {
        "label": "Concepts And Components",
        "tone": "#4b5563",
        "summary": "Algorithmic concepts, update components, and systems primitives.",
    },
    "results": {
        "label": "Results",
        "tone": "#dc2626",
        "summary": "Evidence/result nodes extracted from the survey graph.",
    },
    "other": {
        "label": "Other",
        "tone": "#64748b",
        "summary": "Records that do not fit a narrower view yet.",
    },
}

NETWORK_WIDTH = 1180
NETWORK_HEIGHT = 680

CLUSTER_ANCHORS = {
    "lineage": (180.0, 520.0),
    "muon_core": (520.0, 340.0),
    "variants": (805.0, 340.0),
    "theory": (635.0, 135.0),
    "systems": (900.0, 545.0),
    "applications": (390.0, 555.0),
    "components": (365.0, 225.0),
    "results": (1020.0, 170.0),
    "other": (1030.0, 420.0),
}

THEORY_TERMS = {
    "analysis",
    "analyzing",
    "bound",
    "convergence",
    "convex",
    "curvature",
    "dynamics",
    "geometry",
    "implicit",
    "inexact",
    "noise",
    "nonconvex",
    "norm",
    "provable",
    "quadratic",
    "rates",
    "saddle",
    "scaling law",
    "spectral",
    "theorem",
    "trust-region",
    "variance",
    "wasserstein",
}

SYSTEM_TERMS = {
    "batch",
    "communication",
    "distributed",
    "error feedback",
    "federated",
    "fsdp",
    "gpu",
    "large model",
    "llm",
    "memory",
    "parallel",
    "pretrain",
    "pre-training",
    "quantization",
    "scalable",
    "scaling",
    "throughput",
    "training",
}

APPLICATION_TERMS = {
    "adversarial",
    "associative memory",
    "deployment",
    "distillation",
    "dp-",
    "fine-tune",
    "finetun",
    "grokking",
    "lora",
    "moe",
    "model edit",
    "privacy",
    "scientific",
    "vit",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing graph file: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_graph(data_dir: Path) -> "SimpleGraph":
    nodes = read_csv(data_dir / "nodes.csv")
    edges = read_csv(data_dir / "edges.csv")
    sources = read_csv(data_dir / "sources.csv")
    return SimpleGraph(nodes, edges, sources)


class SimpleGraph:
    def __init__(
        self,
        nodes: list[dict[str, str]],
        edges: list[dict[str, str]],
        sources: list[dict[str, str]],
    ):
        self._nodes = [(node["id"].strip(), node) for node in nodes if node.get("id", "").strip()]
        self._edges = [
            (edge["source"].strip(), edge["target"].strip(), edge)
            for edge in edges
            if edge.get("source", "").strip() and edge.get("target", "").strip()
        ]
        self._sources = [source for source in sources if source.get("id", "").strip()]

    def nodes(self, data: bool = False):
        return self._nodes if data else [node_id for node_id, _ in self._nodes]

    def edges(self, data: bool = False):
        return self._edges if data else [(source, target) for source, target, _ in self._edges]

    def sources(self) -> list[dict[str, str]]:
        return self._sources

    def number_of_nodes(self) -> int:
        return len(self._nodes)

    def number_of_edges(self) -> int:
        return len(self._edges)


def mermaid_id(node_id: str) -> str:
    return "n_" + "".join(ch if ch.isalnum() else "_" for ch in node_id)


def text_blob(node: dict[str, str]) -> str:
    return " ".join(
        [
            node.get("id", ""),
            node.get("label", ""),
            node.get("type", ""),
            node.get("summary", ""),
        ]
    ).lower()


def has_any(text: str, terms: set[str]) -> bool:
    return any(term in text for term in terms)


def classify_node(node: dict[str, str]) -> str:
    node_id = node.get("id", "")
    node_type = node.get("type", "")
    blob = text_blob(node)

    if node_id in LINEAGE_IDS:
        return "lineage"
    if node_type in {"concept", "algorithmic_component", "system_component"}:
        return "components"
    if node_type == "result":
        return "results"
    if node_type == "method":
        return "variants"
    if has_any(blob, THEORY_TERMS):
        return "theory"
    if has_any(blob, SYSTEM_TERMS):
        return "systems"
    if has_any(blob, APPLICATION_TERMS):
        return "applications"
    if "muon" in blob or "newton-schulz" in blob or "orthogonalization" in blob:
        return "muon_core"
    return "other"


def compact(value: str, limit: int = 150) -> str:
    normalized = re.sub(r"\s+", " ", value or "").strip()
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "..."


def split_source_ids(value: str) -> list[str]:
    return [item.strip() for item in (value or "").split(";") if item.strip()]


def stable_unit(text: str, salt: int = 0) -> float:
    total = 0
    for index, char in enumerate(text):
        total += (index + 17 + salt * 13) * ord(char)
    return (math.sin(total * 12.9898 + salt * 78.233) + 1.0) / 2.0


def node_anchor(node: dict[str, str]) -> tuple[float, float]:
    node_id = node.get("id", "")
    if node_id in LINEAGE_IDS:
        index = LINEAGE_IDS.index(node_id)
        return 115.0 + index * 60.0, 560.0 - index * 28.0
    if node_id == "muon":
        return 590.0, 340.0
    return CLUSTER_ANCHORS.get(node.get("cluster", "other"), CLUSTER_ANCHORS["other"])


def apply_network_layout(nodes: list[dict[str, str]], edges: list[dict[str, str]]) -> None:
    node_lookup = {node["id"]: node for node in nodes}
    degree = Counter()
    for edge in edges:
        if edge["source"] in node_lookup and edge["target"] in node_lookup:
            degree[edge["source"]] += 1
            degree[edge["target"]] += 1

    for index, node in enumerate(nodes):
        anchor_x, anchor_y = node_anchor(node)
        cluster_count = sum(1 for item in nodes[:index] if item.get("cluster") == node.get("cluster"))
        angle = 2.0 * math.pi * stable_unit(node["id"], 1)
        ring = 30.0 + 13.0 * math.sqrt(cluster_count + 1)
        node["_x"] = anchor_x + math.cos(angle) * ring
        node["_y"] = anchor_y + math.sin(angle) * ring

    for iteration in range(260):
        cooling = 1.0 - iteration / 260.0
        displacement = {node["id"]: [0.0, 0.0] for node in nodes}

        for left_index, left in enumerate(nodes):
            for right in nodes[left_index + 1 :]:
                dx = left["_x"] - right["_x"]
                dy = left["_y"] - right["_y"]
                distance_sq = max(dx * dx + dy * dy, 16.0)
                distance = math.sqrt(distance_sq)
                same_cluster = left.get("cluster") == right.get("cluster")
                strength = 1600.0 if same_cluster else 2600.0
                force = strength / distance_sq
                push_x = dx / distance * force
                push_y = dy / distance * force
                displacement[left["id"]][0] += push_x
                displacement[left["id"]][1] += push_y
                displacement[right["id"]][0] -= push_x
                displacement[right["id"]][1] -= push_y

        for edge in edges:
            source = node_lookup.get(edge["source"])
            target = node_lookup.get(edge["target"])
            if not source or not target:
                continue
            dx = target["_x"] - source["_x"]
            dy = target["_y"] - source["_y"]
            distance = max(math.sqrt(dx * dx + dy * dy), 1.0)
            same_cluster = source.get("cluster") == target.get("cluster")
            desired = 75.0 if same_cluster else 145.0
            strength = 0.022 if same_cluster else 0.012
            force = (distance - desired) * strength
            pull_x = dx / distance * force
            pull_y = dy / distance * force
            displacement[source["id"]][0] += pull_x
            displacement[source["id"]][1] += pull_y
            displacement[target["id"]][0] -= pull_x
            displacement[target["id"]][1] -= pull_y

        for node in nodes:
            anchor_x, anchor_y = node_anchor(node)
            anchor_strength = 0.045 if node["id"] in LINEAGE_IDS else 0.017
            displacement[node["id"]][0] += (anchor_x - node["_x"]) * anchor_strength
            displacement[node["id"]][1] += (anchor_y - node["_y"]) * anchor_strength

        max_step = 26.0 * cooling + 2.0
        for node in nodes:
            dx, dy = displacement[node["id"]]
            step = max(math.sqrt(dx * dx + dy * dy), 1.0)
            scale = min(max_step, step) / step
            node["_x"] = min(max(node["_x"] + dx * scale, 34.0), NETWORK_WIDTH - 34.0)
            node["_y"] = min(max(node["_y"] + dy * scale, 34.0), NETWORK_HEIGHT - 34.0)

    for node in nodes:
        node_degree = degree[node["id"]]
        node["degree"] = node_degree
        base_radius = 5.5 + min(9.0, math.sqrt(node_degree + 1) * 1.75)
        if node.get("type") == "method":
            base_radius += 3.0
        if node["id"] in LINEAGE_IDS:
            base_radius += 2.0
        node["network_x"] = round(float(node["_x"]), 2)
        node["network_y"] = round(float(node["_y"]), 2)
        node["network_radius"] = round(base_radius, 2)
        node["label_visible"] = bool(
            node["id"] in LINEAGE_IDS
            or node.get("type") == "method"
            or node_degree >= 6
        )
        node.pop("_x", None)
        node.pop("_y", None)


def enrich_graph(graph: SimpleGraph) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    nodes = []
    for node_id, data in graph.nodes(data=True):
        enriched = dict(data)
        enriched["id"] = node_id
        enriched["cluster"] = classify_node(enriched)
        enriched["cluster_label"] = CLUSTER_META[enriched["cluster"]]["label"]
        enriched["cluster_tone"] = CLUSTER_META[enriched["cluster"]]["tone"]
        enriched["short_summary"] = compact(enriched.get("summary", ""), 180)
        enriched["source_id_list"] = split_source_ids(enriched.get("source_ids", ""))
        nodes.append(enriched)

    node_lookup = {node["id"]: node for node in nodes}
    edges = []
    for source, target, data in graph.edges(data=True):
        enriched = dict(data)
        enriched["source"] = source
        enriched["target"] = target
        enriched["source_label"] = node_lookup.get(source, {}).get("label", source)
        enriched["target_label"] = node_lookup.get(target, {}).get("label", target)
        enriched["source_cluster"] = node_lookup.get(source, {}).get("cluster", "other")
        enriched["target_cluster"] = node_lookup.get(target, {}).get("cluster", "other")
        enriched["source_id_list"] = split_source_ids(enriched.get("source_ids", ""))
        edges.append(enriched)

    apply_network_layout(nodes, edges)
    sources = [dict(source) for source in graph.sources()]
    return nodes, edges, sources


def write_mermaid(graph: SimpleGraph, output_path: Path) -> None:
    nodes, edges, _ = enrich_graph(graph)
    node_lookup = {node["id"]: node for node in nodes}
    cluster_counts = Counter(node["cluster"] for node in nodes)
    edge_counts = Counter((edge["source_cluster"], edge["target_cluster"]) for edge in edges)

    lines = ["flowchart LR", "  start[\"Optimizer history\"]"]
    previous = "start"
    for node_id in LINEAGE_IDS:
        if node_id not in node_lookup:
            continue
        node = node_lookup[node_id]
        label = html.escape(f"{node.get('label', node_id)}\\n{node.get('year', '')}")
        current = mermaid_id(node_id)
        lines.append(f'  {current}["{label}"]')
        lines.append(f"  {previous} --> {current}")
        previous = current

    lines.append('  survey["Muon survey corpus"]')
    if "muon" in node_lookup:
        lines.append(f"  {mermaid_id('muon')} --> survey")
    for cluster_id in CLUSTER_ORDER:
        if cluster_id == "lineage" or cluster_counts[cluster_id] == 0:
            continue
        meta = CLUSTER_META[cluster_id]
        current = mermaid_id(f"cluster-{cluster_id}")
        label = html.escape(f"{meta['label']}\\n{cluster_counts[cluster_id]} nodes")
        lines.append(f'  {current}["{label}"]')
        lines.append(f"  survey --> {current}")

    for (source_cluster, target_cluster), count in sorted(edge_counts.items()):
        if (
            source_cluster == target_cluster
            or source_cluster == "lineage"
            or target_cluster == "lineage"
            or count < 3
        ):
            continue
        source_id = mermaid_id(f"cluster-{source_cluster}")
        target_id = mermaid_id(f"cluster-{target_cluster}")
        lines.append(f"  {source_id} -. {count} links .-> {target_id}")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def json_script(value) -> str:
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


def source_link(source: dict[str, str]) -> str:
    url = source.get("url", "").split(";")[0].strip()
    if not url:
        return html.escape(source.get("id", ""))
    label = html.escape(source.get("id", ""))
    return f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noreferrer">{label}</a>'


def stat_card(label: str, value: int | str) -> str:
    return f'<div class="stat"><span>{html.escape(label)}</span><strong>{html.escape(str(value))}</strong></div>'


def render_timeline(nodes: list[dict[str, str]]) -> str:
    node_lookup = {node["id"]: node for node in nodes}
    items = []
    for node_id in LINEAGE_IDS:
        node = node_lookup.get(node_id)
        if not node:
            continue
        items.append(
            f"""
            <button class="timeline-item" data-node-id="{html.escape(node_id, quote=True)}">
              <span class="timeline-year">{html.escape(node.get("year", ""))}</span>
              <span class="timeline-dot"></span>
              <span class="timeline-label">{html.escape(node.get("label", node_id))}</span>
            </button>
            """
        )
    return "\n".join(items)


def render_cluster_cards(nodes: list[dict[str, str]]) -> str:
    cluster_counts = Counter(node["cluster"] for node in nodes)
    cards = []
    for cluster_id in CLUSTER_ORDER:
        count = cluster_counts[cluster_id]
        if not count:
            continue
        meta = CLUSTER_META[cluster_id]
        examples = [
            node.get("label") or node["id"]
            for node in nodes
            if node["cluster"] == cluster_id
        ][:4]
        cards.append(
            f"""
            <button class="cluster-card" data-cluster-id="{html.escape(cluster_id, quote=True)}" style="--tone:{meta['tone']}">
              <span class="cluster-count">{count}</span>
              <strong>{html.escape(meta["label"])}</strong>
              <p>{html.escape(meta["summary"])}</p>
              <small>{html.escape(" / ".join(examples))}</small>
            </button>
            """
        )
    return "\n".join(cards)


def render_network_legend(nodes: list[dict[str, str]]) -> str:
    cluster_counts = Counter(node["cluster"] for node in nodes)
    items = []
    for cluster_id in CLUSTER_ORDER:
        count = cluster_counts[cluster_id]
        if not count:
            continue
        meta = CLUSTER_META[cluster_id]
        items.append(
            f"""
            <button class="legend-item" data-cluster-id="{html.escape(cluster_id, quote=True)}">
              <span class="legend-dot" style="background:{meta['tone']}"></span>
              <span>{html.escape(meta["label"])}</span>
              <strong>{count}</strong>
            </button>
            """
        )
    return "\n".join(items)


def render_node_cards(nodes: list[dict[str, str]]) -> str:
    cards = []
    for cluster_id in CLUSTER_ORDER:
        cluster_nodes = [node for node in nodes if node["cluster"] == cluster_id]
        if not cluster_nodes:
            continue
        meta = CLUSTER_META[cluster_id]
        cluster_cards = []
        for node in sorted(cluster_nodes, key=lambda item: (item.get("year") or "9999", item.get("label") or item["id"])):
            year = node.get("year") or "n.d."
            node_type = node.get("type") or "node"
            cluster_cards.append(
                f"""
                <button class="node-card" data-node-card data-node-id="{html.escape(node["id"], quote=True)}"
                        data-type="{html.escape(node_type, quote=True)}"
                        data-cluster="{html.escape(cluster_id, quote=True)}"
                        data-search="{html.escape(text_blob(node), quote=True)}">
                  <span class="meta-row">
                    <span class="type-pill">{html.escape(node_type)}</span>
                    <span>{html.escape(year)}</span>
                  </span>
                  <strong>{html.escape(node.get("label") or node["id"])}</strong>
                  <p>{html.escape(node.get("short_summary", ""))}</p>
                </button>
                """
            )
        cards.append(
            f"""
            <section class="node-section" data-cluster-section="{html.escape(cluster_id, quote=True)}">
              <div class="section-heading" style="--tone:{meta['tone']}">
                <h2>{html.escape(meta["label"])}</h2>
                <span>{len(cluster_nodes)} nodes</span>
              </div>
              <div class="node-grid">
                {"".join(cluster_cards)}
              </div>
            </section>
            """
        )
    return "\n".join(cards)


def render_node_table(nodes: list[dict[str, str]]) -> str:
    rows = []
    for node in sorted(nodes, key=lambda item: (item.get("cluster_label", ""), item.get("year") or "9999", item.get("label") or item["id"])):
        rows.append(
            f"""
            <tr data-node-row data-node-id="{html.escape(node["id"], quote=True)}"
                data-type="{html.escape(node.get("type", ""), quote=True)}"
                data-cluster="{html.escape(node["cluster"], quote=True)}"
                data-search="{html.escape(text_blob(node), quote=True)}">
              <td>{html.escape(node.get("label") or node["id"])}</td>
              <td>{html.escape(node.get("type", ""))}</td>
              <td>{html.escape(node.get("year", ""))}</td>
              <td>{html.escape(node.get("cluster_label", ""))}</td>
              <td>{html.escape(compact(node.get("summary", ""), 130))}</td>
            </tr>
            """
        )
    return "\n".join(rows)


def render_edge_table(edges: list[dict[str, str]]) -> str:
    rows = []
    for edge in sorted(edges, key=lambda item: (item.get("type", ""), item.get("source_label", ""), item.get("target_label", ""))):
        rows.append(
            f"""
            <tr data-edge-row data-source="{html.escape(edge["source"], quote=True)}"
                data-target="{html.escape(edge["target"], quote=True)}"
                data-type="{html.escape(edge.get("type", ""), quote=True)}"
                data-confidence="{html.escape(edge.get("confidence", ""), quote=True)}">
              <td>{html.escape(edge.get("source_label", edge["source"]))}</td>
              <td>{html.escape(edge.get("type", ""))}</td>
              <td>{html.escape(edge.get("target_label", edge["target"]))}</td>
              <td>{html.escape(edge.get("confidence", ""))}</td>
              <td>{html.escape(compact(edge.get("summary", ""), 140))}</td>
            </tr>
            """
        )
    return "\n".join(rows)


def render_source_table(sources: list[dict[str, str]]) -> str:
    rows = []
    for source in sorted(sources, key=lambda item: (item.get("year") or "9999", item.get("title", ""))):
        rows.append(
            f"""
            <tr>
              <td>{source_link(source)}</td>
              <td>{html.escape(source.get("year", ""))}</td>
              <td>{html.escape(source.get("title", ""))}</td>
              <td>{html.escape(compact(source.get("venue_or_status", ""), 90))}</td>
            </tr>
            """
        )
    return "\n".join(rows)


def write_standalone_html(graph: SimpleGraph, output_path: Path) -> None:
    nodes, edges, sources = enrich_graph(graph)
    type_counts = Counter(node.get("type", "node") for node in nodes)
    edge_counts = Counter(edge.get("type", "related_to") for edge in edges)
    confidence_counts = Counter(edge.get("confidence", "") for edge in edges if edge.get("confidence"))
    cluster_counts = Counter(node["cluster"] for node in nodes)

    type_options = "\n".join(
        f'<option value="{html.escape(node_type, quote=True)}">{html.escape(node_type)} ({count})</option>'
        for node_type, count in sorted(type_counts.items())
    )
    cluster_options = "\n".join(
        f'<option value="{html.escape(cluster_id, quote=True)}">{html.escape(CLUSTER_META[cluster_id]["label"])} ({cluster_counts[cluster_id]})</option>'
        for cluster_id in CLUSTER_ORDER
        if cluster_counts[cluster_id]
    )
    edge_summary = ", ".join(f"{key}: {value}" for key, value in sorted(edge_counts.items()))
    confidence_summary = ", ".join(f"{key}: {value}" for key, value in sorted(confidence_counts.items()))

    output_path.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Optimizer Knowledge Graph</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f8fb;
      --panel: #ffffff;
      --ink: #111827;
      --muted: #5b6472;
      --line: #d9dee8;
      --soft: #eef2f7;
      --focus: #2563eb;
      --shadow: 0 12px 28px rgba(15, 23, 42, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
    }}
    button, input, select {{ font: inherit; }}
    button {{ cursor: pointer; }}
    .app {{ max-width: 1480px; margin: 0 auto; padding: 24px; }}
    .hero {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 24px;
      align-items: start;
      margin-bottom: 18px;
    }}
    h1 {{ margin: 0 0 8px; font-size: 34px; line-height: 1.1; }}
    .subtitle {{ margin: 0; color: var(--muted); max-width: 860px; line-height: 1.55; }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(4, minmax(112px, 1fr));
      gap: 10px;
      min-width: 520px;
    }}
    .stat {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      box-shadow: var(--shadow);
    }}
    .stat span {{ display: block; color: var(--muted); font-size: 12px; }}
    .stat strong {{ display: block; margin-top: 4px; font-size: 24px; }}
    .toolbar {{
      position: sticky;
      top: 0;
      z-index: 5;
      display: grid;
      grid-template-columns: minmax(220px, 1fr) 210px 260px auto;
      gap: 10px;
      padding: 12px;
      margin: 18px 0;
      background: rgba(247, 248, 251, 0.94);
      border: 1px solid var(--line);
      border-radius: 8px;
      backdrop-filter: blur(10px);
    }}
    .toolbar input, .toolbar select {{
      width: 100%;
      min-height: 42px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 0 12px;
      background: var(--panel);
      color: var(--ink);
    }}
    .toolbar button {{
      min-height: 42px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #111827;
      color: white;
      padding: 0 16px;
    }}
    .main-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 360px;
      gap: 18px;
      align-items: start;
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      padding: 18px;
      margin-bottom: 18px;
    }}
    .panel h2 {{ margin: 0 0 12px; font-size: 20px; }}
    .network-panel {{ padding: 0; overflow: hidden; }}
    .network-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 16px 18px;
      border-bottom: 1px solid var(--line);
    }}
    .network-header h2 {{ margin: 0; }}
    .network-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    .network-mode {{
      min-height: 34px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: #fff;
      color: var(--ink);
      padding: 0 12px;
      font-size: 13px;
    }}
    .network-mode.is-active {{
      border-color: #1d4ed8;
      background: #eff6ff;
      color: #1d4ed8;
      font-weight: 700;
    }}
    .network-wrap {{
      position: relative;
      height: 680px;
      background:
        radial-gradient(circle at 50% 50%, rgba(37, 99, 235, 0.08), transparent 32%),
        linear-gradient(180deg, #fbfdff 0%, #f5f7fb 100%);
      overflow: hidden;
    }}
    #networkSvg {{
      width: 100%;
      height: 100%;
      display: block;
      touch-action: none;
    }}
    .network-edge {{
      stroke: #9aa4b2;
      stroke-width: 1.15;
      stroke-opacity: 0.28;
      vector-effect: non-scaling-stroke;
    }}
    .network-edge.is-dim {{ stroke-opacity: 0.06; }}
    .network-edge.is-active {{
      stroke: #111827;
      stroke-width: 2.1;
      stroke-opacity: 0.72;
    }}
    .network-node circle {{
      stroke: #ffffff;
      stroke-width: 2.2;
      filter: drop-shadow(0 3px 5px rgba(15, 23, 42, 0.18));
      transition: stroke-width 0.15s ease, opacity 0.15s ease;
    }}
    .network-node.is-dim circle {{ opacity: 0.28; }}
    .network-node.is-active circle {{
      stroke: #111827;
      stroke-width: 4;
    }}
    .network-node text {{
      paint-order: stroke;
      stroke: rgba(255, 255, 255, 0.92);
      stroke-width: 4px;
      stroke-linejoin: round;
      fill: #111827;
      font-size: 12px;
      font-weight: 700;
      pointer-events: none;
    }}
    .network-node.is-dim text {{ opacity: 0.18; }}
    .network-tooltip {{
      position: absolute;
      max-width: 320px;
      pointer-events: none;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.96);
      box-shadow: var(--shadow);
      padding: 10px 12px;
      color: var(--ink);
      font-size: 13px;
      line-height: 1.4;
      opacity: 0;
      transform: translate(-50%, calc(-100% - 16px));
      transition: opacity 0.1s ease;
    }}
    .network-tooltip.is-visible {{ opacity: 1; }}
    .network-hint {{
      position: absolute;
      left: 16px;
      bottom: 14px;
      color: #475569;
      background: rgba(255, 255, 255, 0.84);
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 6px 10px;
      font-size: 12px;
    }}
    .network-legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      padding: 12px 16px 16px;
      border-top: 1px solid var(--line);
      background: #fff;
    }}
    .legend-item {{
      display: inline-flex;
      align-items: center;
      gap: 7px;
      min-height: 32px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: #fff;
      padding: 0 10px;
      color: var(--ink);
      font-size: 12px;
    }}
    .legend-dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.9), 0 0 0 3px rgba(15, 23, 42, 0.08);
    }}
    .legend-item strong {{ color: var(--muted); }}
    .timeline {{
      display: grid;
      grid-template-columns: repeat({max(len(LINEAGE_IDS), 1)}, minmax(88px, 1fr));
      gap: 0;
      overflow-x: auto;
      padding: 16px 6px 4px;
    }}
    .timeline-item {{
      position: relative;
      min-width: 88px;
      border: 0;
      background: transparent;
      color: var(--ink);
      text-align: center;
      padding: 0 6px 8px;
    }}
    .timeline-item::before {{
      content: "";
      position: absolute;
      left: 0;
      right: 0;
      top: 42px;
      border-top: 2px solid #b7c2d3;
    }}
    .timeline-item:first-child::before {{ left: 50%; }}
    .timeline-item:last-child::before {{ right: 50%; }}
    .timeline-year {{ display: block; height: 24px; color: var(--muted); font-size: 12px; }}
    .timeline-dot {{
      position: relative;
      z-index: 1;
      display: inline-block;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      border: 3px solid #2563eb;
      background: white;
      margin: 10px 0;
    }}
    .timeline-label {{
      display: block;
      min-height: 36px;
      font-weight: 700;
      font-size: 13px;
      line-height: 1.25;
    }}
    .cluster-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 12px;
    }}
    .cluster-card {{
      min-height: 154px;
      border: 1px solid var(--line);
      border-top: 4px solid var(--tone);
      border-radius: 8px;
      background: #fff;
      padding: 14px;
      text-align: left;
    }}
    .cluster-card:hover, .node-card:hover, tr[data-node-row]:hover, tr[data-edge-row]:hover {{
      outline: 2px solid rgba(37, 99, 235, 0.2);
    }}
    .cluster-count {{
      float: right;
      color: var(--tone);
      font-weight: 800;
      font-size: 24px;
    }}
    .cluster-card strong {{ display: block; margin-bottom: 8px; }}
    .cluster-card p {{ margin: 0 0 10px; color: var(--muted); font-size: 13px; line-height: 1.4; }}
    .cluster-card small {{ color: #374151; line-height: 1.4; }}
    .section-heading {{
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: baseline;
      border-left: 4px solid var(--tone);
      padding-left: 10px;
      margin: 6px 0 12px;
    }}
    .section-heading h2 {{ margin: 0; }}
    .section-heading span {{ color: var(--muted); }}
    .node-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
      gap: 10px;
    }}
    .node-card {{
      display: flex;
      min-height: 146px;
      flex-direction: column;
      gap: 8px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fff;
      color: var(--ink);
      padding: 12px;
      text-align: left;
      overflow: hidden;
    }}
    .node-card.is-hidden, tr.is-hidden, .node-section.is-hidden {{ display: none; }}
    .meta-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      color: var(--muted);
      font-size: 12px;
    }}
    .type-pill {{
      display: inline-flex;
      align-items: center;
      max-width: 145px;
      height: 24px;
      padding: 0 8px;
      border-radius: 999px;
      background: var(--soft);
      color: #334155;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .node-card strong {{
      line-height: 1.25;
      overflow-wrap: anywhere;
    }}
    .node-card p {{
      margin: 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.42;
      display: -webkit-box;
      -webkit-line-clamp: 4;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .side-panel {{
      position: sticky;
      top: 86px;
      max-height: calc(100vh - 104px);
      overflow: auto;
    }}
    .detail-title {{ margin: 0 0 8px; font-size: 20px; line-height: 1.25; }}
    .detail-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 12px;
    }}
    .detail-meta span {{
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 4px 8px;
      color: #334155;
      background: #f8fafc;
      font-size: 12px;
    }}
    .detail-summary {{ color: var(--muted); line-height: 1.5; }}
    .relation-list {{
      display: grid;
      gap: 8px;
      margin-top: 12px;
    }}
    .relation {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px;
      background: #fbfcfe;
      font-size: 13px;
      line-height: 1.4;
    }}
    .relation strong {{ display: block; margin-bottom: 4px; }}
    .source-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 12px;
    }}
    .source-links a {{
      color: #1d4ed8;
      border: 1px solid #bfdbfe;
      background: #eff6ff;
      border-radius: 999px;
      padding: 4px 8px;
      text-decoration: none;
      font-size: 12px;
    }}
    .table-wrap {{ overflow: auto; border: 1px solid var(--line); border-radius: 8px; }}
    table {{ width: 100%; min-width: 920px; border-collapse: collapse; background: #fff; }}
    th, td {{ border-bottom: 1px solid var(--line); padding: 10px 12px; text-align: left; vertical-align: top; }}
    th {{ position: sticky; top: 0; background: #f8fafc; font-size: 12px; color: #475569; }}
    td {{ font-size: 13px; line-height: 1.4; }}
    .summary-line {{
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
      margin: 8px 0 0;
    }}
    @media (max-width: 1100px) {{
      .hero, .main-grid {{ grid-template-columns: 1fr; }}
      .stats {{ min-width: 0; grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .side-panel {{ position: static; max-height: none; }}
      .toolbar {{ grid-template-columns: 1fr 1fr; }}
    }}
    @media (max-width: 680px) {{
      .app {{ padding: 14px; }}
      h1 {{ font-size: 28px; }}
      .stats, .toolbar {{ grid-template-columns: 1fr; }}
      .node-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main class="app">
    <header class="hero">
      <div>
        <h1>Optimizer Knowledge Graph</h1>
        <p class="subtitle">A structured view of the SGD-to-Muon lineage, Muon survey corpus, topic clusters, and evidence-backed relationships.</p>
      </div>
      <div class="stats">
        {stat_card("Nodes", len(nodes))}
        {stat_card("Edges", len(edges))}
        {stat_card("Sources", len(sources))}
        {stat_card("Muon papers", cluster_counts["muon_core"] + cluster_counts["theory"] + cluster_counts["systems"] + cluster_counts["applications"])}
      </div>
    </header>

    <section class="toolbar" aria-label="Graph filters">
      <input id="searchBox" type="search" placeholder="Search nodes, papers, concepts" />
      <select id="typeFilter">
        <option value="all">All types ({len(nodes)})</option>
        {type_options}
      </select>
      <select id="clusterFilter">
        <option value="all">All clusters ({len(nodes)})</option>
        {cluster_options}
      </select>
      <button id="resetButton" type="button">Reset</button>
    </section>

    <section class="panel network-panel">
      <div class="network-header">
        <h2>Relationship Network</h2>
        <div class="network-actions" aria-label="Network view modes">
          <button class="network-mode is-active" type="button" data-network-mode="all">All nodes</button>
          <button class="network-mode" type="button" data-network-mode="core">Core map</button>
          <button class="network-mode" type="button" data-network-mode="papers">Papers only</button>
          <button class="network-mode" type="button" data-network-mode="reset-view">Reset view</button>
        </div>
      </div>
      <div class="network-wrap" id="networkWrap">
        <svg id="networkSvg" viewBox="0 0 {NETWORK_WIDTH} {NETWORK_HEIGHT}" role="img" aria-label="Optimizer relationship network">
          <g id="networkViewport">
            <g id="networkEdges"></g>
            <g id="networkNodes"></g>
          </g>
        </svg>
        <div class="network-tooltip" id="networkTooltip"></div>
        <div class="network-hint">Scroll to zoom, drag empty space to pan, click a node to inspect relationships.</div>
      </div>
      <div class="network-legend">
        {render_network_legend(nodes)}
      </div>
    </section>

    <section class="main-grid">
      <div>
        <section class="panel">
          <h2>Lineage Backbone</h2>
          <div class="timeline">
            {render_timeline(nodes)}
          </div>
        </section>

        <section class="panel">
          <h2>Topic Map</h2>
          <div class="cluster-grid">
            {render_cluster_cards(nodes)}
          </div>
          <p class="summary-line">Edge types: {html.escape(edge_summary)}</p>
          <p class="summary-line">Edge confidence: {html.escape(confidence_summary)}</p>
        </section>

        <section class="panel">
          <div class="section-heading" style="--tone:#2563eb">
            <h2>Node Browser</h2>
            <span id="visibleCount">{len(nodes)} visible</span>
          </div>
          <div id="nodeSections">
            {render_node_cards(nodes)}
          </div>
        </section>
      </div>

      <aside class="panel side-panel" id="detailPanel">
        <h2 class="detail-title">Muon</h2>
        <div class="detail-meta"><span>method</span><span>2024</span><span>Optimizer Lineage</span></div>
        <p class="detail-summary">Momentum update for 2D hidden-layer parameters orthogonalized by Newton-Schulz.</p>
        <div class="relation-list"></div>
      </aside>
    </section>

    <section class="panel">
      <div class="section-heading" style="--tone:#0891b2">
        <h2>All Nodes</h2>
        <span id="visibleTableCount">{len(nodes)} rows</span>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Node</th><th>Type</th><th>Year</th><th>Cluster</th><th>Summary</th></tr></thead>
          <tbody>{render_node_table(nodes)}</tbody>
        </table>
      </div>
    </section>

    <section class="panel">
      <h2>Relationships</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Source</th><th>Relation</th><th>Target</th><th>Confidence</th><th>Evidence note</th></tr></thead>
          <tbody>{render_edge_table(edges)}</tbody>
        </table>
      </div>
    </section>

    <section class="panel">
      <h2>Sources</h2>
      <div class="table-wrap">
        <table>
          <thead><tr><th>ID</th><th>Year</th><th>Title</th><th>Venue / Status</th></tr></thead>
          <tbody>{render_source_table(sources)}</tbody>
        </table>
      </div>
    </section>
  </main>

  <script>
    const nodes = {json_script(nodes)};
    const edges = {json_script(edges)};
    const sources = {json_script(sources)};
    const nodeById = new Map(nodes.map(node => [node.id, node]));
    const sourceById = new Map(sources.map(source => [source.id, source]));
    const networkWidth = {NETWORK_WIDTH};
    const networkHeight = {NETWORK_HEIGHT};

    const searchBox = document.getElementById("searchBox");
    const typeFilter = document.getElementById("typeFilter");
    const clusterFilter = document.getElementById("clusterFilter");
    const resetButton = document.getElementById("resetButton");
    const visibleCount = document.getElementById("visibleCount");
    const visibleTableCount = document.getElementById("visibleTableCount");
    const detailPanel = document.getElementById("detailPanel");
    const networkSvg = document.getElementById("networkSvg");
    const networkViewport = document.getElementById("networkViewport");
    const networkEdges = document.getElementById("networkEdges");
    const networkNodes = document.getElementById("networkNodes");
    const networkTooltip = document.getElementById("networkTooltip");
    const networkWrap = document.getElementById("networkWrap");
    const networkModeButtons = [...document.querySelectorAll("[data-network-mode]")];
    let networkMode = "all";
    let selectedNodeId = "muon";
    let networkTransform = {{ x: 0, y: 0, scale: 1 }};
    let isPanning = false;
    let panStart = {{ x: 0, y: 0 }};

    function normalize(value) {{
      return String(value || "").toLowerCase();
    }}

    function escapeHtml(value) {{
      const entities = {{ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }};
      return String(value ?? "").replace(/[&<>"']/g, char => entities[char]);
    }}

    function nodePassesControls(node) {{
      const query = normalize(searchBox.value).trim();
      const type = typeFilter.value;
      const cluster = clusterFilter.value;
      const searchText = normalize([node.id, node.label, node.type, node.summary, node.cluster_label].join(" "));
      const passesSearch = !query || searchText.includes(query);
      const passesType = type === "all" || node.type === type;
      const passesCluster = cluster === "all" || node.cluster === cluster;
      if (!(passesSearch && passesType && passesCluster)) return false;
      if (networkMode === "papers") return node.type === "paper";
      if (networkMode === "core") {{
        return node.cluster === "lineage"
          || node.cluster === "muon_core"
          || node.type === "method"
          || node.degree >= 6;
      }}
      return true;
    }}

    function connectedToSelected(edge) {{
      return edge.source === selectedNodeId || edge.target === selectedNodeId;
    }}

    function updateNetworkTransform() {{
      networkViewport.setAttribute("transform", `translate(${{networkTransform.x}} ${{networkTransform.y}}) scale(${{networkTransform.scale}})`);
    }}

    function resetNetworkView() {{
      networkTransform = {{ x: 0, y: 0, scale: 1 }};
      updateNetworkTransform();
    }}

    function networkColor(node) {{
      return node.cluster_tone || "#64748b";
    }}

    function edgeOpacity(edge) {{
      if (!selectedNodeId) return 0.28;
      return connectedToSelected(edge) ? 0.72 : 0.08;
    }}

    function shouldShowNetworkLabel(node) {{
      if (node.id === selectedNodeId) return true;
      if (networkMode === "papers") return node.degree >= 5;
      return Boolean(node.label_visible);
    }}

    function renderNetwork() {{
      const visibleNodes = nodes.filter(nodePassesControls);
      const visibleIds = new Set(visibleNodes.map(node => node.id));
      const visibleEdges = edges.filter(edge => visibleIds.has(edge.source) && visibleIds.has(edge.target));
      networkEdges.innerHTML = visibleEdges.map(edge => {{
        const source = nodeById.get(edge.source);
        const target = nodeById.get(edge.target);
        if (!source || !target) return "";
        const active = selectedNodeId && connectedToSelected(edge);
        return `<line class="network-edge ${{active ? "is-active" : selectedNodeId ? "is-dim" : ""}}"
          x1="${{source.network_x}}" y1="${{source.network_y}}"
          x2="${{target.network_x}}" y2="${{target.network_y}}"
          data-source="${{edge.source}}" data-target="${{edge.target}}"
          style="stroke-opacity:${{edgeOpacity(edge)}}"></line>`;
      }}).join("");

      const activeNeighborIds = new Set();
      if (selectedNodeId) {{
        visibleEdges.forEach(edge => {{
          if (edge.source === selectedNodeId) activeNeighborIds.add(edge.target);
          if (edge.target === selectedNodeId) activeNeighborIds.add(edge.source);
        }});
      }}
      networkNodes.innerHTML = visibleNodes.map(node => {{
        const active = node.id === selectedNodeId || activeNeighborIds.has(node.id);
        const dim = selectedNodeId && !active;
        const label = shouldShowNetworkLabel(node)
          ? `<text x="${{node.network_x}}" y="${{Number(node.network_y) + Number(node.network_radius) + 15}}" text-anchor="middle">${{escapeHtml(node.label || node.id)}}</text>`
          : "";
        return `<g class="network-node ${{active ? "is-active" : ""}} ${{dim ? "is-dim" : ""}}"
            data-node-id="${{node.id}}" transform="translate(0 0)">
          <circle cx="${{node.network_x}}" cy="${{node.network_y}}" r="${{node.network_radius}}"
            fill="${{networkColor(node)}}" data-node-id="${{node.id}}"></circle>
          ${{label}}
        </g>`;
      }}).join("");

      networkNodes.querySelectorAll("[data-node-id]").forEach(element => {{
        const id = element.dataset.nodeId;
        element.addEventListener("click", event => {{
          event.stopPropagation();
          selectNode(id);
        }});
        element.addEventListener("pointerenter", event => showNetworkTooltip(event, id));
        element.addEventListener("pointermove", event => positionNetworkTooltip(event));
        element.addEventListener("pointerleave", hideNetworkTooltip);
      }});
    }}

    function showNetworkTooltip(event, id) {{
      const node = nodeById.get(id);
      if (!node) return;
      networkTooltip.innerHTML = `<strong>${{escapeHtml(node.label || node.id)}}</strong><br>${{escapeHtml(node.cluster_label)}} - ${{escapeHtml(node.type || "node")}} - degree ${{node.degree || 0}}`;
      networkTooltip.classList.add("is-visible");
      positionNetworkTooltip(event);
    }}

    function positionNetworkTooltip(event) {{
      const rect = networkWrap.getBoundingClientRect();
      networkTooltip.style.left = `${{event.clientX - rect.left}}px`;
      networkTooltip.style.top = `${{event.clientY - rect.top}}px`;
    }}

    function hideNetworkTooltip() {{
      networkTooltip.classList.remove("is-visible");
    }}

    function nodeMatches(element) {{
      const query = normalize(searchBox.value).trim();
      const type = typeFilter.value;
      const cluster = clusterFilter.value;
      const searchText = normalize(element.dataset.search);
      return (!query || searchText.includes(query))
        && (type === "all" || element.dataset.type === type)
        && (cluster === "all" || element.dataset.cluster === cluster);
    }}

    function applyFilters() {{
      let cardCount = 0;
      document.querySelectorAll("[data-node-card]").forEach(card => {{
        const show = nodeMatches(card);
        card.classList.toggle("is-hidden", !show);
        if (show) cardCount += 1;
      }});
      document.querySelectorAll("[data-cluster-section]").forEach(section => {{
        const hasVisibleCard = Boolean(section.querySelector("[data-node-card]:not(.is-hidden)"));
        section.classList.toggle("is-hidden", !hasVisibleCard);
      }});

      let rowCount = 0;
      document.querySelectorAll("[data-node-row]").forEach(row => {{
        const show = nodeMatches(row);
        row.classList.toggle("is-hidden", !show);
        if (show) rowCount += 1;
      }});
      visibleCount.textContent = `${{cardCount}} visible`;
      visibleTableCount.textContent = `${{rowCount}} rows`;
      renderNetwork();
    }}

    function sourceLinks(sourceIds) {{
      const ids = Array.isArray(sourceIds) ? sourceIds : [];
      if (!ids.length) return "";
      const links = ids.map(id => {{
      const source = sourceById.get(id);
        if (!source) return `<span>${{escapeHtml(id)}}</span>`;
        const url = String(source.url || "").split(";")[0].trim();
        if (!url) return `<span>${{escapeHtml(source.id)}}</span>`;
        return `<a href="${{escapeHtml(url)}}" target="_blank" rel="noreferrer">${{escapeHtml(source.id)}}</a>`;
      }}).join("");
      return `<div class="source-links">${{links}}</div>`;
    }}

    function renderRelation(edge, direction) {{
      const otherId = direction === "out" ? edge.target : edge.source;
      const other = nodeById.get(otherId);
      const heading = direction === "out"
        ? `${{edge.type}} -> ${{edge.target_label || otherId}}`
        : `${{edge.source_label || otherId}} -> ${{edge.type}}`;
      const summary = edge.summary ? `<div>${{escapeHtml(edge.summary)}}</div>` : "";
      const confidence = edge.confidence ? `<small>confidence: ${{escapeHtml(edge.confidence)}}</small>` : "";
      const year = other && other.year ? ` - ${{other.year}}` : "";
      return `<div class="relation"><strong>${{escapeHtml(heading)}}</strong><div>${{escapeHtml(other ? other.cluster_label : "Unknown")}}${{escapeHtml(year)}}</div>${{summary}}${{confidence}}${{sourceLinks(edge.source_id_list)}}</div>`;
    }}

    function selectNode(id) {{
      const node = nodeById.get(id);
      if (!node) return;
      selectedNodeId = id;
      const outgoing = edges.filter(edge => edge.source === id);
      const incoming = edges.filter(edge => edge.target === id);
      const relationHtml = [
        ...outgoing.map(edge => renderRelation(edge, "out")),
        ...incoming.map(edge => renderRelation(edge, "in")),
      ].join("");
      detailPanel.innerHTML = `
        <h2 class="detail-title">${{escapeHtml(node.label || node.id)}}</h2>
        <div class="detail-meta">
          <span>${{escapeHtml(node.type || "node")}}</span>
          <span>${{escapeHtml(node.year || "n.d.")}}</span>
          <span>${{escapeHtml(node.cluster_label)}}</span>
          <span>${{escapeHtml(node.id)}}</span>
        </div>
        <p class="detail-summary">${{escapeHtml(node.summary || "")}}</p>
        ${{sourceLinks(node.source_id_list)}}
        <div class="relation-list">${{relationHtml || '<div class="relation">No direct relationships recorded.</div>'}}</div>
      `;
      renderNetwork();
    }}

    document.querySelectorAll("[data-node-id]").forEach(element => {{
      element.addEventListener("click", () => selectNode(element.dataset.nodeId));
    }});
    document.querySelectorAll("[data-cluster-id]").forEach(element => {{
      element.addEventListener("click", () => {{
        clusterFilter.value = element.dataset.clusterId;
        applyFilters();
      }});
    }});
    [searchBox, typeFilter, clusterFilter].forEach(element => {{
      element.addEventListener("input", applyFilters);
      element.addEventListener("change", applyFilters);
    }});
    resetButton.addEventListener("click", () => {{
      searchBox.value = "";
      typeFilter.value = "all";
      clusterFilter.value = "all";
      applyFilters();
    }});

    networkModeButtons.forEach(button => {{
      button.addEventListener("click", () => {{
        const mode = button.dataset.networkMode;
        if (mode === "reset-view") {{
          resetNetworkView();
          return;
        }}
        networkMode = mode;
        networkModeButtons.forEach(item => item.classList.toggle("is-active", item.dataset.networkMode === networkMode));
        renderNetwork();
      }});
    }});

    networkSvg.addEventListener("click", () => {{
      selectedNodeId = "";
      renderNetwork();
    }});

    networkSvg.addEventListener("wheel", event => {{
      event.preventDefault();
      const rect = networkSvg.getBoundingClientRect();
      const viewX = (event.clientX - rect.left) / rect.width * networkWidth;
      const viewY = (event.clientY - rect.top) / rect.height * networkHeight;
      const beforeX = (viewX - networkTransform.x) / networkTransform.scale;
      const beforeY = (viewY - networkTransform.y) / networkTransform.scale;
      const factor = event.deltaY < 0 ? 1.12 : 0.89;
      const nextScale = Math.min(3.2, Math.max(0.52, networkTransform.scale * factor));
      networkTransform.x = viewX - beforeX * nextScale;
      networkTransform.y = viewY - beforeY * nextScale;
      networkTransform.scale = nextScale;
      updateNetworkTransform();
    }}, {{ passive: false }});

    networkSvg.addEventListener("pointerdown", event => {{
      if (event.target.dataset.nodeId) return;
      isPanning = true;
      panStart = {{ x: event.clientX - networkTransform.x, y: event.clientY - networkTransform.y }};
      networkSvg.setPointerCapture(event.pointerId);
    }});

    networkSvg.addEventListener("pointermove", event => {{
      if (!isPanning) return;
      networkTransform.x = event.clientX - panStart.x;
      networkTransform.y = event.clientY - panStart.y;
      updateNetworkTransform();
    }});

    networkSvg.addEventListener("pointerup", event => {{
      isPanning = false;
      try {{ networkSvg.releasePointerCapture(event.pointerId); }} catch (error) {{}}
    }});

    networkSvg.addEventListener("pointerleave", () => {{
      isPanning = false;
      hideNetworkTooltip();
    }});

    selectNode("muon");
    applyFilters();
  </script>
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
    write_standalone_html(graph, args.out_dir / "optimizer-graph.html")
    print(f"nodes={graph.number_of_nodes()} edges={graph.number_of_edges()} out={args.out_dir}")


if __name__ == "__main__":
    main()
