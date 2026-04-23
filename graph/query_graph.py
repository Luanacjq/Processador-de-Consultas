import networkx as nx
import matplotlib.pyplot as plt

class QueryGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build(self, parsed_query):
        self.graph.clear()

        tables = parsed_query["from"]
        conditions = parsed_query["where"]

        # TABELAS
        for table in tables:
            self.graph.add_node(table, type="table")

        last_nodes = tables.copy()

        # SELEÇÃO (reduz tuplas)
        if conditions:
            selection_nodes = []

            for i, cond in enumerate(conditions):
                node = f"SELECT_{i}"
                self.graph.add_node(node, type="selection", condition=cond)

                for table in tables:
                    self.graph.add_edge(table, node)

                selection_nodes.append(node)

            last_nodes = selection_nodes

        # JOIN
        if len(last_nodes) > 1:
            join_node = "JOIN"
            self.graph.add_node(join_node, type="join")

            for node in last_nodes:
                self.graph.add_edge(node, join_node)

            last_nodes = [join_node]

        # PROJEÇÃO (reduz atributos)
        proj = "PROJECTION"
        self.graph.add_node(proj, type="projection")

        for node in last_nodes:
            self.graph.add_edge(node, proj)

        return self.graph

    def draw(self):
        pos = nx.spring_layout(self.graph)

        labels = {}
        for node, data in self.graph.nodes(data=True):
            if data.get("type") == "selection":
                labels[node] = f"{node}\n({data['condition']})"
            else:
                labels[node] = node

        nx.draw(
            self.graph,
            pos,
            labels=labels,
            with_labels=True,
            node_color="lightblue",
            node_size=2500
        )

        plt.title("Grafo de Operadores (OTIMIZADO)")
        plt.show()