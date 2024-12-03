import sys
from pygraphml import GraphMLParser

from core.node import CNode
from core.edge import CEdge
from core.nodes import CNodes
from core.edges import CEdges
from core.model import CModel

def parser(model_path: str, traceability_path: str) -> CModel:
    """Parser for architectural representations as created by MicroDepGraph.
    Takes paths to input model and traceability file, returns CModels object.
    """

    nodes, edges = set(), set()

    gmlparser = GraphMLParser()
    g = gmlparser.parse(model_path)

    # Nodes
    ml_nodes = g._nodes
    for n in ml_nodes:
        nodes.add(CNode(n.id, list(), list(), list()))


    # Edges 
    ml_edges = g._edges    
    for e in ml_edges:
        sender = e.node1.id
        receiver = e.node2.id
        for node in nodes:
            if node.name == sender:
                sender = node
            elif node.name == receiver:
                receiver = node
        if isinstance(sender, str):
            sender = CNode(sender, list(), list(), list())
        if isinstance(receiver, str):
            receiver = CNode(receiver, list(), list(), list())
        edges.add(CEdge(sender, receiver, list(), list()))

    return CModel("Model_parsed_from_MicroDepGraph", CNodes(nodes), CEdges(edges))


if __name__ == "__main__":
    model = parser(sys.argv[1], None)
    print(model.nodes)
    print(model.edges)



#
