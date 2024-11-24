import { Suspense } from "react";
import { fetchData } from "../fetchData";

const apiData = fetchData("http://localhost:5000/trivias/1/questions");
export default function AdminView() {
  const data = apiData.read();
  return (
    <div className="Questions">
      <h1 className="text-2xl font-bold">Preguntas...</h1>
      <Suspense fallback={<div>Loading...</div>}>
        <ul className="space-y-3 mt-10">
          {data.map((question, index) => (
            <li key={question.id} className="py-1 ">
              <input
                type="text"
                value={question.question}
                onChange={(event) => handleInputChange(index, event)}
                className="border p-1 rounded mx-auto max-w-lg w-full"
              />
            </li>
          ))}
        </ul>
      </Suspense>
    </div>
  );
}
