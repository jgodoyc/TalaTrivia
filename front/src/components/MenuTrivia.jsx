import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getTrivias } from "../api";

export default function MenuTrivia({ onSelect }) {
  const [trivias, setTrivias] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTrivias = async () => {
      try {
        const data = await getTrivias();
        setTrivias(data);
      } catch (error) {
        console.error("Error al obtener las trivias:", error);
      }
    };

    fetchTrivias();
  }, []);

  const handleTriviaSelect = (triviaId) => {
    onSelect(triviaId);
    navigate(`/home/trivias/${triviaId}`);
  };

  return (
    <div>
      <h2 className="text-2xl font-bold">Elige una Trivia</h2>
      <ul className="space-y-3 mt-10">
        {trivias.map((trivia) => (
          <button
            className="block w-1/2 p-2 text-left border rounded hover:bg-teal-300"
            key={trivia.id}
            onClick={() => handleTriviaSelect(trivia.id)}
          >
            {trivia.name}
          </button>
        ))}
      </ul>
    </div>
  );
}
