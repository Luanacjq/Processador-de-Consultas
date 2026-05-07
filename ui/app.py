import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

from parser.sql_parser import parse_sql
from algebra.relational_algebra import to_relational_algebra
from heuristics.optimizer import apply_heuristics
from graph.operator_graph import build_tree_advanced, build_optimized_tree, hierarchy_pos
from utils.validator import validate


# ── paleta de cores ──────────────────────────────────────────────────────────
NODE_COLORS = {
    "π":    "#4A90E2",
    "σ":    "#7ED321",
    "|X|":  "#F5A623",
    "table":"#FFFFFF",
}


def get_node_color(node: str) -> str:
    if node.startswith("π"):   return NODE_COLORS["π"]
    if node.startswith("σ"):   return NODE_COLORS["σ"]
    if "|X|" in node:          return NODE_COLORS["|X|"]
    return NODE_COLORS["table"]


def render_graph_on_canvas(G: nx.DiGraph, frame: ctk.CTkFrame, title: str) -> None:
    for widget in frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor("#1e1e2e")
    ax.set_facecolor("#1e1e2e")

    root = [n for n, d in G.in_degree() if d == 0][0]
    pos  = hierarchy_pos(G, root)

    colors = [get_node_color(n) for n in G.nodes()]
    sizes  = [1500 + len(str(n)) * 120 for n in G.nodes()]

    nx.draw_networkx_nodes(G, pos, ax=ax,
                           node_color=colors, node_size=sizes,
                           edgecolors="white", node_shape="s")
    nx.draw_networkx_edges(G, pos, ax=ax,
                           edge_color="white", arrows=True, arrowsize=15)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_color="black")

    import matplotlib.patches as mpatches
    legend = [
        mpatches.Patch(color=NODE_COLORS["π"],   label="π  Projeção"),
        mpatches.Patch(color=NODE_COLORS["σ"],   label="σ  Seleção"),
        mpatches.Patch(color=NODE_COLORS["|X|"], label="|X|  Junção"),
        mpatches.Patch(facecolor=NODE_COLORS["table"],
                       edgecolor="white",         label="Tabela"),
    ]
    ax.legend(handles=legend, loc="upper left",
              facecolor="#2e2e3e", labelcolor="white", fontsize=8)
    ax.set_title(title, color="white", fontsize=12, pad=10)
    ax.axis("off")
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    plt.close(fig)


def build_execution_plan(G: nx.DiGraph) -> list[str]:
    topo_reversed = list(reversed(list(nx.topological_sort(G))))
    plan = []
    for step, node in enumerate(topo_reversed, 1):
        label = str(node)
        if label.startswith("σ"):
            plan.append(f"Passo {step}: {label}  <- Seleção (reduz tuplas)")
        elif label.startswith("π"):
            plan.append(f"Passo {step}: {label}  <- Projeção (reduz atributos)")
        elif "|X|" in label:
            plan.append(f"Passo {step}: {label}  <- Junção")
        else:
            plan.append(f"Passo {step}: {label}  <- Leitura da tabela")
    return plan


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        self.title("Processador de Consultas SQL")
        self.geometry("1200x800")
        self.configure(fg_color="#1e1e2e")

        self._G_orig = None
        self._G_opt  = None

        # ── painel esquerdo ───────────────────────────────────────────────
        left = ctk.CTkFrame(self, fg_color="#2e2e3e", width=400)
        left.pack(side="left", fill="y", padx=(10, 5), pady=10)
        left.pack_propagate(False)

        ctk.CTkLabel(left, text="Consulta SQL",
                     font=("Courier New", 15, "bold"),
                     text_color="#89b4fa").pack(pady=(12, 4))

        self.input = ctk.CTkTextbox(left, height=150, font=("Courier New", 12),
                                    fg_color="#1e1e2e", text_color="#cdd6f4")
        self.input.pack(fill="x", padx=12)
        self.input.insert("1.0",
            "SELECT cliente.nome, produto.nome, pedido.valortotalpedido\n"
            "FROM cliente\n"
            "INNER JOIN pedido ON cliente.idcliente = pedido.cliente_idcliente\n"
            "INNER JOIN pedido_has_produto "
            "ON pedido.idpedido = pedido_has_produto.pedido_idpedido\n"
            "INNER JOIN produto "
            "ON produto.idproduto = pedido_has_produto.produto_idproduto\n"
            "WHERE pedido.valortotalpedido > 100 AND produto.preco > 50"
        )

        ctk.CTkButton(left, text="▶  Executar",
                      command=self.run,
                      fg_color="#89b4fa", text_color="#1e1e2e",
                      hover_color="#b4befe",
                      font=("Courier New", 13, "bold")
                      ).pack(pady=(10, 4), padx=12, fill="x")

        ctk.CTkLabel(left, text="Resultado",
                     font=("Courier New", 13, "bold"),
                     text_color="#89b4fa").pack(pady=(6, 2))

        self.output = ctk.CTkTextbox(left, font=("Courier New", 11),
                                     fg_color="#1e1e2e", text_color="#cdd6f4")
        self.output.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # ── painel direito ────────────────────────────────────────────────
        right = ctk.CTkFrame(self, fg_color="#1e1e2e")
        right.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        # barra de navegação
        nav = ctk.CTkFrame(right, fg_color="#2e2e3e", height=50)
        nav.pack(fill="x", pady=(0, 6))
        nav.pack_propagate(False)

        self.lbl_view = ctk.CTkLabel(nav, text="Aguardando execução...",
                                     font=("Courier New", 13, "bold"),
                                     text_color="#6c7086")
        self.lbl_view.pack(side="left", padx=14)

        self.btn_next = ctk.CTkButton(nav, text="Próximo: Árvore Otimizada →",
                                      command=self.show_otimizada,
                                      fg_color="#f38ba8", text_color="#1e1e2e",
                                      hover_color="#eba0ac",
                                      font=("Courier New", 11, "bold"),
                                      state="disabled", width=230)
        self.btn_next.pack(side="right", padx=10, pady=8)

        self.btn_prev = ctk.CTkButton(nav, text="← Voltar: Árvore Original",
                                      command=self.show_original,
                                      fg_color="#89b4fa", text_color="#1e1e2e",
                                      hover_color="#b4befe",
                                      font=("Courier New", 11, "bold"),
                                      state="disabled", width=210)
        self.btn_prev.pack(side="right", padx=(0, 4), pady=8)

        # área do grafo
        self.graph_frame = ctk.CTkFrame(right, fg_color="#2e2e3e")
        self.graph_frame.pack(fill="both", expand=True)

    # ── navegação ─────────────────────────────────────────────────────────

    def show_original(self):
        if self._G_orig is None:
            return
        self.lbl_view.configure(text="Etapa 1 — Árvore Original",
                                text_color="#a6e3a1")
        self.btn_prev.configure(state="disabled")
        self.btn_next.configure(state="normal")
        render_graph_on_canvas(self._G_orig, self.graph_frame, "Árvore Original")

    def show_otimizada(self):
        if self._G_opt is None:
            return
        self.lbl_view.configure(text="Etapa 2 — Árvore Otimizada",
                                text_color="#f38ba8")
        self.btn_next.configure(state="disabled")
        self.btn_prev.configure(state="normal")
        render_graph_on_canvas(self._G_opt, self.graph_frame, "Árvore Otimizada")

    # ── execução ──────────────────────────────────────────────────────────

    def run(self):
        query = self.input.get("1.0", "end").strip()
        self.output.delete("1.0", "end")
        self._G_orig = None
        self._G_opt  = None
        self.btn_next.configure(state="disabled")
        self.btn_prev.configure(state="disabled")
        self.lbl_view.configure(text="Aguardando execução...", text_color="#6c7086")
        for w in self.graph_frame.winfo_children():
            w.destroy()

        try:
            parsed = parse_sql(query)

            resolved = {**parsed, "tables": list(parsed["alias_map"].values())}
            errors = validate(resolved)
            if errors:
                self.output.insert("end", "ERROS DE VALIDAÇÃO:\n")
                for e in errors:
                    self.output.insert("end", f"  * {e}\n")
                return

            algebra = to_relational_algebra(parsed)
            self.output.insert("end", "=== ÁLGEBRA RELACIONAL ===\n")
            self.output.insert("end", algebra + "\n\n")

            heuristics = apply_heuristics(parsed)
            self.output.insert("end", "=== HEURÍSTICAS ===\n")
            for h in heuristics:
                self.output.insert("end", h + "\n\n")

            self._G_orig = build_tree_advanced(parsed)
            self._G_opt  = build_optimized_tree(parsed)

            # começa sempre na etapa 1
            self.show_original()

            plan = build_execution_plan(self._G_opt)
            self.output.insert("end", "=== PLANO DE EXECUÇÃO ===\n")
            for line in plan:
                self.output.insert("end", line + "\n")

        except Exception as e:
            self.output.insert("end", f"Erro: {str(e)}\n")


if __name__ == "__main__":
    app = App()
    app.mainloop()