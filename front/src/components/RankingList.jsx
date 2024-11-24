import { useEffect, useState } from "react";

export default function RankingList({ triviaId }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRanking = async () => {
      try {
        const response = await fetch(
          `http://localhost:5000/trivias/${triviaId}/ranking`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        );
        if (!response.ok) {
          throw new Error("Error al obtener el ranking");
        }
        const result = await response.json();
        setData(result);
      } catch (err) {
        console.error("Error al cargar el ranking:", err);
        setError(err.message);
      }
    };

    if (triviaId) {
      fetchRanking();
    }
  }, [triviaId]);

  if (error) {
    return <p>Error al cargar el ranking: {error}</p>;
  }

  if (!data) {
    return <p>Cargando...</p>;
  }

  return (
    <div className="mt-8">
      <h2 className="text-xl font-bold mb-4">
        Puntuaciones más altas históricamente
      </h2>
      <div className="flex justify-center">
        <table className="w-5/6 bg-slate-400">
          <thead>
            <tr>
              <th className="py-2">Nombre</th>
              <th className="py-2">Puntuación</th>
            </tr>
          </thead>
          <tbody>
            {data.map((score, index) => (
              <tr key={`${score.id}-${index}`} className="bg-gray-100">
                <td className="py-2 px-4">{score.name}</td>
                <td className="py-2 px-4">{score.score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
