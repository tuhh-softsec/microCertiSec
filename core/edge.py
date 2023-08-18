from core.node import CNode


class CEdge:
    """Class CEdge for edges in the model / DFD.
    Each edge is represented by its sender and receiver, stereotypes, and tagged values.
    """

    def __init__(self, sender, receiver, stereotypes, traceability):
        self.sender = sender
        self.receiver = receiver
        self.stereotypes = stereotypes
        self.traceability = traceability
        self.name = sender.name + " -> " + receiver.name

    def __str__(self):
        return f"Edge {self.name}; stereotypes {self.stereotypes}"
