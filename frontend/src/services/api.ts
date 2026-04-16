export async function enviarQuery(query: string) {
  const res = await fetch("http://localhost:8080/query", {
    method: "POST",
    headers: {
      "Content-Type": "text/plain",
    },
    body: query,
  });

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json();
}