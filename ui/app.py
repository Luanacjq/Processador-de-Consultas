import tkinter as tk
from tkinter import ttk, messagebox

from parser.sql_parser import SQLParser
from graph.query_graph import QueryGraph
from processor.query_processor import QueryProcessor


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Processador de Consultas SQL")
        self.root.geometry("850x600")

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.parser = SQLParser()
        self.graph_builder = QueryGraph()
        self.processor = QueryProcessor()

        self.build_ui()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Processador de Consultas SQL",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=10)

        # INPUT
        self.query_input = tk.Text(frame, height=6, font=("Consolas", 11))
        self.query_input.pack(fill="x")

        self.query_input.insert("1.0",
            """SELECT Cliente.Nome, Pedido.ValorTotalPedido
            FROM Cliente
            INNER JOIN Pedido
            ON Cliente.idCliente = Pedido.Cliente_idCliente
            WHERE Pedido.ValorTotalPedido > 200
            AND Pedido.ValorTotalPedido < 1000""")

        # BOTÕES
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Executar", command=self.run_query).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Mostrar Grafo", command=self.show_graph).pack(side="left", padx=10)

        # OUTPUT
        self.output = tk.Text(frame, height=15, font=("Consolas", 10))
        self.output.pack(fill="both", expand=True)

    def run_query(self):
        query = self.query_input.get("1.0", tk.END)

        try:
            parsed = self.parser.parse(query)
            graph = self.graph_builder.build(parsed)
            order = self.processor.execution_order(graph)

            self.output.delete("1.0", tk.END)

            self.output.insert(tk.END, "=== PARSE ===\n")
            self.output.insert(tk.END, f"{parsed}\n\n")

            self.output.insert(tk.END, "=== GRAFO OTIMIZADO ===\n")
            self.output.insert(tk.END, "- Seleção (redução de tuplas)\n")
            self.output.insert(tk.END, "- Junção (evita produto cartesiano)\n")
            self.output.insert(tk.END, "- Projeção (redução de atributos)\n\n")

            self.output.insert(tk.END, "=== ORDEM DE EXECUÇÃO ===\n")
            for step in order:
                self.output.insert(tk.END, f"-> {step}\n")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def show_graph(self):
        try:
            parsed = self.parser.parse(self.query_input.get("1.0", tk.END))
            self.graph_builder.build(parsed)
            self.graph_builder.draw()
        except Exception as e:
            messagebox.showerror("Erro", str(e))