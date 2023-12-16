import json

from core.node import CNode
from core.edge import CEdge
from core.nodes import CNodes
from core.edges import CEdges
from core.model import CModel
from core.parsers.parser_tuhh_json import parser as parser_tuhh_json
from core.parsers.parser_vienna_python import parser as parser_vienna_python


nodes, edges = set(), set()
traceability = dict()


def load_model(dfd_path: str, traceability_path: str = None, parser: str = "TUHH"):
    """Loads CodeableModels file and instantiates Node and Edge objects for each item.
    """

    global nodes, edges, traceability

    if parser == "TUHH":
        return parser_tuhh_json(dfd_path, traceability_path)
    elif parser == "VIENNA":
        return parser_vienna_python(dfd_path, traceability_path)
    if traceability_path:
        with open(traceability_path, 'r') as traceability_file:
            traceability = json.load(traceability_file)

    with open(dfd_path, 'r') as dfd_file:
        codeable_models = dfd_file.readlines()

    # Parse nodes
    for line_nr, line in enumerate(codeable_models):
        if "CClass(external_component" in line:
            add_node(line, "external_entity")
        elif "CClass(service" in line:
            add_node(line, "service")
        elif "CClass(component" in line:
            complete_line = line.strip()
            if not ")" in line:
                count = line_nr + 1
                found = False
                while (count < len(codeable_models)) and (not found):
                    complete_line += codeable_models[count].strip()
                    if ")" in codeable_models[count]:
                        found = True
                    count += 1
            add_node(complete_line, "service")

    # Parse edges
    for line_nr, line in enumerate(codeable_models):
        if "add_links(" in line:
            complete_line = line.strip()
            if not ")" in line:
                count = line_nr + 1
                found = False
                while (count < len(codeable_models)) and (not found):
                    complete_line += codeable_models[count].strip()
                    if ")" in codeable_models[count]:
                        found = True
                    count += 1

            add_edge(complete_line)

    nodes = CNodes(nodes)
    edges = CEdges(edges)

    nodes = set_edges(nodes, edges)
    model = CModel("testmodel", nodes, edges)

    return model


def set_edges(nodes, edges):
    """Sets the edges variable in CNode objects.
    """

    for edge in edges:
        sender = edge.sender.name
        for node in nodes:
            if node.name == sender:
                node.edges.add(edge)

    return nodes


def parser_vienna():
    pass


def add_node(line: str, type: str):
    """Parses passed line from CodeableModels file and produces a node-tuple.
    """

    global nodes, traceability

    stereotypes = list()


    name = line.split("=")[0].strip()
    if "stereotype_instances" in line:
        stereotype_part = line.split("stereotype_instances")[1].split("=")[1].strip()

        if stereotype_part[0] == "[":
            stereotypes = [item.strip() for item in stereotype_part.split("]")[0].split("[")[1].split(",")]
        else:
            stereotypes = list()
            stereotypes.append(stereotype_part.split(",")[0].strip(")").strip())

    # Traceability
    try:
        node_traceability = traceability["nodes"][name.replace("_", "-")]
    except:
        node_traceability = "No traceability found."

    stereotypes.append(type)

    nodes.add(CNode(name, stereotypes, node_traceability))

    return 0


def add_edge(line: str):
    """Parses passed line from CodeableModels file and produces an edge-tuple.
    """

    global edges, nodes

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
        sender = CNode(sender, list(), "No traceability found.")
    if isinstance(receiver, str):
        receiver = CNode(receiver, list(), "No traceability found.")


    if "stereotype_instances" in line:
        stereotype_part = line.split("stereotype_instances")[1].split("=")[1].strip()

        if stereotype_part[0] == "[":
            stereotypes = [item.strip() for item in stereotype_part.split("]")[0].split("[")[1].split(",")]
        else:
            stereotypes = list()
            stereotypes.append(stereotype_part.split(",")[0].strip(")").strip())

    # Traceability
    flow = sender_name + " -> " + receiver_name
    try:
        edge_traceability = traceability["edges"][flow]
    except:
        edge_traceability = "No traceability found."

    edges.add(CEdge(sender, receiver, stereotypes, edge_traceability))

    return
