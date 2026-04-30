import networkx as nx
import matplotlib.pyplot as plt


def build_tree_advanced(parsed):
    G = nx.DiGraph()

    root = f"π {', '.join(parsed['select'])}"
    G.add_node(root)

    if parsed["joins"]:
        join_node = f"|X| {parsed['joins'][0]}"
    else:
        join_node = "|X|"
    G.add_node(join_node)
    G.add_edge(root, join_node)

    for table in parsed["tables"]:
        last_node = table
        G.add_node(table)
        G.add_edge(join_node, table)

        for cond in parsed["where"]:
            if cond.startswith(table):
                selection = f"σ {cond}"
                G.add_node(selection)

                G.remove_edge(join_node, table)
                G.add_edge(join_node, selection)
                G.add_edge(selection, table)

    return G


def hierarchy_pos(G, root, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """
    Cria layout hierárquico fixo (árvore vertical)
    """
    pos = {root: (xcenter, vert_loc)}
    children = list(G.successors(root))

    if children:
        dx = width / len(children)
        next_x = xcenter - width / 2 + dx / 2

        for child in children:
            pos.update(
                hierarchy_pos(
                    G,
                    child,
                    width=dx,
                    vert_gap=vert_gap,
                    vert_loc=vert_loc - vert_gap,
                    xcenter=next_x,
                )
            )
            next_x += dx

    return pos


def draw_tree(G):
    plt.figure(figsize=(10, 8))

    root = [node for node, degree in G.in_degree() if degree == 0][0]

    pos = hierarchy_pos(G, root)

    node_colors = []
    for node in G.nodes():
        if str(node).startswith("π"):
            node_colors.append("#4A90E2")
        elif str(node).startswith("σ"):
            node_colors.append("#7ED321")
        elif "|X|" in str(node):
            node_colors.append("#F5A623")
        else:
            node_colors.append("#FFFFFF")

    node_sizes = []

    for node in G.nodes():
        tamanho = len(str(node))
        node_sizes.append(1500 + tamanho * 120)

    nx.draw_networkx_nodes(
        G,
        pos,
        node_color=node_colors,
        node_size=node_sizes,
        edgecolors="black",
        node_shape="s"
    )

    nx.draw_networkx_edges(G, pos)

    nx.draw_networkx_labels(G, pos, font_size=9)

    import matplotlib.patches as mpatches

    legenda = [
        mpatches.Patch(color="#4A90E2", label="π Projeção"),
        mpatches.Patch(color="#7ED321", label="σ Seleção"),
        mpatches.Patch(color="#F5A623", label="|X| Junção"),
        mpatches.Patch(color="#FFFFFF", label="Tabela", ec="black"),
    ]

    plt.legend(
        handles=legenda,
        loc="upper left",
        bbox_to_anchor=(1, 1)
    )

    plt.title("Árvore de Álgebra Relacional")
    plt.axis("off")
    plt.tight_layout()
    plt.show()