from enum import Enum
import networkx as nx
from core.types import DeadlockType

class DeadlockDetector:
    def detect(self, graph: nx.DiGraph) -> DeadlockType:
        """Detect and classify deadlock type"""
        if not graph or not graph.edges:
            return DeadlockType.NONE

        edges = list(graph.edges)
        edges_set = set(edges)

        if any(u == v for u, v in edges):
            return DeadlockType.MUTUAL_EXCLUSION

        if any((v, u) in edges_set for u, v in edges):
            try:
                nx.find_cycle(graph, orientation="original")
                return DeadlockType.CIRCULAR_WAIT
            except nx.NetworkXNoCycle:
                return DeadlockType.NO_PREEMPTION

        try:
            nx.find_cycle(graph, orientation="original")
            return DeadlockType.CIRCULAR_WAIT
        except nx.NetworkXNoCycle:
            pass

        for u in graph.nodes:
            outgoing = set(v for _, v in graph.out_edges(u))
            incoming = set(v for v, _ in graph.in_edges(u))
            if outgoing and incoming and u not in outgoing:
                return DeadlockType.HOLD_AND_WAIT

        return DeadlockType.NONE

    def resolve(self, graph: nx.DiGraph) -> str:
        """Attempt to resolve deadlock by breaking cycle"""
        try:
            cycle = nx.find_cycle(graph, orientation='original')
            process_to_remove = cycle[0][0]
            graph.remove_node(process_to_remove)
            return process_to_remove
        except nx.NetworkXNoCycle:
            return None
