from django.urls import path,include
from .views import *
urlpatterns = [
    path('login/',login),
    path('question/<int:id_question>/<int:id_answer>/like/',likeAnswer),
    path('question/<int:id_question>/delete/',deleteQuestion),
    path('question/<int:id_question>/answer/create/',postAnswer),
    path('question/<int:id>/',getQuestion),
    path('question/create',postQuestion),
    path('question/like/',likeQuestion),
    path('questions/',getQuestions),
    path('answer/<int:id_answer>/delete/',deleteAnswer),
    path('univercities/',getUnivercities),
]