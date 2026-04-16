import { useState } from "react";

type Props = {
  onSubmit: (query: string) => void;
};

export default function QueryInput({ onSubmit }: Props) {
  const [query, setQuery] = useState("");

  const handleSubmit = () => {
    if (!query.trim()) return;
    onSubmit(query);
  };

  return (
    <div className="space-y-3">
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="SELECT * FROM usuarios WHERE idade > 18"
        className="w-full h-32 p-3 bg-zinc-950 border border-zinc-800 rounded-lg text-sm text-zinc-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <button
        onClick={handleSubmit}
        className="px-4 py-2 bg-blue-600 hover:bg-blue-500 transition rounded-lg font-medium"
      >
        Executar Query
      </button>
    </div>
  );
}
