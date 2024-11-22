from .db import db

class Question:
    def __init__(self, id, question, answer):
        self.id = id
        self.question = question
        self.answer = answer
