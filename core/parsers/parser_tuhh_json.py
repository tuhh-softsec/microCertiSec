import json

from core.node import CNode
from core.edge import CEdge
from core.nodes import CNodes
from core.edges import CEdges
from core.model import CModel

def parser(dfd_path: str, traceability_path: str) -> CModel:
    """Parser for JSON files structured following the TUHH style.
    Takes paths to dfd and traceability file, returns CModels object.
    """

    nodes, edges = set(), set()

    with open(dfd_path, "r") as dfd_file:
        dfd = json.load(dfd_file)

    with open(traceability_path, "r") as traceability_file:
        traceability = json.load(traceability_file)

    for node in dfd["services"]:
        stereotypes = node["stereotypes"]
        for id, stereotype in enumerate(stereotypes):
            stereotypes[id] = (stereotype, "traceability")
        stereotypes.append(("service", "traceability"))
        node_traceability = "traceability"
        connected_nodes = [i["receiver"] for i in dfd["information_flows"] if i["sender"] == node["name"]]

        nodes.add(CNode(node["name"], stereotypes, node_traceability, connected_nodes))

    for node in dfd["external_entities"]:
        stereotypes = node["stereotypes"]
        for id, stereotype in enumerate(stereotypes):
            stereotypes[id] = (stereotype, "traceability")
        stereotypes.append(("external_entity", "traceability"))
        node_traceability = "traceability"
        nodes.add(CNode(node["name"], stereotypes, node_traceability))


    for information_flow in dfd["information_flows"]:
        stereotypes = information_flow["stereotypes"]
        for id, stereotype in enumerate(stereotypes):
            stereotypes[id] = (stereotype, "traceability")
        tagged_values = information_flow["tagged_values"]
        for t in tagged_values:
            if t == "Protocol" and tagged_values[t] == "HTTPS":
                stereotypes.append(("encrypted", "traceability"))
        flow_traceability = "traceability"

        for node in nodes:
            if node.name == information_flow["sender"]:
                sender = node
            elif node.name == information_flow["receiver"]:
                receiver = node

        if isinstance(sender, str):
            sender = CNode(information_flow["sender"], list(), "No traceability found.")
        if isinstance(receiver, str):
            receiver = CNode(information_flow["receiver"], list(), "No traceability found.")

        edges.add(CEdge(sender, receiver, stereotypes, flow_traceability))

    # Replacing node names in connected_nodes with corresponding CNode objects
    for node1 in nodes:
        for node2 in nodes:
            if node2.name in node1.connected_nodes:
                node1.connected_nodes.append(node2)
                node1.connected_nodes.remove(node2.name)

    return CModel("testmodel", CNodes(nodes), CEdges(edges))



#
