# TalaTrivia

TalaTrivia es una aplicación web para gestionar trivias y usuarios. La aplicación incluye una API backend construida con Flask y una interfaz frontend construida con React. También incluye una base de datos MySQL para almacenar los datos de las trivias, preguntas, opciones y usuarios.

## Características

- Autenticación de usuarios con JWT.
- Gestión de usuarios (crear, actualizar, eliminar).
- Gestión de trivias (crear, actualizar, eliminar).
- Gestión de preguntas y opciones (crear, actualizar, eliminar).
- Envío y evaluación de respuestas de trivias.
- Visualización de rankings de trivias.

## Requisitos

- Docker
- Docker Compose

## Configuración

1. Clona el repositorio:

   ```sh
   git clone https://github.com/jgodoyc/TalaTrivia.git
   cd TalaTrivia
   ```

2. Construye y levanta los contenedores de Docker:

   ```sh
   docker-compose up --build
   ```

3. La aplicación estará disponible en `http://localhost:3000` para el frontend y `http://localhost:5000` para la API.

## Uso

## Link documentacion: https://documenter.getpostman.com/view/18045846/2sAYBUDsEi

La API proporciona varios endpoints para gestionar usuarios, trivias, preguntas y opciones. Aquí hay algunos ejemplos:

- **Iniciar sesión**: `POST /login`
- **Obtener usuarios**: `GET /users`
- **Crear usuario**: `POST /users`
- **Actualizar usuario**: `PUT /users/:user_id`
- **Eliminar usuario**: `DELETE /users/:user_id`
- **Obtener trivias**: `GET /trivias`
- **Crear trivia**: `POST /trivias`
- **Actualizar trivia**: `PUT /trivias/:trivia_id`
- **Eliminar trivia**: `DELETE /trivias/:trivia_id`
- **Obtener preguntas**: `GET /questions`
- **Crear pregunta**: `POST /questions`
- **Actualizar pregunta**: `PUT /questions/:question_id`
- **Eliminar pregunta**: `DELETE /questions/:question_id`

### Frontend

El frontend proporciona una interfaz de usuario para interactuar con la API. Incluye las siguientes vistas:

- **Inicio**: Muestra una lista de trivias disponibles.
- **Login**: Permite a los usuarios iniciar sesión.
- **Admin**: Permite a los administradores gestionar trivias, preguntas y usuarios.

### Pendientes

- ## Importante! Validaciones para la API
- Realizar pruebas unitarias
- Por mejorar la documentacion, se intentó utilizar Flask-RESTx pero la inversion de tiempo era imporante. Se documentó parcialmente con la herramienta Postman
- Falta agregar mas endpoint, para casos de una aplicacion real, como por ejemplo obtener, borrar, actualizar la puntuacion de una persona para una trivia.
- Refactorizar el codigo, actualmente está solo en un archivo grande los servicios y las rutas. Se puede mejorar separando por el tipo de objeto, usuario, questions, options (respuestas), trivias
