
import networkx as nx

class QueryProcessor:
    def execution_order(self, graph):
        try:
            order = list(nx.topological_sort(graph))
            return order
        except:
            return []