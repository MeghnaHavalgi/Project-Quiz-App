from enum import unique
from marshmallow.schema import Schema
from sqlalchemy.orm import session
from app import application
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

"""
[DataBase Access Details]
Below is the configuration mentioned by which the application can make connection with MySQL database
"""
username = 'root'
password = 'homna123'
application.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{username}:{password}@localhost/quiz_app"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(application)

class UserMaster(db.Model):
        __tablename__ = 'user_master'

        id = db.Column(db.String(100), primary_key = True)
        name = db.Column(db.String(200), unique=True)
        username = db.Column(db.String(200), unique=True)
        password = db.Column(db.String(200))
        is_admin = db.Column(db.Integer, default=0)
        is_active = db.Column(db.Integer, default = 1)
        created_ts = db.Column(db.DateTime, default = datetime.utcnow)
        updated_ts = db.Column(db.DateTime)

        def __init__(self, id, name, username, password, is_admin):
            self.id = id
            self.name = name
            self.username = username
            self.password = password
            self.is_admin = is_admin
            self.is_active = 1
            self.created_ts = datetime.utcnow()
            
class UserSession(db.Model):
        __tablename__ = 'user_session'
        
        id = db.Column(db.String(100), primary_key = True)
        user_id = db.Column(db.String(200), db.ForeignKey('user_master.id'))
        session_id = db.Column(db.String(200), unique=True)
        is_active = db.Column(db.Integer, default = 1)
        created_ts = db.Column(db.DateTime, default = datetime.utcnow)
        updated_ts = db.Column(db.DateTime)
        
        def __init__(self, id, user_id, session_id):
            self.id = id
            self.user_id = user_id
            self.session_id = session_id
            self.is_active = 1
            self.created_ts = datetime.utcnow()
        
class QuestionMaster(db.Model):
        
        __tablename__ = 'question_master'
        
        id = db.Column(db.String(100), primary_key = True)
        question = db.Column(db.String(500), unique=True)
        choice1 = db.Column(db.String(500))
        choice2 = db.Column(db.String(500))
        choice3 = db.Column(db.String(500))
        choice4 = db.Column(db.String(500))
        answer = db.Column(db.Integer)
        marks = db.Column(db.Integer)
        remarks = db.Column(db.String(200))
        is_active = db.Column(db.Integer, default = 1)
        created_ts = db.Column(db.DateTime, default = datetime.utcnow)
        updated_ts = db.Column(db.DateTime)
        
        def __init__(self, id, question, choice1, 
                     choice2, choice3, choice4, answer, marks, remarks):
            self.id = id
            self.question = question
            self.choice1 = choice1
            self.choice2 = choice2
            self.choice3 = choice3
            self.choice4 = choice4
            self.marks = marks
            self.remarks = remarks
            self.answer = answer
            self.is_active = 1
            self.created_ts = datetime.utcnow()
            
class QuizMaster(db.Model):
    
        __tablename__ = 'quiz_master'
        
        id = db.Column(db.String(100), primary_key = True)
        quiz_name = db.Column(db.String(200), unique=True)
        is_active = db.Column(db.Integer, default = 1)
        created_ts = db.Column(db.DateTime, default = datetime.utcnow)
        updated_ts = db.Column(db.DateTime)
        
        def __init__(self, id, quiz_name):
            self.id = id
            self.quiz_name = quiz_name
            self.is_active = 1
            self.created_ts = datetime.utcnow()
            
class QuizQuestions(db.Model):
        
        __tablename__ = 'quiz_questions'
        __table_args__ = (
                db.UniqueConstraint('quiz_id', 'question_id', name='unique_quiz_question'),
        )
        
        id = db.Column(db.String(100), primary_key = True)
        quiz_id = db.Column(db.String(200), db.ForeignKey('quiz_master.id'))
        question_id = db.Column(db.String(200), db.ForeignKey('question_master.id'))
        is_active = db.Column(db.Integer, default = 1)
        created_ts = db.Column(db.DateTime, default = datetime.utcnow)
        updated_ts = db.Column(db.DateTime)
        
        def __init__(self, id, quiz_id, question_id):
            self.id = id
            self.quiz_id = quiz_id
            self.question_id = question_id
            self.is_active = 1
            self.created_ts = datetime.utcnow()
     
class QuizInstance(db.Model):
        __tablename__ = 'quiz_instance'
        __table_args__ = (
                db.UniqueConstraint('quiz_id', 'user_id', name='unique_quiz_user'),
        )
        
        id = db.Column(db.String(100), primary_key = True)
        quiz_id = db.Column(db.String(200), db.ForeignKey('quiz_master.id'))
        user_id = db.Column(db.String(200), db.ForeignKey('user_master.id'))
        score_achieved = db.Column(db.Integer, default = 0)
        is_submitted = db.Column(db.Integer, default = 0)
        is_active = db.Column(db.Integer, default = 1)
        created_ts = db.Column(db.DateTime, default = datetime.utcnow)
        updated_ts = db.Column(db.DateTime)
        
        def __init__(self, id, quiz_id, user_id):
            self.id = id
            self.quiz_id = quiz_id
            self.user_id = user_id
            self.score_achieved = 0
            self.is_submitted = 0
            self.is_active = 1
            self.created_ts = datetime.utcnow()
            
class UserResponses(db.Model):
        __tablename__ = 'user_responses'
        __table_args__ = (
                db.UniqueConstraint('quiz_id', 'user_id', 'question_id', name='unique_quiz_user_question'),
        )
        
        id = db.Column(db.String(100), primary_key = True)
        quiz_id = db.Column(db.String(200), db.ForeignKey('quiz_master.id'))
        user_id = db.Column(db.String(200), db.ForeignKey('user_master.id'))
        question_id = db.Column(db.String(200), db.ForeignKey('question_master.id'))
        response = db.Column(db.Integer, default = 0)
        is_active = db.Column(db.Integer, default = 1)
        created_ts = db.Column(db.DateTime, default = datetime.utcnow)
        updated_ts = db.Column(db.DateTime)
        
        def __init__(self, id, quiz_id, user_id, question_id, response):
            self.id = id
            self.quiz_id = quiz_id
            self.user_id = user_id
            self.question_id = question_id
            self.response = response
            self.is_active = 1
            self.created_ts = datetime.utcnow()
        
    
db.create_all()
db.session.commit()