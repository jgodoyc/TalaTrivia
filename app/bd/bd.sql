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
('Admin', 'admin@example.com', 'admin', 'admin'),
('Natalia', 'natalia@example.com', 'natalia', 'player'),
('User', 'user@example.com', 'user', 'player');

INSERT INTO questions (question, difficulty) VALUES
('Cual es el proceso de seleccion de personal?', 'easy'),
('Que documentos se requieren para la contratacion?', 'medium'),
('Cuales son los beneficios de los empleados?', 'hard'),
('Que es una evaluacion de desempeño?', 'easy'),
('Cuales son las politicas de vacaciones?', 'medium'),
('Como se maneja el ausentismo?', 'hard'),
('Que es el onboarding?', 'easy'),
('Cuales son las politicas de seguridad en el trabajo?', 'medium'),
('Que es el plan de carrera?', 'hard');

INSERT INTO options (question_id, option_text, is_correct) VALUES 
(1, 'Entrevista, prueba tecnica, entrevista final', TRUE),
(1, 'Solo entrevista', FALSE),
(1, 'Prueba tecnica y entrevista final', FALSE),
(1, 'Entrevista inicial y final', FALSE),

(2, 'Identificacion, contrato firmado, referencias', TRUE),
(2, 'Solo identificacion', FALSE),
(2, 'Contrato firmado y referencias', FALSE),
(2, 'Identificacion y contrato firmado', FALSE),

(3, 'Seguro medico, vacaciones, bonos', TRUE),
(3, 'Solo seguro medico', FALSE),
(3, 'Vacaciones y bonos', FALSE),
(3, 'Seguro medico y vacaciones', FALSE),

(4, 'Evaluacion del rendimiento del empleado', TRUE),
(4, 'Evaluacion de la empresa', FALSE),
(4, 'Evaluacion de los clientes', FALSE),
(4, 'Evaluacion de los proveedores', FALSE),

(5, 'Dias libres pagados segun antiguedad', TRUE),
(5, 'Dias libres no pagados', FALSE),
(5, 'Dias libres pagados sin importar antiguedad', FALSE),
(5, 'No hay politicas de vacaciones', FALSE),

(6, 'Registro y seguimiento de ausencias', TRUE),
(6, 'No se maneja', FALSE),
(6, 'Solo registro de ausencias', FALSE),
(6, 'Solo seguimiento de ausencias', FALSE),

(7, 'Proceso de integracion de nuevos empleados', TRUE),
(7, 'Proceso de seleccion de personal', FALSE),
(7, 'Proceso de evaluacion de desempeño', FALSE),
(7, 'Proceso de capacitacion', FALSE),

(8, 'Normas y procedimientos para la seguridad', TRUE),
(8, 'Normas de conducta', FALSE),
(8, 'Politicas de vacaciones', FALSE),
(8, 'Politicas de ausentismo', FALSE),

(9, 'Plan de desarrollo profesional', TRUE),
(9, 'Plan de evaluacion de desempeño', FALSE),
(9, 'Plan de capacitacion', FALSE),
(9, 'Plan de seleccion de personal', FALSE);

INSERT INTO trivias (name, description) VALUES
('Recursos Humanos Basico', 'Trivia sobre conceptos basicos de recursos humanos.'), 
('Politicas de la Empresa', 'Trivia sobre las politicas internas de la empresa.'),
('Desarrollo Profesional', 'Trivia sobre el desarrollo profesional en la empresa.');

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
(1, 2, 2),  
(1, 3, 3);  

INSERT INTO user_scores (user_id, trivia_id, score) VALUES 
(1, 1, 6);