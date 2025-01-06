import json
import sys

from core.node import CNode
from core.edge import CEdge
from core.nodes import CNodes
from core.edges import CEdges
from core.model import CModel

def parser(model_path: str, traceability_path: str) -> CModel:
    """Parser for architectural representations as created by Attack Graph Generator.
    Takes paths to input model and traceability file, returns CModels object.
    """

    nodes, edges = set(), set()


    with open(model_path, "r") as input_file:
        input = json.load(input_file)

    for n in input:
        nodes.add(CNode(n, list(), list(), list()))

    for n in input:
        raw_edges = set()
        sender = n
        for e in input[n]:
            receiver = e
            raw_edges.add((sender, receiver))

        for e in raw_edges:
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

    return CModel("Model_parsed_from_attack-graph-generator", CNodes(nodes), CEdges(edges))


if __name__ == "__main__":
    model = parser(sys.argv[1], None)
    print(model.nodes)
    print(model.edges)
    



#
