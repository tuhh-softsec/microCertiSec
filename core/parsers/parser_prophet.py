import json
import sys

from core.node import CNode
from core.edge import CEdge
from core.nodes import CNodes
from core.edges import CEdges
from core.model import CModel

def parser(model_path: str, traceability_path: str) -> CModel:
    """Parser for architectural representations as created by Prophet.
    Takes paths to input model and traceability file, returns CModels object.
    """

    nodes, edges = set(), set()
    nodes_raw, edges_raw = set(), set()

    with open(model_path, "r") as input_file:
        input = json.load(input_file)

    if "communication" in input["global"] and input["global"]["communication"]:
        flows = [x for x in input["global"]["communication"].split("\n") if x][1:]
        for f in flows:
            try:
                sender = f.split("-->")[0]
                receiver = f.split("|")[2]

                nodes_raw.add(sender)
                nodes_raw.add(receiver)
                edges_raw.add((sender, receiver))
            except Exception as e:
                print(e)

    services = input["ms"]
    for s in services:
        nodes_raw.add(s["name"])


    for n in nodes_raw:
        nodes.add(CNode(n, list(), list(), list()))
    for e in edges_raw:
        for node in nodes:
            if node.name == e[0]:
                sender = node
            elif node.name == e[1]:
                receiver = node
        if isinstance(sender, str):
            sender = CNode(sender, list(), list(), list())
        if isinstance(receiver, str):
            receiver = CNode(receiver, list(), list(), list())

    
        edges.add(CEdge(sender, receiver, list(), list()))

    return CModel("Model_parsed_from_prophet", CNodes(nodes), CEdges(edges))


if __name__ == "__main__":
    model = parser(sys.argv[1], None)
    print(model.nodes)
    print(model.edges)



#
