import { useState } from "react";
import { Routes, Route } from "react-router-dom";
import MenuTrivia from "./MenuTrivia";
import TriviaQuestions from "./TriviaQuestions";

export default function Home() {
  const [score, setScore] = useState(null);

  return (
    <>
      <header className="bg-teal-400 py5">
        <h1 className="text-center text-4xl font-black">TalaTrivia</h1>
      </header>

      <main className="text-center mx-auto py-20 grid grid-cols-3">
        <div>
          <MenuTrivia />
        </div>
        <div>
          <Routes>
            <Route
              path="/trivias/:triviaId"
              element={<TriviaQuestions setScore={setScore} />}
            />
          </Routes>
        </div>
        <div>
          <h2>Puntuacion...</h2>
          {score !== null && <p className="text-2xl font-bold">{score}</p>}
        </div>
      </main>
    </>
  );
}
