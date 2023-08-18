
from .edge import CEdge
from .node import CNode
from .edges import CEdges
from .nodes import CNodes


class CModel:

    def __init__(self, name: str, nodes: CNodes, edges: CEdges):
        self.name = name
        self.nodes = nodes
        self.edges = edges


    def __str__(self):
        return self.name
