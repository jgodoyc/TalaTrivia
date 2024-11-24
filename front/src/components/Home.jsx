import { useState } from "react";
import { Routes, Route } from "react-router-dom";
import MenuTrivia from "./MenuTrivia";
import TriviaQuestions from "./TriviaQuestions";
import RankingList from "./RankingList";
import AdminView from "./AdminView";

export default function Home() {
  const [score, setScore] = useState(null);
  const [triviaId, setTriviaId] = useState(null);
  const role = localStorage.getItem("role");

  const handleTriviaSubmit = (id) => {
    setTriviaId(id);
  };

  const handleTriviaSelect = (id) => {
    setTriviaId(id);
  };

  return (
    <>
      <header className="bg-teal-400 py-5">
        <h1 className="text-center text-4xl font-black">TalaTrivia</h1>
      </header>

      <main className="text-center mx-auto py-20 grid grid-cols-3 gap-4">
        {role === "admin" ? (
          <div className="col-span-3">
            <AdminView />
          </div>
        ) : (
          <>
            <div className="col-span-1">
              <MenuTrivia onSelect={handleTriviaSelect} />
            </div>
            <div className="col-span-1">
              <Routes>
                <Route
                  path="trivias/:triviaId"
                  element={
                    <TriviaQuestions
                      setScore={setScore}
                      onSubmit={handleTriviaSubmit}
                    />
                  }
                />
              </Routes>
            </div>
            <div className="col-span-1 flex flex-col gap-4">
              <div>
                <h2 className="text-2xl font-bold">Puntuación...</h2>
                {score !== null && (
                  <p className="text-2xl font-bold">{score}</p>
                )}
              </div>
              <div className="flex-grow overflow-auto">
                <RankingList triviaId={triviaId} />
              </div>
            </div>
          </>
        )}
      </main>
    </>
  );
}
