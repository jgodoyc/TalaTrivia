from flask_restx import fields, Namespace

api = Namespace('api', description='Operaciones relacionadas con la API')

user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='El ID del usuario'),
    'name': fields.String(required=True, description='El nombre del usuario'),
    'email': fields.String(required=True, description='El email del usuario'),
    'role': fields.String(required=True, description='El rol del usuario')
})

question_model = api.model('Question', {
    'id': fields.Integer(readonly=True, description='El ID de la pregunta'),
    'question': fields.String(required=True, description='El texto de la pregunta'),
    'difficulty': fields.String(required=True, description='La dificultad de la pregunta')
})

option_model = api.model('Option', {
    'id': fields.Integer(readonly=True, description='El ID de la opción'),
    'question_id': fields.Integer(required=True, description='El ID de la pregunta asociada'),
    'option_text': fields.String(required=True, description='El texto de la opción'),
    'is_correct': fields.Boolean(required=True, description='Indica si la opción es correcta')
})

trivia_model = api.model('Trivia', {
    'id': fields.Integer(readonly=True, description='El ID de la trivia'),
    'name': fields.String(required=True, description='El nombre de la trivia'),
    'description': fields.String(required=True, description='La descripción de la trivia'),
    'questions': fields.List(fields.Nested(question_model), description='Las preguntas de la trivia'),
    'users': fields.List(fields.Nested(user_model), description='Los usuarios asociados a la trivia')
})