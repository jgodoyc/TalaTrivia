import { Suspense } from "react";
import { fetchData } from "../fetchData";

const apiData = fetchData("http://localhost:5000/trivias/1/questions");
export default function AdminView() {
  const data = apiData.read();
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold text-gray-700">En construcción</h1>
    </div>
  );
}
