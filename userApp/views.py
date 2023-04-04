from django.shortcuts import render ,redirect
from django.core  import serializers
from django.http import HttpRequest, HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import *
# Create your views here.

@csrf_exempt
def verify(body,syscall = True) :
    body_unicode = body.decode('utf-8')
    body = json.loads(body_unicode)
    token = body['credential']
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(),'591544022842-gac7dfpof6ni0bpve67t5ilupoi4p3ic.apps.googleusercontent.com')

        user = User.objects.filter(email__exact=idinfo['email'])
        if len(user) !=0  and syscall :
            print('already loged user')
            return user[0]
        elif len(user) !=0:
            return HttpResponse("already loged user")
        user = User(
            email =idinfo['email'],
            name = idinfo['name'],
            url = idinfo['picture']
        )
        print(user)
        user.save()
        print('created new user')
        return HttpResponse("valid login")
    except ZeroDivisionError:
        print("invalid")
        return HttpResponse("post",status=400) 
@csrf_exempt
def login(request:HttpRequest) :
    if request.method == 'GET' :
        return HttpResponse("get")
    elif request.method == 'POST':
        return verify(request.body,syscall=False)
        
    
@csrf_exempt
def getQuestions(request:HttpRequest) :
    if request.method == 'POST':
        user = verify(request.body)
    top_objects = Question.objects.select_related('user').  all()[:10]
    # data = QuestionSerializer('json', top_objects)
    data = []
    for x in top_objects :
        d ={}
        d['pk'] = x.pk
        d["name"] = x.user.name 
        d["title"] = x.title
        d['detailed_question'] = x.detailed_question
        d["url"] = x.user.url
        d['domain'] = x.university.mail
        d['date'] = x.date
        d['votes'] = len(x.upvotes.all()) - len(x.downvotes.all())
        if request.method == 'POST' :
            d['your_vote'] = "yes" if user in x.upvotes.all() else "no" if user in x.downvotes.all() else ""
            print(d['your_vote'])
        data.append(d)
        data = sorted(data,key= lambda x : -x['votes'])
    return JsonResponse(data,safe=False)

@csrf_exempt
def postQuestion(request:HttpRequest):
    if request.method == 'POST' :
        user = verify(request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        name = body['name']
        univercity = University.objects.filter(name = name)[0]
        question = Question()
        question.title = body['title']
        question.detailed_question =body['detailed_question']
        question.user = user
        question.university = univercity
        question.save()
        print('Question is posted')
        return HttpResponse('ok')

@csrf_exempt
def deleteQuestion(request:HttpRequest,id_question):
    if request.method == 'POST' :
        user = verify(request.body)
        question = Question.objects.get(id = id_question)
        print('processing ...')
        if user.email == question.user.email :
            question.delete()
            print('Question is deleted')
            return HttpResponse('ok')
        return HttpResponse('your can\'t delete others post ' ,status=400)

@csrf_exempt
def postAnswer(request:HttpRequest,id_question):
    if request.method == 'POST' :
        user = verify(request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        question = Question.objects.get(id = id_question)
        mail = question.university.mail
        if user.email[-len(mail):] == mail :
            answer = Answer()
            answer.question = question
            answer.text = body['text']
            answer.user = user
            answer.save()
            print('Answer is posted')
            return redirect('/question/1/')   
        return HttpResponse('your are not allowed to post answer to this question' , status=400)
    
@csrf_exempt
def deleteAnswer(request:HttpRequest,id_answer):
    if request.method == 'POST' :
        user = verify(request.body)
        answer = Answer.objects.get(id = id_answer)
        print('processing ...')
        if user.email == answer.user.email :
            answer.delete()
            print('Answer is deleted')
            return HttpResponse('ok')
        return HttpResponse('your can\'t delete others answer ' ,status=400)
    

@csrf_exempt
def getUnivercities(request:HttpRequest) :
    result = []
    data = University.objects.all()
    for x in data :
        result.append(x.name)
    return JsonResponse(result ,safe=False)

@csrf_exempt
def likeQuestion(request:HttpRequest) :
    if request.method == 'POST':
        user = verify(request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        question = Question.objects.get(id=body['pk'])
        mail = question.university.mail
        if user.email[-len(mail):] == mail :
            if body['option'] == 'yes':
                question.upvotes.add(user)
                question.downvotes.remove(user)
                # pass
            elif body['option'] == 'no':
                question.upvotes.remove(user)
                question.downvotes.add(user)
            else :
                question.upvotes.remove(user)
                question.downvotes.remove(user)
            likes = question.upvotes.count() - question.downvotes.count()
            return JsonResponse({"option":body['option'],'likes':likes})
        else :
            return HttpResponse("you cant like toks question",status=400)
    
@csrf_exempt
def getQuestion(request:HttpRequest,id) :
    if request.method == 'POST':
        user = verify(request.body);
    question = Question.objects.get(id= id)
    answers = Answer.objects.filter(question = question)
    result = []
    data ={}
    data['pk'] = question.pk
    data["name"] = question.user.name 
    data["title"] = question.title
    data['detailed_question'] = question.detailed_question
    data["url"] = question.user.url
    data['domain'] = question.university.mail
    data['date'] = question.date
    if request.method == 'POST' :
        data['your_vote'] = "yes" if user in question.upvotes.all() else "no" if user in question.downvotes.all() else ""
    data['votes'] = len(question.upvotes.all()) - len(question.downvotes.all())
    for x in answers :
        d= {}
        d['pk'] = x.pk
        d["text"] = x.text
        d["name"] = x.user.name
        d['votes'] = x.upvotes.count() - x.downvotes.count()
        if request.method == 'POST' :
            d['your_vote'] = "yes" if user in x.upvotes.all() else "no" if user in x.downvotes.all() else ""
        d['date'] = x.date
        d['url'] = x.user.url
        result.append(d)
    data['answers'] = result
    return JsonResponse(data, safe=False)
    
@csrf_exempt
def likeAnswer(request:HttpRequest,id_question,id_answer):
    if request.method == 'POST':
        user = verify(request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        question = Question.objects.get(id=id_question)
        answer  = Answer.objects.get(id=id_answer)
        mail = question.university.mail
        print(body)
        if user.email[-len(mail):] == mail :
            if body['option'] == 'yes':
                answer.upvotes.add(user)
                answer.downvotes.remove(user)
                # pass
            elif body['option'] == 'no':
                answer.upvotes.remove(user)
                answer.downvotes.add(user)
            else :
                answer.upvotes.remove(user)
                answer.downvotes.remove(user)
            likes = answer.upvotes.count() - answer.downvotes.count()
            return JsonResponse({"option":body['option'],'likes':likes})
        else :
            print('not a verified user to like')
            return HttpResponse("you cant like this question",status=400)
    