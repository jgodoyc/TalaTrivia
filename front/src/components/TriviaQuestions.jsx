import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { getTriviaQuestions, submitAnswers } from "../api";

export default function TriviaQuestions({ setScore }) {
  const { triviaId } = useParams();
  const [questions, setQuestions] = useState([]);
  const [selectedOptions, setSelectedOptions] = useState({});

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const data = await getTriviaQuestions(triviaId);
        setQuestions(data);
      } catch (error) {
        console.error("Error al obtener las preguntas:", error);
      }
    };

    fetchQuestions();
  }, [triviaId]);

  const handleOptionChange = (questionId, optionId) => {
    setSelectedOptions((prev) => ({
      ...prev,
      [questionId]: optionId,
    }));
  };

  const handleSubmit = async () => {
    const answers = Object.keys(selectedOptions).map((questionId) => ({
      question_id: questionId,
      selected_option_id: selectedOptions[questionId],
    }));

    try {
      const score = await submitAnswers(triviaId, answers);
      setScore(score);
    } catch (error) {
      console.error("Error al enviar las respuestas:", error);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold">Preguntas de la Trivia</h2>
      <ul>
        {questions.map((question) => (
          <li key={question.id} className="mb-4">
            <h3 className="font-semibold">{question.question}</h3>
            <ul>
              {question.options.map((option) => (
                <li key={option.id}>
                  <label>
                    <input
                      type="radio"
                      name={`question-${question.id}`}
                      value={option.id}
                      checked={selectedOptions[question.id] === option.id}
                      onChange={() =>
                        handleOptionChange(question.id, option.id)
                      }
                    />
                    {option.option_text}
                  </label>
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
      <button
        className="mt-4 px-4 py-2 font-bold text-white bg-teal-500 rounded hover:bg-teal-700"
        onClick={handleSubmit}
      >
        Enviar Respuestas
      </button>
    </div>
  );
}
