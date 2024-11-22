CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
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


INSERT INTO users (name, email) VALUES ('John Doe', 'john.doe@example.com');


INSERT INTO questions (question, difficulty) VALUES 
('What is the capital of France?', 'easy'),
('What is the square root of 144?', 'medium'),
('Explain the theory of relativity.', 'hard');


INSERT INTO options (question_id, option_text, is_correct) VALUES 
(1, 'Paris', TRUE),
(1, 'London', FALSE),
(1, 'Berlin', FALSE),
(1, 'Madrid', FALSE),

(2, '10', FALSE),
(2, '12', TRUE),
(2, '14', FALSE),
(2, '16', FALSE),

(3, 'It is a theory by Einstein', TRUE),
(3, 'It is a theory by Newton', FALSE),
(3, 'It is a theory by Galileo', FALSE),
(3, 'It is a theory by Tesla', FALSE);


INSERT INTO trivias (name, description) VALUES ('General Knowledge', 'A trivia to test your general knowledge.');


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