from marshmallow import Schema, fields, base


"""
This module aims at providing the request and response format for the various api calls.
This also helpful for creating swagger docs for apis testing.
"""


class APIResponse(Schema):
    message = fields.Str(default="Success")
    
class SignUpRequest(Schema):
    username = fields.Str(default = "username")
    password = fields.Str(default = "password")
    name = fields.Str(default = "name")
    is_admin = fields.Int(default = 0)
    
class LoginRequest(Schema):
    username = fields.Str(default="username")
    password = fields.Str(default="password")
    
class LogoutRequest(Schema):
    session_id = fields.Str(default="session_id")
    
class QuestionsRequest(Schema):
    session_id = fields.Str(default="session_id")
    
class ListQuestionsResponse(Schema):
    questions = fields.List(fields.Dict())
    
class AddQuestionRequest(Schema):
    session_id = fields.Str(default="session_id")
    question = fields.Str(default="question")
    choice1 = fields.Str(default="choice1")
    choice2 = fields.Str(default="choice2")
    choice3 = fields.Str(default="choice3")
    choice4 = fields.Str(default="choice4")
    marks = fields.Int(default=0)
    remarks = fields.Str(default="remarks")
    answer = fields.Int(default=0)
    
class CreateQuizRequest(Schema):
    session_id = fields.Str(default="session_id")
    quiz_name = fields.Str(default="quiz_name")
    question_ids = fields.List(fields.Str)
    
class AssignQuizRequest(Schema):
    session_id = fields.Str(default="session_id")
    quiz_id = fields.Str(default="quiz_id")
    user_id = fields.Str(default="user_id")
    
class ViewQuizRequest(Schema):
    session_id = fields.Str(default="session_id")
    quiz_id = fields.Str(default="quiz_id")
    
class ViewQuizResponse(Schema):
    questions = fields.List(fields.Dict())
    
class AssignedQuizRequest(Schema):
    session_id = fields.Str(default="session_id")
    
class AssignedQuizResponse(Schema):
    quiz_info = fields.List(fields.Dict())
    
class ViewAllQuizRequest(Schema):
    session_id = fields.Str(default="session_id")
    
class ViewAllQuizReponse(Schema):
    quiz_info = fields.List(fields.Dict())

class AttemptQuizRequest(Schema):
    session_id = fields.Str(default="session_id")
    quiz_id = fields.Str(default="quiz_id")
    responses = fields.List(fields.Dict())
    
    
class AttemptQuizResponse(Schema):
    score_achieved = fields.Int(default=0)
    
    
class QuizResultRequest(Schema):
    session_id = fields.Str(default="session_id")
    quiz_id = fields.Str(default="quiz_id")
    
class QuizResultResponse(Schema):
    results = fields.List(fields.Dict())