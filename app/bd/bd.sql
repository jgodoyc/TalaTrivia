CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'player') NOT NULL DEFAULT 'jugador'
);

CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT NOT NULL,
    difficulty ENUM('easy', 'medium', 'hard') NOT NULL
);


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


INSERT INTO users (name, email, password, role) VALUES ('Chiki', 'admin@example.com', 'admin', 'admin');
INSERT INTO users (name, email, password, role) VALUES ('jebus', 'jebus@example.com', 'root', 'player');


INSERT INTO questions (question, difficulty) VALUES 
('¿Cual es la capital de Chile?', 'easy'),
('¿Cuanto es la raiz cuadrada de 144?', 'medium'),
('¿Quien explica la teoría de la relatividad?', 'hard');


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
(3, 'Es una teoria de Tesla', FALSE);

INSERT INTO trivias (name, description) VALUES ('Conocimientos generales', 'Una trivia para probar tus conocimientos generales.');


INSERT INTO trivia_questions (trivia_id, question_id) VALUES 
(1, 1),
(1, 2),
(1, 3);


INSERT INTO trivia_users (trivia_id, user_id) VALUES 
(1, 1);


INSERT INTO user_answers (user_id, question_id, selected_option_id) VALUES 
(1, 1, 1), 
(1, 2, 6),  
(1, 3, 9);  


INSERT INTO user_scores (user_id, trivia_id, score) VALUES 
(1, 1, 6);  