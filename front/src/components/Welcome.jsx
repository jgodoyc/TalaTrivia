import { useNavigate } from "react-router-dom";

export default function Welcome() {
  const navigate = useNavigate();

  const handleLoginClick = () => {
    navigate("/login");
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-700 mb-6">
          Bienvenido a TalaTrivia
        </h1>
        <button
          onClick={handleLoginClick}
          className="px-4 py-2 font-bold text-white bg-teal-500 rounded hover:bg-teal-700"
        >
          Ir al Login
        </button>
      </div>
    </div>
  );
}
