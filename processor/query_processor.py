import networkx as nx

class QueryProcessor:
    def execution_order(self, graph):
        try:
            return list(nx.topological_sort(graph))
        except:
            raise ValueError("Erro ao gerar ordem de execução")