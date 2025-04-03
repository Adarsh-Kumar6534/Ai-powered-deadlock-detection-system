import networkx as nx

class GraphManager:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_from_table(self, table_data: list[list[str]]) -> nx.DiGraph:
        """Build graph from table data"""
        self.graph = nx.DiGraph()
        processes = ["P1", "P2", "P3", "P4", "P5"]
        
        for i in range(5):
            for j in range(5):
                if table_data[i][j] == "1":
                    self.graph.add_edge(processes[i], processes[j])
        
        return self.graph

    def get_graph(self) -> nx.DiGraph:
        return self.graph
