import yaml
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


    with open(model_path) as stream:
        try:
            input = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
        
    nodes_raw, edges_raw = dict(), set()

    for node in input["topology_template"]["node_templates"]:
        sender = node
        nodes_raw[sender] = [input["topology_template"]["node_templates"][node]["type"].split(".")[-1]]
        if input["topology_template"]["node_templates"][node]["requirements"]:
            for inter in input["topology_template"]["node_templates"][node]["requirements"]:
                receiver = inter["interaction"]
                edges_raw.add((sender, receiver))
    if "groups" in input["topology_template"]:
        if "edge" in input["topology_template"]["groups"]:
            for node in input["topology_template"]["groups"]["edge"]["members"]:
                for n in nodes_raw:
                    if node == n:
                        nodes_raw[n].append("entrypoint")

    for n in nodes_raw:
        nodes.add(CNode(n, nodes_raw[n], list(), list()))

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
    
    


    return CModel("Model_parsed_from_microMiner", CNodes(nodes), CEdges(edges))



    # groups edge is accessible from outside -> stereotype "entrypoint"



if __name__ == "__main__":
    model = parser(sys.argv[1], None)
    print(model.nodes)
    print(model.edges)



#
