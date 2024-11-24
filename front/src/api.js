export async function getTrivias() {
  const response = await fetch("http://localhost:5000/trivias", {
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      Authorization: `Bearer ${localStorage.getItem("token")}`, // Si necesitas autenticación
    },
  });
  if (!response.ok) {
    throw new Error("Error al obtener las trivias");
  }
  return response.json();
}

export async function login(email, password) {
  const response = await fetch("http://localhost:5000/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) {
    throw new Error("Error al iniciar sesión");
  }
  const data = await response.json();
  return { token: data.token, userId: data.userId, role: data.role };
}

export async function getTriviaQuestions(triviaId) {
  const response = await fetch(
    `http://localhost:5000/trivias/${triviaId}/questions`,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    }
  );
  if (!response.ok) {
    throw new Error("Error al obtener las preguntas de la trivia");
  }
  return response.json();
}

export async function submitAnswers(triviaId, answers) {
  const userId = localStorage.getItem("user_id");
  const response = await fetch(
    `http://localhost:5000/trivias/${triviaId}/users/${userId}/answers`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({ answers }),
    }
  );
  if (!response.ok) {
    throw new Error("Error al enviar las respuestas");
  }
  const data = await response.json();
  return data.score;
}

export async function getQuestions() {
  const response = await fetch("http://localhost:5000/questions", {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });
  if (!response.ok) {
    throw new Error("Error al obtener las preguntas");
  }
  return response.json();
}

export async function updateQuestion(questionId, questionData) {
  const response = await fetch(
    `http://localhost:5000/questions/${questionId}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify(questionData),
    }
  );
  if (!response.ok) {
    throw new Error("Error al actualizar la pregunta");
  }
  return response.json();
}
