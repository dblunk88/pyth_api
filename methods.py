#!flask/bin/python
import json

from flask import Response
from sqlalchemy import text

from Database import Answer_Type,Assessment,Questions,Question_Answer,User_Type,Users,Companies,Forms,Results
from settings import session


# TODO: Implement sendAssessments (by userid), get_pendingAssessments (by userid)
def send_form(user_id,form_id):
    current_pending = session.query(Users.pending_forms).filter(Users.uid == user_id).one()

    new_pending = [int(form_id)]
    for form in current_pending[0]:
        if int(form) not in new_pending:
            new_pending.append(int(form))

    session.query(Users) \
        .filter(Users.uid == user_id) \
        .update(dict(pending_forms=new_pending))

    session.commit()

    return get_user(user_id)


def submit_form(user_id,form_id,data):
    current_pending = session.query(Users.pending_forms).filter(Users.uid == user_id).one()

    new_completed = [int(form_id)]
    new_pending = []
    for form in current_pending[0]:
        if int(form) not in new_pending and int(form_id) != int(form):
            new_pending.append(int(form))

    session.query(Users) \
        .filter(Users.uid == user_id) \
        .update(dict(completed_forms=new_completed,pending_forms=new_pending))
    session.commit()

    # insert a result for each assessment question
    for question in data["results"]:
        value = (10 / question["answer"])
        answer_type = 3
        if question["answer"] > 7:
            answer_type = 4
        elif question["answer"] < 4:
            answer_type = 2

        extra_data = session \
            .query(Companies.company_name,
                   Assessment.title,
                   Users.user_id,
                   Assessment.assessment_id,
                   Companies.company_id) \
            .filter(Users.uid == user_id,Users.company_id == Companies.company_id,
                    Assessment.assessment_id == question["questionId"]) \
            .one()

        results = Results()
        results.user_id = extra_data[2]
        results.category = extra_data[1]
        results.parent_company = extra_data[0]
        results.value = int(round(value))
        results.assessment_id = int(question["questionId"])
        results.answer_type_id = answer_type

        session.add(results)
        session.commit()

    return get_user(user_id)


def get_questions():
    query = session.query(Questions.questions_id,Questions.question).all()
    return formatResponse(query)


def get_forms():
    query = session.query(Forms.form_id,Forms.form_title).all()
    results = []
    for item in query:
        results.append({"id": item[0],"title": item[1]})
    return formatResponse(results)


def get_policy_holders_by_company(company):
    query = session.query(Users.username,Users.uid,Users.email,Companies.company_name,Users.img_url) \
        .join(Companies,Companies.company_id == Users.company_id) \
        .filter(Users.user_type_id == 2,Companies.company_name.like("{}".format(company))).all()

    results = []
    for item in query:
        results.append({"username": item[0],"uid": item[1],"email": item[2],"company": item[3],"img_url": item[4]})

    return formatResponse(results)


def search_policy_holders(search):
    query = session.query(Users.username,Users.uid,Users.email,Companies.company_name,Users.img_url) \
        .join(Companies,Companies.company_id == Users.company_id) \
        .filter(Users.email.like("%{}%".format(search))).all()

    results = []
    for item in query:
        results.append({"username": item[0],"uid": item[1],"email": item[2],"company": item[3],"img_url": item[4]})

    return formatResponse(results)


def get_institutions():
    query = session.query(Companies.company_name,Companies.img_url).all()

    results = []
    for item in query:
        results.append({"name": item[0],"img_url": item[1]})

    return formatResponse(results)


def get_users():
    query = session.query(Users.username,Users.email,User_Type.user_type_id) \
        .filter(Users.user_type_id == User_Type.user_type_id).all()
    return formatResponse(query)


def get_user(user_id):
    query = session \
        .query(Users.username,Users.email,User_Type.type,
               User_Type.user_type_id,Users.pending_forms,Users.completed_forms,Users.img_url) \
        .filter(Users.uid == user_id,Users.user_type_id == User_Type.user_type_id).one()

    results = {
        "userType": {
            "id": query[3],
            "type": query[2]
        },
        "pending_forms": query[4],
        "completed_forms": query[5],
        "img_url": query[6]
    }

    return formatResponse(results)


def get_assessments():
    query = session.query(Assessment.description,Assessment.title,Assessment.category).all()
    return formatResponse(query)


# ignore
def get_question_answers():
    query = session.query(Questions.questions_id,Questions.question,Answer_Type.answer_type).filter(
        Questions.questions_id == Question_Answer.question_id,
        Answer_Type.answer_type_id == Question_Answer.answer_type_id).all()

    response = []
    for item in query:
        response.append({"questionId": item[0],"question": item[1],"answerType": item[2]})

    return formatResponse(response)


def get_form_questions(form):
    query = session.query(Assessment.assessment_id,Assessment.description,Forms.form_title). \
        from_statement(text("SELECT assessment_id, description, forms.form_title FROM assessment, forms "
                            "WHERE assessment.category = forms.form_title "
                            "AND forms.form_id = {};".format(form))).all()
    titles = session.query(Forms.form_title)
    questions = []
    for item in query:
        questions.append({"questionId": item[0],"question": item[1]})
    res = {"formId": form,"title": query[-1][-1],"questions": questions}
    return formatResponse(res)


def formatResponse(query):
    resp = Response(
        response=json.dumps(query),
        status=200,
        mimetype='application/json')

    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Credentials"] = True

    return resp
