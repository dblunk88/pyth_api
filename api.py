#!flask/bin/python
import json

from flask import request,Response

from methods import get_forms,get_questions,get_users,get_policy_holders_by_company,search_policy_holders \
    ,get_assessments,get_question_answers,get_form_questions,send_form,get_user,submit_form,get_institutions
from settings import app


@app.route('/pythapi/authorized/api/<route>',methods=['OPTIONS'])
def authorized_options(route):
    if route == "submitForm":
        resp = Response(
            status=200,
            mimetype='application/json')

        resp.headers["Access-Control-Allow-Origin"] = "https://pyth.app"
        resp.headers["Access-Control-Allow-Credentials"] = True
        resp.headers["Access-Control-Max-Age"] = 60
        resp.headers["Access-Control-Allow-Headers"] = ["origin", "content-type", "accept"]
        resp.headers["Access-Control-Allow-Methods"] = ["POST", "OPTIONS"]

        return resp

    else:
        return Response(
            response=json.dumps("The route you specified was not found"),
            status=404)


@app.route('/pythapi/authorized/api/<route>',methods=['POST'])
def authorized_post(route):
    if route == "sendForm":
        user_id = request.args.get('userId')
        form_id = request.args.get('formId')
        return send_form(user_id, form_id)

    elif route == "submitForm":
        user_id = request.args.get('userId')
        form_id = request.args.get('formId')
        data = request.get_json()
        return submit_form(user_id, form_id, data)

    else:
        return Response(
            response=json.dumps("The route you specified was not found"),
            status=404)


@app.route('/pythapi/authorized/api/<route>',methods=['GET'])
def authorized_get(route):
    if route == "getPolicyHoldersByCompany":
        company = request.args.get('company')
        return get_policy_holders_by_company(company)

    elif route == "getUser":
        user_id = request.args.get('userId')
        return get_user(user_id)

    elif route == "searchPolicyHolders":
        search = request.args.get('search')
        return search_policy_holders(search)

    elif route == "getInstitutions":
        return get_institutions()

    elif route == "getUsers":
        return get_users()

    elif route == "getQuestionAnswers":
        return get_question_answers()

    else:
        return Response(
            response=json.dumps("The route you specified was not found"),
            status=404
            )


@app.route('/pythapi/unauthorized/api/<route>',methods=['GET'])
def unauthorized(route):
    if route == "getQuestions":
        return get_questions()

    elif route == "getForms":
        return get_forms()

    elif route == "getFormQuestions":
        form = request.args.get('formId')
        return get_form_questions(form)

    elif route == "getAssessments":
        return get_assessments()

    else:
        return Response(
            response=json.dumps("The route you specified was not found"),
            status=404)


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",ssl_context=('/etc/letsencrypt/live/api.pyth.app/fullchain.pem','/etc/letsencrypt/live/api.pyth.app/privkey.pem'))
