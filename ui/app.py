import tkinter as tk
from tkinter import ttk, messagebox

from parser.sql_parser import SQLParser
from graph.query_graph import QueryGraph
from processor.query_processor import QueryProcessor


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Processador de Consultas")
        self.root.geometry("750x550")
        self.root.configure(bg="#f5f5f5")

        self.parser = SQLParser()
        self.graph_builder = QueryGraph()
        self.processor = QueryProcessor()

        self.build_ui()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(
            frame,
            text="Processador de Consultas SQL",
            font=("Arial", 18)
        )
        title.pack(pady=10)

        # Input SQL
        self.query_input = tk.Text(frame, height=5, font=("Consolas", 11))
        self.query_input.pack(fill="x", pady=10)
        self.query_input.insert(
            "1.0",
            "SELECT Nome FROM Cliente WHERE idCliente > 10"
        )

        # Botões
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        ttk.Button(
            btn_frame,
            text="Executar",
            command=self.run_query
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="Mostrar Grafo",
            command=self.show_graph
        ).pack(side="left", padx=5)

        # Output
        self.output = tk.Text(frame, height=15, font=("Consolas", 10))
        self.output.pack(fill="both", expand=True, pady=10)

    def run_query(self):
        query = self.query_input.get("1.0", tk.END)

        try:
            parsed = self.parser.parse(query)
            graph = self.graph_builder.build(parsed)
            order = self.processor.execution_order(graph)

            self.output.delete("1.0", tk.END)

            self.output.insert(tk.END, "=== PARSE ===\n")
            self.output.insert(tk.END, f"{parsed}\n\n")

            self.output.insert(tk.END, "=== ORDEM DE EXECUÇÃO ===\n")
            for step in order:
                self.output.insert(tk.END, f"-> {step}\n")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def show_graph(self):
        query = self.query_input.get("1.0", tk.END)

        try:
            parsed = self.parser.parse(query)
            self.graph_builder.build(parsed)
            self.graph_builder.draw()
        except Exception as e:
            messagebox.showerror("Erro", str(e))