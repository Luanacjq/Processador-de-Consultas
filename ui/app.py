import customtkinter as ctk

from parser.sql_parser import parse_sql
from algebra.relational_algebra import to_relational_algebra
from heuristics.optimizer import apply_heuristics
from graph.operator_graph import build_tree_advanced, build_optimized_tree, draw_tree
from utils.validator import validate

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Processador de Consultas")
        self.geometry("900x600")

        ctk.CTkLabel(self, text="Digite sua consulta SQL:", font=("Arial", 18)).pack(pady=10)

        self.input = ctk.CTkTextbox(self, height=100)
        self.input.pack(fill="x", padx=20)

        example_sql = """SELECT cliente.nome, produto.nome, pedido.valortotalpedido
            FROM cliente
            INNER JOIN pedido ON cliente.idcliente = pedido.cliente_idcliente
            INNER JOIN pedido_has_produto ON pedido.idpedido = pedido_has_produto.pedido_idpedido
            INNER JOIN produto ON produto.idproduto = pedido_has_produto.produto_idproduto
            WHERE pedido.valortotalpedido > 100 AND produto.preco > 50"""

        self.input.insert("1.0", example_sql)

        ctk.CTkButton(self, text="Executar", command=self.run).pack(pady=10)

        self.output = ctk.CTkTextbox(self)
        self.output.pack(fill="both", expand=True, padx=20, pady=10)

    def run(self):
        query = self.input.get("1.0", "end")

        self.output.delete("1.0", "end")

        try:
            parsed = parse_sql(query)

            errors = validate(parsed)
            if errors:
                self.output.insert("end", "\n".join(errors))
                return

            algebra = to_relational_algebra(parsed)
            heuristics = apply_heuristics(parsed)

            # árvore original
            self.output.insert("end", "\n=== ÁRVORE ORIGINAL ===\n(Grafo exibido em janela separada)\n")
            draw_tree(build_tree_advanced(parsed))

            # árvore otimizada
            self.output.insert("end", "\n=== ÁRVORE OTIMIZADA ===\n(Grafo exibido em janela separada)\n")
            draw_tree(build_optimized_tree(parsed))

            self.output.insert("end", "\n=== ÁLGEBRA RELACIONAL ===\n")
            self.output.insert("end", algebra + "\n\n")

            self.output.insert("end", "=== HEURÍSTICAS ===\n")
            for h in heuristics:
                self.output.insert("end", h + "\n\n")

            self.output.insert("end",
            "=== PLANO DE EXECUÇÃO ===\n"
            "1. Aplicar seleções (σ)\n"
            "2. Aplicar projeções (π)\n"
            "3. Executar junções (|X|)\n"
            "4. Projeção final\n"
            )

        except Exception as e:
            self.output.insert("end", f"Erro: {str(e)}")