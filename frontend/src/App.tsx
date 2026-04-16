import { useState } from "react";
import { enviarQuery } from "./services/api";
import QueryInput from "./components/QueryInput";

type QueryResult = {
  campos: string[];
  tabela: string;
  condicao?: string;
};

export default function App() {
  const [resultado, setResultado] = useState<QueryResult | null>(null);
  const [erro, setErro] = useState("");

  const executar = async (query: string) => {
    setErro("");
    setResultado(null);

    try {
      const data = await enviarQuery(query);
      setResultado(data);
    } catch (e: unknown) {
      setErro(e instanceof Error ? e.message : "Erro desconhecido");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="w-full max-w-3xl space-y-6">
        {/* HEADER */}
        <div className="text-center">
          <h1 className="text-3xl font-bold">Processador de Consultas</h1>
          <p className="text-zinc-400 mt-2">
            Execute queries SQL e visualize o resultado
          </p>
        </div>

        {/* INPUT */}
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4">
          <QueryInput onSubmit={executar} />
        </div>

        {/* ERROR */}
        {erro && (
          <div className="bg-red-500/10 border border-red-500 text-red-400 p-3 rounded-lg">
            {erro}
          </div>
        )}

        {/* RESULT */}
        {resultado && (
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-4">
            <h2 className="font-semibold mb-2">Resultado</h2>
            <pre className="text-sm text-zinc-300 overflow-auto">
              {JSON.stringify(resultado, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
