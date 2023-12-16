import json

from core.node import CNode
from core.edge import CEdge
from core.nodes import CNodes
from core.edges import CEdges
from core.model import CModel


nodes, edges = set(), set()
traceability = dict()


def parser(dfd_path: str, traceability_path: str) -> CModel:
    """Parser for Python files structured following the VIENNA style.
    Takes paths to dfd and traceability file, returns CModels object.
    """

    global nodes, edges, traceability

    with open(dfd_path, 'r') as dfd_file:
        dfd = dfd_file.readlines()

    with open(traceability_path, "r") as traceability_file:
        traceability_raw = json.load(traceability_file)

    node_traces, edge_traces = dict(), dict()
    for trace in traceability_raw:
        if "component" in trace.keys():
            if trace["traces"]:
                for t in trace["traces"]:
                    file = ("/").join(t["trace"]["locations"][0].split(", line ")[0].split("/")[2:])
                    try:
                        line = t["trace"]["locations"][0].split(", line ")[1]
                    except:
                        line = t["trace"]["locations"][0].split(", lines ")[1].split(" ")[0]

                    trace_link = f"https://github.com/sqshq/piggymetrics/blob/master/{file}#L{line}"
                    node_traces[trace["component"]] = trace_link
        else:
            edge = f"{trace['connectorSource']} -> {trace['connectorTarget']}"
            if trace["traces"]:
                for t in trace["traces"]:
                    file = ("/").join(t["trace"]["locations"][0].split(", line ")[0].split("/")[2:])
                    try:
                        line = t["trace"]["locations"][0].split(", line ")[1]
                    except:
                        line = t["trace"]["locations"][0].split(", lines ")[1].split(" ")[0]

                    trace_link = f"https://github.com/sqshq/piggymetrics/blob/master/{file}#L{line}"
                    edge_traces[edge] = trace_link

    traceability = {"nodes": node_traces,
                    "edges": edge_traces}

    for line_nr, line in enumerate(dfd):
        if "CClass(component" in line:
            complete_line = line.strip()
            if not ")" in line:
                count = line_nr + 1
                found = False
                while (count < len(dfd)) and (not found):
                    complete_line += dfd[count].strip()
                    if ")" in dfd[count]:
                        found = True
                    count += 1

            add_node(complete_line)

    for line_nr, line in enumerate(dfd):
        if "add_links(" in line:
            complete_line = line.strip()
            if not ")" in line:
                count = line_nr + 1
                found = False
                while (count < len(dfd)) and (not found):
                    complete_line += dfd[count].strip()
                    if ")" in dfd[count]:
                        found = True
                    count += 1
            add_edge(complete_line)
    return CModel("first_evaluation_model", CNodes(nodes), CEdges(edges))


def add_node(line: str):
    """Parses passed line from CodeableModels file and produces a node-tuple.
    """

    global nodes, traceability

    stereotypes = list()
    name = line.split("=")[0].strip()

    if "stereotype_instances" in line:
        stereotype_part = line.split("stereotype_instances")[1].split("=")[1].strip()

        if stereotype_part[0] == "[":
            stereotypes_raw = [item.strip() for item in stereotype_part.split("]")[0].split("[")[1].split(",")]
            stereotypes = list()
            client = False
            for s in stereotypes_raw:
                stereotypes.append((s, None))
                if s == "client":
                    client = True
            if client:
                stereotypes.append(("external_component", "heuristic, based on stereotype client"))
        else:
            stereotypes = list()
            stereotypes.append((stereotype_part.split(",")[0].strip(")").strip(), None))
            client = False
            for s in stereotypes:
                if s[0] == "client":
                    client = True
            if client:
                stereotypes.append(("external_component", "heuristic based on stereotype client"))

    # Traceability
    try:
        node_traceability = traceability["nodes"][name.replace("_", "-")]
    except:
        node_traceability = None

    nodes.add(CNode(name, stereotypes, node_traceability))

    return 0


def add_edge(line: str):
    """Parses passed line from CodeableModels file and produces an edge-tuple.
    """

    global edges, nodes, traceability

    stereotypes = set()

    sender = line.split("}")[0].split(":")[0].split("{")[1].strip()
    receiver = line.split("}")[0].split(":")[1].strip()
    sender_name = sender
    receiver_name = receiver

    for node in nodes:
        if node.name == sender:
            sender = node
        elif node.name == receiver:
            receiver = node

    if isinstance(sender, str):
        sender = CNode(sender, list(), None)
    if isinstance(receiver, str):
        receiver = CNode(receiver, list(), None)

    if "stereotype_instances" in line:
        stereotype_part = line.split("stereotype_instances")[1].split("=")[1].strip()

        if stereotype_part[0] == "[":
            stereotypes_raw = [item.strip() for item in stereotype_part.split("]")[0].split("[")[1].split(",")]
            stereotypes = list()

            for s in stereotypes_raw:
                stereotypes.append((s, None))

        else:
            stereotypes = list()
            stereotypes.append((stereotype_part.split(",")[0].strip(")").strip(), None))


    # Traceability
    flow = sender_name.replace("_", "-") + " -> " + receiver_name.replace("_", "-")
    try:
        edge_traceability = traceability["edges"][flow]
    except:
        edge_traceability = None

    edges.add(CEdge(sender, receiver, stereotypes, edge_traceability))

    return 0
#
