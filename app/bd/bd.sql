CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'player') NOT NULL DEFAULT 'player'
);

CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT NOT NULL,
    difficulty ENUM('easy', 'medium', 'hard') NOT NULL
) DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS trivias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);


CREATE TABLE IF NOT EXISTS trivia_questions (
    trivia_id INT NOT NULL,
    question_id INT NOT NULL,
    PRIMARY KEY (trivia_id, question_id),
    FOREIGN KEY (trivia_id) REFERENCES trivias(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS trivia_users (
    trivia_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY (trivia_id, user_id),
    FOREIGN KEY (trivia_id) REFERENCES trivias(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS user_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    selected_option_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    FOREIGN KEY (selected_option_id) REFERENCES options(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS user_scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    trivia_id INT NOT NULL,
    score INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (trivia_id) REFERENCES trivias(id) ON DELETE CASCADE
);


INSERT INTO users (name, email, password, role) VALUES
('Chiki', 'admin@example.com', 'admin', 'admin'),
('jebus', 'jebus@example.com', 'root', 'player');


INSERT INTO questions (question, difficulty) VALUES
('Cúales son los tíldes y caracteres que no conoces ##!@??¿', 'hard'),
('¿Cual es la capital de Chile?', 'easy'),
('¿Cuanto es la raiz cuadrada de 144?', 'medium'),
('¿Quien explica la teoría de la relatividad?', 'hard'),
('¿Quién fue el primer presidente de los Estados Unidos?', 'easy'),
('¿En qué año comenzó la Segunda Guerra Mundial?', 'medium'),
('¿Quién descubrió América?', 'hard'),
('¿Cuál es el planeta más grande del sistema solar?', 'easy'),
('¿Cuál es la fórmula química del agua?', 'medium');


INSERT INTO options (question_id, option_text, is_correct) VALUES 
(1, 'Santiago', TRUE),
(1, 'Valdivia', FALSE),
(1, 'Lima', FALSE),
(1, 'Buenos Aires', FALSE),

(2, '10', FALSE),
(2, '12', TRUE),
(2, '14', FALSE),
(2, '16', FALSE),

(3, 'Es una teoria de Einstein', TRUE),
(3, 'Es una teoria de Newton', FALSE),
(3, 'Es una teoria de Galileo', FALSE),
(3, 'Es una teoria de Tesla', FALSE),

(4, 'George Washington', TRUE),
(4, 'Thomas Jefferson', FALSE),
(4, 'Abraham Lincoln', FALSE),
(4, 'John Adams', FALSE),

(5, '1939', TRUE),
(5, '1941', FALSE),
(5, '1935', FALSE),
(5, '1945', FALSE),

(6, 'Cristóbal Colón', TRUE),
(6, 'Vasco da Gama', FALSE),
(6, 'Fernando de Magallanes', FALSE),
(6, 'Hernán Cortés', FALSE),

(7, 'Júpiter', TRUE),
(7, 'Saturno', FALSE),
(7, 'Marte', FALSE),
(7, 'Tierra', FALSE),

(8, 'H2O', TRUE),
(8, 'CO2', FALSE),
(8, 'O2', FALSE),
(8, 'H2', FALSE),

(9, 'Charles Darwin', TRUE),
(9, 'Isaac Newton', FALSE),
(9, 'Albert Einstein', FALSE),
(9, 'Galileo Galilei', FALSE);

INSERT INTO trivias (name, description) VALUES
('Conocimientos generales', 'Una trivia para probar tus conocimientos generales.'), 
('Historia', 'Trivia sobre eventos históricos importantes.'),
('Ciencia', 'Trivia sobre conceptos científicos básicos.');


INSERT INTO trivia_questions (trivia_id, question_id) VALUES 
(1, 1),
(1, 2),
(1, 3),
(2, 4),
(2, 5),
(2, 6),
(3, 7),
(3, 8),
(3, 9);


INSERT INTO trivia_users (trivia_id, user_id) VALUES 
(1, 1),
(2, 1),
(3, 1);


INSERT INTO user_answers (user_id, question_id, selected_option_id) VALUES 
(1, 1, 1), 
(1, 2, 6),  
(1, 3, 9);  


INSERT INTO user_scores (user_id, trivia_id, score) VALUES 
(1, 1, 6);  