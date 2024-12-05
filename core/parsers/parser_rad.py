import json
import sys

from core.node import CNode
from core.edge import CEdge
from core.nodes import CNodes
from core.edges import CEdges
from core.model import CModel

def parser(model_path: str, traceability_path: str) -> CModel:
    """Parser for architectural representations as created by RAD / RAD-source.
    Takes paths to input model and traceability file, returns CModels object.
    """

    nodes, edges = set(), set()


    with open(model_path, "r") as input_file:
        input = json.load(input_file)

    nodes_raw = dict()
    for rec in input["restEntityContexts"]:
        for re in rec["restEntities"]:
            service = re["applicationName"]
            if service in nodes_raw.keys():
                nodes_raw[service].add(re["path"])
            else:
                nodes_raw[service] = {re["path"]}
    
    for n in nodes_raw:
        nodes.add(CNode(n, list(), {"endpoints": nodes_raw[n]}, list()))


    return CModel("Model_parsed_from_RAD", CNodes(nodes), CEdges(edges))


if __name__ == "__main__":
    model = parser(sys.argv[1], None)
    print(model.nodes)
    print(model.edges)



#
