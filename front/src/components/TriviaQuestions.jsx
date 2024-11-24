import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { getTriviaQuestions, submitAnswers } from "../api";

export default function TriviaQuestions({ setScore, onSubmit }) {
  const { triviaId } = useParams();
  const [questions, setQuestions] = useState([]);
  const [selectedOptions, setSelectedOptions] = useState({});
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    setScore(null);
    setSelectedOptions({});
    setSubmitted(false);

    const fetchQuestions = async () => {
      try {
        const data = await getTriviaQuestions(triviaId);
        setQuestions(data);
      } catch (error) {
        console.error("Error al obtener las preguntas:", error);
      }
    };

    fetchQuestions();
  }, [triviaId, setScore]);

  const handleOptionChange = (questionId, optionId) => {
    setSelectedOptions((prev) => ({
      ...prev,
      [questionId]: optionId,
    }));
  };

  const handleSubmit = async () => {
    const answers = questions
      .map((question) => ({
        question_id: question.id,
        selected_option_id: selectedOptions[question.id] || null,
      }))
      .filter((answer) => answer.selected_option_id !== null);

    try {
      const score = await submitAnswers(triviaId, answers);
      setScore(score);
      setSubmitted(true);
      onSubmit(triviaId); // Llama a la función de callback pasando la triviaId
    } catch (error) {
      console.error("Error al enviar las respuestas:", error);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">Preguntas de la Trivia</h2>
      <ul className="space-y-6">
        {questions.map((question) => (
          <li key={question.id} className="bg-white p-4 rounded shadow">
            <h3 className="text-lg font-semibold mb-3">{question.question}</h3>
            <ul className="space-y-2">
              {question.options.map((option) => (
                <li key={option.id}>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      name={`question-${question.id}`}
                      value={option.id}
                      checked={selectedOptions[question.id] === option.id}
                      onChange={() =>
                        handleOptionChange(question.id, option.id)
                      }
                      className="form-radio"
                    />
                    <span>{option.option_text}</span>
                  </label>
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
      <button
        className="mt-6 px-4 py-2 font-bold text-white bg-teal-500 rounded hover:bg-teal-700"
        onClick={handleSubmit}
      >
        {submitted ? "Actualizar Respuestas" : "Enviar Respuestas"}
      </button>
    </div>
  );
}
