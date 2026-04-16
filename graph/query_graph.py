import networkx as nx
import matplotlib.pyplot as plt

class QueryGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build(self, parsed_query):
        self.graph.clear()

        # Tabelas
        for table in parsed_query['from']:
            self.graph.add_node(table, type="table")

        # Seleção (WHERE)
        if parsed_query['where']:
            select_node = "SELECT_OP"
            self.graph.add_node(select_node, type="selection")

            for table in parsed_query['from']:
                self.graph.add_edge(table, select_node)
        else:
            select_node = None

        # Projeção (SELECT)
        proj_node = "PROJECTION"
        self.graph.add_node(proj_node, type="projection")

        if select_node:
            self.graph.add_edge(select_node, proj_node)
        else:
            for table in parsed_query['from']:
                self.graph.add_edge(table, proj_node)

        return self.graph

    def draw(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(
            self.graph,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=2000,
            font_size=10
        )
        plt.title("Grafo de Operadores")
        plt.show()