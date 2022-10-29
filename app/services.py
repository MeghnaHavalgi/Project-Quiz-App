from sqlalchemy.orm.session import sessionmaker
from app.models import QuestionMaster, QuizInstance, QuizMaster, QuizQuestions, UserMaster, UserResponses, UserSession
from app import db
import uuid
from flask import session
import datetime
from typing import List

#This method will publish the user details in database 
# which will be further used will performing login and access checking activities
def create_user(**kwargs):
    try:
        user = UserMaster(
                    uuid.uuid4(), 
                    kwargs['name'], 
                    kwargs['username'], 
                    kwargs['password'], 
                    kwargs['is_admin']
                )

        db.session.add(user)
        db.session.commit()
    except Exception as e:
        raise e
    
#This method will check if the session for the mentioned user_id is active or not.
def check_user_session_is_active(user_id):
    try:
        user_session = UserSession.query.filter_by(user_id=user_id, is_active = 1).first()
        if user_session:
            return True, user_session.session_id
        else:
            return False, None
        
    except Exception as e:
        raise e


#This method will check the credentials for the user and perform login activity accordingly
def login_user(**kwargs):
    try:
        user = UserMaster.query.filter_by(username=kwargs['username'], password = kwargs['password']).first()
        if user:
            print('logged in')
            
            is_active, session_id = check_user_session_is_active(user.id)
            
            if not is_active:
                session_id = uuid.uuid4()
                user_session = UserSession(uuid.uuid4(), user.id, session_id)
                db.session.add(user_session)
                db.session.commit()
                
            else:
                session['session_id'] = session_id
                
            
            session['session_id'] = session_id   
            return True, session_id
        
        else:
            return False, None
    
    except Exception as e:
            raise e
        
        
#This method will check the login session for the user and perform logout activity accordingly     
def logout_user(session_id):
    try:
        if session['session_id']:
            user_session = UserSession.query.filter_by(session_id = session['session_id']).first()
            user_session.is_active = 0
            user_session.updated_ts = datetime.datetime.utcnow()
            
            db.session.add(user_session)
            db.session.commit()
            
            session['session_id'] = None
            
            return True
        else:
            return False
    except Exception as e:
        raise e
    
    
#This method will check if the provided user is admin user or not
def check_if_admin(user_id):
    try:
        print('Inside check admin method')
        user = UserMaster.query.filter_by(id=user_id, is_active = 1).first()
        print(user)
        if user:
            if user.is_admin == 1:
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        print(str(e))
        raise e
    
#This method will check if the session for the mentioned user_id is active or not.
def check_if_session_is_active(session_id):
    try:
        user_session = UserSession.query.filter_by(session_id=session_id, is_active=1).first()
        if user_session:
            return True, user_session.user_id
        else:
            return False, None
        
    except Exception as e:
        raise e
            
#This method will add question to database with the provided parameter values
def add_question(**kwargs):
    try:
        question = QuestionMaster(
                uuid.uuid4(),
                kwargs['question'],
                kwargs['choice1'],
                kwargs['choice2'],
                kwargs['choice3'],
                kwargs['choice4'],
                kwargs['answer'],
                kwargs['marks'],
                kwargs['remarks']
            )
        db.session.add(question)
        db.session.commit()
           
    except Exception as e:
        raise e
    
    
#This method will list all questions' details present in database as apart of question bank
def list_questions():
    try:
        questions = QuestionMaster.query.all()
        # print(len(questions))
        
        result = list()
        
        for question in questions:
            question_obj = dict()
            
            question_obj['question_id'] = question.id
            question_obj['question_description'] = question.question
            question_obj['choice1'] = question.choice1
            question_obj['choice2'] = question.choice2
            question_obj['choice3'] = question.choice3
            question_obj['choice4'] = question.choice4
            question_obj['marks'] = question.marks
            question_obj['remarks'] = question.remarks
            question_obj['answer'] = question.answer
            
            result.append(question_obj)
            
        print(result)
        return result
    
    except Exception as e:
        print(e)
        raise e            
    

#This method will create quiz with the given parameters in the request body
def create_quiz(**kwargs):
    try:
        quiz_name = kwargs['quiz_name']
        
        quiz_id = uuid.uuid4()
        quiz = QuizMaster(quiz_id, quiz_name)
        db.session.add(quiz)
        
        question_ids = kwargs['question_ids']
        
        for question_id in question_ids:
            quiz_question = QuizQuestions(uuid.uuid4(), quiz_id, question_id)
            db.session.add(quiz_question)
            
        db.session.commit()
        
    except Exception as e:
        print(e)
        raise e
    
    
#This mehtod will assign quiz to the respective user as apart of request body
def assign_quiz(**kwargs):
    try:
        quiz_instance = QuizInstance(uuid.uuid4(), kwargs['quiz_id'], kwargs['user_id'])
        
        db.session.add(quiz_instance)
        db.session.commit()
        
    except Exception as e:
        print(str(e))
        raise e      
    
#This method aims at checking the access of the quiz to the user
def check_quiz_access(quiz_id, user_id):
    try:
        if check_if_admin(user_id) == True:
            return True
       
        quiz_access = QuizInstance.query.filter_by(user_id=user_id, quiz_id=quiz_id, is_active = 1).first()
       
        if quiz_access:
            return True
        else:
            return False
    
    except Exception as e:
        print(str(e))
        raise e
   
   
#This method outputs the quiz details such as questions tagged with respective data 
def view_quiz(**kwargs):
    try:
        quiz_id = kwargs['quiz_id']
        quiz_questions = QuizQuestions.query.filter_by(quiz_id=quiz_id, is_active=1)
        question_ids = list()
        for q in quiz_questions:
            question_ids.append(q.question_id)
            
        print(question_ids)
        
        questions = list()
        for question_id in question_ids:
            question = QuestionMaster.query.filter_by(id=question_id).first()
            question_obj = dict()
            
            question_obj['question_id'] = question.id
            question_obj['question_description'] = question.question
            question_obj['choice1'] = question.choice1
            question_obj['choice2'] = question.choice2
            question_obj['choice3'] = question.choice3
            question_obj['choice4'] = question.choice4
            question_obj['marks'] = question.marks
            question_obj['remarks'] = question.remarks
            
            questions.append(question_obj)
        
        return questions
    except Exception as e:
        print(str(e))
        raise e
    

#This method will provide data for the assigned quizes to the respective user 
def get_assigned_quiz_info(user_id):
    try:
        quizes = QuizInstance.query.filter_by(user_id=user_id, is_active=1)
        
        quiz_info = list()
        
        for quiz in quizes:
            quiz_obj = dict()
            quiz_obj['quiz_id'] = quiz.quiz_id
            quiz_obj['quiz_name'] = QuizMaster.query.filter_by(id=quiz.quiz_id).first().quiz_name
            quiz_obj['is_submitted'] = quiz.is_submitted
            quiz_obj['score_achieved'] = quiz.score_achieved
            
            quiz_info.append(quiz_obj)
            
        return quiz_info
    
    except Exception as e:
        print(str(e))
        raise e
    
#This method will provide data for the all the created quizes
def get_all_quiz_info(user_id):
    try:
        quizes = QuizMaster.query.all()
        
        quiz_info = list()
        
        for quiz in quizes:
            quiz_obj = dict()
            quiz_obj['quiz_id'] = quiz.id
            quiz_obj['quiz_name'] = quiz.quiz_name
            
            quiz_info.append(quiz_obj)
            
        return quiz_info
    
    except Exception as e:
        print(str(e))
        raise e
    
#Here in this method, score calculation is done against all the mentioned responses
def attempt_quiz(user_id, quiz_id, responses):
    try:
        quiz_questions = QuizQuestions.query.filter_by(quiz_id=quiz_id, is_active=1)
        question_ids = list()
        for q in quiz_questions:
            print(q)
            question_ids.append(q.question_id)
            
        print(f'Question Ids : {question_ids}')
        
        answer_key = dict()
        for question_id in question_ids:
            question = QuestionMaster.query.filter_by(id=question_id).first()
            
            question_obj = dict()
            
            question_obj['answer'] = question.answer
            question_obj['marks'] = question.marks
            
            answer_key[question.id] = question_obj
            
        score_achieved = 0
        
        for response in responses:
            question_id = response['question_id']
            selected_answer = response['answer']
            
            if answer_key[question_id]['answer'] == selected_answer:
                score_achieved += answer_key[question_id]['marks']
            
            user_response = UserResponses(uuid.uuid4(), quiz_id, user_id, question_id, response['answer'])
            db.session.add(user_response)
        
        quiz_instance = QuizInstance.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()
        quiz_instance.score_achieved = score_achieved
        quiz_instance.is_submitted = 1
        
        db.session.add(quiz_instance)
        db.session.commit()
                
        return score_achieved

        
    except Exception as e:
        print(str(e))
        raise e
            
#Here in this method, quiz results are fetched and the scores are sorted in descinding order
def quiz_results(quiz_id):
    try:
        quiz = QuizMaster.query.filter_by(id=quiz_id, is_active=1).first()
        if not quiz:
            return []
        
        quiz_instances = QuizInstance.query.filter_by(quiz_id=quiz_id, is_active=1)
        
        if not quiz_instances:
            return []
        
        quiz_results = list()
        
        for instance in quiz_instances:
            instance_obj = dict()
            
            instance_obj['user_id'] = instance.user_id
            instance_obj['is_submitted'] = instance.is_submitted
            instance_obj['score_achieved'] = instance.score_achieved
            
            quiz_results.append(instance_obj)
            
        sorted(quiz_results, key = lambda x : x['score_achieved'], reverse=True)
        return quiz_results
    
    except Exception as e:
        print(str(e))
        raise e